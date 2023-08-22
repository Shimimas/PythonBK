from vkt import VKTest

class VKTRunner:
    """
    Класс для запуска VKTest.

    Атрибуты:
        test: Объект класса VKTest.
        test_file: путь к файлу вопросов для теста.

    Методы:
        run(): запускает VKTest для предоставленного тестового файла.
    """
    def __init__(self, test_file: str):
        self.test = VKTest(test_file)
        
    def run(self) -> None:
        self.test.get_questions()
        print("You passed the test!" if self.test.run_test() else "You failed the test!")