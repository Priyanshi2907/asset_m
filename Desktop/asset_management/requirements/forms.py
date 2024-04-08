from django import forms
from orders.models import CustomerDetail
from .models import RequirementDetail

class ExcelUploadForm(forms.Form):
    customer=forms.ModelChoiceField(queryset=CustomerDetail.objects.all())
    r_orderstartdate=forms.DateField()
    r_orderdeploydate=forms.DateField()
    r_orderenddate=forms.DateField()
    r_loc=forms.CharField(max_length=100)
    csv_file=forms.FileField(label="select and excel file")