from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib import messages
from .serializers import OrderDetailSerializer, CustomerDetailSerializer
from asset_master.serializers import *
import pandas as pd
from orders.pagination import OrderDetailPagination
from asset_master.pagination import AssetMasterPagination
from django.db.models import Q
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import filters
import csv
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
from django.http import FileResponse, QueryDict
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.tables import Table, TableStyle, colors
from django.forms.models import model_to_dict
import random
from asset_master.models import *
from orders.models import *
from .models import RequirementDetail,RequirementCust
from .forms import *

# Create your views here.
def requirement_report_main_page(request):
   ctx={}

   requirement = RequirementCust.objects.values('id','r_cust_id','customer__id',
                                                'customer__customer',
    'r_order_startdate','r_order_depdate', 'r_order_enddate' )

   ctx['requirement']=requirement

   return render(request, 'requirement_report_main_page.html', ctx)

# requirement per customer
def requirement_per_customer(request,id):
    ctx = {}
    
    # Fetching the customer object by id
    customer_obj = RequirementDetail.objects.filter(r_unique_id=id).values('r_unique_id','r_category', 'r_subcategory', 'r_description', 
            'r_brand', 'r_modelno', 'r_serialno')
    req_no=RequirementCust.objects.filter(r_cust_id=id).values('r_cust_id','id','customer__customer')
    ctx['customer_obj'] = customer_obj
    ctx['req_no'] = req_no
    print(customer_obj)
    
    return render(request, 'requirement_per_customer.html', ctx)

#create requirement asset form
def requirement_asset_form(request):
    ctx={}
    customer=CustomerDetail.objects.all()
    ctx['customer']=customer
    return render(request,'requirement_asset.html',ctx)

#save requirement form
def requirement_save_form(request):
    
    if request.method=='POST':
        print("helloooooo")
        form=ExcelUploadForm(request.POST,request.FILES)
        print("save req me aa gya hun")
        if form.is_valid():
            print("pr me yhn nhi aa paa rha hun")
            try:

                    customer=form.cleaned_data['customer']
                    print(customer)
                    r_order_startdate =form .cleaned_data['r_orderstartdate']
                    r_order_depdate=form.cleaned_data['r_orderdeploydate']
                    r_order_enddate=form.cleaned_data['r_orderenddate']
                    r_order_loc=form.cleaned_data['r_loc']
                    csv_file=request.FILES['csv_file']
                    print("yhn aa rhi")
                    r_unique_id=request.POST['auto_id']
                    
              
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    csv_reader = csv.DictReader(decoded_file)
                    print(csv_reader)

        
                    for row in csv_reader:
                        print(row)
                        r_category=row['CATEGORY']
                        r_subcategory=row['SUB CATEGORY']
                        r_description=row['DESCRIPTION']
                        r_brand=row['BRAND']
                        r_modelno=row['MODEL NO']
                        r_serialno=row['SERIAL NO']
                        print("relation 1",row['RELATION'])
                        relation = int(row['RELATION'])
                        mapping = row['MAPPING']
                        sku =row['SKU']
                        asset_tag = row['ASSET TAG']
                        area = row['AREA']
                        fc_no = row['FC NO.']
                        status = row['STATUS']
                        box_number=row['BOX NO.']
                        print("box num ",row['BOX NO.'])
        
                        requirement=RequirementDetail(
                            customer=customer,
                            r_unique_id=r_unique_id,
                            r_category=r_category,
                            r_subcategory=r_subcategory,
                            r_description=r_description,
                            r_brand=r_brand,
                            r_modelno=r_modelno,
                            r_serialno=r_serialno,
                            relation = relation,
                            mapping = mapping,
                            sku = sku,
                            asset_tag = asset_tag,
                            area = area,
                            fc_no = fc_no,
                            status = status,
                            box_number =box_number)
                         
                        requirement.save()
                        
                    requirementcust=RequirementCust(
                            customer=customer,
                            r_cust_id=r_unique_id,
                            r_order_startdate=r_order_startdate,
                            r_order_depdate=r_order_depdate,
                            r_order_enddate=r_order_enddate,
                            r_order_loc=r_order_loc,
                    ) 
                    requirementcust.save()   

                    print("me save ho gya hun")
                    return redirect ("requirement_report_main_page")
            except Exception as e:
                print("error:------------",e)
                return render(request,'requirement_asset.html')
    else:
       form=ExcelUploadForm()
    return render(request,'requirement_asset.html' , {'form':form})  
               
   

#Confirmed order Export to CSV
@login_required
def requirement_export_to_csv(request):
    r_unique_id=request.GET.get('r_unique_id')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    if len(request.GET.getlist(' r_assetIds'))>0:
         r_assetIds=request.GET.getlist(' r_assetIds[]')
         queryset = list(RequirementDetail.objects.filter(r_unique_id=r_unique_id,RequirementDetail__r_unique_id__in=r_assetIds).values_list(
                                                                                                                                    'r_category',
                                                                                                                                    'r_subcategory',
                                                                                                                                    'r_description',
                                                                                                                                    'r_brand',
                                                                                                                                    'r_modelno',
                                                                                                                                    'r_serialno'))      
    else:
         queryset = list(RequirementDetail.objects.filter(r_unique_id=r_unique_id,).values_list(
                                                                                    'r_category',
                                                                                    'r_subcategory',
                                                                                    'r_description',
                                                                                    'r_brand',
                                                                                    'r_modelno',
                                                                                    'r_serialno')) 
         
                                                                                                                                                                                                                                                                               
    print(queryset)                                                                                                                                                                                                                                                                                    
    writer = csv.writer(response)
    writer.writerow(["CATEGORY", "SUBCATEGORY", "DISCRIPTION","BRAND", "MODELNO","SERIALNO"])
    for obj in queryset:
        writer.writerow(obj)  
        
    return response
    
# import csv
def upload_requirement_excel(request):
    print("requiremnt me jaa rha hun")
    try:
        if request.method== 'POST':
          form=ExcelUploadForm(request.POST,request.FILES)
          if forms.is_valid():
            customer=forms.cleaned_data['customer']
            csv_file=request.FILES['csv_file']
            if csv_file.name.endswith('.csv'):
              df = pd.read_csv(csv_file)
            elif csv_file.name.endswith('.xlsx'):
              df = pd.read_excel(csv_file)
          
            for index,row in df.iterrows():
             asset=RequirementDetail(
               customer_id=customer,
               r_category=row['CATEGORY'],
               r_subcategory=row['SUB CATEGORY'],
               r_description=row['DESCRIPTION'],
               r_brand=row['BRAND'],
               r_modelno=row['MODEL NO'],
               r_serialno=row['SERIAL NO'],
               relation = row['RELATION'],
               mapping = row['MAPPING'],
               sku =row['SKU'],
               asset_tag = row['ASSET TAG'],
               area = row['AREA'],
               fc_no = row['FC NO.'],
               status = row['STATUS'],
               box_number=row['BOX NO.']
            )
             asset.save()
            print("uploaded")
            messages.success(request,"file uploaded")
            return  render (request,'requirement_report_main_page.html')
        else:
           form=ExcelUploadForm()
           
    except Exception as e:
        print(e,"----------------")
        messages.error(request,"this file is not supported")
        return render(request,"requirement_report_main_page.html")














# class ConfirmOrderListView(ListAPIView, LoginRequiredMixin):
#     # pagination_class = OrderDetailPagination
#     template_name = 'requirement_report_main_page.html'
#     serializer_class = OrderDetailSerializer
#     filter_backends = [filters.OrderingFilter]
#     authentication_classes = [BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     ordering = ["id"]
#     def get_queryset(self, request):
#         query = None
#         filter_type = None
#         if self.request.GET.get('q') is not None:
#             query = self.request.GET.get('q').strip()
#         if self.request.GET.get('filter_type') is not None:
#             filter_type = self.request.GET.get('filter_type').strip()
#         request.session['filter_type'] = filter_type
#         request.session['query'] = query
#         if query and not filter_type:
#             return OrderDetail.objects.filter(
#                 Q(organization__icontains=query) |
#                 Q(prepared_by_name__icontains=query),
#             )
#         elif query and filter_type=='customer_id':
#             return OrderDetail.objects.filter(customer_id__customer__iexact=query)
#         # elif query and filter_type=='deployment_date':
#         #     return OrderDetail.objects.filter(model_no__iexact=query)
#         elif query and filter_type=='order_id':
#             return OrderDetail.objects.filter(id=query)
#         # elif query and filter_type=='return_date':
#         #     return OrderDetail.objects.filter(brand__iexact=query, sold_asset=False, rented_asset=False,
#         #         loaned_asset=False, add_to_order=True, confirm_order=False)
#         else:
#             return OrderDetail.objects.all()
            
#     def get(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset(request))
#         queryset_length = len(queryset)
#         query_params_q = None
#         query_params_filter_value = None
#         if request.query_params.get('q') is not None:
#             query_params_q = request.query_params.get('q').strip()
#         if self.request.GET.get('filter_type') is not None:
#             query_params_filter_value = self.request.GET.get('filter_type').strip()
#         page = self.paginate_queryset(queryset)
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data,
#                     queryset_length, query_params_q, query_params_filter_value, request)

#     def get_paginated_response(self, data, queryset_length, query_params_q, query_params_filter_value, request):
#         ctx = {}
#         ctx = { "query_params_q": query_params_q, "query_params_filter_value": query_params_filter_value} 
#         paginated_assets = self.paginator if hasattr(self, 'paginator') else None
#         return render(
#             self.request,
#             self.template_name,
#             {'orders': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
#         )
