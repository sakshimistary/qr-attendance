from django.contrib import admin

from users.models import Student, User, Trainer


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name', "user__username", "user__email"]

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    pass
