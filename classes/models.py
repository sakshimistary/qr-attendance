from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F

from users.models import Trainer, Student

# Create your models here.


class Batch(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    trainer = models.OneToOneField(Trainer, on_delete=models.PROTECT)
    students = models.ManyToManyField(
        Student, blank=True, null=True, through="BatchStudent"
    )

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError("end_time must be greater than start_time")

    def __str__(self):
        return f"{self.code} - {self.name} ({self.start_date})"


class BatchStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    join_date = models.DateField()


class Attendance(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    marked_at = models.DateField(blank=True, null=True)

    def clean(self):
        if not BatchStudent.objects.filter(
            batch=self.batch, student=self.student
        ).exists():
            raise ValidationError("Student does not belong to batch")

        # To prevent duplicate records
        if (
            Attendance.objects.filter(
                batch=self.batch, student=self.student, date=self.date
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                f"Attendance already exists for student {self.student}, batch {self.batch}, date: {self.date}"
            )

    def __str__(self):
        return f"{self.batch.code} - {self.student.user.get_full_name()} ({self.date})"

    class Meta:
        unique_together = ("batch", "student", "date")
