from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import Test, IQTestResult, EQTestResult
from .serializers import TestSerializer, IQTestResultSerializer, EQTestResultSerializer
from .utils import generate_unique_login
from .validations import validate_answers


class TestCreateView(APIView):
    def post(self, request):
        login = generate_unique_login()
        serializer = TestSerializer(data={'login': login})
        if serializer.is_valid():
            test = serializer.save()
            return Response({'login': test.login}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestResultView(APIView):
    """Вью для получения результатов тестов по login

    Пример запроса:
    GET /api/result/generated_login/
    """

    def get(self, request, login):
        try:
            test = Test.objects.prefetch_related(
                Prefetch('iq_test_result', queryset=IQTestResult.objects.all()),
                Prefetch('eq_test_result', queryset=EQTestResult.objects.all())
            ).get(login=login)

            iq_serializer = IQTestResultSerializer(test.iq_test_result.all(), many=True)
            eq_serializer = EQTestResultSerializer(test.eq_test_result.all(), many=True)

            return Response({
                'iq_results': iq_serializer.data,
                'eq_results': eq_serializer.data,
                'login': test.login,
            }, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response({'detail': 'Test not found.'}, status=status.HTTP_404_NOT_FOUND)


class IQTestResultCreateView(APIView):
    """View для добавления результатов IQ тестов

    Пример тела запроса:
    {
    "login":  "generated_login",
    "score": 25
    }
    """

    def post(self, request):
        login = request.data.get('login')
        score = request.data.get('score')

        test = get_object_or_404(Test, login=login)

        data = {'test': test.id, 'score': score, 'timestamp': timezone.now()}
        serializer = IQTestResultSerializer(data=data)

        if serializer.is_valid():
            serializer.save(test=test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EQTestResultCreateView(APIView):
    """View для добавления результатов EQ тестов
    Пример тела запроса:

    "login":  "generated_login",
    "answers": ["а", "б", "в", "г", "д"]
    }
    """

    def post(self, request):
        login = request.data.get('login')
        answers = request.data.get('answers')
        test = get_object_or_404(Test, login=login)

        try:
            validate_answers(answers)
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        result = EQTestResult.objects.create(test=test, answers=answers, timestamp=timezone.now())
        serializer = EQTestResultSerializer(result)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
