import os
from labglo_site import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def email_notification(notify_to, context_data):
    from_email = settings.DEFAULT_FROM_EMAIL
    bcc_email = settings.BCC_EMAILS

    if notify_to == 'candidate':
        candidate_email = context_data['candidate_obj'].email
        candidate_subject = "Congratulations ! Labglo received your application."
        # Take candidate mail content
        candidate_content_text = render_to_string(
            'career/mail-notify/candidate_mail_content.txt',
            {'data': context_data})
        candidate_content_htmly = render_to_string(
            'career/mail-notify/candidate_mail_content.html',
            {'data': context_data})
        if candidate_email != '':
            candidate_msg = EmailMultiAlternatives(candidate_subject,
                candidate_content_text, from_email, [candidate_email,], bcc=bcc_email)
            candidate_msg.attach_alternative(candidate_content_htmly, "text/html")
            candidate_msg.send()
        else:
            pass

    elif notify_to == 'admin':
        admin_ids = settings.NOTIFY_EMAILS
        admin_subject = "Job Application - %s" % (context_data['post_name'],)
        # Take admin mail content
        admin_content_text = render_to_string(
            'career/mail-notify/hr_mail_content.txt', context_data)
        admin_content_htmly = render_to_string(
            'career/mail-notify/hr_mail_content.html', context_data)
        # Find path and open the resume file of candidate
        candidate_cv = context_data['candidate_obj'].resume
        # Send mail to admins with resume file attached
        admin_msg = EmailMultiAlternatives(admin_subject,
            admin_content_text, from_email, admin_ids)
        admin_msg.attach_alternative(admin_content_htmly, "text/html")
        admin_msg.attach_file(candidate_cv.path)
        admin_msg.send()

    elif notify_to == 'drive_registration_confirm':
        user_email = context_data['user_obj'].email
        subject = "Congratulations, Your Registration For Labglo upcoming drive confirmed."
        # Take candidate mail content
        user_content_text = render_to_string(
            'career/mail-notify/drive_registration_confirm.txt', context_data)
        user_content_htmly = render_to_string(
            'career/mail-notify/drive_registration_confirm.html', context_data)
        if user_email != '':
            user_msg = EmailMultiAlternatives(subject,
                user_content_text, from_email, [user_email,], bcc=bcc_email)
            user_msg.attach_alternative(user_content_htmly, "text/html")
            user_msg.send()
        else:
            pass

    elif notify_to == 'drive_application_received':
        user_email = context_data['user_obj'].email
        subject = "Labglo Technologies: Received Application For Walk-in Drive"
        # Take candidate mail content
        user_content_text = render_to_string(
            'career/mail-notify/application_for_drive.txt', context_data)
        user_content_htmly = render_to_string(
            'career/mail-notify/application_for_drive.html', context_data)
        if user_email != '':
            user_msg = EmailMultiAlternatives(subject,
                user_content_text, from_email, [user_email,], bcc=bcc_email)
            user_msg.attach_alternative(user_content_htmly, "text/html")
            user_msg.send()
        else:
            pass

    elif notify_to == 'confirm_drive_slot_time':
        user_email = context_data['user_obj'].email
        subject = "Labglo Technologies: Placement Drive Entry Confirmation"
        # Take candidate mail content
        user_content_text = render_to_string(
            'career/mail-notify/drive_time_slot_inform.txt', context_data)
        user_content_htmly = render_to_string(
            'career/mail-notify/drive_time_slot_inform.html', context_data)
        if user_email != '':
            user_msg = EmailMultiAlternatives(subject,
                user_content_text, from_email, [user_email,], bcc=bcc_email)
            user_msg.attach_alternative(user_content_htmly, "text/html")
            user_msg.send()
        else:
            pass
    else:
        pass