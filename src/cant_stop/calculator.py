"""
A dice roll probability simulator for the board game: Can't Stop

Given game pieces on a set of numbers, what is the chance that a dice roll will fail?
"""
import random


class DicePair:
    """Represent the four dice in Can't Stop"""
    def __init__(self):
        self.a, self.b, self.c, self.d = (0, 0, 0, 0)

    def roll(self):
        self.a = random.randint(1, 6)
        self.b = random.randint(1, 6)
        self.c = random.randint(1, 6)
        self.d = random.randint(1, 6)
        return self

    def get_groups(self):
        return {
            self.a + self.b,
            self.c + self.d,
            self.a + self.c,
            self.b + self.d,
            self.a + self.d,
            self.b + self.c,
        }

    def __str__(self):
        return f"{self.a} {self.b} {self.c} {self.d}"


def run(numbers):
    rolls = 1_000_000
    failure_count = 0
    p = DicePair()
    for _ in range(rolls):
        p.roll()
        roll_groups = p.get_groups()
        fail = numbers.isdisjoint(roll_groups)
        if fail:
            failure_count += 1

    success_percent = (rolls-failure_count)/rolls
    print(f"playing these numbers {numbers}")
    print(f"{failure_count} out of {rolls} rolls resulted in failure. ({success_percent*100:.2f}% success rate)")

    cur_percent = success_percent
    for attempt in range(1, 8):
        print(f"Going for {attempt} attempt(s) would carry a {cur_percent*100:.2f}% success rate")
        cur_percent = success_percent * cur_percent


if __name__ == '__main__':
    while True:
        print()
        resp = input("Enter numbers that have pieces on them (separated by spaces): ")
        tokens = resp.split()
        set_of_nums = {int(n) for n in tokens}
        run(set_of_nums)
