from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import process_csv_and_save
from .models import User
from .serializers import UserSerializer

class UserCSVUploadView(APIView):
    def post(self,request):
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File is not a CSV"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            age_report = process_csv_and_save(csv_file, User)
            return Response({"message": "CSV processed and users saved.","age_distribution":age_report}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

               
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        
