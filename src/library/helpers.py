import logging
import string
import re

from library.models import Author

def get_author_from_string(name: str):
    """
    Converts a string to a single or multiple comma seperated authors

    Raises a value error if the string is not in expected format

    returns:
        authors: List of author objects
    """

    # Remove common names and replace splitting characters
    name = name.replace("et al.", "")
    name = name.replace("et. al.", "")
    name = name.replace("et. Al", "")
    name = name.replace("et al", "")
    name = name.replace("⁺", "")
    name = name.replace(";", ",")
    name = name.replace("&", ",")
    name = name.replace("/", ",")
    if name.strip() == "":
       raise ValueError("Author must be a non-empty string")


    authors = []
    # Case for Multiple authors such as "Schreiner, Müller"
    author_strings = name.split(",")
    if len(author_strings) > 1:
        for author_string in author_strings:
            splitted_author = author_string.split(" ")
            first_name = splitted_author[0:-1]
            last_name = splitted_author[-1]
            try:
                # Creating the author
                author = Author.objects.filter(first_name=first_name, last_name=last_name)[0]
                authors.append(author)
                # This will fail for authors with more than one name, multiple authors etc..
            except IndexError:
                authors.append(Author.objects.create(first_name=first_name, last_name=last_name))
                logging.info(f"Adding author {first_name} {last_name}")
        return authors

    splitted_author = author_strings[0].split(" ")
    first_name = splitted_author[0:-1]
    last_name = splitted_author[-1]

    # This will fail for authors with more than one name, multiple authors etc..
    authors = Author.objects.filter(first_name=first_name, last_name=last_name)
    if len(authors) == 0:
        logging.info(f"Adding author {first_name} {last_name}")
        return [Author.objects.create(first_name=first_name, last_name=last_name)]
    else:
        return authors

def get_label_end(index) -> str:
    """
    Returns a one to two character long label e.g. `bf`

    The labels will follow with `a`, `b`, ... `z`, `aa`, `ab`, ...
    An index above 676 will raise a value error
    """
    if index > 26*26:
        raise ValueError("Index > 676 not supported")
    label_end = ""
    if int(index / 26) > 0:
        label_end = string.ascii_lowercase[int(index / 26) % 26 - 1]
    label_end += string.ascii_lowercase[index % 26]
    return label_end

def validate_book_prefix(prefix:str) -> str:
    """
    Will check if the book prefix is valid

    Returns a (cleaned) book prefix or raises a value error
    """
    stripped_prefix = prefix.strip()
    match = re.fullmatch("[A-Z][A-Z][0-9]+", stripped_prefix)
    if not match:
        raise ValueError("Book prefix not in a valid format")
    return stripped_prefix
