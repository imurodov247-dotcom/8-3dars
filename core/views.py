from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,ListAPIView
# Create your views here.

class HelloView(APIView):
    def get(self,request):
        return Response({"text":"Heloo world"})
    
    
class TestModelViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.TestSerializers
    queryset = models.Test.objects.all()
    
    
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)
        
        
        
class QuestionApiView(APIView):
    # permission_classes = [IsAuthenticated]
   
    
    def post(self, request,test_pk):
        try:
            test = models.Test.objects.get(pk=test_pk)
        except models.Test.DoesNotExist:
            return Response({"error":"test not found"})
        
        
        question_serializer = serializers.QuestionSerializer(data=request.data)
        question_serializer.is_valid(raise_exception=True)
        question_serializer.sava(test=test)
        
        return Response(question_serializer.data,status=201)
    
    
class SubmissionApiview(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self,request,test_pk):
        try:
            test = models.Test.objects.get(pk=test_pk)
        except models.Test.DoesNotExist:
            return Response({"error":"test not found"})
        
        serializer = serializers.SubmissionSerializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        serializer.sava(test=test,user=self.request.user)
        
        
        return Response(serializer.data, status=201)
    
class SubmissionListView(ListAPIView):
    serializer_class = serializers.SubmissionSerializer
    queryset =  models.Submission.objects.all()            