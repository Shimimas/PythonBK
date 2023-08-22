import sys
sys.path.append('internal')
from runner import VKTRunner

if __name__ == "__main__":
    runner = VKTRunner('questions.json')
    runner.run()