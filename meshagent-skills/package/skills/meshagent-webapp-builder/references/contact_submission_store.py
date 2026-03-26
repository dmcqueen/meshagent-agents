from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from meshagent.api import RoomClient
from meshagent.api.room_server_client import TextDataType, TimestampDataType


CONTACT_SUBMISSIONS_TABLE = "contact_submissions"


async def ensure_contact_submissions_table(*, room: RoomClient) -> None:
    await room.database.create_table_with_schema(
        name=CONTACT_SUBMISSIONS_TABLE,
        schema={
            "name": TextDataType(),
            "email": TextDataType(),
            "phone": TextDataType(),
            "message": TextDataType(),
            "submitted_at": TimestampDataType(),
            "user_agent": TextDataType(),
            "source_ip": TextDataType(),
        },
        mode="create_if_not_exists",
        data=None,
    )


async def persist_contact_submission(
    *,
    room: RoomClient,
    values: dict[str, str],
    user_agent: str = "",
    source_ip: str = "",
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "name": values["name"],
        "email": values["email"] or None,
        "phone": values["phone"] or None,
        "message": values["message"],
        "submitted_at": datetime.now(timezone.utc),
        "user_agent": user_agent,
        "source_ip": source_ip,
    }
    await room.database.insert(table=CONTACT_SUBMISSIONS_TABLE, records=[record])
    return record
