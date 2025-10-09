from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserModel


# Register your models here.
@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Data User", {"fields": ("nama", "no_hp", "role", "created_at")}),
        (
            "permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    readonly_fields = ["created_at"]

    add_fieldsets = [
        (
            "",
            {
                "classes": ["wide"],
                "fields": [
                    "username",
                    "nama",
                    "password1",
                    "password2",
                    # "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ],
            },
        )
    ]

    # add_fieldsets = (
    #     None,
    #     {
    #         "classes": ("wide",),
    #         "fields": ("username", "nama", "no_hp", "role", "password1", "password2"),
    #     },
    # )

    list_display = ["user_id", "username", "nama", "no_hp", "role", "is_active"]
    search_fields = ["username", "nama", "role"]
    ordering = ["user_id"]
