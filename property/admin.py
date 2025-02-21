from django.contrib import admin


from .models import Flat


class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'address', 'owner')
    readonly_fields = ['created_at']
    list_display = ('address', 'price', 'new_building', 'created_at', 'town')
    list_editable = ['new_building']

admin.site.register(Flat, FlatAdmin)


# Поля для отображения
#
#     Адрес квартиры
#     Цена квартиры
#     Новостройка
#     Год постройки
#     Город
