from datetime import timedelta
from typing import Optional

from django.template.loader import render_to_string
from django.conf import settings
from django.core import mail
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
import logging

from library.models import User, TransactionalEmail, SentStatusChoices, EmailBackendChoices


class NotificationTypeChoices(models.TextChoices):
    TEST_MAIL = "test_mail", _("Testmail")


class NotificationDisplayMapping:
    def __init__(self, email_html_template, email_plain_template):
        self.email_html_template = email_html_template
        self.email_plain_template = email_plain_template


# ndm = notification display mapping
ndm = {
    NotificationTypeChoices.TEST_MAIL: NotificationDisplayMapping(
        email_html_template='library/mail/notifications/test-mail.html',
        email_plain_template="library/mail/notifications/test-mail.txt", ),
}


class DuplicateEmailSend(Exception):
    pass


def send_notification_email(notification_type,
                            data,
                            target_user: Optional[User] = None,
                            force_send: bool = False,
                            dry: bool = False):
    subject = f"{data['subject']}"
    context = {"notification": data["context"], }
    html_message = render_to_string(ndm[notification_type].email_html_template, context)
    plain_message = render_to_string(ndm[notification_type].email_plain_template, context)
    if target_user is not None:
        target_email = target_user.email
    else:
        target_email = data["target_email"]

    setting_backend = settings.EMAIL_BACKEND
    match setting_backend:
        case "django.core.mail.backends.console.EmailBackend":
            backend = EmailBackendChoices.CONSOLE
        case "django.core.mail.backends.smtp.EmailBackend":
            backend = EmailBackendChoices.SMTP
            if target_email.endswith("@example.com") or target_email.endswith("@example.org"):
                dry = True
        case _:
            raise NotImplementedError

    recent_send_exists = TransactionalEmail.objects.filter(email=target_email, subject=subject,
                                                           created_at__gt=timezone.now() - timedelta(
                                                               minutes=5)).exists()
    if recent_send_exists and not force_send:
        raise DuplicateEmailSend("An E-Mail with this subject and recipient was already sent in the last 5 minutes.")
    transactional_email = TransactionalEmail.objects.create(
        email=target_email,
        user=target_user,
        subject=subject,
        text=plain_message,
        html=html_message,
        backend=backend
    )
    transactional_email.save()

    if not dry:
        mail.send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL,
                       [target_email],
                       html_message=html_message)
    else:
        logging.info(f"E-Mail to {target_email} not sent as it was marked as dry run")

    transactional_email.status = SentStatusChoices.SENT
    transactional_email.save()
