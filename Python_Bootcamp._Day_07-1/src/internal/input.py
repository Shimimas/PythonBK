class InputData:
    """
    Класс, описывающий информацию о пациенте.

    Атрибуты:
        respiration (int): Частота дыхания в минуту.
        heart_rate (int): Частота сердечных сокращений в минуту.
        blushing_level (int): Степень покраснения на лице по шкале от 1 до 6.
        pupillary_dilation (int): Диаметр зрачков в миллиметрах.
        
    Методы:
        update(self) -> bool: Обновляет информацию о пациенте на основе пользовательского ввода
        check(self) -> bool: Проверяет, соответствует ли информация о пациенте нормальным параметрам

    """
    def __init__(self):
        self.respiration: int = None
        self.heart_rate: int = None
        self.blushing_level: int = None
        self.pupillary_dilation: int = None

    def update(self) -> bool:
        """
        Обновляет информацию о пациенте на основе пользовательского ввода.
        
        Возвращает:
            bool: Статус обновления информации.
        """
        self.respiration = int(input("Respiration rate (int breaths per minute): "))
        self.heart_rate = int(input("Heart rate (in beats per minute): "))
        self.blushing_level = int(input("Blushing level (on a scale of 1-6): "))
        self.pupillary_dilation = int(input("Pupillary dilation (in mm): "))
        return self.check()
    
    def check(self) -> bool:
        """
        Проверяет, соответствует ли информация о пациенте нормальным параметрам.
        
        Возвращает:
            bool:Статус соотвествия информации нормальным параметрам.
        """
        return 12 <= self.respiration <= 16 and \
               60 <= self.heart_rate <= 100 and \
               1 <= self.blushing_level <= 6 and \
               2 <= self.pupillary_dilation <= 8