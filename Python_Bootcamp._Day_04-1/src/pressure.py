import random
import time

def emit_gel(step: int):
    value = 50
    sign = +1
    while True:
        back = yield value
        if back is not None:
            sign = -sign
        increment = random.randint(0, step)
        value += sign * increment
        time.sleep(0.3)


def valve(gen):
    for val in gen:
        #print(valve)
        if val < 10 or val > 90:
            gen.close()
            break
        if val < 20 or val > 80:
            gen.send('flip')


if __name__ == '__main__':
    gen2 = emit_gel(15)
    valve(gen2)