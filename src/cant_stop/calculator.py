"""
A dice roll probability simulator for the board game: Can't Stop

Given game pieces on a set of numbers, what is the chance that a dice roll will fail?
"""
import random
from multiprocessing import Pool


class FourDice:
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


def do_multiple_rolls(set_of_numbers, num_of_rolls):
    """Given the set of numbers your pieces are on, do multiple rolls and see how many failures you would get"""
    failure_count = 0
    p = FourDice()
    for _ in range(num_of_rolls):
        p.roll()
        roll_groups = p.get_groups()
        fail = set_of_numbers.isdisjoint(roll_groups)
        if fail:
            failure_count += 1
    return num_of_rolls, failure_count


def print_summary(players_numbers, rolls, failure_count):
    success_percent = (rolls-failure_count)/rolls
    print(f"playing these numbers {players_numbers}")
    print(f"{failure_count} out of {rolls} rolls resulted in failure. ({success_percent*100:.2f}% success rate)")

    cur_percent = success_percent
    for attempt in range(1, 8):
        print(f"Going for {attempt} attempt(s) would carry a {cur_percent*100:.2f}% success rate")
        cur_percent = success_percent * cur_percent


def run(players_numbers):
    procs = 8
    count = 1_000_000
    with Pool(processes=procs) as pool:
        jobs = []
        for num in range(procs):
            job = pool.apply_async(do_multiple_rolls, (players_numbers, count // procs))
            jobs.append(job)
        ttl_rolls = 0
        ttl_failures = 0
        for j in jobs:
            rolls, failures = j.get()
            ttl_rolls += rolls
            ttl_failures += failures
    print_summary(players_numbers, ttl_rolls, ttl_failures)


if __name__ == '__main__':
    while True:
        print()
        resp = input("Enter the numbers, separated by spaces, that have game pieces on them (enter nothing to exit): ")
        if len(resp.strip()) == 0:
            break
        tokens = resp.split()
        set_of_player_nums = {int(n) for n in tokens}
        run(set_of_player_nums)
