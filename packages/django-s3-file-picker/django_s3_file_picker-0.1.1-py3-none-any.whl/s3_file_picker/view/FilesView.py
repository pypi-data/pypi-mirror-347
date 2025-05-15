import json
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from django.views import View

from s3_file_picker.service.S3Service import S3Service


class FilesView(View):
	
	def __init__(self, **kwargs: Any):
		super().__init__(**kwargs)
		self.s3 = S3Service(
			region_name=settings.MEDIA_AWS_S3_REGION_NAME,
			endpoint_url=settings.MEDIA_AWS_S3_CUSTOM_DOMAIN,
			aws_access_key_id=settings.MEDIA_AWS_ACCESS_KEY_ID,
			aws_secret_access_key=settings.MEDIA_AWS_SECRET_ACCESS_KEY,
			bucket_name=settings.MEDIA_AWS_STORAGE_BUCKET_NAME,
		)
	
	def get(self, request):
		if request.user.is_authenticated:
			folder = request.GET["path"]
			data = self.s3.list_folder_items(folder=folder)
			return HttpResponse(
				content=json.dumps(data, default=str),
				content_type="application/json"
			)
		else:
			return HttpResponse(
				content="Forbidden",
				status=403
			)

