# Simulating percentages of a Risk-like dice roll competition

import sys
import random


        
class cPlayer:
    def __init__(self, startArmies, preferredDiceToRoll):
        #print "cPlayer.init"
        #cPlayerStats.__init__(self)
        self.armiesStart = startArmies
        self.armiesCur = self.armiesStart
        self.preferredDiceToRoll = preferredDiceToRoll
        self.lastRoll = [] 
        self.battlesPlayed = 0
        self.battlesWon = 0
        self.totalArmiesRemaining = 0
        self.maxArmiesRemaining = 0
        self.minArmiesRemaining = self.armiesStart
        self.armiesKilled = 0
        
    def canContinue(self):
        print("cPlayer.canContinue()")

    def roll(self):
        self.lastRoll = []
        numToRoll = self.numDiceToRoll()
        self.lastRoll = [random.randint(1, 6) for x in range(numToRoll)]        
        self.lastRoll.sort()
        self.lastRoll.reverse()
        
    def resolveRolls(self, defender):
        diceMatches = min(len(self.lastRoll), len(defender.lastRoll))
        for i in range(diceMatches):
            if (defender.lastRoll[i] >= self.lastRoll[i]):
                self.armiesCur -= 1
            else:
                defender.armiesCur -= 1
              
##    def printStats(self, msg):
##        print msg
##        print self.lastRoll,
##        print self.armiesCur

    def reset(self):
        self.lastRoll = []
        self.armiesCur = self.armiesStart

    def resetStats(self):
        self.battlesPlayed = 0
        self.battlesWon = 0
        self.totalArmiesRemaining = 0
        self.maxArmiesRemaining = 0
        self.minArmiesRemaining = self.armiesStart
        self.armiesKilled = 0
#    def canContinue():       



class cAttacker(cPlayer):
    def canContinue(self):
        #print "cAttacker.canContinue()"
        return (self.armiesCur > 1)

    def numDiceToRoll(self):
        if (self.armiesCur > self.preferredDiceToRoll):
            return self.preferredDiceToRoll
        else:
            return (self.armiesCur - 1)

    
class cDefender(cPlayer):
    def canContinue(self):
        #print "cDefender.canContinue()"
        return (self.armiesCur > 0)

    def numDiceToRoll(self):
        if (self.armiesCur >= self.preferredDiceToRoll):
            return self.preferredDiceToRoll
        else:
            return self.armiesCur


# a mock C "struct"
class playerSpecs:
    armies = 0
    dice = 0
    
    
def runSimulation(attValues, defValues, numberOfBattles, offset):
    print()
    totalRolls = 0
    minRollsInBattle = 10000000
    maxRollsInBattle = 0
    attacker.armiesStart = attValues.armies
    attacker.preferredDiceToRoll = attValues.dice
    defender.armiesStart = defValues.armies + offset
    defender.preferredDiceToRoll = defValues.dice
    attacker.resetStats()
    defender.resetStats()
    print("Starting armies\t\tDesired dice")
    print("Att: ", attacker.armiesStart, "\t\t", attacker.preferredDiceToRoll)
    print("Def: ", defender.armiesStart, "\t\t", defender.preferredDiceToRoll)
    for bat in range(numberOfBattles):
        attacker.reset()
        defender.reset()
        #print attacker.armiesCur, defender.armiesCur
        roll = 0
        while (attacker.canContinue() and defender.canContinue()):
            roll += 1
            #print "-------#", roll
            attacker.roll()
            defender.roll()
            #print attacker.lastRoll
            #print defender.lastRoll
            attacker.resolveRolls(defender)
            #print attacker.armiesCur, defender.armiesCur
            #print attacker.canContinue(), defender.canContinue()
        totalRolls += roll
        minRollsInBattle = min(minRollsInBattle, roll)
        maxRollsInBattle = max(maxRollsInBattle, roll)
        attacker.battlesPlayed += 1
        defender.battlesPlayed += 1
        attacker.armiesKilled += defender.armiesStart - defender.armiesCur
        defender.armiesKilled += attacker.armiesStart - attacker.armiesCur
        if attacker.canContinue():
            attacker.battlesWon += 1
            #print "ATTACKER!"
        if defender.canContinue():
            defender.battlesWon += 1
            #print "DEFENDER!"
        attacker.maxArmiesRemaining = max(attacker.maxArmiesRemaining, attacker.armiesCur)
        attacker.minArmiesRemaining = min(attacker.minArmiesRemaining, attacker.armiesCur)
        defender.maxArmiesRemaining = max(defender.maxArmiesRemaining, defender.armiesCur)
        defender.minArmiesRemaining = min(defender.minArmiesRemaining, defender.armiesCur)
        
        attacker.totalArmiesRemaining += attacker.armiesCur
        defender.totalArmiesRemaining += defender.armiesCur
        #print attacker.armiesCur, defender.armiesCur
        
    print(attacker.battlesWon, "/", defender.battlesWon, " out of ", defender.battlesPlayed, "battles")
    print("Attacker won", float(attacker.battlesWon) / attacker.battlesPlayed * 100, "%")
    print("min/avg/max rolls:", minRollsInBattle, float(totalRolls) / numberOfBattles, maxRollsInBattle)
    print("min/avg/max armies remaining att:", attacker.minArmiesRemaining, float(attacker.totalArmiesRemaining) / numberOfBattles, attacker.maxArmiesRemaining)
    print("min/avg/max armies remaining def:", defender.minArmiesRemaining, float(defender.totalArmiesRemaining) / numberOfBattles, defender.maxArmiesRemaining)
    print("attacker kill ratio:", attacker.armiesKilled, "/", defender.armiesKilled, float(attacker.armiesKilled) / defender.armiesKilled)


if __name__ == '__main__':
    attacker = cAttacker(10, 3)
    defender = cDefender(10, 2)

    attack = playerSpecs()
    defend = playerSpecs()
    attack.armies = 100
    attack.dice = 3
    defend.armies = 100
    defend.dice = 2
    numBattles = 100
    for offset in range(-14, 14, 2):
        runSimulation(attack, defend, numBattles, offset)
