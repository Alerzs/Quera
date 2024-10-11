from rest_framework import generics
from .models import *
from Bank.models import *
from auth_user.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser ,AllowAny
from rest_framework import status
from django.db.models import Count ,Q
from django.shortcuts import get_object_or_404
from .serializers import *


class SoalView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        if self.request.method == 'GET':
            return [AllowAny()]
    
    def post(self ,request):
        # my_user = request.user
        # name = request.data.get('name')
        # category = request.data.get('category')
        # level = request.data.get('level')
        # soorat = request.data.get('soorat')
        # answer_type = request.data.get('answer_type')
        # test_case = request.data.get('test_case')
        # test_case_answer = request.data.get('test_case_answer')

        # if not name or not category or not level or not soorat or not answer_type:
        #     return Response('name ,category ,level ,soorat and answer_type is required')
        # my_soal = Soal.objects.create(name=name,creator=my_user,category=category,level=level,soorat=soorat,answer_type=answer_type,test_case=test_case,test_case_answer=test_case_answer)
        # serializer = SoalSerializer(my_soal)
        # return Response(serializer.data ,status=status.HTTP_201_CREATED)
        serializer = SoalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self ,request):
        soals = Soal.objects.all()
        serializer = SoalSerializer(soals,many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)   
    

# class SoalDetails(APIView):



