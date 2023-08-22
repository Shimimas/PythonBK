import threading
import random

class Doctor:
    def __init__(self, number):
        self.number = number
        self.__left_hand = None
        self.__right_hand = Screwdriver()
        self.__other_doctor = None
        self.busy = threading.Lock()
    
    @property
    def left_hand(self):
        return self.__left_hand

    @left_hand.setter
    def left_hand(self, value):
        self.__left_hand = value
    
    @property
    def right_hand(self):
        return self.__right_hand

    @right_hand.setter
    def right_hand(self, value):
        self.__right_hand = value
    
    def set_other_doctor(self, other):
        self.__other_doctor = other
    
    def steal_screwdriver(self, other_doctors_hand):
        if not self.left_hand:
            self.left_hand = other_doctors_hand
        elif not self.right_hand:
            self.right_hand = other_doctors_hand

    def try_steal(self):
        with self.__other_doctor.busy:
            if self.__other_doctor.left_hand:
                self.steal_screwdriver(self.__other_doctor.left_hand)
                self.__other_doctor.left_hand = None
                return True
            elif self.__other_doctor.right_hand:
                self.steal_screwdriver(self.__other_doctor.right_hand)
                self.__other_doctor.right_hand = None
                return True
            return False

    def standoff(self):
        while True:
            if self.try_steal() and  self.try_blast():
                break
        
    def try_blast(self):
        with self.busy:
            if not isinstance(self.left_hand, Screwdriver) or not isinstance(self.left_hand, Screwdriver):
                return False
            with threading.Lock():
                print(f"Doctor {self.number}: Blast!")
        return True

class Screwdriver:
    counter = 0
    def __init__(self):
        self.id = self.counter
        Screwdriver.counter += 1

    def __str__(self) -> str:
        return str(self.id)
        

if __name__ == '__main__':
    doctors = []
    for n in range(9, 14):
        doctors.append(Doctor(n))
    left_doctor = None
    for doctor in doctors:
        if left_doctor:
            doctor.set_other_doctor(left_doctor)
        left_doctor = doctor
    doctors[0].set_other_doctor(left_doctor)
    threads = []
    for doctor in doctors:
        thread = threading.Thread(target=doctor.standoff)
        threads.append(thread)
    random.shuffle(threads)
    for thread in threads:
        thread.start() 
    for thread in threads:
        thread.join()