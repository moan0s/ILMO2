from .models import LoanReminder, Loan
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext
from datetime import datetime, timedelta
from django.core import mail


class MailReminder():
    reminder_interval = 28

    def _email_text_from_loan(loan):

        text = gettext('%(item)s is due back on %(due_day)s.%(due_month)s.%(due_year)s') % {'item': loan.item,
                                                                                            'due_day':
                                                                                                loan.due_back.day,
                                                                                            'due_month':
                                                                                                loan.due_back.month,
                                                                                            'due_year':
                                                                                                loan.due_back.year,
                                                                                            }
        return text

    def _gen_loan_text(self, member):
        """
        Checks if loans are due and generates a text for all loans of the given member if applicable.

        Returns
            loan_text:str A email text for the users loans or empty to indicate no reminders that are necessary
        """
        unreturned_loans_by_user = [loan for loan in Loan.objects.filter(borrower=member) if not loan.returned]
        due_loan_texts = []
        other_loan_texts = []
        one_due = False
        one_other = False
        loan_text = ""
        for loan in unreturned_loans_by_user:
            try:
                last_reminder = LoanReminder.objects.filter(loan=loan).latest("sent_on").sent_on
            except LoanReminder.DoesNotExist:
                last_reminder = loan.lent_on
            days_since_last_reminder = datetime.now().date() - last_reminder
            if days_since_last_reminder >= timedelta(days=self.reminder_interval):
                one_due = True
                due_loan_texts.append(MailReminder._email_text_from_loan(loan))
            else:
                one_other = True
                other_loan_texts.append(MailReminder._email_text_from_loan(loan))
        if one_due:
            loan_text = _("Your loans that are past their due date" + ":\n\r")
            for text in due_loan_texts:
                loan_text = loan_text + text + "\n\r"
            if one_other:
                loan_text = _("Your other loans" + ":\n\r")
                for text in other_loan_texts:
                    loan_text = loan_text + text + "\n\r"
        return loan_text

    def send(self):
        messages = self._gen_messages()
        for message in messages:
            message.send()

    def _gen_messages(self):
        # Probably inefficient collection of information to send reminders
        messages = []
        member_with_unreturned_loans = set([loan.borrower for loan in Loan.objects.all() if not loan.returned])

        loans_by_user = {}
        for member in member_with_unreturned_loans:
            # Check if member has an e-mail address given
            if member.user.email is None:
                continue
            loan_text = self._gen_loan_text(member)

            # Checks if a reminder is necessary. If it is, it adds the mail to the messages that should be sent
            if loan_text != "":
                subject = _("Your unreturned loans")
                greeting = _("Hello %(first_name)s %(lastname)s,\r\n") % {"first_name": member.user.first_name,
                                                                          "lastname": member.user.last_name}
                message = greeting+loan_text
                messages.append(mail.EmailMessage(subject, message, "from@example.com", [member.user.email]))
            else:
                continue
        return messages
