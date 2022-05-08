from django.db import IntegrityError

from library.models import Book, BookInstance, Material, MaterialInstance, Member, Language, Author, Loan, LoanReminder
from django.contrib.auth.models import User
import string
import json
from datetime import datetime


with open('../legacy_migration/loan.json') as json_file:
    data = json.load(json_file)
    old_loan_list = data[2]["data"]
    print(f"Loaded {len(old_loan_list)} loans.")

unhandled_loans = []
for legacy_loan in old_loan_list:
    print(f"Loan {legacy_loan}")
    try:
        if legacy_loan["type"] == "book":
            try:
                item = BookInstance.objects.get(label=legacy_loan["ID"])
            except BookInstance.DoesNotExist:
                item = BookInstance.objects.get(label=legacy_loan["ID"]+" a")
        else:
            try:
                item = MaterialInstance.objects.get(label=legacy_loan["ID"])
            except MaterialInstance.DoesNotExist:
                item = BookInstance.objects.get(label=legacy_loan["ID"]+" a")

        loan = Loan.objects.filter(item=item, lent_on=legacy_loan["pickup_date"])
        return_date = legacy_loan["return_date"]
        """
        if return_date != "0000-00-00":
            return_date_as_dt = datetime.strptime(return_date, "%Y-%m-%d").date()
            item.return_item()
        last_reminder = legacy_loan["last_reminder"]
        loan.save()
        """
        print(loan)
    except Exception as e:
        print(e)
        unhandled_loans.append(legacy_loan)
    continue
print(f"Could not handle the following loans {unhandled_loans}")