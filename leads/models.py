from django.db import models

class Lead(models.Model):
    CONTACT_CHOICES = (("email", "Email"), ("phone", "Phone"))
    PLAN_CHOICES = (
        ("Minimal-Growth", "Minimal-Growth"),
        ("Standard-Growth", "Standard-Growth"),
        ("Explosive-Growth", "Explosive-Growth"),
    )

    name = models.CharField(max_length=120)
    contact_method = models.CharField(max_length=10, choices=CONTACT_CHOICES)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    growth_plan = models.CharField(max_length=32, choices=PLAN_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    consent = models.BooleanField(default=False)  # optional

    def __str__(self):
        return f"{self.name} • {self.growth_plan} • {self.created_at:%Y-%m-%d}"
