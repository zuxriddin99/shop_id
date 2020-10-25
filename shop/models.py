from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def get_products(self):
        return Product.objects.filter(category=self)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class ProductType(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def get_products(self):
        return Product.objects.filter(product_type=self)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, related_name='type', on_delete=models.PROTECT, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_4 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_5 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_6 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(blank=True, default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pixels = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ('created', 'name')
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
