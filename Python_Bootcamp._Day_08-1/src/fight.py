import asyncio

from enum import Enum, auto
from random import choice
import random


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)


async def fight():
    agent=Agent()
    async for el in agent:
        if (agent.health > 0):
            if el == Action.HIGHKICK:
                print(f"Agent: {el}, Neo: {Action.HIGHBLOCK}, Agent Health: {agent.health}")
            elif el == Action.LOWKICK:
                print(f"Agent: {el}, Neo: {Action.LOWBLOCK}, Agent Health: {agent.health}")
            elif el == Action.HIGHBLOCK:
                agent.health -= 1
                print(f"Agent: {el}, Neo: {Action.LOWKICK}, Agent Health: {agent.health}")
            else:
                agent.health -= 1
                print(f"Agent: {el}, Neo: {Action.HIGHKICK}, Agent Health: {agent.health}")
        else:
            print('Neo wins!')
            break
    
async def fightmany(n):
    agents = [Agent().__aiter__() for _ in range(n)]
    while len(agents):
        number = random.randint(0, len(agents) - 1)
        agent = agents[number]
        el = await agent.__anext__()
        if (agent.health > 0):
            if el == Action.HIGHKICK:
                print(f"Agent: {el}, Neo: {Action.HIGHBLOCK}, Agent {number + 1} Health: {agent.health}")
            elif el == Action.LOWKICK:
                print(f"Agent: {el}, Neo: {Action.LOWBLOCK}, Agent {number + 1} Health: {agent.health}")
            elif el == Action.HIGHBLOCK:
                agent.health -= 1
                print(f"Agent: {el}, Neo: {Action.LOWKICK}, Agent {number + 1} Health: {agent.health}")
            else:
                agent.health -= 1
                print(f"Agent: {el}, Neo: {Action.HIGHKICK}, Agent {number + 1} Health: {agent.health}")
        else:
            agents.remove(agent)
    print('Neo wins!')

if __name__ == "__main__":
    print("First part!")
    asyncio.run(fight())
    print("Bonus part!")
    asyncio.run(fightmany(3))
