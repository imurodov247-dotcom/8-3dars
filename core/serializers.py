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
    id = serializers.CharField(required=False)    
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
    
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title",instance.title)
        instance.save()
        
        answers_data = validated_data.pop("answers")
        new_answer_ids = []
        
        for answer_data in answers_data:
            try:
                try:
                    answer_data["id"] = int(answer_data["id"])
                except:
                    new_answer = Answers.objects.create(
                        title=answer_data['title'],
                        is_correct=answer_data['is_correct'],
                        question = instance
                        )
                    new_answer_ids.append(new_answer.id) 
                    continue        
               
                answer = Answers.objects.get(pk=answer_data['id'])
                answer = answer_data["title"]
                answer.is_correct = answer_data["is_correct"]
                new_answer_ids.append(answer.id)
                answer.save()
            except Answers.DoesNotExist:
                continue
                   
        instance.answers.exclude(id__in = new_answer_ids).delete()
        return instance
    
   
    def validate_answers(self,answers):
        count = 0
        for answer in answers:
            if answer["is_corrext"]:
                count+=1
        if count !=1:
            raise serializers.ValidationError("Kamida bittasida togri javob bolishi kerak")
        return answers
        
    
class TestSerializers(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Test
        fields = ["id","nomi","creator","questions",'created_at']
        
    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        test = Test.objects.create(**validated_data)
        
        for question_data in questions_data:
            question_serializer = QuestionSerializer(data=questions_data)
            question_serializer.is_valid(raise_exception=True)
            question_serializer.save(test=test)
        return test
    
class SelectedAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    question_title = serializers.CharField(read_only = True)
    answer_title = serializers.CharField(read_only = True)
    correct_answer_title = serializers.CharField(read_only = True)
    is_correct = serializers.BooleanField(read_only = True)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.PrimaryKeyRelatedField(queryset=Answers.objects.all())
    


class SubmissionSerializer(serializers.Serializer):
    # test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())
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
            question = selected_answer["question"]
            correct_answer_title = ""
            correct_answer_list = question.answer.filter(is_correct=True)
            if correct_answer_list:
                correct_answer_title = correct_answer_list[0].title
            
            SelectedAnswer.objects.create(
                **selected_answer,
                submission=submission,
                is_correct=answer.is_correct,
                question_title = question.title,
                answet_title = answer.title,
                correct_answer_title = correct_answer_title)
            
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
    
    
class MySubmissionSerializer(serializers.ModelSerializer):
        test_name = serializers.SerializerMethodField()
        correct_count = serializers.SerializerMethodField()
        total_count = serializers.SerializerMethodField()
        class Meta:
            model = Submission
            fields = ['id','test','test_name','correct_count','total_count','created_at']
    
    
        def get_correct_count(self, obj):
            return obj.selected_answers.filter(is_correct=True).count()
        
        
        def get_total_count(self,obj):
            return obj.selected_answers.count()
        
            
        def get_test_name(self,obj):
            return obj.test.nomi()
        
        
        
class SelectedAnswerFullSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    question_title = serializers.CharField(read_only = True)
    answer_title = serializers.CharField(read_only = True)
    correct_answer_title = serializers.CharField(read_only = True)
    is_correct = serializers.BooleanField(read_only = True)
    question = QuestionSerializer()
    answer = AnswerSerializer()
        
        
class SubmissionFullSerializer(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    correct_count = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()
    selected_answers = SelectedAnswerFullSerializer(many=True)
    class Meta:
        model = Submission
        fields = ['id','selected-answer','test','test_name','correct_count','total_count','created_at']
        
        
        
        def get_correct_count(self, obj):
            return obj.selected_answers.filter(is_correct=True).count()
        
        
        def get_total_count(self,obj):
            return obj.selected_answers.count()
        
            
        def get_test_name(self,obj):
            return obj.test.nomi()