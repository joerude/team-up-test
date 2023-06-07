from django.contrib import admin

from iq_eq_tests.models import IQTestResult, EQTestResult, Test

admin.site.register(IQTestResult)
admin.site.register(EQTestResult)
admin.site.register(Test)
