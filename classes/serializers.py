import datetime

from rest_framework import serializers

from classes.models import Batch, BatchStudent
from users.models import Student


class AttendanceRequestSerializer(serializers.Serializer):
    student_username = serializers.CharField(required=True)
    batch_code = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    logging_at = serializers.DateTimeField(default=datetime.datetime.now)

    def validate(self, attrs):
        student_username = attrs.get("student_username")
        batch_code = attrs.get("batch_code")

        student = Student.objects.filter(user__username=student_username).first()
        batch = Batch.objects.filter(code=batch_code).first()

        if student is None:
            raise serializers.ValidationError(
                {"student_username": "No student exist for the given username"}
            )

        if batch is None:
            raise serializers.ValidationError(
                {"batch_code": "No batch exist for the given batch code"}
            )

        if not BatchStudent.objects.filter(batch=batch, student=student).exists():
            raise serializers.ValidationError(
                {"student_username": "Student does not belong to this batch"}
            )

        return attrs

    class Meta:
        fields = ("student_username", "batch_code", "date", "logging_at")
