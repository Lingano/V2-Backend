from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloWorldAPI(APIView):
    """
    A simple API view that returns a greeting
    """
    permission_classes = []  # Allow anyone to access
    
    def get(self, request):
        return Response({
            "message": "Hello from the Django API!",
            "status": "success"
        })


class CurrentTimeAPI(APIView):
    """
    An API view that returns the current server time
    """
    permission_classes = []  # Allow anyone to access
    
    def get(self, request):
        from datetime import datetime
        now = datetime.now()
        return Response({
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "success"
        })