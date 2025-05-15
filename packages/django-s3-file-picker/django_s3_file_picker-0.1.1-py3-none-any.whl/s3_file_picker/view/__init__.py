from django.http import HttpResponse

from main.settings import BASE_DIR


def resource_view(request):
	with open(BASE_DIR / "filemanager" / "templates" / "js" / "filebrowser.js") as reader:
		return HttpResponse(
			content=reader.read(),
			content_type="text/javascript"
		)
