from django.db import models
from  django.contrib.auth.models import  AbstractUser
from phonenumber_field.phonenumber import PhoneNumber

class UserProfile(AbstractUser):
    phone_number = PhoneNumber()
    RoleChoices = (
    ('client','client'),
    ('owner', 'owner'),
    ('courier', 'courier')
    )
    user_role = models.CharField(max_length=30, choices=RoleChoices, default='client')
    date_register = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name},{self.username}'


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Store(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_store')
    store_name = models.CharField(max_length=30)
    store_img = models.ImageField(upload_to='store_photo')
    descriptions = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.store_name

    def get_avg_rating(self):
        reviews = self.review_store.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(), 1)
        return 0

    def get_count_person(self):
         return self.review_store.count()

class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_contact')
    contact_name = models.CharField(max_length=20)
    contact_number = PhoneNumber()

    def __str__(self):
        return f'{self.store},{self.contact_name}'

class Address(models.Model):
    store = models.ForeignKey(Store,on_delete=models.CASCADE, related_name='address_store')
    address_name = models.CharField(max_length=50)

    def __str__(self):
        return self.address_name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_store')
    product_name = models.CharField(max_length=50)
    product_img = models.ImageField(upload_to='product_photo')
    price = models.PositiveSmallIntegerField(default=True)
    product_description = models.TextField()

    def __str__(self):
        return self.product_name


class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order')
    StatusChoices = (
    ('pending','pending'),
    ('canceled','canceled'),
    ('delivered','delivered')
    )
    status = models.CharField(max_length=30, choices=StatusChoices, default='pending')
    delivery_address = models.TextField()
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.product}, {self.status}'

class Courier(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='courier_assignments')
    CourierStatusChoices = (
    ('busy','busy'),
    ('available','available')
    )
    courier_status = models.CharField(max_length=20, choices=CourierStatusChoices)

    def __str__(self):
        return f'{self.courier_status},{self.user}'

class Review(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.rating}'