from django.db import models
from django.utils.text import slugify
from account.models import User


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    name = models.CharField(max_length=100, verbose_name='Название категрии')
    slug = models.SlugField(unique=True, verbose_name='Название ссылки на категории', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-name',)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='пользователь')
    name = models.CharField(max_length=100, verbose_name='название продукта')
    description = models.TextField(verbose_name='описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products', verbose_name='категория')
    activ = models.BooleanField(default=False, verbose_name='в наличии или нет')
    created = models.DateField(auto_now_add=True, verbose_name='дата добавления')
    image = models.ImageField(blank=True, null=True, upload_to='product/', verbose_name='картинка')
    rating = models.IntegerField(default=0, verbose_name='рейтинг')
    likes = models.ManyToManyField(User, through='Like', related_name='liked_products')

    def __str__(self):
        return self.name


class Favorites(models.Model):
    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='пользователь')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name='товар')
    is_favorite = models.BooleanField(default=False, verbose_name='избранный')

    def __str__(self):
        return f'{self.user.email} - {self.product.name}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_likes', verbose_name='товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    def __str__(self):
        return f'Like by {self.user.email} on {self.product.name}'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    text = models.TextField(verbose_name='текст комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return f'Комментарий к продукту {self.product.name} от пользователя {self.user.email}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        product = self.products  # Получить связанный объект Product
        self.total_amount = product.price * self.quantity  # Вычислить общую стоимость
        super().save(*args, **kwargs)  # Сохранить объект Order

    def __str__(self):
        return f"Корзина #{self.user}, {self.created_at}"


class OrderItem(models.Model):
    REGION = (
        ("ОШ", "ОШ"),
        ("BISH", "BISH"),
        ("ТАЛАС", "ТАЛАС"),
        ("НАРЫН", "НАРЫН"),
        ("ИК", "ИК")
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    address = models.CharField(max_length=100)
    region = models.CharField(max_length=100, choices=REGION, default=1)

    def __str__(self):
        return f"Заказ --- {self.order}"
