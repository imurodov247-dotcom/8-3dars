from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound
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
    
    
class CustomObtainPairview(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainViewSerializer
    
class MyTestListview(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MyTestSerializers
    
    def get_queryset(self):
        return models.Test.objects.filter(creator=self.request.user)
    
    
class TestQuestionListView(ListCreateAPIView):
    serializer_class = serializers.QuestionSerializer
    
    def get_test(self):
        try:
            return models.Test.objects.get(pk=self.kwargs["test_id"])
        except models.Test.DoesNotExist:
            raise NotFound(detail="Test not found ")
        
    
    def get_queryset(self):
        test=self.get_test()
        return models.Question.objects.filter(test=test)
    
    def perform_create(self, serializer):
        test = self.get_test()
        serializer.save(test=test)
    
    
class TestQuestionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all()
    