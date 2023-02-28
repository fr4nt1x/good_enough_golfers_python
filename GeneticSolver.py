import random
import itertools
import math


class GeneticSolver:
    GENERATIONS = 30
    INITIAL_POPULATION = 5
    RANDOM_MUTATIONS = 2
    MAX_DESCENDANTS_TO_EXPLORE = 100
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
        self.weights = [[0 for i in range(
            0, self.totalPeople)] for j in range(0, self.totalPeople)]

    def scoreGroups(self, groups):
        groupScores = []
        for group in groups:
            groupScore = sum([int(math.pow(self.weights[pair[0]][pair[1]], 2))
                              for pair in itertools.combinations(group, 2)])
            # groupScore = max([int(self.weights[pair[0]][pair[1]])
            #                   for pair in itertools.combinations(group, 2)])
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
            groupsOnly = [group[0] for group in groupsZippedSorted]
            for personIndex in range(0, self.sizeOfGroups):
                for swapGroupIndex in range(1, self.numberOfGroups):
                    for swapPersonIndex in range(0, self.sizeOfGroups):
                        groupsOnlyCopy = list(groupsOnly)

                        group1 = groupsOnly[0]
                        group2 = groupsOnly[swapGroupIndex]
                        newGroup1 = list(group1)
                        newGroup1[personIndex] = group2[swapPersonIndex]
                        newGroup2 = list(group2)
                        newGroup2[swapPersonIndex] = group1[personIndex]

                        groupsOnlyCopy[0] = tuple(newGroup1)
                        groupsOnlyCopy[swapGroupIndex] = tuple(newGroup2)

                        # groupsOnlyCopy[0][personIndex] = groupsOnly[swapGroupIndex][swapPersonIndex]
                        # groupsOnlyCopy[swapGroupIndex][swapPersonIndex] = groupsOnly[0][personIndex]
                        groupScores = self.scoreGroups(groupsOnlyCopy)
                        totalScore = sum(groupScores)
                        mutatedOptions.append(
                            {self.OPTIONS_GROUPS: groupsOnlyCopy, self.OPTIONS_GROUPSCORES: groupScores, self.OPTIONS_TOTALSCORE: totalScore})
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
            print("round: ", round)
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
