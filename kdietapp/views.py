from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login, authenticate  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this


# Create your views here.
def indexPageView(request):
    return render(request, 'index.html')


def aboutPageView(request):
    return render(request, 'subpages/about.html')


def contactPageView(request):
    return render(request, 'subpages/contact.html')


def pricingPageView(request):
    return render(request, 'subpages/pricing.html')


def bloghomePageView(request):
    return render(request, 'subpages/blog-home.html')


def blogpostPageView(request):
    return render(request, 'subpages/blog-post.html')


def faqPageView(request):
    return render(request, 'subpages/faq.html')


def portoverviewPageView(request):
    return render(request, 'subpages/portfolio-overview.html')


def portitemPageView(request):
    return render(request, 'subpages/portfolio-item.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index.html")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'register.html', context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', context={"login_form": form})
