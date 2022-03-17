from django.db import IntegrityError

from library.models import Book, BookInstance, Material, MaterialInstance, Member, Language, Author, Loan, LoanReminder
from django.contrib.auth.models import User
import string
import json
from datetime import datetime

with open('../legacy_migration/user.json') as json_file:
    data = json.load(json_file)
    user_list = data[2]["data"]
    print(f"Loaded {len(user_list)} user.")

with open('../legacy_migration/books.json') as json_file:
    data = json.load(json_file)
    old_bookinstance_list = data[2]["data"]
    print(f"Loaded {len(old_bookinstance_list)} book instances.")

with open('../legacy_migration/material.json') as json_file:
    data = json.load(json_file)
    old_materialinstance_list = data[2]["data"]
    print(f"Loaded {len(old_materialinstance_list)} material instances.")

with open('../legacy_migration/loan.json') as json_file:
    data = json.load(json_file)
    old_loan_list = data[2]["data"]
    print(f"Loaded {len(old_loan_list)} loans.")

for legacy_user in user_list:
    try:
        user = User.objects.create(first_name=legacy_user["forename"],
                               last_name=legacy_user["surname"],
                               email=legacy_user["email"],
                               username=f"{legacy_user['forename']}.{legacy_user['surname']}")
    except IntegrityError:
        print(f"Could not create user, {legacy_user['user_ID']} is already a username")
        exit(1)
    member = Member.objects.get(user=user)
    language = legacy_user['language']
    if language == "":
        language = "english"
    try:
        member.preferred_language = Language.objects.get(name=language)
    except Language.DoesNotExist:
        member.preferred_language = Language.objects.create(name=language)
    member.UID = legacy_user["UID"]


def get_stem(book_ID):
    label_stem = book_ID.split(" ")[0]
    return label_stem


test_cases = [("ZB2 y", "ZB2"),
              ("ZB2 ay", "ZB2"),
              ("WS24 a", "WS24"),
              ("WS24 ab", "WS24"),
              ("TE2", "TE2")]

for test in test_cases:
    try:
        stem = get_stem(test[0])
        assert stem == test[1]
    except AssertionError:
        print(f"Calculated: {stem}, Expected {test[1]}")
        raise AssertionError

books = dict()
for old_book_instance in old_bookinstance_list:
    label_stem = get_stem(old_book_instance['book_ID'])
    try:
        books[label_stem]["number"] += 1
    except KeyError:
        # print(f"Creating new book: {label_stem}")
        books[label_stem] = {"title": old_book_instance["title"],
                             "author": old_book_instance["author"],
                             "number": 1}
print(f"Derived {len(books)} books")


def get_author(name: str):
    """
    Tries to extract authors

    Creates an unknown author if no name is given

    returns:
        authors: List of author objects
    """
    name.replace("et al.", "")
    if name == "":
        try:
            return [Author.objects.get(first_name="Unknown")]
        except Author.DoesNotExist:
            return [Author.objects.create(first_name="Unknown", last_name="Author")]


    authors = []
    # Case for Multiple authors such as "Schreiner, Müller"
    author_strings = name.split(",")
    if len(author_strings) > 1:
        print("Multiple authors")
        for author_string in author_strings:
            last_name = author_string.strip()
            try:
                # Creating the author
                author = Author.objects.filter(last_name=last_name)[0]
                authors.append(author)
                # This will fail for authors with more than one name, multiple authors etc..
            except IndexError:
                authors.append(Author.objects.create(last_name=last_name))
        return authors


    print("Single author")
    last_name = name.strip()

    # This will fail for authors with more than one name, multiple authors etc..
    authors = Author.objects.filter(last_name=last_name)
    if len(authors) == 0:
        print("Creating author")
        return [Author.objects.create(last_name=last_name)]
    else:
        print("Author already exists")
        return authors



def get_label_end(index):
    label_end = ""
    if int(index / 26) > 0:
        label_end = string.ascii_lowercase[int(index / 26) % 26 - 1]
    label_end += string.ascii_lowercase[index % 26]
    return label_end


def test_label_end():
    cases = [(27, "ab"),
             (0, "a"),
             (26, "aa"),
             (25, "z"),
             (52, "ba"),
             (1, "b"),
             (2, "c")]
    for index, expected in cases:
        try:
            label = get_label_end(index)
            assert label == expected
        except AssertionError:
            print(f"Label: {label}, Expected {expected}")
            raise AssertionError


test_label_end()

for book_label in books:
    book_dict = books[book_label]
    print(f"Book dict {book_dict}")
    authors = get_author(book_dict["author"])
    book = Book.objects.create(title=book_dict["title"])
    for author in authors:
        print(f"Adding author {author} to book")
        book.author.add(author)
    for i in range(0, book_dict["number"]):
        label_end = get_label_end(i)
        label = f"{book_label} {label_end}"
        BookInstance.objects.create(book=book,
                                    status="a",
                                    label=label)

materials = dict()
for old_material_instance in old_materialinstance_list:
    label_stem = get_stem(old_material_instance['material_ID'])
    try:
        materials[label_stem]["number"] += 1
    except KeyError:
        # print(f"Creating new material: {label_stem}")
        materials[label_stem] = {"title": old_material_instance["name"],
                                 "number": 1}
print(f"Derived {len(materials)} materials")

for material_label in materials:
    material_dict = materials[material_label]
    print(f"Material dict {material_dict}")
    material = Material.objects.create(name=material_dict["title"])
    for i in range(0, material_dict["number"]):
        label_end = i+1
        label = f"{material_label} {label_end}"
        MaterialInstance.objects.create(material=material,
                                        status="a",
                                        label=label)
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

        user = User.objects.get(username=legacy_loan["user_ID"])
        member = Member.objects.get(user=user)
        item.borrow(member, lent_on=legacy_loan["pickup_date"])
        return_date = legacy_loan["return_date"]
        if return_date != "0000-00-00":
            return_date_as_dt = datetime.strptime(return_date, "%Y-%m-%d").date()
            loan.return_date = return_date_as_dt
        last_reminder = legacy_loan["last_reminder"]
        if last_reminder != "0000-00-00":
            loan = Loan.objects.filter(item=item).latest("lent_on")
            last_reminder_as_datetime = datetime.strptime(last_reminder, "%Y-%m-%d").date()
            LoanReminder.objects.create(loan=loan, sent_on=last_reminder_as_datetime)
    except Exception:
        unhandled_loans.append(legacy_loan)
    continue
print(f"Could not handle the following loans {unhandled_loans}")
