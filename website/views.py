from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from leads.models import Lead
# Create your views here.


def home(request):
    return render(request, 'website/home.html')

def self_starter(request):
    return render(request, 'website/self_starter.html')

def growth(request):
    return render(request, 'website/growth.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name","").strip()
        contact_method = request.POST.get("contact_method")
        email = request.POST.get("email","").strip()
        phone = request.POST.get("phone","").strip()
        growth_plan = request.POST.get("growth_plan")
        message = request.POST.get("message","").strip()
        consent = bool(request.POST.get("consent"))

        # define 'valid'
        if contact_method == "email":
            valid = bool(email)
        elif contact_method == "phone":
            valid = bool(phone)
        else:
            valid = False

        if not valid:
            messages.error(request, "Please provide a valid contact method (email or phone).")
        elif not growth_plan:
            messages.error(request, "Please choose a growth plan.")
        else:
            Lead.objects.create(
                name=name,
                contact_method=contact_method,
                email=email,
                phone=phone,
                growth_plan=growth_plan,
                message=message,
                # consent=consent,  # add this if your model has the field
            )

            # Optional email to yourself (won't error if email isn't configured)
            try:
                subject = f"New Lead: {name} • {growth_plan}"
                body = (
                    f"Name: {name}\n"
                    f"Method: {contact_method}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Plan: {growth_plan}\n\n"
                    f"Message:\n{message}\n"
                )
                send_mail(subject, body, getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@weblylocal.com"),
                          ["hello@weblylocal.com"], fail_silently=True)
            except Exception:
                pass

            messages.success(request, "Thanks! We’ll reach out soon.")
            return redirect("website:contact")  # avoid resubmits on refresh

    return render(request, "website/contact.html")