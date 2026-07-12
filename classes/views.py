import io
from asyncio import mixins

import qrcode
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from classes.models import Attendance
from classes.serializers import AttendanceRequestSerializer

# Create your views here.


class AttendanceView(APIView):
    def get(self, request, format=None):
        return Response({"status": "success"})

    def post(self, request, format=None):
        data = request.data
        serializer = AttendanceRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        student_username = serializer.validated_data["student_username"]
        batch_code = serializer.validated_data["batch_code"]

        if Attendance.objects.filter(
            student__user__username=student_username,
            batch__code=batch_code,
            date=serializer.validated_data["date"],
        ).exists():
            raise ValidationError(
                {
                    "student_username": "Attendance already exists.",
                }
            )

        qr = qrcode.make(data)
        img_byte_arr = io.BytesIO()
        qr.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return HttpResponse(img_byte_arr.getvalue(), content_type="image/png")
