import os
import time

from django.core.management import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from labglo_site import settings

from career.models import DriveRegistration, DriveTimeSlot


class Command(BaseCommand):

    def handle(self, *args, **options):
        drive_time_slots = DriveTimeSlot.objects.all().values_list('drive_registration__id', flat=True)
        drive_registrations = DriveRegistration.objects.filter(is_confirmed=True).exclude(id__in=drive_time_slots)
        from_email = settings.DEFAULT_FROM_EMAIL
        bcc_email = settings.BCC_EMAILS

        for registration in drive_registrations:
            # send mail to registration.email here
            to_mail = registration.email
            subject = "Labglo Technologies: Placement Drive Entry Confirmation"
            # Take mail content
            content_text = render_to_string(
                'career/mail-notify/mail_to_time_slot_not_allotted_candidates.txt',
                {'candidate': registration})
            content_htmly = render_to_string(
                'career/mail-notify/mail_to_time_slot_not_allotted_candidates.html',
                {'candidate': registration})
            if to_mail != '':
                msg = EmailMultiAlternatives(subject,
                    content_text, from_email, [to_mail,], bcc=bcc_email)
                msg.attach_alternative(content_htmly, "text/html")
                msg.send()
                print registration.id, registration.email, " ---> mail senddddddd"
            else:
                pass
            time.sleep(5)
