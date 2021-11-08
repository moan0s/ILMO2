# from library.models import Book, BookInstance, Material, MaterialInstance, User
# from django.contrib.auth.models import User
import json

with open('user.json') as json_file:
    data = json.load(json_file)
    user_list = data[2]["data"]
    print(f"Loaded {len(user_list)} user.")

with open('books.json') as json_file:
    data = json.load(json_file)
    old_bookinstance_list = data[2]["data"]
    print(f"Loaded {len(old_bookinstance_list)} book instances.")

with open('material.json') as json_file:
    data = json.load(json_file)
    old_materialinstance_list = data[2]["data"]
    print(f"Loaded {len(old_materialinstance_list)} material instances.")

with open('loan.json') as json_file:
    data = json.load(json_file)
    old_loan_list = data[2]["data"]
    print(f"Loaded {len(old_loan_list)} loans.")

for user in user_list:
    pass


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
        #print(f"Calculated: {stem}, Expected {test[1]}")
        raise AssertionError

books = dict()
for old_book_instance in old_bookinstance_list:
    label_stem = get_stem(old_book_instance['book_ID'])
    try:
        books[label_stem]["number"] += 1
    except KeyError:
        #print(f"Creating new book: {label_stem}")
        books[label_stem] = {"title": old_book_instance["title"],
                             "number": 1}
print(f"Derived {len(books)} books")

material = dict()
for old_material_instance in old_materialinstance_list:
    label_stem = get_stem(old_material_instance['material_ID'])
    try:
        material[label_stem]["number"] += 1
    except KeyError:
        #print(f"Creating new material: {label_stem}")
        material[label_stem] = {"title": old_material_instance["name"],
                                "number": 1}
print(f"Derived {len(material)} materials")
