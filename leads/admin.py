from django.contrib import admin
from .models import Lead
import csv
from django.http import HttpResponse

@admin.action(description="Export selected to CSV")
def export_leads_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="leads.csv"'
    writer = csv.writer(response)
    writer.writerow(["created_at","name","contact_method","email","phone","growth_plan","message"])
    for obj in queryset:
        writer.writerow([obj.created_at, obj.name, obj.contact_method, obj.email, obj.phone, obj.growth_plan, obj.message])
    return response

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at","name","growth_plan","contact_method","email","phone")
    list_filter = ("growth_plan","contact_method","created_at")
    search_fields = ("name","email","phone","message")
    actions = [export_leads_csv]
