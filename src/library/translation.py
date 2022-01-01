from modeltranslation.translator import translator, TranslationOptions
from .models import *

class GenreTranslationOption(TranslationOptions):
    fields = ('name',)

class MaterialTranslationOption(TranslationOptions):
    fields = ('name',)

#class BookTranslationOption(TranslationOptions):
#    fields = ('title', 'genre', 'summary',)

#class LanguageTranslationOption(TranslationOptions):
#    fields = ('name')

translator.register(Genre, GenreTranslationOption)
translator.register(Material, MaterialTranslationOption)
#translator.register((Book, BookTranslationOption))
#translator.register((Language, LanguageTranslationOption))