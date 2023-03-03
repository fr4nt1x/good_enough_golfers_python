import random
import itertools
import math


class GeneticSolver:
    """
    Class for solving the social golfer problem.
    Uses only standard library functions.

    returns a list of dicts.
    each dict contains a key self.OPTIONS_GROUPS and self.OPTIONS_TOTALSCORE.
    self.OPTIONS_GROUPS contains a list containing the groups and
    self.OPTIONS_TOTALSCORE contains the score.

    persons are integers from 0 to sizeOfGroups*numberOfGroups

    """

    # Constants
    GENERATIONS = 30
    INITIAL_POPULATION = 5
    RANDOM_MUTATIONS = 2
    MAX_DESCENDANTS_TO_EXPLORE = 100
    # dict keys used later
    OPTIONS_GROUPS = "groups"
    OPTIONS_GROUPSCORES = "groupScores"
    OPTIONS_TOTALSCORE = "totalScore"

    def __init__(self, numberOfGroups, sizeOfGroups, numberOfRounds):
        self.numberOfGroups = numberOfGroups
        self.sizeOfGroups = sizeOfGroups
        self.numberOfRounds = numberOfRounds
        self.totalPeople = self.numberOfGroups*self.sizeOfGroups
        # use list comprehension the list with different list objects
        # do not use [[0]*self.totalPeople]*self.totalPeople as then the changing one row element
        # will change all rows
        self.weights = [[0 for _ in range(
            0, self.totalPeople)] for _ in range(0, self.totalPeople)]
        self.weightsSquared = [[0 for _ in range(
            0, self.totalPeople)] for _ in range(0, self.totalPeople)]

    def scoreGroups(self, groups):
        groupScores = []
        for group in groups:
            groupScore = sum([int(self.weightsSquared[pair[0]][pair[1]])
                              for pair in itertools.combinations(group, 2)])
            groupScores.append(groupScore
                               )
        return groupScores

    def generatePermutations(self):
        permutation = list(range(0, self.totalPeople))
        random.shuffle(permutation)
        # split into groups
        groups = [0] * self.numberOfGroups

        for groupIndex, _ in enumerate(groups):
            groups[groupIndex] = tuple(permutation[groupIndex *
                                                   self.sizeOfGroups: (groupIndex+1)*self.sizeOfGroups])
        return groups

    def generateRandomOptions(self, numberOfOptions):
        groupOptions = []
        for _ in range(0, numberOfOptions):
            groups = self.generatePermutations()
            groupScores = self.scoreGroups(groups)
            totalScore = sum(groupScores)
            groupOptions.append(
                {self.OPTIONS_GROUPS: groups, self.OPTIONS_GROUPSCORES: groupScores, self.OPTIONS_TOTALSCORE: totalScore})
        return groupOptions

    def updateWeights(self, groups):
        for group in groups:
            for pair in itertools.combinations(group, 2):
                index0 = pair[0]
                index1 = pair[1]
                self.weights[index0][index1] = self.weights[index0][index1]+1
                self.weights[index1][index0] = self.weights[index0][index1]
                squared = int(math.pow(
                    self.weights[index0][index1], 2))
                self.weightsSquared[index0][index1] = squared
                self.weightsSquared[index1][index0] = squared

    def switchGroups(self, group1, group2, personIndex, swapPersonIndex):
        newGroup1 = list(group1)
        newGroup1[personIndex] = group2[swapPersonIndex]
        newGroup2 = list(group2)
        newGroup2[swapPersonIndex] = group1[personIndex]
        return newGroup1, newGroup2

    def scoreMutatedGroup(self, orgGroup, newGroup, oldScore, orgPersonIndex):
        score = oldScore
        for i in range(0, self.sizeOfGroups):
            if i == orgPersonIndex:
                continue
            score += self.weightsSquared[newGroup[orgPersonIndex]][newGroup[i]]

        for i in range(0, self.sizeOfGroups):
            if i == orgPersonIndex:
                continue
            score -= self.weightsSquared[orgGroup[orgPersonIndex]][orgGroup[i]]
        return score

    def generateMutations(self, groupOptions):
        mutatedOptions = []
        for option in groupOptions:
            # add the original option always
            mutatedOptions.append(option)
            # find the group with the highest score
            groupsZipped = list(zip(
                option[self.OPTIONS_GROUPS], option[self.OPTIONS_GROUPSCORES]))
            groupsZippedSorted = sorted(
                groupsZipped, key=lambda t: t[1], reverse=True)
            oldTotal = option[self.OPTIONS_TOTALSCORE]
            groupScores = [zipped[1]
                           for zipped in groupsZippedSorted]
            for personIndex in range(0, self.sizeOfGroups):
                for swapGroupIndex in range(1, self.numberOfGroups):
                    for swapPersonIndex in range(0, self.sizeOfGroups):
                        groupsOnlyCopy = [group[0]
                                          for group in groupsZippedSorted]

                        group1 = groupsZippedSorted[0][0]
                        group2 = groupsZippedSorted[swapGroupIndex][0]
                        newGroup1, newGroup2 = self.switchGroups(
                            group1, group2, personIndex, swapPersonIndex)

                        groupsOnlyCopy[0] = tuple(newGroup1)
                        groupsOnlyCopy[swapGroupIndex] = tuple(newGroup2)

                        groupScoresCopy = groupScores[:]

                        groupScoresCopy[0] = self.scoreMutatedGroup(
                            group1, newGroup1, groupScores[0], personIndex)

                        groupScoresCopy[swapGroupIndex] = self.scoreMutatedGroup(
                            group2, newGroup2, groupScores[swapGroupIndex], swapPersonIndex)
                        totalScore = sum(groupScoresCopy)
                        # Later only all options with the best score will be evaluated
                        # as we know at least one option score we can eliminate everything that
                        # has a worse score
                        if totalScore <= oldTotal:
                            mutatedOptions.append(
                                {self.OPTIONS_GROUPS: groupsOnlyCopy, self.OPTIONS_GROUPSCORES: groupScoresCopy, self.OPTIONS_TOTALSCORE: totalScore})
            # Random mutations for each option
            mutatedOptions = mutatedOptions + (self.generateRandomOptions(
                self.RANDOM_MUTATIONS))
        return mutatedOptions

    def getOptionsWithSpecificValue(self, options, value):
        optionsWithValue = []
        for option in options:
            if option[self.OPTIONS_TOTALSCORE] == value:
                optionsWithValue.append(option)
        return optionsWithValue

    def solve(self):
        rounds = []
        for round in range(0, self.numberOfRounds):
            print("Calculating round: ", round)
            groupOptions = self.generateRandomOptions(self.INITIAL_POPULATION)
            for i in range(0, self.GENERATIONS):
                # print("Generation", i)
                # why only if the first group has a total of 0
                if groupOptions[0][self.OPTIONS_TOTALSCORE] == 0:
                    break
                newMutationOptions = self.generateMutations(groupOptions)
                newMutationOptionsSorted = sorted(
                    newMutationOptions, key=lambda d: d[self.OPTIONS_TOTALSCORE])
                lowestScore = newMutationOptionsSorted[0][self.OPTIONS_TOTALSCORE]

                lowestScoreOptions = self.getOptionsWithSpecificValue(
                    newMutationOptionsSorted, lowestScore)
                # Dont use all descendants
                random.shuffle(lowestScoreOptions)
                groupOptions = lowestScoreOptions[0:
                                                  self.MAX_DESCENDANTS_TO_EXPLORE]
            bestOption = groupOptions[0]
            rounds.append(
                {"groups": bestOption[self.OPTIONS_GROUPS], "roundScore": bestOption[self.OPTIONS_TOTALSCORE]})
            self.updateWeights(bestOption[self.OPTIONS_GROUPS])
        return rounds
