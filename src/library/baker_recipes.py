from django.contrib.auth.models import User
from model_bakery.recipe import Recipe, seq
from library.models import Book, Author

book = Recipe(
    Book,
    title=seq('TestBook_'),
)

user = Recipe(
    User,
    username=seq('Abi_'),
)

author = Recipe(
    Author,
    first_name=seq('Mia_'),
    last_name=seq('Maigold_'),
)
