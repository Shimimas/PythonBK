from input import InputData
from validation import validate_data
from json import load
from random import shuffle

class VKTest:
    """
    Класс для проведения тестирования пользователей.

    Атрибуты:
    questions_file(str): Путь к файлу с вопросами.

    Методы:
    get_questions(): Загружает вопросы из файла
    run_test() -> bool: Запускает тестирование и возвращает результат
    is_valid(length: int) -> str: Проверяет ввод пользователя на корректность.
    """
    def __init__(self, questions_file: str):
        """
        Создает новый объект класса VKTest.

        Аргументы:
        questions_file (str): Путь к файлу с вопросами.
        """
        self.questions_file: str = questions_file
        self.input_data: InputData = InputData()
        self.questions: list = None
    def get_questions(self) -> None:
        """
        Загружает вопросы из указанного файла.
        """
        try:
            with open(self.questions_file) as f:
                data = load(f)
                validate_data(data)
                self.questions = data['questions']
                shuffle(self.questions)
        except FileNotFoundError:
            print(f'{self.questions_file} not found.')
    def run_test(self) -> bool:
        """
        Запускает тестирование пользователя и возвращает результат.

        Возвращает:
        bool: Результат тестирования (True - прошел, False - не прошел).
        """
        score: int = 0
        for question in self.questions:
            print(question['question'])
            for i, answer in enumerate(question['answers']):
                print(f"{i+1} {answer['answer']}")
            choice = self.is_valid(len(question['answers']))
            score += question['answers'][int(choice) - 1]['value'] * \
                     1 if self.input_data.update() else 2
            if score > 10:
                return False
        return True
    def is_valid(self, length:int) -> str:
        """
        Проверяет, корректен ли ввод пользователя.

        Аргументы:
        length(int): Максимальное число ответов на вопрос.

        Возвращает:
        str: Номер выбранного пользователем ответа.
        """
        while True:
            choice = input('Your choice: ')
            if choice.isdigit() and 1 <= int(choice) <= length:
                return choice
            print('Enter a number between 1 and ', length)