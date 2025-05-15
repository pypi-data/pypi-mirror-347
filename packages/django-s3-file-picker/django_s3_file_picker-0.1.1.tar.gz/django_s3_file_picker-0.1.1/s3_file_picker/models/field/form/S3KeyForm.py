from django import forms

from s3_file_picker.models.field.form.S3KeyInput import S3KeyInput


class S3KeyForm(forms.Field):

    def __init__(self, *args, **kwargs):
        super().__init__()

    widget = S3KeyInput
