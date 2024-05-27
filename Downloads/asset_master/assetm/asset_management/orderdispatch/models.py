from django.db import models

class LogisticDetails(models.Model):
    kit_checker=models.CharField(max_length=100,null=True,blank=True)
    kit_physical_verifier=models.CharField(max_length=100,null=True,blank=True)
    logistic_assigner=models.CharField(max_length=100,null=True,blank=True)

