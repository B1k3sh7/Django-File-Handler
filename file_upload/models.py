from django.db import models
from django.contrib.auth.models import User


class FileUpload(models.Model):
  file = models.FileField(upload_to='uploads/')
  uploaded_at = models.DateTimeField(auto_now_add=True)
  schema_match = models.BooleanField(default=False)


class SchemaFile(models.Model):
  name = models.CharField(max_length=255)
  schema_content = models.TextField()


class ModifiedFile(models.Model):
  original_file = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
  modified_content = models.JSONField()
  column_mapping = models.JSONField(default=dict)
  modified_at = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)

