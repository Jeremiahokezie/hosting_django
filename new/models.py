from django.db import models
from django.db.models.fields import IntegerField
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.utils import timezone


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your models here.

@login_required(login_url='new:login')
def dashboard(request):
    global admin
    admin = request.user
    if request.method == "POST":
        product = request.POST.get("good")
        qty = request.POST.get("quantity")
        if Stock.objects.filter(Product=product).exists():
            price = Stock.objects.get(Product=product).Price 
            num_qty = int(qty)
            tprice = num_qty * price
            good = Stock.objects.all().values()
            purchase = Cart.objects.all().values()
            if Cart.objects.filter(Product = product).exists():
                Cart.objects.filter(Product = product).update(Quantity=qty, TPrice=tprice)

                

                context = {
                    "purchase":purchase,
                    "good":good
                }
                messages.success(request, "Successfully addedd to cart")
                return render(request, "new/dashboard.html", context)
            else:
                Cart.objects.create(Product=product, Price=price, Quantity=qty, TPrice=tprice)
                

                context = {
                    "purchase":purchase,
                    "good":good
                }
                messages.success(request, "Successfully addedd to cart")
                return render(request, "new/dashboard.html", context)
            
        else:
            messages.info(request, "Product doesn't exist")
            return redirect("new:dashboard")
            
        
    else:
        good = Stock.objects.all().values()
        purchase = Cart.objects.all().values()
        context = {
            "purchase":purchase,
            "good":good,
            "user":admin
        }

        return render(request, "new/dashboard.html", context)

class UserRecoverTable(models.Model):
    emails = models.EmailField()
    otp = models.CharField(max_length=10, null=True)
    ids = models.IntegerField()

    def __str__(self):
        return self.emails


class Stock(models.Model):
    Product = models.CharField(max_length=1000)
    Price = models.IntegerField()
    Quantity = models.CharField(max_length=1000)

    def __str__(self):
        return self.Product

class Cart(models.Model):
    Product = models.CharField(max_length=1000, unique=True)
    Price = models.IntegerField()
    Quantity = models.CharField(max_length=1000)
    TPrice = models.CharField(max_length=1000)

    def __str__(self):
        return self.Product

class CustomerReciept(models.Model):
    Product = models.CharField(max_length=1000)
    Price = models.IntegerField()
    Quantity = models.CharField(max_length=1000)
    TPrice = models.CharField(max_length=1000)
    Generated_By = models.CharField(max_length=100)

    def __str__(self):
        return self.Generated_By



@receiver(post_save, sender=Cart)
def reciept(sender, instance, created, *args, **kwargs):
    if created:
        print("It saved")
        Product = instance.Product
        Price = instance.Price
        Quantity = instance.Quantity
        TPrice = instance.TPrice
        Generated_By = str(admin)
        reciept = CustomerReciept(Product=Product, Price=Price, Quantity=Quantity, TPrice=TPrice, Generated_By=Generated_By) 
        reciept.save()

#post_save.connect(reciept, sender=Cart)


class Article(models.Model):
    Title = models.CharField(max_length=1000)
    Content = models.CharField(max_length=10000)
    Slug = models.SlugField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        # if self.slug is None:
        #     self.slug = slugify(self.Title)
        super().save(*args, **kwargs)
