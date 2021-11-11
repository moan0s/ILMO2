from library.models import Book, BookInstance, Material, MaterialInstance, Member, Language, Author
from django.contrib.auth.models import User
import string
import json

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
                               last_name=legacy_user["surname"],
                               email=legacy_user["email"],
                               username=legacy_user["user_ID"],
                               password="Dada")
    member = Member.objects.get(user=user)
    language = legacy_user['language']
    if language == "":
        language = "english"
    try:
        member.preferred_language = Language.objects.get(name=language)
    except Language.DoesNotExist:
        raise Language.DoesNotExist(f"Language {language} does not exist and has to manually created")
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
    # Creates an unknown author if no name is given
    if name == "":
        try:
            return Author.objects.get(first_name="Unknown")
        except Author.DoesNotExist:
            return Author.objects.create(first_name="Unknown", last_name="Author")
    # Case for "Muster, Max"
    if len(name.split(",")) > 1:
        first_name = name.split(",")[1].strip()
        last_name = name.split(",")[0].strip()
        try:
            # This will fail for authors with more than one name, multiple autors etc..
            return Author.objects.filter(first_name=first_name).filter(last_name=last_name)[0]
        except IndexError:
            Author.objects.create(first_name=first_name, last_name=last_name)

    try:
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1]
        try:
            # This will fail for authors with more than one name, multiple autors etc..
            return Author.objects.filter(first_name=first_name).filter(last_name=last_name)[0]
        except IndexError:
            Author.objects.create(first_name=first_name, last_name=last_name)
    except IndexError:
        last_name = name
        try:
            # This will fail for authors with more than one name, multiple autors etc..
            return Author.objects.filter(last_name=last_name)[0]
        except IndexError:
            Author.objects.create(last_name=last_name)




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
    print(f"Book label: {book_label}")
    book_dict = books[book_label]
    print(f"Book dict {book_dict}")
    author = get_author(book_dict["author"])
    book = Book.objects.create(title=book_dict["title"],
                               author=author)
    for i in range(0, book_dict["number"]):
        print(i)
        label_end = get_label_end(i)
        label = f"{book_label} {label_end}"
        print(label)
        BookInstance.objects.create(book=book,
                                    status="a",
                                    label=label)

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
