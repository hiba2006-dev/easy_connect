import json

from sqlalchemy.orm import Session

import app.models as models


def record_activity(
    db: Session,
    user_id: int,
    activity_type: str,
    detail: str,
    metadata: dict | None = None,
) -> models.ActivityLog:
    entry = models.ActivityLog(
        user_id=user_id,
        activity_type=activity_type,
        detail=detail,
        meta_info=json.dumps(metadata, ensure_ascii=False) if metadata else None,
    )
    db.add(entry)
    return entry
