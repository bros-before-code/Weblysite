from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from leads.models import Lead
# Create your views here.


def home(request):
    return render(request, 'website/home.html')

def examples(request):
    return render(request, 'website/examples.html')

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

# Central config so you only maintain content in one place.
INDUSTRY_EXAMPLES = {
    "restaurant": {
        "emoji": "🍽️",
        "title": "Restaurant Website Demo",
        "short_label": "Restaurant",
        "audience_label": "Restaurants & Cafés",
        "subtitle": "Menus, online ordering, hours, and location—front and center.",
        # If you have a live demo, add the URL below; otherwise leave None and we’ll show screenshots.
        "demo_url": None,  # e.g. "https://restaurant.weblylocal.com"
        "og_image": "/static/website/images/examples/restaurant-hero.png",
        "highlight_image": "website/images/examples/restaurant-highlight.png",
        "gallery": [
            "website/images/examples/restaurant-01.png",
            "website/images/examples/restaurant-02.png",
            "website/images/examples/restaurant-03.png",
        ],
        "points": [
            "Menu-first layout with daily specials component.",
            "One-tap call + directions for mobile visitors.",
            "Reservation or online ordering integration ready.",
        ],
        "features": [
            {"title": "Menu & Specials", "desc": "Structured menu, specials ribbon, and dietary tags."},
            {"title": "Ordering/Reservations", "desc": "Integrate DoorDash, Toast, OpenTable, or custom forms."},
            {"title": "Local SEO", "desc": "Schema for restaurant, hours, and Google Business Profile sync."},
        ],
        "cta_blurb": "Includes menu setup, photo galleries, hours, and integrations you already use.",
        "seo_title": "Restaurant Website Design Demo",
        "seo_desc": "See a high-converting restaurant site layout: menus, ordering, hours, and local SEO baked in.",
        "faq": [
            {"q": "Can you connect online ordering I already use?",
             "a": "Yes. We can embed or link to DoorDash, Uber Eats, Toast, or your POS’s native ordering."},
            {"q": "Can I update my menu myself?",
             "a": "Absolutely. We’ll give you an editor so you can change items, prices, and photos anytime."}
        ],
    },

    "salon": {
        "emoji": "💇",
        "title": "Salon Website Demo",
        "short_label": "Salon",
        "audience_label": "Salons & Spas",
        "subtitle": "Booking-first design with services, stylists, and photo proof.",
        "demo_url": None,
        "og_image": "/static/website/images/examples/salon-hero.png",
        "highlight_image": "website/images/examples/salon-highlight.png",
        "gallery": [
            "website/images/examples/salon-01.png",
            "website/images/examples/salon-02.png",
        ],
        "points": [
            "Prominent ‘Book Now’ on every page.",
            "Reviews and stylist profiles to build trust.",
            "Service list with transparent pricing.",
        ],
        "features": [
            {"title": "Bookings", "desc": "Integrate GlossGenius, Square, or Fresha for real-time scheduling."},
            {"title": "Before & After", "desc": "Grid gallery for transformations and trends."},
            {"title": "Reviews", "desc": "Pull in Google reviews to boost social proof."},
        ],
        "cta_blurb": "Perfect for stylists who want more bookings without DM chaos.",
        "faq": [],
    },

    # Add more: contractor, retail, professional, etc.
}

def examples_index(request):
    # Build a lightweight list to render the grid.
    listing = []
    for slug, data in INDUSTRY_EXAMPLES.items():
        listing.append({
            "slug": slug,
            "title": data["title"],
            "emoji": data["emoji"],
            "subtitle": data["subtitle"],
            "thumb": data.get("og_image") or "/static/website/images/examples/placeholder.png",
        })
    return render(request, "website/examples/index.html", {"examples": listing})

def example_detail(request, slug):
    page = get_object_or_404(INDUSTRY_EXAMPLES, slug)
    return render(request, "website/examples/detail.html", {"page": INDUSTRY_EXAMPLES[slug]})