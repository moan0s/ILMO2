from library.models import Book, BookInstance, Material, MaterialInstance, Member, Language
from django.contrib.auth.models import User

import json
import os

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
    user = User.objects.create(first_name=legacy_user["forename"],
                               last_name=legacy_user["forename"],
                               email=legacy_user["email"],
                               username=legacy_user["user_ID"])
    member = Member.objects.get(user=user)
    print(legacy_user['language'])
    member.preferred_language = Language.objects.get(name=legacy_user['language'])
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
                             "number": 1}
print(f"Derived {len(books)} books")

material = dict()
for old_material_instance in old_materialinstance_list:
    label_stem = get_stem(old_material_instance['material_ID'])
    try:
        material[label_stem]["number"] += 1
    except KeyError:
        # print(f"Creating new material: {label_stem}")
        material[label_stem] = {"title": old_material_instance["name"],
                                "number": 1}
print(f"Derived {len(material)} materials")
