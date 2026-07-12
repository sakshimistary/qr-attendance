from django.contrib import admin

from classes.models import Batch, Attendance, BatchStudent
from users.models import Student

# Register your models here.


class BatchStudentInline(admin.TabularInline):
    model = BatchStudent
    autocomplete_fields = ("student", "batch")
    extra = 0


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    search_fields = ["name", "code"]
    inlines = [BatchStudentInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ("student", "batch")
