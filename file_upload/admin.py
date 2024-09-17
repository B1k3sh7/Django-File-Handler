from django.contrib import admin
from .models import FileUpload, SchemaFile, ModifiedFile

admin.site.register(FileUpload)
admin.site.register(SchemaFile)
admin.site.register(ModifiedFile)
