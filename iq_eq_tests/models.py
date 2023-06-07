from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Test(models.Model):
    """Модель тестов для IQ и EQ"""

    login = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.login

    class Meta:
        ordering = ['login']
        verbose_name_plural = 'tests'


class IQTestResult(models.Model):
    """Модель результатов IQ тестов """

    test = models.ForeignKey(Test,
                             on_delete=models.CASCADE,
                             related_name='iq_test_result')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.test.login}: {self.score}'

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'iq test results'


class EQTestResult(models.Model):
    """Модель результатов EQ тестов """

    test = models.ForeignKey(Test,
                             on_delete=models.CASCADE,
                             related_name='eq_test_result')
    answers = models.CharField(max_length=5)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.test.login}: {self.answers}'

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'eq test results'
