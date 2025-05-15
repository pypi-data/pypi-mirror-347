import urllib3
from storages.backends.s3 import S3Storage

from s3_file_picker.storage.AddressingStyle import AddressingStyle


class CustomS3Storage(S3Storage):

    s3_custom_domain: str
    s3_bucket_name: str
    s3_access_key: str
    s3_secret_key: str
    url_style: AddressingStyle
    s3_default_acl: str
    location: str

    def __init__(self, **settings):
        super().__init__(**settings)

    def get_default_settings(self) -> dict:
        result: dict = super().get_default_settings()
        result.update({"location": self.location})
        result.update({"custom_domain": self.s3_custom_domain})
        result.update({"bucket_name": self.s3_bucket_name})
        result.update({"access_key": self.s3_access_key})
        result.update({"secret_key": self.s3_secret_key})
        result.update({"default_acl": self.s3_default_acl})
        result.update({"addressing_style": self.url_style})
        result.update({"endpoint_url": f"https://{self.s3_custom_domain}/"})
        return result

    def url(self, name, parameters=None, expire=None, http_method=None):
        url = super().url(name, parameters, expire, http_method)
        parsed_url = urllib3.util.parse_url(url)
        url_path = parsed_url.path
        if self.url_style is AddressingStyle.VIRTUAL_DOMAIN:
            new_url = f"{self.url_protocol}//{self.s3_bucket_name}.{self.s3_custom_domain}"
        else:
            new_url = f"{self.url_protocol}//{self.s3_custom_domain}/{self.s3_bucket_name}"
        return f"{new_url}{url_path}"
