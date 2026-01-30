from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Courier)
admin.site.register(Contact)
admin.site.register(Review)
admin.site.register(Store)
admin.site.register(Address)

