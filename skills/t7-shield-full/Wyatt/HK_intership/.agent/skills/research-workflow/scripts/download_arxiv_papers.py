from __future__ import annotations

import argparse
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import ssl


def extract_arxiv_id(url: str) -> str | None:
    try:
        p = urllib.parse.urlparse(url.strip())
        if not p.netloc.endswith("arxiv.org"):
            return None
        if p.path.startswith("/pdf/"):
            seg = p.path.split("/pdf/")[1]
            if seg.endswith(".pdf"):
                seg = seg[:-4]
            return seg
        if p.path.startswith("/abs/"):
            return p.path.split("/abs/")[1]
        m = re.search(r"arxiv\.org/(?:abs|pdf)/([^/?#]+)", url)
        if m:
            v = m.group(1)
            return v[:-4] if v.endswith(".pdf") else v
        return None
    except Exception:
        return None


def fetch_title(arxiv_id: str, timeout: int = 20) -> str | None:
    try:
        q = f"http://export.arxiv.org/api/query?search_query=id:{urllib.parse.quote(arxiv_id)}&max_results=1"
        req = urllib.request.Request(q, headers={"User-Agent": "Mozilla/5.0"})
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None
        title_el = entry.find("atom:title", ns)
        if title_el is None:
            return None
        return " ".join(title_el.text.split())
    except Exception:
        return None


def sanitize_filename(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"-{2,}", "-", name)
    name = name.strip(".- ")
    # Keep paper directories well below Windows path limits once
    # paper_artifacts and hashed image names are added during conversion.
    if len(name) > 48:
        name = name[:48].rstrip()
    return name


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def download_pdf(arxiv_id: str, outdir: str, filename: str, timeout: int = 60, retries: int = 3) -> str:
    ensure_dir(outdir)
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    target = os.path.join(outdir, filename)
    tmp = target + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    ctx = ssl._create_unverified_context()

    last_error = None
    for attempt in range(1, retries + 1):
        try:
            print(f"尝试下载 {arxiv_id} (第 {attempt}/{retries} 次)...")
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp, open(tmp, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
            os.replace(tmp, target)
            return target
        except Exception as e:
            last_error = e
            print(f"下载失败 (第 {attempt} 次): {e}")
            if attempt < retries:
                sleep_time = 2 * attempt  # 指数退避: 2s, 4s, 6s...
                time.sleep(sleep_time)
            
    if os.path.exists(tmp):
        try:
            os.remove(tmp)
        except OSError:
            pass
    raise last_error or Exception("Unknown download error")


def process_link(url: str, outdir: str) -> tuple[bool, str]:
    url = url.strip().lstrip("\ufeff")
    if not url or url.startswith("#"):
        return True, "跳过空行或注释"
    arxiv_id = extract_arxiv_id(url)
    if not arxiv_id:
        try:
            p = urllib.parse.urlparse(url)
            base = os.path.basename(p.path) or "paper"
            if base.lower().endswith(".pdf"):
                base = base[:-4]
            fname_base = sanitize_filename(base)
            paper_dir = os.path.join(outdir, fname_base)
            ensure_dir(paper_dir)
            fname = "paper.pdf"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            ctx = ssl._create_unverified_context()
            tmp_target = os.path.join(paper_dir, fname) + ".part"
            final_target = os.path.join(paper_dir, fname)
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp, open(tmp_target, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
            os.replace(tmp_target, final_target)
            return True, f"已下载并重命名: {final_target}"
        except Exception as e:
            return False, f"无法解析或下载链接: {url} 错误: {e}"
    title = fetch_title(arxiv_id)
    if not title:
        title = f"arXiv {arxiv_id}"
    fname_base = sanitize_filename(title)
    paper_dir = os.path.join(outdir, fname_base)
    ensure_dir(paper_dir)
    fname = "paper.pdf"
    try:
        final_path = download_pdf(arxiv_id, paper_dir, fname)
        return True, f"已下载并重命名: {final_path}"
    except Exception as e:
        return False, f"下载失败 {arxiv_id}: {e}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="paper_list.txt")
    parser.add_argument("--outdir", default="downloads")
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero code if any download fails")
    args = parser.parse_args()
    if not os.path.isfile(args.input):
        print(f"未找到输入文件: {args.input}", file=sys.stderr)
        sys.exit(1)
    ensure_dir(args.outdir)
    total = 0
    ok = 0
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            total += 1
            success, msg = process_link(line, args.outdir)
            print(msg)
            if success:
                ok += 1
            time.sleep(args.delay)
    print(f"完成: {ok}/{total} 成功")
    
    if args.strict and ok < total:
        print(f"严谨模式: 存在 {total - ok} 个失败项，退出码非零。", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
