from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    owner = models.ManyToManyField(
        'Owner',
        verbose_name='Владельцы',
        blank=True)

    new_building = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField(
        'Текст объявления',
        blank=True,
        default='')
    price = models.IntegerField('Цена квартиры', db_index=True)
    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True,
        blank=True,
        default='')
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное',
        default='')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4',
        blank=True,
        default='')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж',
        blank=True,
        default='')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.NullBooleanField('Наличие балкона', db_index=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)
    liked_by = models.ManyToManyField(User,
                                      verbose_name='Кто лайкнул',
                                      related_name='liked_flats',
                                      blank=True)


    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Complaint(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Кто жаловался',
        related_name='complaints',
        null=True)
    flat = models.ForeignKey(
        Flat,
        on_delete=models.SET_NULL,
        verbose_name='Квартира, на которую пожаловались',
        related_name='complaints',
        null=True)
    text_complaint = models.TextField(
        verbose_name='Текст жалобы',
        blank=True,
        default='')

    def __str__(self):
        return f'{self.flat} - [{self.text_complaint}].'


class Owner(models.Model):
    owner = models.CharField(
        'ФИО владельца',
        max_length=200,
        blank=True,
        default='',
        db_index=True)
    owner_pure_phone = PhoneNumberField(
        verbose_name='Нормализованный номер владельца',
        region="RU",
        max_length=12,
        blank=True,
        db_index=True)
    flats = models.ManyToManyField(
        Flat,
        verbose_name='Квартиры в собственности',
        related_name='owners',
        blank=True)

    def __str__(self):
        return f'{self.owner}.'