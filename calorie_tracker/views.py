from django.shortcuts import render, redirect
from .models import FoodItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Track food for today
@login_required
def index(request):
    today = timezone.now().date()
    items = FoodItem.objects.filter(user=request.user, date_added=today)
    total_calories = sum(item.calories for item in items)

    if request.method == "POST":
        if "reset" in request.POST:
            items.delete()
        else:
            name = request.POST.get("name")
            calories = request.POST.get("calories")
            if name and calories.isdigit():
                FoodItem.objects.create(
                    name=name,
                    calories=int(calories),
                    user=request.user,
                    date_added=today
                )
        return redirect("index")

    return render(request, "index.html", {
        "items": items,
        "total_calories": total_calories
    })


# Delete item
@login_required
def delete_item(request, item_id):
    FoodItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect("index")


# Dashboard page
@login_required
def dashboard_view(request):
    today = timezone.now().date()
    items = FoodItem.objects.filter(user=request.user, date_added=today)
    total_calories = sum(item.calories for item in items)
    return render(request, "dashboard.html", {
        "items": items,
        "total_calories": total_calories
    })


# Redirect home to index
@login_required
def home_view(request):
    return redirect("index")


# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login.html", {
            "form": {}, "error": "Invalid username or password"
        })

    return render(request, "login.html", {"form": {}})


# Signup view
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password match check
        if password1 != password2:
            return render(request, "signup.html", {
                "form": {}, "error": "Passwords do not match"
            })

        # Username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "form": {}, "error": "Username already exists"
            })

        # Create user
        user = User.objects.create_user(
            username=username, password=password1, email=email
        )
        login(request, user)
        return redirect("dashboard")

    return render(request, "signup.html", {"form": {}})
def logout_view(request):
    logout(request)
    return redirect('login')  