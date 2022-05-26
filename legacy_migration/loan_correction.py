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

print(old_loan_list)
unhandled_loans = []
for legacy_loan in old_loan_list:
    new_id = int(legacy_loan["loan_ID"])-1
    try:
        loan = Loan.objects.get(pk=new_id)
        unhandled_loans.append(legacy_loan)
    except Loan.DoesNotExist:
        continue
    return_date = legacy_loan["return_date"]
    if return_date != "0000-00-00":
        return_date_as_dt = datetime.strptime(return_date, "%Y-%m-%d").date()
        loan.return_loan(return_date_as_dt)
        print(f"Returned {loan}")
    loan.save()

print(unhandled_loans)
print(len(unhandled_loans))