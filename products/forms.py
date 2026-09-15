from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'image', 'name', 'description', 'price', 'old_price',
            'discount', 'rating', 'reviews', 'temporary_discount',
            'sale_end_at',
            'categories', 'colors', 'sizes'
        ]

    def clean(self):
        cleaned_data = super().clean()

        # Optional fields - clear errors if present
        optional_fields = [
            'old_price', 'discount', 'reviews', 'colors',
            'sizes', 'temporary_discount', 'sale_end_at'
        ]

        for field in optional_fields:
            if field in self.errors:
                del self.errors[field]

        return cleaned_data

    def clean_colors(self):
        colors = self.cleaned_data.get('colors')
        if colors and colors.count() > 10:
            raise forms.ValidationError("Maksimum 10 ta color tanlash mumkin")
        return colors

    def clean_sizes(self):
        sizes = self.cleaned_data.get('sizes')
        if sizes and sizes.count() > 10:
            raise forms.ValidationError("Maksimum 10 ta size tanlash mumkin")
        return sizes

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount is None:
            return 0
        return discount

    def clean_reviews(self):
        reviews = self.cleaned_data.get('reviews')
        if reviews is None:
            return 0
        return reviews

    def clean_temporary_discount(self):
        temporary_discount = self.cleaned_data.get('temporary_discount')
        if temporary_discount is None:
            return 0
        return temporary_discount

