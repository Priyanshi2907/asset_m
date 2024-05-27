#from asset_master.models import AssetMasterAccessories,AssetMaster
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import socket
from asset_master.models import AssetMasterComment
from django.forms.models import model_to_dict
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send reminder emails for asset verification ending in 15 days'

    def handle(self, *args, **kwargs):
        today_date = datetime.datetime.now().date()
        print("---",today_date)
        reminder_date = today_date - datetime.timedelta(days=365)
        print(reminder_date)

        # Fetch assets where date_time is equal to the reminder_date
        # date=AssetMasterComment.objects.values('date_time')
        # print("date : ",date)
        assets = AssetMasterComment.objects.filter(date_time=reminder_date)

        for asset in assets:
            self.send_asset_ver_reminder_email(asset)

    def send_asset_ver_reminder_email(self, asset):
        print("coming here")
        subject = 'Asset verification Reminder'
        print(asset.asset_id.category)
        context = {
            'present_date':datetime.datetime.now().date(),
            'previous_date': asset.date_time,
            'comment': asset.comment,
            'category': asset.asset_id.category,
            'description': asset.asset_id.description,
            'brand': asset.asset_id.brand,
            'model_no': asset.asset_id.model_no,
            'serial_no': asset.asset_id.serial_no,
            'user_email_admin_1': 'erpadmin@zoomcom.tv',
            'user_email_admin_2': 'ghoshshaibal@zoomcom.tv',
            'user_email_admin_3': '2907priyanshi@gmail.com'


        }
        html_message = render_to_string('asset_verification_email.html', context)
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject,
            plain_message,
            'priyanshiprajapati29@gmail.com',  # Replace with your sender email
            ['ghoshshaibal@zoomcom.tv','erpadmin@zoomcom.tv','2907priyanshi@gmail.com']

            
        )
        email.attach_alternative(html_message, "text/html")
        
        email.send()
print('sending asset verification email to admin')

        