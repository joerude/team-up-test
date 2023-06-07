from django.urls import path
from .views import TestCreateView, IQTestResultCreateView, EQTestResultCreateView, TestResultView

urlpatterns = [
    path('test/', TestCreateView.as_view()),
    path('result/iq/', IQTestResultCreateView.as_view()),
    path('result/eq/', EQTestResultCreateView.as_view()),
    path('result/<str:login>/', TestResultView.as_view()),
]
