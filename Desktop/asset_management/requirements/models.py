from django.db import models
import datetime
from asset_master.models import *
from orders.models import CustomerDetail


# Create your models here.
class RequirementDetail(models.Model):
    
    customer=models.ForeignKey(CustomerDetail,on_delete=models.SET_NULL,null=True,blank=True)
    r_unique_id=models.CharField(max_length=10,null=True,blank=True)
    r_category = models.CharField(max_length=100, null=True, blank=True)
    r_subcategory = models.CharField(max_length=100, null=True, blank=True)
    r_description = models.CharField(max_length=100, null=True, blank=True)
    r_brand = models.CharField(max_length=100, null=True, blank=True)
    r_modelno = models.CharField(max_length=100, null=True, blank=True)
    r_serialno = models.CharField(max_length=100, null=True, blank=True)
    
    relation = models.IntegerField(null=True,blank=True)
    mapping = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    asset_tag = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    fc_no = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    box_number = models.CharField(max_length=100, null=True, blank=True, default="")
    
class RequirementCust(models.Model):
    #requirement=models.ForeignKey(RequirementDetail,on_delete=models.SET_NULL,null=True)
    r_cust_id=models.CharField(max_length=10,null=True,blank=True)
    customer=models.ForeignKey(CustomerDetail,on_delete=models.SET_NULL,null=True)
    r_order_startdate = models.DateField(null=True, blank=True)
    r_order_depdate = models.DateField(null=True, blank=True)
    r_order_enddate = models.DateField(null=True, blank=True)
    r_order_loc=models.CharField(max_length=1000,blank=True, null=True)

    