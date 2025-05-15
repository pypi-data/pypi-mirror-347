from typing import TypedDict, List

from s3_file_picker.models.typed_dict.S3FileItem import S3FileItem


class S3FolderContent(TypedDict):
    folder: str
    files: List[S3FileItem]
    