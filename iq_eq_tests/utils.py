from random import choices
import string
from .models import Test


def generate_unique_login() -> str:
    """Генерируем уникальный логин (набор в 10 знаков)"""
    login_length = 10
    characters = string.ascii_letters + string.digits
    while True:
        login = ''.join(choices(characters, k=login_length))
        if not Test.objects.filter(login=login).exists():
            return login
