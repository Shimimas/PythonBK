import random

def constructor(self):
    points_left = 100
    self.neuroticism = random.randint(0, points_left)
    points_left -= self.neuroticism
    self.openness = random.randint(0, points_left)
    points_left -= self.openness
    self.conscientiousness = random.randint(0, points_left)
    points_left -= self.conscientiousness
    self.extraversion = random.randint(0, points_left)
    points_left -= self.extraversion
    self.agreeableness = points_left

    

def turrets_generator():
    while True:
        Turret = type("Turret", (object,), {
            "__init__": constructor,
            "shoot": lambda _: print('Shooting'),
            "search": lambda _: print('Searching'),
            "talk": lambda _: print('Talking'),
        })
        yield Turret()


def main():
    t1 = turrets_generator()
    t1 = next(t1)
    t1.shoot()
    t1.search()
    t1.talk()
    print(t1.neuroticism)
    print(t1.openness)
    print(t1.conscientiousness)
    print(t1.extraversion)
    print(t1.agreeableness)


if __name__ == '__main__':
    main()