from django.http import JsonResponse
from django.utils import timezone
from .models import Product


def product_list(request):
    products = []
    for product in Product.objects.prefetch_related('colors', 'sizes', 'images', 'categories'):
        product_data = {
            'id': product.id,
            'image': request.build_absolute_uri(product.image.url) if product.image else None,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'oldPrice': str(product.old_price) if product.old_price else None,
            'discount': product.discount,
            'rating': str(product.rating),
            'reviews': product.reviews,
            'temporaryDiscount': product.temporary_discount,
            'saleEndAt': timezone.localtime(product.sale_end_at).isoformat() if product.temporary_discount and product.sale_end_at else None,
            'categories': [{'id': category.id, 'name': category.name} for category in product.categories.all()],
            'colors': [{'id': c.id, 'name': c.name, 'hexCode': c.hex_code} for c in product.colors.all()],
            'sizes': [{'id': s.id, 'name': s.name} for s in product.sizes.all()],
            'images': [request.build_absolute_uri(img.image.url) for img in product.images.all()],
            'isBestSelling': product.is_best_selling,
            'isFlashSale': product.is_flash_sale,
        }
        products.append(product_data)

    return JsonResponse(products, safe=False)