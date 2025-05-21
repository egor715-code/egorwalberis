from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(
        verbose_name="Наименование",
        max_length=200,
    )
    desc = models.TextField(
        verbose_name="Описание",
        max_length=600,
    )

    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=10, 
        decimal_places=2,
        )

    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="products/",
    )
    category = models.ForeignKey(
        "Category",
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    brand = models.ForeignKey(
        "Brand",
        verbose_name="Бренд",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        "URL",
        max_length=250,
        unique=True, 
        null=True,
        editable=True,
    )


    class Meta:
        verbose_name="Товар"
        verbose_name_plural="Товары"
    def str(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        "URL", 
        max_length=250,
        unique=True, 
        null=True,
        editable=True,
    )
    
    class Meta:
        verbose_name="Категория"
        verbose_name_plural="Категории"
    def str(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    site_url = models.URLField(
        verbose_name="Ссылка на сайт",
        max_length=200,
    )

    country = models.CharField(
        verbose_name="Страна",
        max_length=200,
    )
    class Meta:
        verbose_name="Бренд"
        verbose_name_plural="Бренды"

    def str(self):
        return self.name
    
    # price 
    # brand 
    # name
    # category
    # desc
    # image

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)  # для неавторизованных
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price