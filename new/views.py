from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Article, UserRecoverTable, Stock, Cart

from .forms import ArticleForm

from .slidedata import slideIndexs
import random



# Create your views here.

def home(request):
    return render(request, "new/html.html", {"sliders":slideIndexs})

def sign_up(request):
    if request.method == "POST":
        
        first = request.POST.get("fname")
        last = request.POST.get("lname")
        email = request.POST.get("e-mail")
        username = request.POST.get("uname")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Emai taken")
                return redirect("new:signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect("new:signup")
            else:
                messages.success(request, "Registration Successful")
                new_user1 = User.objects.create_user(username=username, email=email, first_name=first, last_name=last, password=password)
                new_user1.save()
                
                """if your registration form has more inputs other than this you can
                    use this logic to save the users input to the database

                new_user2 = UserTable(Firstname=first, Lastname=last, Email=email, Username=username, Password=password)
                new_user2.save()"""

                
                return redirect("new:login")
        else:
            messages.info(request, "Password mismatch")
            return redirect("new:signup")
    else:
        return render(request, "new/sign.html", )

def log_in(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("password1")
        user = authenticate(request, username=username, password=password)

        """to authenticate with email:
           user = authenticate(request, email=emal(users email), password=password)"""
        if  user is not None:
            login(request, user)
            return redirect("new:dashboard")
        else: 
            messages.info(request, "Inavalid login details")
            return redirect("new:login")
    else:
        return render(request, "new/login.html")



def otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        
        if otp == OTP:
            """Get OTP from the backend in the Userrecovertable. I haven't figured out how to send 
            emails in django to send the otp to the user with his email  but there's a code I have tried out at the bottom of this views.py"""
            return redirect("new:setpassword")
            
        else:
            messages.info(request, "Invalid OTP")
            return redirect("new:otp")
        
        
    else:
        return render(request, "new/otp.html")
    
    

def forgottenpassword(request):
    chars = "1234567890"
    global OTP
    OTP = "".join(random.sample(chars, 6))  #generating a random OTP
    if request.method == "POST":
        useremail = request.POST.get("email")
        if User.objects.filter(email = useremail).exists():
            ids = User.objects.get(email=useremail).id
            reset = UserRecoverTable(emails=useremail, otp=OTP, ids=ids)
            reset.save()

            subject = 'OTP for Kodecamp-Dipoze'
            message = f'Hi there, your generated OTP is {OTP}, use this to proceed to your password reset page. NOTE:This is just a confirmation mail'
            email_from = settings.EMAIL_HOST_USER
            emailS = useremail
            # email2 = 'iniememt@gmail.com'
            recipient_list = [emailS]
            send_mail(subject, message, email_from, recipient_list)
            print("success")


            return redirect("new:otp")
            
        else:
            messages.info(request, "Enter your registered email")
            return redirect("new:forgotpassword")
        
    else:
        return render(request, "new/forgotpassword.html")

def setpassword(request):
    
    if request.method == "POST":
        passwords = request.POST.get("password")
        password2 = request.POST.get("password2")
        if passwords == password2:
            ids = UserRecoverTable.objects.get(otp=OTP).ids
            user = User.objects.get(id = ids)
            user.set_password(passwords)
            user.save()
            idss = UserRecoverTable.objects.get(otp=OTP)
            idss.delete()
            return redirect("new:login")
        else:
            messages.info(request, "Password mismatch")
            return redirect("new:setpassword")
    else:
        return render(request, "new/setpassword.html")

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
            context = {
                "purchase":purchase,
                "good":good
            }
            if Cart.objects.filter(Product = product).exists():
                Cart.objects.filter(Product = product).update(Quantity=qty, TPrice=tprice)
                
                messages.success(request, "Cart successfully updated")
                return render(request, "new/dashboard.html", context)
            else:
                Cart.objects.create(Product=product, Price=price, Quantity=qty, TPrice=tprice)

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
            "user":admin,
        }

        return render(request, "new/dashboard.html", context)

@login_required(login_url='new:login')
def reciept(request):
    if request.method == "POST":
        pass
    return render(request, "new/reciept.html")



    

@login_required(login_url='new:login')
def logout_view(request):
    logout(request)
    clear = Cart.objects.all()
    clear.delete()
    return redirect("new:home")

def chat(request):
    return render(request, "new/chat.html")



def article(request):
    form = ArticleForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        form.save()
        context["form"] = ArticleForm() 
    article_created = Article.objects.all().values()
    context["articles"] = article_created
    return render(request, "new/website.html", context)

def article_details(request, ID=None):
    qs = None
    if ID is not None:
        qs = Article.objects.get(id = ID)
        
    context = {
        "detail":qs
    }
    return render(request, "new/article_detail.html", context)
