from django.urls import path,include


from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register("",views.TestModelViewSet)

urlpatterns = [
    path('', views.HelloView.as_view(),name="hello"),
    path('api/',include(router.urls)),
     path('api/auth/login/', views.CustomObtainPairview.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/tests/<int:test_pk>/questions',views.QuestionApiView.as_view(),name="question_post"),
    path('api/tests/<int:test_pk>/submission',views.SubmissionApiview.as_view(),name="submission_post"),
    path('api/submissions',views.SubmissionListView.as_view(),name="submission_post"),
    path('api/my_test',views.SubmissionListView.as_view(),name="mytest-list"),
    path('api/tests/<int:test_id>/questions',views.TestQuestionListView.as_view(),name="mytest-list"),
    path('api/questions/<int:pk>/questions',views.TestQuestionDetailView.as_view(),name="question-detail"),
    
]
