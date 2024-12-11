from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from allauth.account.models import EmailConfirmation
from allauth.account.utils import user_email
from allauth.account import app_settings
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest



class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        ctx = {
            "user": emailconfirmation.email_address.user,
        }
        if app_settings.EMAIL_VERIFICATION_BY_CODE_ENABLED:
            ctx.update({"code": emailconfirmation.key})
        else:
            ctx.update(
                {
                    "key": emailconfirmation.key,
                    "activate_url": self.get_email_confirmation_url(
                        request, emailconfirmation
                    ),
                }
            )
        if signup:
            email_template = "account/email/email_confirmation_signup"    
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx) 
        
    def get_email_confirmation_url(self, request, emailconfirmation):
        custom_domain = "http://54.82.253.10:8000" 
        url = reverse("account_confirm_email", args=[emailconfirmation.key])
        return f"{custom_domain}{url}"    