# AI_TRAVEL PDF-to-index pipeline reference

Use this when Wyatt asks about PDF/OCR/indexing in `/Volumes/T7 Shield/AI_TRAVEL` or similar RAG knowledge-upload projects.

## Key paths inspected

Project root observed in session:
`/Volumes/T7 Shield/AI_TRAVEL/agri-model-platform-nwafu-windows-complete/agri-model-platform-nwafu`

Important files:
- `backend/app/api/v1/knowledge.py` — upload endpoint, chunk generation, metadata/asset persistence, index call.
- `backend/app/services/pdf_enhanced_parser.py` — enhanced PDF parser with page rendering, layout detection, table extraction, asset crops.
- `backend/app/services/knowledge_index_service.py` — indexes documents into DB/vector stores.
- `backend/app/services/rag_service.py` — retrieval orchestration and fallback stores.
- `backend/app/infra/chroma_store.py` — Chroma vector upsert/query.
- `backend/app/infra/postgres.py` — PostgreSQL knowledge tables.
- `backend/app/core/config.py` — parser/model paths and feature toggles.
- `src/cucumber_irrigation/rag/json_store.py` — local JSON fallback search.

## Architecture summary

The implementation is not a pure scanned-PDF OCR pipeline. It is better described as:

1. Text-based PDF extraction:
   - Use PyMuPDF (`fitz`) first, typically `page.get_text("text")`.
   - Fall back to PyPDF2 if PyMuPDF fails.
   - Split text into chunks and attach metadata: `source_type=user`, `content_type=user_literature`, `page_num`, `doc_id`, `category`.

2. Enhanced layout/table assets:
   - Render PDF pages to JPEG.
   - Run DocLayout-YOLO to detect layout blocks such as figures/tables.
   - Run Table Transformer detection to detect table regions.
   - Crop detected figure/table regions into asset images.
   - Extract table text primarily with `pdfplumber`, then write Markdown/CSV assets.

3. Indexing/storage:
   - Always writes JSON sidecars/chunks under `data/user_literature/` as fallback.
   - If enabled/available, writes document/chunk/asset metadata to PostgreSQL.
   - If enabled/available, upserts text chunks into Chroma vector DB.
   - RAG can fall back from Chroma to `JsonKnowledgeStore`.

## Open-source models involved

The “YOLO and table model” Wyatt remembered map to:

- DocLayout-YOLO (`doclayout_yolo.YOLOv10`) for page layout detection.
  - Default path observed: `./.tools/pdf_parsers/models/doclayout-yolo/doclayout_yolo_docstructbench_imgsz1024.pt`
  - Typical settings observed: `imgsz=1024`, `conf=0.2`, device from config, often CPU.

- Microsoft Table Transformer for object detection via Hugging Face `transformers`.
  - `AutoImageProcessor`
  - `TableTransformerForObjectDetection`
  - Default detection model directory observed: `./.tools/pdf_parsers/models/table-transformer-detection`
  - Threshold observed around `0.75`.

A Table Transformer structure-recognition path may be configured, but in the inspected code the table text/structure extraction was mostly done by `pdfplumber`, not by a full Table Transformer structure pass.

## Important distinction to state clearly

DocLayout-YOLO and Table Transformer are layout/table detection models, not full OCR engines. They locate and crop regions; they do not by themselves convert scanned page images into searchable text. For scanned PDFs with no embedded text, this project may produce little/no textual chunk content unless an OCR engine such as PaddleOCR, RapidOCR, Tesseract, marker, Surya, etc. is added.

## Investigation checklist for similar projects

When asked “how does PDF go into the index DB?” inspect in this order:

1. Upload/API entrypoint: `knowledge.py`, `upload.py`, FastAPI routers, multipart form handling.
2. Parser service: PDF-to-text, page rendering, OCR/layout/table models, fallback behavior.
3. Config: parser root, model paths, feature toggles, device, Chroma/Postgres enable flags.
4. Storage outputs: `data/user_literature`, chunks JSON, metadata JSON, assets directories.
5. Indexer: PostgreSQL tables, Chroma upsert, JSON fallback.
6. Retrieval layer: ranking/source priority, fallback from vector DB to JSON/local store.
7. Tests/frontend: upload timeout, accepted extensions, integration tests for PDF/image extraction.

## Pitfalls

- Do not call a layout detector an OCR engine unless it actually recognizes text from pixels.
- A project can “use YOLO/Table Transformer for PDF parsing” while still relying on PyMuPDF/PyPDF2/pdfplumber for text.
- Missing local model directories are deployment state, not a durable rule. Report them as current-state observations only.
- Docker/Windows delivery packages may mount model assets in a different path than the macOS inspection path; preserve configured paths unless explicitly refactoring.
