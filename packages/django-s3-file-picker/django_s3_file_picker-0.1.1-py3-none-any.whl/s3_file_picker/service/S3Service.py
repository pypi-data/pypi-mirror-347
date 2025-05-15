from io import BytesIO
from pathlib import Path
from typing import Optional, List, Union

import boto3
from mypy_boto3_s3.client import S3Client

from s3_file_picker.models.typed_dict.S3FileItem import S3FileItem
from s3_file_picker.models.typed_dict.S3FolderContent import S3FolderContent


class S3Service:
    def __init__(
        self,
        region_name: str,
        endpoint_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        bucket_name: str,
    ) -> None:
        session = boto3.Session()
        self.client: Optional[S3Client] = session.client(
            service_name="s3",
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket_name = bucket_name

    def get_file_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate a presigned URL to access the file."""
        url = self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': key},
            ExpiresIn=expires_in
        )
        return url

    def list_folder_items(self, folder: str = "") -> S3FolderContent:
        """List items in the given folder/prefix."""
        response = self.client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=folder,
            Delimiter="/"
        )

        files: List[S3FileItem] = []

        for prefix in response.get("CommonPrefixes", []):
            if prefix["Prefix"] != folder:
                files.append(S3FileItem(
                    is_folder=True,
                    key=prefix["Prefix"],
                    url=None,
                    size=None,
                    last_modified=None
                ))

        for item in response.get('Contents', []):
            if item['Key'] != folder:
                files.append(S3FileItem(
                    is_folder=False,
                    key=item['Key'],
                    url=self.get_file_url(item['Key']),
                    size=item['Size'],
                    last_modified=item['LastModified']
                ))

        return S3FolderContent(folder=folder, files=files)

    def delete_file(self, key: str) -> bool:
        """Delete a file by its key."""
        self.client.delete_object(Bucket=self.bucket_name, Key=key)
        return True

    def rename_file(self, old_key: str, new_key: str) -> bool:
        """Rename a file by copying it to a new key and deleting the old one."""
        copy_source = {'Bucket': self.bucket_name, 'Key': old_key}
        self.client.copy_object(
            Bucket=self.bucket_name,
            CopySource=copy_source,
            Key=new_key
        )
        self.client.delete_object(Bucket=self.bucket_name, Key=old_key)
        return True
    
    def upload_file(
            self,
            file: Union[Path, BytesIO, bytes],
            key: str,
            content_type: Optional[str] = None
    ) -> bool:
        """
        Upload a file to the given S3 key.

        :param file: Path to local file or a BytesIO buffer
        :param key: Target key in S3 bucket (e.g. 'uploads/myfile.png')
        :param content_type: Optional MIME type
        """
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        
        if isinstance(file, Path):
            with open(file, "rb") as f:
                self.client.upload_fileobj(f, self.bucket_name, key, ExtraArgs=extra_args)
        elif isinstance(file, BytesIO):
            self.client.upload_fileobj(file, self.bucket_name, key, ExtraArgs=extra_args)
        else:
            raise TypeError("`file` must be a Path or BytesIO")
        
        return True
    