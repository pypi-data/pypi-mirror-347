from datetime import datetime
from typing import TypedDict, Optional


class S3FileItem(TypedDict):
    key: str
    is_folder: bool
    url: Optional[str]
    size: Optional[int]
    last_modified: Optional[datetime]
    