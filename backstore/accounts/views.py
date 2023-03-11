import logging
from utils.logging_config import configure_logger
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout, authenticate, login as auth_login


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
    return render(request, "view_profile.html", context)

    # return render(request, "profile.html", {"user": request.user})


@login_required
def update_profile(request):
    logger.info("update_profile() was called.")
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if hasattr(request.user, "account"):
            profile_form = ProfileUpdateForm(
                request.POST, instance=request.user.account
            )
            if (
                user_form.is_valid()
                and profile_form.is_valid()
                and password_form.is_valid()
            ):
                user_form.save()
                profile_form.save()
                password_form.save()
                update_session_auth_hash(request, request.user)
                return redirect("accounts:profile")
        else:
            if user_form.is_valid() and password_form.is_valid():
                user_form.save()
                password_form.save()
                update_session_auth_hash(request, request.user)
                return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

        if hasattr(request.user, "account"):
            profile_form = ProfileUpdateForm(instance=request.user.account)
        else:
            profile_form = None

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "password_form": password_form,
    }
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
            # username = form.cleaned_data.get("username")
            # raw_password = form.cleaned_data.get("password1")
            # Create a new account for the user
            # user = form.save()
            # Account.objects.create(user=user)
            # Log the user in and redirect to the profile page
            # return redirect("accounts:profile")
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
