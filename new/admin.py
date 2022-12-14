from django.contrib import admin
from .models import UserRecoverTable, Stock, Cart, CustomerReciept, Article

# Register your models here.

admin.site.register(UserRecoverTable)
admin.site.register(Stock)
admin.site.register(Cart)
admin.site.register(CustomerReciept)
admin.site.register(Article)