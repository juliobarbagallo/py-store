import logging
from django.contrib import messages
from utils.logging_config import configure_logger
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import (
    update_session_auth_hash,
    logout,
    authenticate,
    login as auth_login,
)


app_name = "accounts"
log_file_path = f"{app_name}/{app_name}.out"
log_level = logging.DEBUG
logger = configure_logger(log_file_path, log_level)


def login(request):
    if request.method == "POST":
        # get the username and password from the form data
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate the user
        user = authenticate(request, username=username, password=password)

        # check if authentication was successful
        if user is not None:
            # log the user in and redirect to their profile page
            auth_login(request, user)
            return redirect("accounts:view_profile")
        else:
            # authentication failed, show an error message
            error_message = "Invalid username or password."
            return render(request, "login.html", {"error_message": error_message})
    else:
        # display the login form
        return render(request, "login.html")


@login_required
def view_profile(request):
    logger.info("view_profile() was called.")
    context = {
        "user": request.user,
    }
    logger.debug(f"{context=}")
    return render(request, "view_profile.html", context)

    # return render(request, "profile.html", {"user": request.user})


@login_required
def update_profile(request):
    logger.debug("update_profile() was called.")
    user = request.user
    logger.debug(f"{user=}")
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, instance=user.account)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("accounts:update_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=user)
        if hasattr(user, "account"):
            profile_form = ProfileUpdateForm(instance=user.account)
        else:
            profile_form = ProfileUpdateForm()

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "update_profile.html", context)


def register(request):
    logger.info("register() was called.")
    if request.method == "POST":
        logger.debug(f"request method was POST. - {request.POST=} - {request.body=}")
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            logger.debug("form is valid")
            form.save()
            return redirect("accounts:view_profile")
        logger.error(f"Seems like form is not valid! - {form.errors=}")
    else:
        logger.debug(
            f"request method was NOT POST. - {request.POST=} - {request.body=}"
        )
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def orders(request):
    logger.info("orders() was called.")
    # TODO: add logic to display user's orders
    return render(request, "orders.html", {})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
