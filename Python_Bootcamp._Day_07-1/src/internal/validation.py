def validate_data(data: dict) -> None:
    """
     Проверяет словарь данных, который представляет вопросы и ответы опроса.
     В словаре должен быть ключ «вопросы» со списочным значением, содержащим вопросно-ответные словари.
     Каждый словарь вопросов и ответов должен иметь поле «вопрос» и поле «ответы» со значением списка,
     Поле «ответы» должно содержать словари, представляющие возможные варианты ответов на вопрос,
     каждый с полем «ответ» и полем «значение», которое является логическим значением, указывающим, правильный ли выбор ответа.

     :param data: Словарь данных для проверки (dict)
     :return: не возвращает значение, но вызывает ValueError, если возникает какая-либо ошибка проверки.
    """
    if not isinstance(data, dict):
        raise ValueError('Invalid data format')
    if 'questions' not in data:
        raise ValueError('Expected "questions" field')
    questions = data['questions']
    if not isinstance(questions, list):
        raise ValueError('"questions" should be a list')
    for question in questions:
        if 'question' not in question or 'answers' not in question:
            raise ValueError('Should have "question" and "answers" field')
        answers = question['answers']
        if not isinstance(answers, list):
            raise ValueError('"answers" should be a list')
        for answer in answers:
            if 'answer' not in answer or 'value' not in answer:
                raise ValueError('Should have "answer" and "value" field')