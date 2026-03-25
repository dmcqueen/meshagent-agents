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
    :root {
      color-scheme: light;
      --bg: #f6f1e8;
      --panel: rgba(255, 252, 247, 0.92);
      --panel-border: rgba(128, 94, 63, 0.18);
      --text: #24180f;
      --muted: #6f5a49;
      --accent: #a64b2a;
      --accent-strong: #8a381b;
      --field: #fffdf9;
      --field-border: rgba(87, 61, 40, 0.18);
      --error-bg: #fff1ef;
      --error-text: #8e1f1f;
      --success-bg: #edf8ef;
      --success-text: #1f6c3d;
      --shadow: 0 24px 60px rgba(71, 41, 17, 0.12);
      font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at top, rgba(230, 178, 136, 0.32), transparent 36%),
        linear-gradient(180deg, #fbf7f1 0%, var(--bg) 100%);
      color: var(--text);
    }
    .shell {
      width: min(1080px, calc(100% - 32px));
      margin: 0 auto;
      padding: 56px 0 72px;
    }
    .panel {
      display: grid;
      grid-template-columns: minmax(0, 0.88fr) minmax(280px, 0.72fr);
      gap: 28px;
      align-items: start;
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: 32px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .intro {
      padding: 48px 44px;
      background:
        linear-gradient(160deg, rgba(166, 75, 42, 0.09), rgba(255, 255, 255, 0)),
        linear-gradient(180deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0));
    }
    .eyebrow {
      margin: 0 0 12px;
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 0.76rem;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--accent);
    }
    h1 {
      margin: 0;
      font-size: clamp(3rem, 7vw, 5.2rem);
      line-height: 0.96;
      letter-spacing: -0.04em;
    }
    .lede {
      max-width: 30rem;
      margin: 22px 0 0;
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 1.05rem;
      line-height: 1.7;
      color: var(--muted);
    }
    .notes {
      margin: 28px 0 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 10px;
      font-family: "Helvetica Neue", Arial, sans-serif;
      color: var(--text);
    }
    .notes li::before {
      content: "•";
      margin-right: 10px;
      color: var(--accent);
    }
    .form-wrap {
      padding: 32px;
      background: rgba(255, 255, 255, 0.62);
      border-left: 1px solid rgba(128, 94, 63, 0.14);
    }
    .flash {
      margin: 0 0 18px;
      padding: 14px 16px;
      border-radius: 16px;
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 0.96rem;
      line-height: 1.5;
    }
    .flash.error { background: var(--error-bg); color: var(--error-text); }
    .flash.success { background: var(--success-bg); color: var(--success-text); }
    form { display: grid; gap: 16px; }
    .row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }
    label {
      display: grid;
      gap: 8px;
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text);
    }
    input, textarea, button {
      font: inherit;
      border-radius: 16px;
    }
    input, textarea {
      width: 100%;
      padding: 14px 15px;
      border: 1px solid var(--field-border);
      background: var(--field);
      color: var(--text);
      outline: none;
      transition: border-color 120ms ease, box-shadow 120ms ease, transform 120ms ease;
    }
    input:focus, textarea:focus {
      border-color: rgba(166, 75, 42, 0.45);
      box-shadow: 0 0 0 4px rgba(166, 75, 42, 0.12);
    }
    textarea {
      min-height: 180px;
      resize: vertical;
    }
    .actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-top: 4px;
    }
    .hint {
      margin: 0;
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 0.88rem;
      line-height: 1.5;
      color: var(--muted);
    }
    button {
      border: 0;
      padding: 14px 24px;
      min-width: 180px;
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 1rem;
      font-weight: 700;
      color: #fffaf5;
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
      box-shadow: 0 16px 32px rgba(138, 56, 27, 0.22);
      cursor: pointer;
      transition: transform 120ms ease, box-shadow 120ms ease, filter 120ms ease;
    }
    button:hover {
      transform: translateY(-1px);
      box-shadow: 0 18px 36px rgba(138, 56, 27, 0.24);
      filter: saturate(1.05);
    }
    @media (max-width: 860px) {
      .panel { grid-template-columns: 1fr; }
      .form-wrap { border-left: 0; border-top: 1px solid rgba(128, 94, 63, 0.14); }
    }
    @media (max-width: 640px) {
      .shell { width: min(100% - 20px, 1080px); padding: 18px 0 32px; }
      .intro, .form-wrap { padding: 24px 18px; }
      .row { grid-template-columns: 1fr; }
      .actions { flex-direction: column; align-items: stretch; }
      button { width: 100%; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="panel">
      <div class="intro">
        <p class="eyebrow">Direct Line</p>
        <h1>Contact Me</h1>
        <p class="lede">Tell me what you are building, where you are blocked, or what kind of collaboration you need. Thoughtful notes get the fastest replies.</p>
        <ul class="notes">
          <li>Share the outcome you want, not just the task.</li>
          <li>Leave an email or phone number so I can reply the right way.</li>
          <li>Short or detailed messages are both welcome.</li>
        </ul>
      </div>
      <div class="form-wrap">
        __FLASH__
        <form method="post" action="/">
          <div class="row">
            <label>Name<input name="name" maxlength="80" required value="__NAME__"></label>
            <label>Email<input name="email" type="email" maxlength="120" value="__EMAIL__"></label>
          </div>
          <label>Phone<input name="phone" type="tel" maxlength="20" pattern="\\+?[0-9()\\-\\s]{7,20}" value="__PHONE__"></label>
          <label>Message<textarea name="message" maxlength="4000" required>__MESSAGE__</textarea></label>
          <div class="actions">
            <p class="hint">Your note goes directly to my inbox. I read every message.</p>
            <button type="submit">Send Message</button>
          </div>
        </form>
      </div>
    </section>
  </main>
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
        api_url = os.getenv("MESHAGENT_API_URL", "")
        if ".life" in api_url:
            hostname = "mail.meshagent.life"
        elif ".com" in api_url:
            hostname = "mail.meshagent.com"
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
                flash='<p class="flash error">Name is required.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if not values["message"]:
        return web.Response(
            text=render_page(
                flash='<p class="flash error">Message is required.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if not values["email"] and not values["phone"]:
        return web.Response(
            text=render_page(
                flash='<p class="flash error">Provide a valid email and/or phone number.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if values["email"] and not is_valid_email(values["email"]):
        return web.Response(
            text=render_page(
                flash='<p class="flash error">Please enter a valid email address.</p>',
                values=values,
            ),
            content_type="text/html",
            status=400,
        )
    if values["phone"] and not is_valid_phone(values["phone"]):
        return web.Response(
            text=render_page(
                flash='<p class="flash error">Please enter a valid phone number.</p>',
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
                flash=f'<p class="flash error">Unable to send mail: {html.escape(type(exc).__name__)}</p>',
                values=values,
            ),
            content_type="text/html",
            status=500,
        )

    return web.Response(
        text=render_page(
            flash='<p class="flash success">Thanks - your message has been sent.</p>'
        ),
        content_type="text/html",
    )
