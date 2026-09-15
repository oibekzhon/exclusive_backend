from django.contrib import admin

from .models import Product, Color, Size, Category, ProductImage
from .forms import ProductForm


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    max_num = 10
    verbose_name = 'Product Image'
    verbose_name_plural = 'Product Images (Maksimum 10 ta)'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price', 'discount', 'rating', 'reviews', 'is_best_selling_display', 'is_flash_sale_display')
    list_filter = ('categories',)
    search_fields = ('name', 'description')
    filter_horizontal = ('categories', 'colors', 'sizes')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'categories', 'image')
        }),
        ('Pricing', {
            'fields': ('price', 'old_price', 'discount', 'temporary_discount', 'sale_end_at')
        }),
        ('Ratings & Reviews', {
            'fields': ('rating', 'reviews')
        }),
        ('Product Variants (Maksimum 10 taga teng)', {
            'fields': ('colors', 'sizes'),
            'description': 'Har bir product uchun maximum 10 color and size is allowed'
        }),
    )

    def is_best_selling_display(self, obj):
        return obj.is_best_selling
    is_best_selling_display.short_description = 'Best Selling'
    is_best_selling_display.boolean = True

    def is_flash_sale_display(self, obj):
        return obj.is_flash_sale
    is_flash_sale_display.short_description = 'Flash Sale'
    is_flash_sale_display.boolean = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'color_preview')
    search_fields = ('name',)

    def color_preview(self, obj):
        return f'<div style="width: 20px; height: 20px; background-color: {obj.hex_code}; border: 1px solid #ccc;"></div>'
    color_preview.allow_tags = True
    color_preview.short_description = 'Preview'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'uploaded_at')
    list_filter = ('product', 'uploaded_at')
    readonly_fields = ('uploaded_at',)