from asset_master.models import AssetMasterAccessories,AssetMaster
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import socket
from asset_master.models import *
from django.forms.models import model_to_dict
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send reminder emails for warranties ending in 15 days'

    def handle(self, *args, **kwargs):
        reminder_date = datetime.datetime.now().date() + timedelta(days=15)
        print(reminder_date)
        # + timedelta(days=15)
        assets = AssetMaster.objects.filter(warranty_period=reminder_date)

        for asset in assets:
            self.send_warranty_reminder_email(asset)

    def send_warranty_reminder_email(self, asset):
        print("coming here")
        subject = 'Warranty Period Reminder for AMC'
        context = {
            'warranty_period': asset.warranty_period,
            'category': asset.category,
            'description': asset.description,
            'brand': asset.brand,
            'model_no': asset.model_no,
            'serial_no': asset.serial_no,
            'user_email_admin_1': 'erpadmin@zoomcom.tv',
            'user_email_admin_2': 'ghoshshaibal@zoomcom.tv',
            'user_email_admin_3': '2907priyanshi@gmail.com'


        }
        html_message = render_to_string('warranty_reminder_email.html', context)
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject,
            plain_message,
            'priyanshiprajapati29@gmail.com',  # Replace with your sender email
            ['ghoshshaibal@zoomcom.tv','erpadmin@zoomcom.tv','2907priyanshi@gmail.com']
        )
        email.attach_alternative(html_message, "text/html")
        
        email.send()
print('sending Email to admin')

        