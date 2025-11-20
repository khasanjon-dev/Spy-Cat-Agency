from django.contrib import admin

from .models import SpyCat, Mission, Target


@admin.register(SpyCat)
class SpyCatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "breed", "years_of_experience", "salary")


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("id", "cat", "is_completed", "created_at")


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ("id", "mission", "name", "country", "is_completed")
