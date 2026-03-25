from __future__ import annotations

import html
import os
import re
import smtplib
from email.message import EmailMessage

from aiohttp import web
from meshagent.api import RoomClient

RECIPIENT = "__DESTINATION_EMAIL_ADDRESS__"
MAILBOX_SENDER = "__MAILBOX_ADDRESS_FROM_MESHAGENT_MAILBOX_COMMAND__"

EMAIL_RE = re.compile(r"^[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,63}$", re.IGNORECASE)
PHONE_RE = re.compile(r"^\+?[0-9()\-\s]{7,20}$")

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contact Me</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px auto; max-width: 720px; padding: 0 16px; }
    form { display: grid; gap: 12px; }
    input, textarea, button { font: inherit; padding: 10px; }
    textarea { min-height: 140px; }
    .error { color: #991b1b; }
    .success { color: #166534; }
  </style>
</head>
<body>
  <h1>Contact Me</h1>
  __FLASH__
  <form method="post" action="/">
    <label>Name <input name="name" maxlength="80" required value="__NAME__"></label>
    <label>Email <input name="email" type="email" maxlength="120" value="__EMAIL__"></label>
    <label>Phone <input name="phone" type="tel" maxlength="20" pattern="\\+?[0-9()\\-\\s]{7,20}" value="__PHONE__"></label>
    <label>Message <textarea name="message" maxlength="4000" required>__MESSAGE__</textarea></label>
    <button type="submit">Send</button>
  </form>
</body>
</html>"""


def sanitize_single_line(value: str, *, max_len: int) -> str:
    value = (value or "").strip().replace("\r", " ").replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[<>]", "", value)
    return value[:max_len]


def sanitize_multiline(value: str, *, max_len: int) -> str:
    value = (value or "").strip().replace("\r\n", "\n").replace("\r", "\n")
    value = value.replace("\x00", "")
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value[:max_len]


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_RE.fullmatch(value or ""))


def is_valid_phone(value: str) -> bool:
    if not PHONE_RE.fullmatch(value or ""):
        return False
    digits = re.sub(r"\D", "", value)
    return 7 <= len(digits) <= 15


def render_page(*, flash: str = "", values: dict[str, str] | None = None) -> str:
    values = values or {}
    return (
        PAGE.replace("__FLASH__", flash)
        .replace("__NAME__", html.escape(values.get("name", ""), quote=True))
        .replace("__EMAIL__", html.escape(values.get("email", ""), quote=True))
        .replace("__PHONE__", html.escape(values.get("phone", ""), quote=True))
        .replace("__MESSAGE__", html.escape(values.get("message", "")))
    )


def _room_smtp_config(*, room: RoomClient) -> tuple[str | None, str | None, int, str]:
    username = os.getenv("SMTP_USERNAME")
    if username is None:
        participant_name = room.local_participant.get_attribute("name")
        username = participant_name if isinstance(participant_name, str) else None

    password = os.getenv("SMTP_PASSWORD")
    if password is None:
        password = room.protocol.token

    hostname = os.getenv("SMTP_HOSTNAME")
    if hostname is None:
        raise RuntimeError(
            "SMTP_HOSTNAME is not configured for this runtime; inspect the room mail configuration before using direct SMTP."
        )

    port = int(os.getenv("SMTP_PORT", "587"))
    return username, password, port, hostname


async def handler(*, room: RoomClient, req: web.Request) -> web.StreamResponse:
    if req.method == "GET":
        return web.Response(text=render_page(), content_type="text/html")

    data = await req.post()
    values = {
        "name": sanitize_single_line(data.get("name", ""), max_len=80),
        "email": sanitize_single_line(data.get("email", ""), max_len=120),
        "phone": sanitize_single_line(data.get("phone", ""), max_len=20),
        "message": sanitize_multiline(data.get("message", ""), max_len=4000),
    }

    if not values["name"]:
        return web.Response(
            text=render_page(
                flash='<p class="error">Name is required.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if not values["message"]:
        return web.Response(
            text=render_page(
                flash='<p class="error">Message is required.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if not values["email"] and not values["phone"]:
        return web.Response(
            text=render_page(
                flash='<p class="error">Provide a valid email and/or phone number.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if values["email"] and not is_valid_email(values["email"]):
        return web.Response(
            text=render_page(
                flash='<p class="error">Please enter a valid email address.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if values["phone"] and not is_valid_phone(values["phone"]):
        return web.Response(
            text=render_page(
                flash='<p class="error">Please enter a valid phone number.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )

    msg = EmailMessage()
    msg["Subject"] = f"Contact form submission from {values['name']}"
    msg["From"] = MAILBOX_SENDER
    msg["To"] = RECIPIENT
    if values["email"]:
        msg["Reply-To"] = values["email"]
    msg.set_content(
        "New contact form submission\n\n"
        f"Name: {values['name']}\n"
        f"Email: {values['email'] or '(not provided)'}\n"
        f"Phone: {values['phone'] or '(not provided)'}\n\n"
        f"Message:\n{values['message']}\n"
    )

    try:
        username, password, port, hostname = _room_smtp_config(room=room)
        with smtplib.SMTP(hostname, port, timeout=20) as smtp:
            smtp.starttls()
            if username and password:
                smtp.login(username, password)
            smtp.send_message(msg)
    except Exception as exc:
        return web.Response(
            text=render_page(
                flash=f'<p class="error">Unable to send mail: {html.escape(type(exc).__name__)}</p>',
                values=values,
            ),
            content_type="text/html",
            status=500,
        )

    return web.Response(
        text=render_page(
            flash='<p class="success">Thanks - your message has been sent.</p>'
        ),
        content_type="text/html",
    )
