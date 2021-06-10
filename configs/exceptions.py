from rest_framework.exceptions import APIException


class AttachmentUploadError(APIException):
    status_code = 500
    default_detail = 'attachment upload error'
    default_code = 'attachment_upload_error'