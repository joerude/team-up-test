from rest_framework.exceptions import ValidationError

ALLOWED_ANSWERS = ["а", "б", "в", "г", "д"]


def validate_answers(self, answers: list[str]) -> None:
    if not isinstance(answers, list) or len(answers) != 5:
        raise ValidationError("Поле 'answers' должно содержать 5 элементов.")

    invalid_answers = [answer for answer in answers if answer not in self.ALLOWED_ANSWERS]
    if invalid_answers:
        invalid_answers_str = ', '.join(invalid_answers)
        raise ValidationError(
            f"Некорректный ответ: {invalid_answers_str}. "
            f"Допустимые значения ответов: 'а', 'б', 'в', 'г', 'д'."
        )