from model_bakery.recipe import Recipe, seq
from library.models import Book

book = Recipe(
    Book,
    title=seq('TestBook_'),
)
