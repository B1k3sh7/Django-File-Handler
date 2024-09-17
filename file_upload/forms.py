from django import forms 

class UploadForm(forms.Form):
  file = forms.FileField()


class ModifyForm(forms.Form):
  new_columns = forms.JSONField(label='New column names')