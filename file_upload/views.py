from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.conf import settings
from .models import FileUpload, SchemaFile, ModifiedFile
from .forms import UploadForm, ModifyForm
import pandas as pd
import json
import os
from datetime import datetime
from pymongo import MongoClient


# Initilizing MongoDB client
mongo_client = MongoClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB_NAME]


def upload_file(request):
  if request.method == "POST":
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
      file = form.cleaned_data['file']
      if file.size > 10 * 1024 * 1024:    #10MB
        return HttpResponse("File size exceeds 10 MB limit.")
      
      if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
        return HttpResponse('Only CSV and Excel files are allowed')

      # saving file to local storage
      file_path = default_storage.save(f'uploads/{file.name}', file)
      file_url = os.path.join(settings.MEDIA_ROOT, file_path)

      # checking schema match
      schema_match = False
      schemas = SchemaFile.objects.all()
      for schema in schemas:
          if file.name.endswith(schema.name):
            schema_match = True
            break
      
      # loading data into DataFrame
      if file.content_type == 'text/csv':
        df = pd.read_csv(file_url)
      else:
        df =pd.read_excel(file_url)
      
      if schema_match:
          #  saving to MYSQL
          columns = df.columns.tolist()
          modified = ModifiedFile(
            original_file=FileUpload(file=file, schema_match=True),
            modified_content=json.loads(df.to_json(orient='records')),
            column_mapping={col: f'modified_{col}' for col in columns},
            owner=request.user
          )
          modified.save()
      else:
        # saving to MongoDB
        data = df.to_dict(orient='records')
        mongo_db.files.insert_one({
          'file_name': file.name,
          'content': data,
          'uploaded_at': datetime.now()
        })      
      
      return redirect('file_list')
  else:
    form = UploadForm()
  
  return render(request, 'upload_file.html', {'form': form})


def file_list(request):
  uploads = FileUpload.objects.all()
  return render(request, 'file_list.html', {'uploads': uploads})


def retrieve_content(request, pk):
  try:
    upload = FileUpload.objects.get(pk=pk)
    if upload.schema_match:
      modified_file = ModifiedFile.objects.filter(original_file=upload).first()
      if modified_file:
        return render(request, 'content.html', {
          'content': json.loads(modified_file.modified_content),
          'column_mapping': modified_file.column_mapping,
        })
      else:
        return HttpResponse('Content not available')
    else:
        # Retrieving from MongoDB
        mongo_record = mongo_db.files.find_one({'file_name': upload.file.name})
        if mongo_record:
          return render(request, 'content.html', {
            'content': mongo_record['content'],
            'column_mapping': None
          })
        return HttpResponse('Content not found')
  
  except FileUpload.DoesNotExist:
    return HttpResponse('File not found')
  

def modify_content(request, pk):
  try:
    upload = FileUpload.objects.get(pk=pk)
    modified_file = ModifiedFile.objects.filter(original_file=upload).first()
    if request.method == "POST":
      form = ModifyForm(request.POST)
      if form.is_valid():
        new_columns = form.cleaned_data['new_columns']
        if modified_file:
          modified_file.column_mapping.update(new_columns)
          modified_file.save()
          return redirect('retrieve_content', pk=pk)
    else:
      initial_columns = modified_file.column_mapping.keys() if modified_file else []
      form = ModifyForm(initial={'new_columns': initial_columns})
    
    return render(request, 'modify_file.html', {'form': form, 'pk': pk})
  
  except FileUpload.DoesNotExist:
    return HttpResponse('File not found')