from django.contrib import admin

from .models import Contact, Experience, Profile, Project, Visit


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return super().has_add_permission(request) and not Profile.objects.exists()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "position")
    list_editable = ("published", "position")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created", "emailed")
    readonly_fields = ("created", "emailed")
    search_fields = ("name", "email", "message")


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("created", "ip", "country", "region", "city", "referrer_host")
    list_filter = ("country", "created")
    readonly_fields = ("created", "ip", "country", "region", "city", "device", "language", "referrer_host")
    ordering = ("-created",)

    def has_add_permission(self, request):
        return False


admin.site.site_header = "Alan Shaju · Portfolio CMS"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "period", "published", "position")
    list_editable = ("published", "position")
    search_fields = ("title", "organization")
