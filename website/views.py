from django.shortcuts import render, redirect
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
        "demo_url": None,
        "og_image": "/static/website/images/examples/rest-thumb.png",
        "highlight_image": "website/images/examples/rest.png",
        "gallery": [
            "website/images/examples/rest-menu.png",
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
            {"title": "Local SEO", "desc": "Restaurant schema, hours, and GBP sync."},
        ],
        "cta_blurb": "Includes menu setup, photo galleries, hours, and integrations you already use.",
        "seo_title": "Restaurant Website Design Demo",
        "seo_desc": "See a high-converting restaurant site layout: menus, ordering, hours, and local SEO baked in.",
        "faq": [
            {"q": "Can you connect online ordering I already use?",
             "a": "Yes—DoorDash, Uber Eats, Toast, or your POS’s native ordering."},
            {"q": "Can I update my menu myself?",
             "a": "Absolutely. You’ll get an editor to change items, prices, and photos anytime."}
        ],
        # Optional per-demo brand colors for styling:
        "brand_top": "#550305",
        "brand_bottom": "#F62944",
    },

    "salon": {
        "emoji": "💇",
        "title": "Salon Website Demo",
        "short_label": "Salon",
        "audience_label": "Salons & Spas",
        "subtitle": "Booking-first design with services, stylists, and photo proof.",
        "demo_url": None,
        "og_image": "/static/website/images/examples/salon-thumb.png",
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
        "seo_title": "Salon Website Demo",
        "seo_desc": "Booking-first salon website with services, pricing, reviews, and gallery.",
        "faq": [],
        "brand_top": "#F9D8FF",
        "brand_bottom": "#B86AD9",
    },
}

# -----------------------------
# EXAMPLES: index + detail
# -----------------------------
def examples_index(request):
    listing = [{
        "slug": slug,
        "title": data["title"],
        "emoji": data["emoji"],
        "subtitle": data["subtitle"],
        "thumb": data.get("og_image") or "/static/website/images/examples/placeholder.png",
    } for slug, data in INDUSTRY_EXAMPLES.items()]
    return render(request, "website/examples/index.html", {"examples": listing})

def example_detail(request, slug):
    page = INDUSTRY_EXAMPLES.get(slug)
    if not page:
        raise Http404("Example not found.")
    # also pass slug so templates can put a body class, etc.
    return render(request, "website/examples/detail.html", {"page": page, "slug": slug})