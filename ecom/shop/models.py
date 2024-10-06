from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    cat_title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    cat_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_title
        


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    image = models.ImageField(upload_to='products')
    brand = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def gatPrice(self):
        return f"₹%d" % self.price
    
    def gatDiscountprice(self):
        return f"₹%d" % self.discount_price
    
class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title
    
    def get_discount_total_price(self):
        return self.item.discount_price * self.qty
    def get_total_price(self):
        return self.item.price * self.qty
    def get_saving_amount(self):
        total = self.get_total_price() - self.get_discount_total_price()
        return f"₹%d" % total
    
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount =  models.FloatField()

    def __str__(self):
        return self.code
    
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    alt_contact = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=(("Home","Home"),("Office","Office")))

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, null=True,blank=True,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Order #{self.id}"
    




