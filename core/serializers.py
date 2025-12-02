from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Test,Question,Answers,Submission,SelectedAnswer

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
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all(),write_only=True)
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
    
        