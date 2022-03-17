from modeltranslation.translator import translator, TranslationOptions
from .models import Genre
from .models import Material
from .models import Language as LanguageModel
from .models import BookInstance
from .models import Room

class GenreTranslationOption(TranslationOptions):
    fields = ('name',)

class MaterialTranslationOption(TranslationOptions):
    fields = ('name',)

#class BookTranslationOption(TranslationOptions):
#    fields = ('title', 'genre', 'summary',)

#class LanguageTranslationOption(TranslationOptions):
#    fields = ('name',)

class BookInstanceTranslationOption(TranslationOptions):
    fields = ('imprint',)

class RoomTranslationOption(TranslationOptions):
    fields = ('name',)

translator.register(Genre, GenreTranslationOption)
translator.register(Material, MaterialTranslationOption)
#translator.register((Book, BookTranslationOption))
#translator.register((LanguageModel, LanguageTranslationOption))
translator.register(BookInstance, BookInstanceTranslationOption)
translator.register(Room, RoomTranslationOption)