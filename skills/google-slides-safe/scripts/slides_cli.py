#!/usr/bin/env python3
import argparse
import io
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials as UserCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive.file",
]

PT = 12700  # EMU per point
LAYOUTS = {
    "default": {
        "title": {"x": 36, "y": 28, "w": 648, "h": 52, "font": 26, "bold": True},
        "body": {"x": 36, "y": 98, "w": 420, "h": 320, "font": 16, "bold": False},
        "image": {"x": 475, "y": 110, "w": 205, "h": 250},
    },
    "cover": {
        "title": {"x": 60, "y": 80, "w": 560, "h": 70, "font": 30, "bold": True},
        "body": {"x": 60, "y": 160, "w": 560, "h": 80, "font": 18, "bold": False},
        "image": {"x": 250, "y": 260, "w": 200, "h": 200},
    },
    "problem": {
        "title": {"x": 36, "y": 24, "w": 648, "h": 48, "font": 24, "bold": True},
        "body": {"x": 36, "y": 82, "w": 320, "h": 320, "font": 16, "bold": False},
        "image": {"x": 390, "y": 96, "w": 290, "h": 220},
        "image2": {"x": 390, "y": 326, "w": 290, "h": 170},
    },
    "solution": {
        "title": {"x": 36, "y": 24, "w": 648, "h": 48, "font": 24, "bold": True},
        "body": {"x": 36, "y": 350, "w": 648, "h": 120, "font": 15, "bold": False},
        "image": {"x": 80, "y": 86, "w": 560, "h": 240},
    },
    "market": {
        "title": {"x": 36, "y": 24, "w": 648, "h": 48, "font": 24, "bold": True},
        "body": {"x": 36, "y": 88, "w": 340, "h": 320, "font": 16, "bold": False},
        "image": {"x": 400, "y": 110, "w": 260, "h": 240},
    },
    "traction": {
        "title": {"x": 36, "y": 24, "w": 648, "h": 48, "font": 24, "bold": True},
        "body": {"x": 36, "y": 350, "w": 648, "h": 120, "font": 15, "bold": False},
        "image": {"x": 80, "y": 86, "w": 560, "h": 230},
    },
    "team": {
        "title": {"x": 36, "y": 30, "w": 648, "h": 48, "font": 24, "bold": True},
        "body": {"x": 60, "y": 110, "w": 580, "h": 300, "font": 18, "bold": False},
        "image": {"x": 480, "y": 330, "w": 140, "h": 140},
    },
}


def emu(n: float) -> int:
    return int(n * PT)


def load_credentials(auth_mode: str, credentials_path: str, token_path: Optional[str] = None):
    credentials_file = Path(credentials_path)
    if not credentials_file.exists():
        raise FileNotFoundError(f"Credentials file not found: {credentials_file}")

    if auth_mode == "service-account":
        return service_account.Credentials.from_service_account_file(str(credentials_file), scopes=SCOPES)

    token_file = Path(token_path) if token_path else credentials_file.with_suffix(".token.json")
    creds = None
    if token_file.exists():
        creds = UserCredentials.from_authorized_user_file(str(token_file), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), SCOPES)
        creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json())
    return creds


def slides_service(creds):
    return build("slides", "v1", credentials=creds)


def drive_service(creds):
    return build("drive", "v3", credentials=creds)


def create_presentation(slides, title: str) -> str:
    resp = slides.presentations().create(body={"title": title}).execute()
    return resp["presentationId"]


def duplicate_first_slide_to_remove_default(slides, presentation_id: str):
    pres = slides.presentations().get(presentationId=presentation_id).execute()
    first_slide = pres["slides"][0]["objectId"]
    slides.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": [{"deleteObject": {"objectId": first_slide}}]},
    ).execute()


def add_text_box_requests(page_id: str, shape_id: str, text: str, box: Dict[str, float]) -> List[Dict[str, Any]]:
    return [
        {
            "createShape": {
                "objectId": shape_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": page_id,
                    "size": {
                        "width": {"magnitude": emu(box["w"]), "unit": "EMU"},
                        "height": {"magnitude": emu(box["h"]), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": emu(box["x"]),
                        "translateY": emu(box["y"]),
                        "unit": "EMU",
                    },
                },
            }
        },
        {"insertText": {"objectId": shape_id, "text": text}},
        {
            "updateTextStyle": {
                "objectId": shape_id,
                "style": {
                    "fontSize": {"magnitude": box.get("font", 16), "unit": "PT"},
                    "bold": box.get("bold", False),
                },
                "textRange": {"type": "ALL"},
                "fields": "fontSize,bold",
            }
        },
    ]


def add_image_request(page_id: str, image_id: str, url: str, box: Dict[str, float]) -> Dict[str, Any]:
    return {
        "createImage": {
            "objectId": image_id,
            "url": url,
            "elementProperties": {
                "pageObjectId": page_id,
                "size": {
                    "width": {"magnitude": emu(box["w"]), "unit": "EMU"},
                    "height": {"magnitude": emu(box["h"]), "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1,
                    "scaleY": 1,
                    "translateX": emu(box["x"]),
                    "translateY": emu(box["y"]),
                    "unit": "EMU",
                },
            },
        }
    }


def bullet_text(items: List[str]) -> str:
    return "\n".join(items)


def ensure_drive_file_public(drive, file_id: str):
    drive.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
        fields="id",
    ).execute()


def drive_file_to_image_url(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=view&id={file_id}"


def resolve_image_url(slide: Dict[str, Any], drive, publish_drive_images: bool) -> Optional[str]:
    if slide.get("image_url"):
        return slide["image_url"]
    file_id = slide.get("drive_file_id")
    if file_id:
        if publish_drive_images:
            ensure_drive_file_public(drive, file_id)
        return drive_file_to_image_url(file_id)
    return None


def resolve_second_image_url(slide: Dict[str, Any], drive, publish_drive_images: bool) -> Optional[str]:
    if slide.get("image2_url"):
        return slide["image2_url"]
    file_id = slide.get("drive_file_id_2")
    if file_id:
        if publish_drive_images:
            ensure_drive_file_public(drive, file_id)
        return drive_file_to_image_url(file_id)
    return None


def add_slide_requests(index: int, slide: Dict[str, Any], drive, publish_drive_images: bool) -> List[Dict[str, Any]]:
    page_id = slide.get("id") or f"slide_{index}"
    layout_name = slide.get("layout", "default")
    layout = LAYOUTS.get(layout_name, LAYOUTS["default"])
    reqs: List[Dict[str, Any]] = [
        {"createSlide": {"objectId": page_id, "insertionIndex": index, "slideLayoutReference": {"predefinedLayout": "BLANK"}}}
    ]

    title = slide.get("title", "")
    if title:
        reqs.extend(add_text_box_requests(page_id, f"title_{index}", title, layout["title"]))

    body_lines = slide.get("bullets") or []
    body_text = slide.get("body") or bullet_text(body_lines)
    if body_text:
        reqs.extend(add_text_box_requests(page_id, f"body_{index}", body_text, layout["body"]))
        if body_lines:
            reqs.append({
                "createParagraphBullets": {
                    "objectId": f"body_{index}",
                    "textRange": {"type": "ALL"},
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                }
            })

    image_url = resolve_image_url(slide, drive, publish_drive_images)
    if image_url and "image" in layout:
        reqs.append(add_image_request(page_id, f"image_{index}", image_url, layout["image"]))

    image2_url = resolve_second_image_url(slide, drive, publish_drive_images)
    if image2_url and "image2" in layout:
        reqs.append(add_image_request(page_id, f"image2_{index}", image2_url, layout["image2"]))

    return reqs


def build_deck(slides_api, drive, presentation_id: str, spec: Dict[str, Any], publish_drive_images: bool = False):
    slides = spec.get("slides") or []
    requests: List[Dict[str, Any]] = []
    for idx, slide in enumerate(slides):
        requests.extend(add_slide_requests(idx, slide, drive, publish_drive_images))
    if requests:
        slides_api.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": requests},
        ).execute()


def move_to_folder(drive, file_id: str, folder_id: str):
    meta = drive.files().get(fileId=file_id, fields="parents").execute()
    prev_parents = ",".join(meta.get("parents", []))
    drive.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=prev_parents,
        fields="id, parents",
    ).execute()


def export_pdf(drive, presentation_id: str, out_path: str):
    request = drive.files().export_media(fileId=presentation_id, mimeType="application/pdf")
    fh = io.FileIO(out_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.close()


def cmd_auth_check(args):
    creds = load_credentials(args.auth_mode, args.credentials, args.token_path)
    about = drive_service(creds).about().get(fields="user(displayName,emailAddress)").execute()
    user = about.get("user", {})
    print(json.dumps({
        "ok": True,
        "scopes": SCOPES,
        "user": user,
        "auth_mode": args.auth_mode,
    }, indent=2))


def cmd_create_from_spec(args):
    creds = load_credentials(args.auth_mode, args.credentials, args.token_path)
    slides = slides_service(creds)
    drive = drive_service(creds)
    spec = json.loads(Path(args.spec).read_text())
    title = args.title or spec.get("title") or "Untitled deck"
    presentation_id = create_presentation(slides, title)
    duplicate_first_slide_to_remove_default(slides, presentation_id)
    build_deck(slides, drive, presentation_id, spec, publish_drive_images=args.publish_drive_images)
    if args.folder_id:
        move_to_folder(drive, presentation_id, args.folder_id)
    result = {
        "presentation_id": presentation_id,
        "title": title,
        "slides_url": f"https://docs.google.com/presentation/d/{presentation_id}/edit",
    }
    if args.export_pdf:
        export_pdf(drive, presentation_id, args.export_pdf)
        result["pdf_path"] = args.export_pdf
    print(json.dumps(result, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description="Safe Google Slides CLI with explicit auth, layout presets, and minimal scopes.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_auth_flags(sp):
        sp.add_argument("--auth-mode", choices=["service-account", "oauth"], required=True)
        sp.add_argument("--credentials", required=True, help="Path to service-account JSON or OAuth client secret JSON")
        sp.add_argument("--token-path", help="Optional OAuth token JSON path")

    s1 = sub.add_parser("auth-check", help="Verify credentials and print resolved Google account")
    add_auth_flags(s1)
    s1.set_defaults(func=cmd_auth_check)

    s2 = sub.add_parser("create-from-spec", help="Create a Google Slides deck from a JSON spec")
    add_auth_flags(s2)
    s2.add_argument("--spec", required=True, help="Path to JSON spec file")
    s2.add_argument("--title", help="Override deck title")
    s2.add_argument("--folder-id", help="Optional Drive folder id")
    s2.add_argument("--export-pdf", help="Optional output path for exported PDF")
    s2.add_argument("--publish-drive-images", action="store_true", help="Make referenced Drive image files link-readable so Slides can fetch them by drive_file_id")
    s2.set_defaults(func=cmd_create_from_spec)
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
