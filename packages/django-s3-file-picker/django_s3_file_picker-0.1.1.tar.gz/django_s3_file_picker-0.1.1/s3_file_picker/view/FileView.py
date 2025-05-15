import base64
import os
from pathlib import Path
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from django.views import View

from s3_file_picker.service.S3Service import S3Service


class FileView(View):
	
	def __init__(self, **kwargs: Any):
		super().__init__(**kwargs)
		self.s3 = S3Service(
			region_name=settings.MEDIA_AWS_S3_REGION_NAME,
			endpoint_url=settings.MEDIA_AWS_S3_CUSTOM_DOMAIN,
			aws_access_key_id=settings.MEDIA_AWS_ACCESS_KEY_ID,
			aws_secret_access_key=settings.MEDIA_AWS_SECRET_ACCESS_KEY,
			bucket_name=settings.MEDIA_AWS_STORAGE_BUCKET_NAME,
		)
	
	def delete(self, request, encoded_key: str):
		if request.user.is_authenticated:
			key = base64.b64decode(encoded_key).decode()
			self.s3.delete_file(key=key)
			return HttpResponse(
				content=True
			)
		else:
			return HttpResponse(
				content="Forbidden",
				status=403
			)
	
	def patch(self, request, encoded_key: str):
		if request.user.is_authenticated:
			key = base64.b64decode(encoded_key).decode()
			new_key = request.GET["new_key"]
			self.s3.rename_file(old_key=key, new_key=new_key)
			return HttpResponse(
				content=True
			)
		else:
			return HttpResponse(
				content="Forbidden",
				status=403
			)
	
	def post(self, request, encoded_key: str):
		if request.user.is_authenticated:
			key = base64.b64decode(encoded_key).decode()
			content_type = request.headers["Content-Type"]
			tmp_file = Path(f"/tmp/{encoded_key}")
			with open(tmp_file, "wb") as writer:
				writer.write(request.body)
			self.s3.upload_file(
				key=key,
				file=tmp_file,
				content_type=content_type
			)
			os.remove(tmp_file)
			return HttpResponse(
				content=True
			)
		else:
			return HttpResponse(
				content="Forbidden",
				status=403
			)
