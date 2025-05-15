from django import forms
from django.conf import settings


class S3FilePickerWidget(forms.TextInput):
    template_name = 's3_file_picker.html'

    class Media:
        js = ('admin/js/jquery.init.js',)
        
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        file_max_size = settings.DATA_UPLOAD_MAX_MEMORY_SIZE / 1024 / 1024
        context['widget'].update({
            'current_value': value,
            "file_max_size": file_max_size
        })
        return context
