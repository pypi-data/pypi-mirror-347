# Django S3 File Picker

Simple file picker

## Setup 

1. Add **"s3_file_picker"** to *INSTALLED_APPS*
2. Add environments to settings.py:

### environments:

```python
dotenv.load_dotenv()

ENV = os.getenv

MEDIA_AWS_ACCESS_KEY_ID = ENV("MEDIA_AWS_ACCESS_KEY_ID")
MEDIA_AWS_SECRET_ACCESS_KEY = ENV("MEDIA_AWS_SECRET_ACCESS_KEY")
MEDIA_AWS_STORAGE_BUCKET_NAME = ENV("MEDIA_AWS_STORAGE_BUCKET_NAME")
MEDIA_AWS_S3_CUSTOM_DOMAIN = ENV("MEDIA_AWS_S3_CUSTOM_DOMAIN")
MEDIA_AWS_S3_REGION_NAME = ENV("MEDIA_AWS_S3_REGION_NAME")

class PublicMediaStorage(CustomS3Storage):
    s3_default_acl = 'public-read'
    # file_overwrite = False
    location = ""
    s3_access_key = MEDIA_AWS_ACCESS_KEY_ID
    s3_secret_key = MEDIA_AWS_SECRET_ACCESS_KEY
    s3_bucket_name = MEDIA_AWS_STORAGE_BUCKET_NAME
    s3_custom_domain = MEDIA_AWS_S3_CUSTOM_DOMAIN
    region_name = MEDIA_AWS_S3_REGION_NAME
    url_style = AddressingStyle.PATH.value


MEDIA_URL = f"https://{ENV('MEDIA_AWS_S3_CUSTOM_DOMAIN')}/"
DEFAULT_FILE_STORAGE = "main.settings.PublicMediaStorage"
```

