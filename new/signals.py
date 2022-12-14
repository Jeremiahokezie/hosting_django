from .views import  Cart
import views
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

def reciept(sender, instance, created, *args, **kwargs):
    if created:
        Product = instance.Product
        Price = instance.Price
        Quantity = instance.Quantity
        TPrice = instance.Tprice
        Generated_By = views.admin
        #Reciept.objects.create(Product=Product, Price=Price, Quantity=Quantity, TPrice=TPrice, Generated_By=Generated_By) 
        
#post_save.connect(reciept, sender=Cart)