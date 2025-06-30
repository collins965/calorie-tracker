from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Public index + private tracking
def index(request):
    today = timezone.now().date()
    items = []
    total_calories = 0

    if request.user.is_authenticated:
        items = FoodItem.objects.filter(user=request.user, date_added=today)
        total_calories = sum(item.calories for item in items)

        if request.method == "POST":
            if "reset" in request.POST:
                items.delete()
                messages.success(request, "All today's entries were reset.")
            else:
                name = request.POST.get("name")
                calories = request.POST.get("calories")

                # Validation
                if not name or not calories:
                    messages.error(request, "Both fields are required.")
                elif not calories.isdigit() or int(calories) <= 0:
                    messages.error(request, "Calories must be a positive number.")
                else:
                    FoodItem.objects.create(
                        name=name.strip(),
                        calories=int(calories),
                        user=request.user,
                        date_added=today
                    )
                    messages.success(request, f"Added {name} ({calories} kcal).")
            return redirect("index")

    return render(request, "index.html", {
        "items": items,
        "total_calories": total_calories
    })

# Delete food item securely
@login_required
def delete_item(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, f"Deleted '{item.name}' from today's list.")
    return redirect("index")

# Dashboard view — only for logged-in users
@login_required
def dashboard_view(request):
    today = timezone.now().date()
    items = FoodItem.objects.filter(user=request.user, date_added=today)
    total_calories = sum(item.calories for item in items)
    return render(request, "dashboard.html", {
        "items": items,
        "total_calories": total_calories
    })

# Home redirects to index
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

        if password1 != password2:
            return render(request, "signup.html", {
                "form": {}, "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "form": {}, "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username, password=password1, email=email
        )
        login(request, user)
        return redirect("dashboard")

    return render(request, "signup.html", {"form": {}})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        calories = request.POST.get("calories")

        if not name or not calories or not calories.isdigit() or int(calories) <= 0:
            messages.error(request, "Invalid input. Ensure all fields are filled correctly.")
        else:
            item.name = name
            item.calories = int(calories)
            item.save()
            messages.success(request, "Food item updated successfully.")
            return redirect("index")

    return render(request, "edit_item.html", {"item": item})