import logging
from utils.logging_config import configure_logger
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Account

app_name = "accounts"
log_file_path = f"{app_name}/{app_name}.out"
log_level = logging.DEBUG
logger = configure_logger(log_file_path, log_level)


@login_required
def profile(request):
    logger.info("profile() was called.")
    # TODO: add logic to display user's orders and account information
    return render(request, "profile.html", {"user": request.user})


def register(request):
    logger.info("register() was called.")
    if request.method == "POST":
        logger.debug(f"request method was POST. - {request.POST=} - {request.body=}")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            logger.debug("form is valid")
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            # Create a new account for the user
            user = form.save()
            Account.objects.create(user=user)
            # Log the user in and redirect to the profile page
            return redirect("accounts:profile")
    else:
        logger.debug(
            f"request method was NOT POST. - {request.POST=} - {request.body=}"
        )
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
