from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Test,Question,Answers,Submission,SelectedAnswer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","firstname","lastname","username"]
        




    
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ["id","title","is_correct"]
         

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    # test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all(),write_only=True)
    class Meta:
        model = Question
        fields = ["id",'title','answers','test']
        
    def create(self, validated_data):
        answers = validated_data.pop("answers")
        
        
        question = Question.objects.create(**validated_data)
        
        for answer in answers:
            Answers.objects.create(question=question,**answer)
            
        return question
    
    def validate_answers(self,answers):
        count = 0
        for answer in answers:
            if answer["is_corrext"]:
                count+=1
        if count !=1:
            raise serializers.ValidationError("Kamida bittasida togri javob bolishi kerak")
        return answers
        
    
class TestSerializers(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    question = QuestionSerializer(many=True,read_only=True)
    class Meta:
        model = Test
        fields = ["id","nomi","creator","questions"]
    
class SelectedAnswerSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=Answers.objects.all())
    


class SubmissionSerializer(serializers.Serializer):
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())
    selected_answers = SelectedAnswerSerializer(many=True)
    corrected_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    
    def create(self, validated_data):
        test = validated_data.pop("test")
        user =  validated_data.pop("user")
        
        submission = Submission.objects.create(test=test,user=user)
        
        count=0
        
        for selected_answer in validated_data["selected_answers"]:
            answer = selected_answer["answer"]
            SelectedAnswer.objects.create(**selected_answer,submission=submission,is_correct=answer.is_correct)
            
            if answer.is_correct:
                corrected_count+=1
        return submission
     
     
class CustomTokenObtainViewSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data = {}
        data["accessToken"] = data.pop("access")
        data["refreshToken"] = data.pop("refresh")
        data["user"] = {
            "user_id":self.user.id,
            "username":self.user.username,
            "avatar_url":""
        }
        
        return data
        
class MyTestSerializers(serializers.ModelSerializer):
    savollar_soni = serializers.SerializerMethodField()
    submissionlar_soni = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ["id","nomi","created_at","savollar_soni","submissionlar_soni"]
        
    def get_savollar_soni(self, obj):
        return obj.questions.count()
    
    def get_submissionlar_soni(self, obj):
        return obj.submissions.count()
    