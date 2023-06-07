from django.urls import path
from .views import TestCreateView, IQTestResultCreateView, EQTestResultCreateView, TestResultView

urlpatterns = [
    path('test/', TestCreateView.as_view(), name='test-create'),
    path('result/iq/', IQTestResultCreateView.as_view(), name='iq-test-result-create'),
    path('result/eq/', EQTestResultCreateView.as_view(), name='eq-test-result-create'),
    path('result/<str:login>/', TestResultView.as_view(), name='test-result'),
]
