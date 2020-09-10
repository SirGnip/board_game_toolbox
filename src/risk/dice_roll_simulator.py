"""Simulating percentages of a Risk-like dice roll competition"""
import random


class Player:
    """Player base class"""
    def __init__(self, start_armies, preferred_dice_to_roll):
        self.armies_start = start_armies
        self.armies_cur = self.armies_start
        self.preferred_dice_to_roll = preferred_dice_to_roll
        self.last_roll = []
        self.battles_played = 0
        self.battles_won = 0
        self.total_armies_remaining = 0
        self.max_armies_remaining = 0
        self.min_armies_remaining = self.armies_start
        self.armies_killed = 0

    def can_continue(self):
        raise NotImplementedError

    def num_dice_to_roll(self):
        raise NotImplementedError

    def roll(self):
        self.last_roll = []
        count_to_roll = self.num_dice_to_roll()
        self.last_roll = [random.randint(1, 6) for _ in range(count_to_roll)]
        self.last_roll.sort()
        self.last_roll.reverse()

    def resolve_rolls(self, defender_player):
        dice_matches = min(len(self.last_roll), len(defender.last_roll))
        for i in range(dice_matches):
            if defender_player.last_roll[i] >= self.last_roll[i]:
                self.armies_cur -= 1
            else:
                defender_player.armies_cur -= 1

    def reset(self):
        self.last_roll = []
        self.armies_cur = self.armies_start

    def reset_stats(self):
        self.battles_played = 0
        self.battles_won = 0
        self.total_armies_remaining = 0
        self.max_armies_remaining = 0
        self.min_armies_remaining = self.armies_start
        self.armies_killed = 0


class Attacker(Player):
    """Player logic for when attacking"""
    def can_continue(self):
        return self.armies_cur > 1

    def num_dice_to_roll(self):
        if self.armies_cur > self.preferred_dice_to_roll:
            return self.preferred_dice_to_roll
        return self.armies_cur - 1


class Defender(Player):
    """Player logic for when defending"""
    def can_continue(self):
        return self.armies_cur > 0

    def num_dice_to_roll(self):
        if self.armies_cur >= self.preferred_dice_to_roll:
            return self.preferred_dice_to_roll
        return self.armies_cur


class PlayerSpecs:
    """Track values for each player"""
    armies = 0
    dice = 0


def run_simulation(att_values, def_values, number_of_battles, defender_armies_offset):
    print()
    total_rolls = 0
    min_rolls_in_battle = 10000000
    max_rolls_in_battle = 0
    attacker.armies_start = att_values.armies
    attacker.preferred_dice_to_roll = att_values.dice
    defender.armies_start = def_values.armies + defender_armies_offset
    defender.preferred_dice_to_roll = def_values.dice
    attacker.reset_stats()
    defender.reset_stats()
    print("Starting armies\t\tDesired dice")
    print("Att: ", attacker.armies_start, "\t\t", attacker.preferred_dice_to_roll)
    print("Def: ", defender.armies_start, "\t\t", defender.preferred_dice_to_roll)
    for _ in range(number_of_battles):
        attacker.reset()
        defender.reset()
        roll = 0
        while attacker.can_continue() and defender.can_continue():
            roll += 1
            attacker.roll()
            defender.roll()
            attacker.resolve_rolls(defender)
        total_rolls += roll
        min_rolls_in_battle = min(min_rolls_in_battle, roll)
        max_rolls_in_battle = max(max_rolls_in_battle, roll)
        attacker.battles_played += 1
        defender.battles_played += 1
        attacker.armies_killed += defender.armies_start - defender.armies_cur
        defender.armies_killed += attacker.armies_start - attacker.armies_cur
        if attacker.can_continue():
            attacker.battles_won += 1
        if defender.can_continue():
            defender.battles_won += 1
        attacker.max_armies_remaining = max(attacker.max_armies_remaining, attacker.armies_cur)
        attacker.min_armies_remaining = min(attacker.min_armies_remaining, attacker.armies_cur)
        defender.max_armies_remaining = max(defender.max_armies_remaining, defender.armies_cur)
        defender.min_armies_remaining = min(defender.min_armies_remaining, defender.armies_cur)

        attacker.total_armies_remaining += attacker.armies_cur
        defender.total_armies_remaining += defender.armies_cur

    print(attacker.battles_won, "/", defender.battles_won, " out of ", defender.battles_played, "battles")
    print("Attacker won", float(attacker.battles_won) / attacker.battles_played * 100, "%")
    print("min/avg/max rolls:", min_rolls_in_battle, float(total_rolls) / number_of_battles, max_rolls_in_battle)
    print("min/avg/max armies remaining att:", attacker.min_armies_remaining, float(attacker.total_armies_remaining) / number_of_battles, attacker.max_armies_remaining)
    print("min/avg/max armies remaining def:", defender.min_armies_remaining, float(defender.total_armies_remaining) / number_of_battles, defender.max_armies_remaining)
    print("attacker kill ratio:", attacker.armies_killed, "/", defender.armies_killed, float(attacker.armies_killed) / defender.armies_killed)


if __name__ == '__main__':
    attacker = Attacker(10, 3)
    defender = Defender(10, 2)

    attack = PlayerSpecs()
    defend = PlayerSpecs()
    attack.armies = 100
    attack.dice = 3
    defend.armies = 100
    defend.dice = 2
    numBattles = 100
    for army_offset in range(-14, 14, 2):
        run_simulation(attack, defend, numBattles, army_offset)
