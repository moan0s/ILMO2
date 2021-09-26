from django.contrib import admin
from .models import Book, Material, Loan, BookInstance, MaterialInstance, Genre, Author

admin.site.register(Book)
admin.site.register(Material)
admin.site.register(Loan)
admin.site.register(Genre)
admin.site.register(Author)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('label', 'book', 'status', 'borrower', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','label', 'imprint')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

    @admin.register(MaterialInstance)
    class MaterialInstanceAdmin(admin.ModelAdmin):
        list_display = ('label', 'material', 'status', 'borrower', 'due_back')
        list_filter = ('status', 'due_back')

        fieldsets = (
            (None, {
                'fields': ('material', 'label')
            }),
            ('Availability', {
                'fields': ('status', 'due_back', 'borrower')
            }),
        )
