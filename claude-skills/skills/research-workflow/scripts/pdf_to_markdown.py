from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def _prime_g_drive_model_cache_env() -> None:
    tools_root = Path(os.environ.get("RESEARCH_TOOLS_ROOT", "G:/tools"))
    hf_home = tools_root / "hf"
    hf_hub = hf_home / "hub"
    torch_home = tools_root / "torch"
    for path in (hf_home, hf_hub, torch_home):
        path.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(hf_home))
    os.environ.setdefault("HF_HUB_CACHE", str(hf_hub))
    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", str(hf_hub))
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
    os.environ.setdefault("TORCH_HOME", str(torch_home))


_prime_g_drive_model_cache_env()

# ---------------------------------------------------------------------------
# Hard guard: fail immediately if docling is not properly installed.
# Do NOT catch this error and fall back to pypdf2 / pdfminer / etc.
# ---------------------------------------------------------------------------
try:
    from docling_core.types.doc import ImageRefMode
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption
except ImportError as _e:
    sys.exit(
        f"[FATAL] docling is not installed or broken: {_e}\n"
        "DO NOT use any alternative PDF tool (pypdf2, pdfminer, etc.).\n"
        "Install docling and docling-core first, then retry:\n"
        "  pip install 'docling>=2.0' 'docling-core>=2.0'\n"
        "Verify with: python -c 'import docling, docling_core; print(\"ok\")'"
    )

from download_arxiv_papers import sanitize_filename


DEFAULT_DOCLAYOUT_MODEL = "juliozhao/DocLayout-YOLO-DocStructBench"
DEFAULT_TABLE_DETECTION_MODEL = "microsoft/table-transformer-detection"
DEFAULT_TABLE_STRUCTURE_MODEL = "microsoft/table-transformer-structure-recognition-v1.1-all"


def _ensure_g_drive_model_cache() -> None:
    _prime_g_drive_model_cache_env()


def build_pipeline_options(mode: str = "fast") -> PdfPipelineOptions:
    if mode not in {"fast", "enhanced"}:
        raise ValueError(f"unsupported PDF extraction mode: {mode}")
    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = 2.0
    pipeline_options.generate_page_images = True
    pipeline_options.generate_picture_images = True
    pipeline_options.generate_table_images = mode == "enhanced"
    pipeline_options.do_table_structure = mode == "enhanced"
    pipeline_options.do_ocr = mode == "enhanced"
    if mode == "enhanced" and hasattr(pipeline_options, "table_structure_options"):
        pipeline_options.table_structure_options.do_cell_matching = True
    return pipeline_options


def _warmup_check(mode: str = "fast") -> None:
    """Verify docling models are downloaded and the converter actually works."""
    try:
        import os as _os
        import tempfile

        def _make_minimal_pdf() -> bytes:
            return (
                b"%PDF-1.4\n"
                b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
                b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
                b"3 0 obj<</Type/Page/MediaBox[0 0 3 3]/Parent 2 0 R>>endobj\n"
                b"xref\n0 4\n0000000000 65535 f\r\n"
                b"0000000009 00000 n\r\n0000000058 00000 n\r\n0000000115 00000 n\r\n"
                b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF"
            )

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(_make_minimal_pdf())
            tmp = f.name
        try:
            opts = build_pipeline_options(mode)
            opts.generate_page_images = False
            opts.generate_picture_images = False
            opts.generate_table_images = False
            conv = DocumentConverter(
                format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
            )
            conv.convert(tmp)
        finally:
            _os.unlink(tmp)
    except Exception as e:
        sys.exit(
            f"[FATAL] docling converter failed warm-up check: {e}\n"
            "This usually means AI models were not downloaded yet (needs internet on first run).\n"
            "DO NOT fall back to other PDF tools. Fix docling first:\n"
            "  1. Ensure internet access and re-run this script.\n"
            "  2. Or pre-download models: python -c 'from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline; StandardPdfPipeline.download_models_hf()'"
        )


def build_converter(mode: str = "fast") -> DocumentConverter:
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=build_pipeline_options(mode))
        }
    )


def ensure_paper_folder(pdf_path: Path, root: Path) -> tuple[Path, Path]:
    if pdf_path.parent != root:
        paper_dir = pdf_path.parent
        target_pdf = paper_dir / "paper.pdf"
        if pdf_path != target_pdf and not target_pdf.exists():
            shutil.move(str(pdf_path), target_pdf)
        return paper_dir, target_pdf if target_pdf.exists() else pdf_path
    base = pdf_path.stem
    slug = sanitize_filename(base)
    paper_dir = root / slug
    paper_dir.mkdir(parents=True, exist_ok=True)
    target_pdf = paper_dir / "paper.pdf"
    if not target_pdf.exists():
        shutil.move(str(pdf_path), target_pdf)
    return paper_dir, target_pdf


def convert_one(converter: DocumentConverter, pdf_path: Path, paper_dir: Path, overwrite: bool) -> Path:
    md_path = paper_dir / "paper.md"
    if md_path.exists() and not overwrite:
        return md_path
    conv_res = converter.convert(str(pdf_path))
    paper_dir.mkdir(parents=True, exist_ok=True)
    (paper_dir / "paper_artifacts").mkdir(parents=True, exist_ok=True)
    conv_res.document.save_as_markdown(md_path, image_mode=ImageRefMode.REFERENCED)
    return md_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="downloads")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--mode",
        choices=("fast", "enhanced"),
        default="fast",
        help="fast keeps OCR/table recognition off; enhanced enables Docling OCR and table structure.",
    )
    parser.add_argument("--enhanced", action="store_true", help="Shortcut for --mode enhanced.")
    parser.add_argument(
        "--layout-engine",
        choices=("none", "doclayout-yolo"),
        default="none",
        help="Optional sidecar layout detector for page-level artifacts.",
    )
    parser.add_argument(
        "--table-engine",
        choices=("none", "table-transformer"),
        default="none",
        help="Optional sidecar table detector/structure recognizer.",
    )
    parser.add_argument("--doclayout-model", default=DEFAULT_DOCLAYOUT_MODEL)
    parser.add_argument("--table-detection-model", default=DEFAULT_TABLE_DETECTION_MODEL)
    parser.add_argument("--table-structure-model", default=DEFAULT_TABLE_STRUCTURE_MODEL)
    parser.add_argument("--enhance-device", default="auto", help="auto, cpu, cuda, cuda:0, etc.")
    parser.add_argument("--enhance-conf", type=float, default=0.25)
    parser.add_argument(
        "--enhance-max-pages",
        type=int,
        default=0,
        help="Limit sidecar model pages for quick checks. 0 means all pages.",
    )
    args = parser.parse_args(argv)
    if args.enhanced:
        args.mode = "enhanced"
    if args.mode == "fast" and (args.layout_engine != "none" or args.table_engine != "none"):
        parser.error("--layout-engine and --table-engine require --mode enhanced or --enhanced")
    return args


def _torch_device(requested: str):
    import torch

    if requested != "auto":
        return torch.device(requested)
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _device_arg(requested: str) -> str:
    if requested != "auto":
        return requested
    try:
        import torch

        return "cuda:0" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def _render_page_images(pdf_path: Path, paper_dir: Path, max_pages: int, scale: float = 2.0) -> list[Path]:
    try:
        import pypdfium2 as pdfium
    except ImportError as e:
        raise SystemExit(
            "[FATAL] Enhanced sidecar extraction requires pypdfium2.\n"
            "Install it in the research runtime: pip install pypdfium2"
        ) from e

    pages_dir = paper_dir / "paper_artifacts" / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[Path] = []
    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        page_count = len(pdf)
        limit = min(page_count, max_pages) if max_pages and max_pages > 0 else page_count
        for page_index in range(limit):
            out_path = pages_dir / f"page_{page_index + 1:04d}.png"
            if not out_path.exists():
                page = pdf[page_index]
                bitmap = page.render(scale=scale)
                bitmap.to_pil().save(out_path)
            rendered.append(out_path)
    finally:
        pdf.close()
    return rendered


def _box_records(result) -> list[dict]:
    boxes = getattr(result, "boxes", None)
    if boxes is None:
        return []
    names = getattr(result, "names", {}) or {}
    xyxy = boxes.xyxy.detach().cpu().tolist()
    confs = boxes.conf.detach().cpu().tolist()
    classes = boxes.cls.detach().cpu().tolist()
    records = []
    for coords, score, cls_id in zip(xyxy, confs, classes):
        label = names.get(int(cls_id), str(int(cls_id))) if isinstance(names, dict) else str(int(cls_id))
        records.append(
            {
                "label": label,
                "score": float(score),
                "box": [float(x) for x in coords],
            }
        )
    return records


def _run_doclayout_yolo(page_images: list[Path], paper_dir: Path, args: argparse.Namespace) -> dict:
    try:
        from doclayout_yolo import YOLOv10
    except ImportError as e:
        raise SystemExit(
            "[FATAL] --layout-engine doclayout-yolo requires doclayout-yolo.\n"
            "Install it in the G-drive runtime first:\n"
            "  pip install doclayout-yolo\n"
            "DocLayout-YOLO is AGPL-3.0 licensed; keep it optional unless that is acceptable."
        ) from e

    layout_dir = paper_dir / "paper_artifacts" / "layout_doclayout_yolo"
    layout_dir.mkdir(parents=True, exist_ok=True)
    model_path = Path(args.doclayout_model)
    model = YOLOv10(str(model_path)) if model_path.exists() else YOLOv10.from_pretrained(args.doclayout_model)
    results = model.predict(
        [str(p) for p in page_images],
        imgsz=1024,
        conf=args.enhance_conf,
        device=_device_arg(args.enhance_device),
    )
    pages = []
    for page_path, result in zip(page_images, results):
        annotated = result.plot(pil=True, line_width=4, font_size=16)
        annotated_path = layout_dir / f"{page_path.stem}_layout.png"
        annotated.save(annotated_path)
        pages.append(
            {
                "page_image": str(page_path),
                "annotated_image": str(annotated_path),
                "detections": _box_records(result),
            }
        )
    return {"engine": "doclayout-yolo", "model": args.doclayout_model, "pages": pages}


def _table_detections(image, processor, model, device, threshold: float) -> list[dict]:
    import torch

    inputs = processor(images=image, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]], device=device)
    result = processor.post_process_object_detection(
        outputs,
        threshold=threshold,
        target_sizes=target_sizes,
    )[0]
    labels = model.config.id2label
    records = []
    for score, label, box in zip(result["scores"], result["labels"], result["boxes"]):
        records.append(
            {
                "label": labels[int(label.item())],
                "score": float(score.item()),
                "box": [float(x) for x in box.detach().cpu().tolist()],
            }
        )
    return records


def _draw_boxes(image, detections: list[dict], out_path: Path) -> None:
    from PIL import ImageDraw

    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    for det in detections:
        x0, y0, x1, y1 = det["box"]
        draw.rectangle((x0, y0, x1, y1), outline="red", width=3)
        draw.text((x0, max(0, y0 - 12)), f"{det['label']} {det['score']:.2f}", fill="red")
    annotated.save(out_path)


def _run_table_transformer(page_images: list[Path], paper_dir: Path, args: argparse.Namespace) -> dict:
    try:
        from PIL import Image
        from transformers import AutoImageProcessor, TableTransformerForObjectDetection
    except ImportError as e:
        raise SystemExit(
            "[FATAL] --table-engine table-transformer requires pillow and transformers.\n"
            "Install them in the research runtime: pip install pillow transformers"
        ) from e

    device = _torch_device(args.enhance_device)
    table_dir = paper_dir / "paper_artifacts" / "tables_table_transformer"
    table_dir.mkdir(parents=True, exist_ok=True)

    det_processor = AutoImageProcessor.from_pretrained(args.table_detection_model)
    det_model = TableTransformerForObjectDetection.from_pretrained(args.table_detection_model)
    det_model.to(device).eval()

    struct_processor = AutoImageProcessor.from_pretrained(args.table_structure_model)
    struct_model = TableTransformerForObjectDetection.from_pretrained(args.table_structure_model)
    struct_model.to(device).eval()

    pages = []
    for page_path in page_images:
        image = Image.open(page_path).convert("RGB")
        detections = _table_detections(image, det_processor, det_model, device, args.enhance_conf)
        annotated_path = table_dir / f"{page_path.stem}_tables.png"
        _draw_boxes(image, detections, annotated_path)
        table_records = []
        for index, det in enumerate(detections, start=1):
            if not det["label"].lower().startswith("table"):
                continue
            x0, y0, x1, y1 = [int(round(v)) for v in det["box"]]
            crop = image.crop((max(0, x0), max(0, y0), min(image.width, x1), min(image.height, y1)))
            crop_path = table_dir / f"{page_path.stem}_table_{index:02d}.png"
            crop.save(crop_path)
            structure = _table_detections(crop, struct_processor, struct_model, device, args.enhance_conf)
            structure_path = table_dir / f"{page_path.stem}_table_{index:02d}_structure.json"
            structure_path.write_text(
                json.dumps(structure, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            table_records.append(
                {
                    "detection": det,
                    "crop_image": str(crop_path),
                    "structure_json": str(structure_path),
                    "structure_detections": structure,
                }
            )
        pages.append(
            {
                "page_image": str(page_path),
                "annotated_image": str(annotated_path),
                "detections": detections,
                "tables": table_records,
            }
        )
    return {
        "engine": "table-transformer",
        "detection_model": args.table_detection_model,
        "structure_model": args.table_structure_model,
        "pages": pages,
    }


def write_enhanced_sidecar_artifacts(pdf_path: Path, paper_dir: Path, args: argparse.Namespace) -> Path | None:
    if args.layout_engine == "none" and args.table_engine == "none":
        return None
    _ensure_g_drive_model_cache()
    page_images = _render_page_images(pdf_path, paper_dir, args.enhance_max_pages)
    manifest = {
        "pdf": str(pdf_path),
        "mode": args.mode,
        "page_count_processed": len(page_images),
        "layout": None,
        "tables": None,
    }
    if args.layout_engine == "doclayout-yolo":
        manifest["layout"] = _run_doclayout_yolo(page_images, paper_dir, args)
    if args.table_engine == "table-transformer":
        manifest["tables"] = _run_table_transformer(page_images, paper_dir, args)
    manifest_path = paper_dir / "paper_artifacts" / "enhanced_extraction_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest_path


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"root directory does not exist: {root}")
    _ensure_g_drive_model_cache()
    _warmup_check(args.mode)
    converter = build_converter(args.mode)
    pdf_files: list[Path] = []
    pdf_files.extend(root.glob("*.pdf"))
    for sub in root.iterdir():
        if sub.is_dir():
            pdf_files.extend(sub.glob("*.pdf"))
    pdf_files = sorted({p.resolve() for p in pdf_files})
    if not pdf_files:
        raise SystemExit("No PDF files found under the root directory")
    for pdf in pdf_files:
        paper_dir, final_pdf = ensure_paper_folder(pdf, root)
        md_path = convert_one(converter, final_pdf, paper_dir, args.overwrite)
        manifest_path = write_enhanced_sidecar_artifacts(final_pdf, paper_dir, args)
        print(f"Generated Markdown: {md_path}")
        if manifest_path:
            print(f"enhanced-artifacts: {manifest_path}")


if __name__ == "__main__":
    main()
