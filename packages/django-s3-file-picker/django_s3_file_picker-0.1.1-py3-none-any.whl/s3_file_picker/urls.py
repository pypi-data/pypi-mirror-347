from django.urls import path
from django.conf.urls.static import static

from s3_file_picker.view.FileView import FileView
from s3_file_picker.view.FilesView import FilesView


urlpatterns = [
	path("s3_file_picker/api/files", FilesView.as_view()),
	path("s3_file_picker/api/files/<str:encoded_key>", FileView.as_view())
] + static("s3_file_picker/static/", document_root="s3_file_picker/static")
