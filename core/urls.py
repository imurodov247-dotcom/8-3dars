from django.urls import path,include


from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('', views.HelloView.as_view(),name="hello"),
    path('api/tests/<int:pk>/',views.TestUpdateDestroyApiView.as_view(),name='test delete update'),
    path('api/auth/login/', views.CustomObtainPairview.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/tests/<int:test_pk>/questions',views.QuestionApiView.as_view(),name="question_post"),
    path('api/tests/<int:test_pk>/submission',views.SubmissionApiview.as_view(),name="submission_post"),
    path('api/submissions',views.SubmissionListView.as_view(),name="submission_post"),
    path('api/submissions/<int:pk>',views.SubmissionDetailView.as_view(),name="detail"),
    path('api/my_test',views.MyTestListview.as_view(),name="mytest-list"),
    path('api/tests/<int:test_id>/questions',views.TestQuestionListView.as_view(),name="mytest-list"),
    path('api/questions/<int:pk>/questions',views.TestQuestionDetailView.as_view(),name="question-detail"),
    path('api/my-submissions',views.MysubmissionListView.as_view(),name="my-submission"),
    
]
