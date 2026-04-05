from pathlib import Path


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap_line(text: str, max_chars: int = 92):
    if not text:
        return [""]
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if len(trial) <= max_chars:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paginate(lines, lines_per_page=48):
    pages = []
    page = []
    for line in lines:
        page.append(line)
        if len(page) >= lines_per_page:
            pages.append(page)
            page = []
    if page:
        pages.append(page)
    return pages


def make_pdf(text: str, output_path: Path):
    raw_lines = []
    for src_line in text.splitlines():
        if src_line.startswith("```"):
            raw_lines.append("")
            continue
        if len(src_line) <= 92:
            raw_lines.append(src_line)
        else:
            raw_lines.extend(wrap_line(src_line, 92))

    pages = paginate(raw_lines)
    objects = []

    catalog_id = 1
    pages_id = 2
    font_id = 3
    first_page_id = 4
    first_content_id = 5

    page_ids = []
    content_ids = []

    next_id = first_page_id
    for _ in pages:
        page_ids.append(next_id)
        content_ids.append(next_id + 1)
        next_id += 2

    objects.append(f"{catalog_id} 0 obj\n<< /Type /Catalog /Pages {pages_id} 0 R >>\nendobj\n")

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects.append(
        f"{pages_id} 0 obj\n<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>\nendobj\n"
    )

    objects.append(f"{font_id} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

    for page_num, page_lines in enumerate(pages):
        page_id = page_ids[page_num]
        content_id = content_ids[page_num]
        stream_lines = ["BT", "/F1 10 Tf", "50 780 Td", "14 TL"]
        first = True
        for line in page_lines:
            escaped = pdf_escape(line)
            if first:
                stream_lines.append(f"({escaped}) Tj")
                first = False
            else:
                stream_lines.append(f"T* ({escaped}) Tj")
        stream_lines.append("ET")
        stream = "\n".join(stream_lines) + "\n"
        objects.append(
            f"{page_id} 0 obj\n<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>\nendobj\n"
        )
        objects.append(
            f"{content_id} 0 obj\n<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}endstream\nendobj\n"
        )

    header = "%PDF-1.4\n"
    body = ""
    offsets = [0]
    current = len(header.encode("latin-1"))
    for obj in objects:
        offsets.append(current)
        body += obj
        current += len(obj.encode("latin-1"))

    xref_start = current
    xref = [f"xref\n0 {len(objects) + 1}\n", "0000000000 65535 f \n"]
    for offset in offsets[1:]:
        xref.append(f"{offset:010d} 00000 n \n")
    trailer = (
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
        f"startxref\n{xref_start}\n%%EOF\n"
    )

    output_path.write_bytes((header + body + "".join(xref) + trailer).encode("latin-1"))


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    source = base / "ABC_Verilog_to_AIG_Guide.md"
    output = base / "ABC_Verilog_to_AIG_Guide.pdf"
    make_pdf(source.read_text(encoding="utf-8"), output)
