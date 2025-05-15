from django.forms.widgets import TextInput


class S3KeyInput(TextInput):

    input_type = "text"
    template_name = 's3_file_picker.html'

    class Media:
        js = ('admin/js/jquery.init.js', "/s3_file_picker/static/js/filebrowser.js")

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        file_max_size = 100
        context['widget'].update({
            'current_value': value,
            "file_max_size": file_max_size
        })
        return context

