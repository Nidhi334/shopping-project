
from  django.forms import ModelForm
from .models import Category,Product


class CategoryInsertForm(ModelForm):
    class Meta:
        model = Category
        fields = ['cat_title', 'cat_description','slug']

class ProductInsertForm(ModelForm):
    class Meta:
        model = Product
        fields =['title','price','discount_price','brand','category','slug', 'description','image']
