from django.db import models

from s3_file_picker.models.field.form.S3KeyForm import S3KeyForm


class S3KeyField(models.CharField):

    def formfield(self, **kwargs):
        defaults = {
            "form_class": S3KeyForm
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
