from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, default='#000000')

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return self.name


class Size(models.Model):
    class SizeChoices(models.TextChoices):
        XS = 'xs', 'XS'
        S = 's', 'S'
        M = 'm', 'M'
        L = 'l', 'L'
        XL = 'xl', 'XL'
        XXL = 'xxl', 'XXL'
        XXXL = 'xxxl', 'XXXL'
        ONE_SIZE = 'one_size', 'One Size'

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    reviews = models.PositiveIntegerField(blank=True, default=0, null=True)
    temporary_discount = models.PositiveIntegerField(blank=True, default=0, null=True)
    sale_end_at = models.DateTimeField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='products')
    colors = models.ManyToManyField(Color, blank=True, related_name='products')
    sizes = models.ManyToManyField(Size, blank=True, related_name='products')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.temporary_discount in (None, 0):
            self.sale_end_at = None
        if self.pk:
            if self.colors.count() > 10:
                raise ValueError("Maksimum 10 ta color tanlash mumkin")
            if self.sizes.count() > 10:
                raise ValueError("Maksimum 10 ta size tanlash mumkin")
            if self.images.count() > 10:
                raise ValueError("Maksimum 10 ta rasm qo'shish mumkin")

    @property
    def is_best_selling(self):
        """Check if product is best seller: rating >= 4 and reviews >= 100"""
        return self.rating >= 4 and self.reviews >= 100

    @property
    def is_flash_sale(self):
        """Check if product is flash sale: temporary_discount is not None and not 0"""
        return self.temporary_discount is not None and self.temporary_discount > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.product.name} - Image"
