#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from os import makedirs, replace
from os.path import abspath, basename, exists, expanduser, join, splitext
from shutil import which
from typing import Sequence, cast
from zipfile import ZipFile

from pdf2image import convert_from_path, pdfinfo_from_path

TWIPS_PER_INCH = 1440


def ensure_system_tools() -> None:
    missing = [tool for tool in ("soffice", "pdftoppm") if which(tool) is None]
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(
            f"Missing required system tool(s): {joined}. Install LibreOffice and Poppler first."
        )


def run_quiet(cmd: list[str]) -> None:
    subprocess.run(
        cmd,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=os.environ.copy(),
    )


def convert_to_pdf(doc_path: str, user_profile: str, out_dir: str, stem: str) -> str:
    pdf_path = join(out_dir, f"{stem}.pdf")

    direct = [
        "soffice",
        "-env:UserInstallation=file://" + user_profile,
        "--invisible",
        "--headless",
        "--norestore",
        "--convert-to",
        "pdf",
        "--outdir",
        out_dir,
        doc_path,
    ]
    run_quiet(direct)
    if exists(pdf_path):
        return pdf_path

    via_odt = [
        "soffice",
        "-env:UserInstallation=file://" + user_profile,
        "--invisible",
        "--headless",
        "--norestore",
        "--convert-to",
        "odt",
        "--outdir",
        out_dir,
        doc_path,
    ]
    run_quiet(via_odt)
    odt_path = join(out_dir, f"{stem}.odt")
    if exists(odt_path):
        run_quiet(
            [
                "soffice",
                "-env:UserInstallation=file://" + user_profile,
                "--invisible",
                "--headless",
                "--norestore",
                "--convert-to",
                "pdf",
                "--outdir",
                out_dir,
                odt_path,
            ]
        )
    return pdf_path if exists(pdf_path) else ""


def calc_dpi_from_docx(input_path: str, max_w_px: int, max_h_px: int) -> int:
    with ZipFile(input_path, "r") as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    sect_pr = root.find(".//w:sectPr", ns)
    if sect_pr is None:
        raise RuntimeError("Section properties not found in document.xml")
    pg_sz = sect_pr.find("w:pgSz", ns)
    if pg_sz is None:
        raise RuntimeError("Page size not found in section properties")

    w_twips = pg_sz.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w") or pg_sz.get("w")
    h_twips = pg_sz.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}h") or pg_sz.get("h")
    if not w_twips or not h_twips:
        raise RuntimeError("Page size attributes missing in pgSz")

    width_in = int(w_twips) / TWIPS_PER_INCH
    height_in = int(h_twips) / TWIPS_PER_INCH
    if width_in <= 0 or height_in <= 0:
        raise RuntimeError("Invalid page size values in document.xml")
    return round(min(max_w_px / width_in, max_h_px / height_in))


def calc_dpi_from_pdf(input_path: str, max_w_px: int, max_h_px: int) -> int:
    with tempfile.TemporaryDirectory(prefix="soffice_profile_") as user_profile:
        with tempfile.TemporaryDirectory(prefix="soffice_convert_") as convert_dir:
            stem = splitext(basename(input_path))[0]
            pdf_path = convert_to_pdf(input_path, user_profile, convert_dir, stem)
            if not pdf_path:
                raise RuntimeError("Failed to convert input to PDF for DPI calculation.")

            info = pdfinfo_from_path(pdf_path)
            size_value = info.get("Page size")
            if not isinstance(size_value, str):
                for key, value in info.items():
                    if isinstance(value, str) and "size" in key.lower() and "pts" in value:
                        size_value = value
                        break
            if not isinstance(size_value, str):
                raise RuntimeError("Failed to read PDF page size.")

            match = re.search(r"(\d+)\s*x\s*(\d+)\s*pts", size_value)
            if not match:
                raise RuntimeError("Unrecognized PDF page size format.")

            width_in = int(match.group(1)) / 72.0
            height_in = int(match.group(2)) / 72.0
            if width_in <= 0 or height_in <= 0:
                raise RuntimeError("Invalid PDF page size.")
            return round(min(max_w_px / width_in, max_h_px / height_in))


def rasterize(doc_path: str, out_dir: str, dpi: int, keep_pdf: bool) -> Sequence[str]:
    makedirs(out_dir, exist_ok=True)
    doc_path = abspath(doc_path)
    stem = splitext(basename(doc_path))[0]

    with tempfile.TemporaryDirectory(prefix="soffice_profile_") as user_profile:
        with tempfile.TemporaryDirectory(prefix="soffice_convert_") as convert_dir:
            pdf_path = convert_to_pdf(doc_path, user_profile, convert_dir, stem)
            if not pdf_path:
                raise RuntimeError("Failed to produce PDF for rasterization.")

            raw_paths = cast(
                list[str],
                convert_from_path(
                    pdf_path,
                    dpi=dpi,
                    fmt="png",
                    thread_count=4,
                    output_folder=out_dir,
                    paths_only=True,
                    output_file="page",
                ),
            )

            if keep_pdf:
                replace(pdf_path, join(out_dir, f"{stem}.pdf"))

    pages: list[tuple[int, str]] = []
    for src_path in raw_paths:
        base = splitext(basename(src_path))[0]
        page_num = int(base.split("-")[-1])
        dst_path = join(out_dir, f"page-{page_num}.png")
        replace(src_path, dst_path)
        pages.append((page_num, dst_path))
    pages.sort(key=lambda item: item[0])
    return [path for _, path in pages]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a DOCX-like file to PNG pages.")
    parser.add_argument("input_path", help="Path to the input document.")
    parser.add_argument("--output-dir", default=None, help="Directory for rendered output.")
    parser.add_argument("--width", type=int, default=1600, help="Target max width in pixels.")
    parser.add_argument("--height", type=int, default=2000, help="Target max height in pixels.")
    parser.add_argument("--dpi", type=int, default=None, help="Override computed DPI.")
    parser.add_argument("--keep-pdf", action="store_true", help="Keep the intermediate PDF in the output directory.")
    args = parser.parse_args()

    try:
        ensure_system_tools()
        input_path = abspath(expanduser(args.input_path))
        out_dir = abspath(expanduser(args.output_dir)) if args.output_dir else splitext(input_path)[0]
        dpi = args.dpi
        if dpi is None:
            try:
                if input_path.lower().endswith((".docx", ".docm", ".dotx", ".dotm")):
                    dpi = calc_dpi_from_docx(input_path, args.width, args.height)
                else:
                    raise RuntimeError("Not an OOXML document")
            except Exception:
                dpi = calc_dpi_from_pdf(input_path, args.width, args.height)

        pages = rasterize(input_path, out_dir, int(dpi), args.keep_pdf)
        print(f"Rendered {len(pages)} page(s) to {out_dir}")
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
