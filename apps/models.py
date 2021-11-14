from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from PIL import Image


# Create your models here.
class Category(models.Model):

    class Meta:
        db_table = 'category'
        ordering = ('name',)

    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'


class Product(models.Model):

    class Meta:
        db_table = 'product'
        ordering = ('-date_added',)

    category = models.ForeignKey(
        'apps.Category', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='uploads/thumbnail', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'

    def get_image(self):
        if self.image:
            return f'{settings.SITE_URL}{self.image.url}'
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return f'{settings.SITE_URL}/media/{self.thumbnail}'
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return f'{settings.SITE_URL}/media/{self.thumbnail}'
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


class Order(models.Model):

    class Meta:
        db_table = 'Order'
        ordering = ['-created_at', ]

    user = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    stripe_token = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):

    class Meta:
        db_table = 'order-item'

    order = models.ForeignKey(
        'apps.Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'apps.Product', related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id
