import string
import random
from datetime import datetime

from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView

from .models import Test, IQTestResult, EQTestResult
from .serializers import TestSerializer, IQTestResultSerializer, EQTestResultSerializer


class TestCreateView(APIView):
    def post(self, request):
        login = self.generate_unique_login()
        serializer = TestSerializer(data={'login': login})
        if serializer.is_valid():
            test = serializer.save()
            return Response({'login': test.login}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def generate_unique_login():
        login_length = 10
        characters = string.ascii_letters + string.digits
        while True:
            login = ''.join(random.choices(characters, k=login_length))
            try:
                Test.objects.get(login=login)
            except Test.DoesNotExist:
                return login


class TestResultView(APIView):
    """Вью для получения результатов тестов по login

    Пример запроса:
    GET /api/result/randomdata/
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
    "login":  "randomdata",
    "iq_score": 25
    }
    """

    def post(self, request):
        login = request.data.get('login')
        score = request.data.get('score')

        try:
            test = Test.objects.get(login=login)
        except Test.DoesNotExist:
            raise NotFound(detail='Test not found.')

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

    "login":  "randomdata",
    "answers": ["а", "б", "в", "г", "д"]
    }
    """
    ALLOWED_ANSWERS = ["а", "б", "в", "г", "д"]

    def validate_answers(self, answers):
        if not isinstance(answers, list) or len(answers) != 5:
            raise ValidationError("Поле 'answers' должно содержать 5 элементов.")

        invalid_answers = [answer for answer in answers if answer not in self.ALLOWED_ANSWERS]
        if invalid_answers:
            invalid_answers_str = ', '.join(invalid_answers)
            raise ValidationError(
                f"Некорректный ответ: {invalid_answers_str}. "
                f"Допустимые значения ответов: 'а', 'б', 'в', 'г', 'д'."
            )

    def post(self, request):
        login = request.data.get('login')
        answers = request.data.get('answers')

        try:
            test = Test.objects.get(login=login)
        except Test.DoesNotExist:
            return Response({'detail': 'Test not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            self.validate_answers(answers)
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        result = EQTestResult.objects.create(test=test, answers=answers, timestamp=datetime.now())
        serializer = EQTestResultSerializer(result)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
