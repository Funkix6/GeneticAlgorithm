#Algorithme génétique - Projet du cours d'IA
#Programmé par : Lucas Briot FA 22 Spé. INFO (Travail effectué seul)
#Dernière MAJ le 14-01-2021

from typing import List
from random import choices, randint
import time

Genome = List[int]
Population = List[Genome]
functions = []
unfitness = []
fitness = []
IOmax : int = 32
theChildChosen = []
mask = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pA: int = 0
pB: int = 0
StopBoucle: int = 0

#Création de l'objet fonction posédant toutes les caractéristiques de ces dernières
class Function:
    def __init__(
        self,
        number: int,
        sf: int,
        loIn: int,
        anIn: int,
        loOut: int,
        anOut: int, 
    ):

        self.number = number
        self.sf = sf
        self.loIn = loIn
        self.anIn = anIn
        self.loOut = loOut
        self.anOut = anOut

#Initialisation du Fitness a 0
def InitializeFitness(population: Population):
    for _ in range(len(population)):
        fitness.append(0)
        unfitness.append(0)

#Initialisation des functions, devrait être fait via fichier mais pour le moment non
def InitializeFunctions(_functions: functions) -> functions:
    functions.append(Function(1, 1, 3, 6, 8, 4))
    functions.append(Function(2, 1, 7, 8, 4, 3))
    functions.append(Function(3, 1, 1, 8, 5, 1))
    functions.append(Function(4, 1, 6, 8, 5, 7))
    functions.append(Function(5, 1, 9, 3, 7, 8))
    functions.append(Function(6, 2, 5, 4, 7, 0))
    functions.append(Function(7, 2, 3, 0, 9, 2))
    functions.append(Function(8, 2, 7, 2, 7, 1))
    functions.append(Function(9, 2, 0, 9, 5, 6))
    functions.append(Function(10, 2, 0, 9, 2, 1))
    functions.append(Function(11, 3, 4, 0, 1, 5))
    functions.append(Function(12, 3, 6, 3, 4, 6))
    functions.append(Function(13, 3, 4, 0, 1, 9))
    functions.append(Function(14, 3, 4, 7, 2, 3))
    functions.append(Function(15, 3, 5, 1, 9, 7))
    functions.append(Function(16, 4, 8, 6, 6, 9))
    functions.append(Function(17, 4, 6, 4, 3, 4))
    functions.append(Function(18, 4, 9, 7, 8, 7))
    functions.append(Function(19, 4, 3, 7, 5, 6))
    functions.append(Function(20, 4, 6, 9, 0, 1))
    
    return _functions

#Génération d'un genome respectant les contraintes de SF et CL (Criticité)
def generate_genome(length : int) -> Genome:
    TempList = []
    
    for _ in range(0, int(length * 0.25)):
        TempList.append(randint(1, 7))

    for _ in range(int(length * 0.25) , int(length * 0.5)):
        TempList.append(randint(8, 14))
    
    for _ in range(int(length * 0.5), int(length * 0.75)):
        TempList.append(randint(8, 20))

    for _ in range(int(length * 0.75), length):
        TempList.append(randint(15, 20))    
    return TempList

#Génération de la population
def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

#Teste pour savoir s'il y a des doublons dans les gênes retourne un Booleen
def test_same_genes(population: Population) -> bool:
    check : bool = False
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            if population[i] == population[j]:
                check = True
    return check

#Teste du fitness. Calcule le nombre de controlleurs différents
def test_fitness(population: Population) -> int:    
    for i in range(len(population)):
        fitness[i] = len(set(population[i]))

#Teste la contrainte de capacité et augmente l'Unfitness des solutions si nécessaire. (Utilise test_inputOutputSingle)
def test_inputOutput(population: Population, _functions: functions):
    global IOmax
    for i in range(len(population)):
        test_inputOutputSingle(population[i], _functions)

#Teste la contrainte de capacité pour un genome
def test_inputOutputSingle(genome, _functions: functions) -> int:    
    global IOmax
    global showDebug_advanded
    childUnfitness: int
    childUnfitness = 0
    for i in range(len(genome) + 1):
        tmpLi = 0
        tmpAi = 0
        tmpLo = 0
        tmpAo = 0
        for n, j in enumerate(genome):
            if(j == i):
                tmpLi += _functions[n].loIn
                tmpAi += _functions[n].anIn
                tmpLo += _functions[n].loOut
                tmpAo += _functions[n].anOut
        childUnfitness += max(0, tmpLi - IOmax)
        childUnfitness += max(0, tmpAi - IOmax)
        childUnfitness += max(0, tmpLo - IOmax)
        childUnfitness += max(0, tmpAo - IOmax)
        if(showDebug_advanded == True):
            print("Genome :", genome)
            print("test : ", i, "Logic Input     :", tmpLi)
            print("test : ", i, "Analogic Input  :", tmpAi)
            print("test : ", i, "Logic Output    :", tmpLo)
            print("test : ", i, "Analogic Output :", tmpAo)
            print("Unfitness :", childUnfitness)
            print(" ")
    return childUnfitness

#Teste la contrainte d'exclusion (Ecrit en dur mais possiblement modifiable)
def test_exclusion(population: Population):
    for i in range(len(population)):
        if(population[i][6 - 1] == population[i][11 - 1]):
            unfitness[i] += 1
        if(population[i][8 - 1] == population[i][14 - 1]):
            unfitness[i] += 1
        if(population[i][13 - 1] == population[i][16 - 1]):
            unfitness[i] += 1
        if(population[i][9 - 1] == population[i][12 - 1]):
            unfitness[i] += 1
        if(population[i][15 - 1] == population[i][20 - 1]):
            unfitness[i] += 1
        if(population[i][7 - 1] == population[i][14 - 1]):
            unfitness[i] += 1
        if(population[i][11 - 1] == population[i][18 - 1]):
            unfitness[i] += 1
        if(population[i][13 - 1] == population[i][17 - 1]):
            unfitness[i] += 1
        if(population[i][8 - 1] == population[i][15 - 1]):
            unfitness[i] += 1
        if(population[i][12 - 1] == population[i][19 - 1]):
            unfitness[i] += 1

#Teste la contrainte d'exclusion pour un genome
def test_exclusionSingle(genome: Genome) -> int:
    childUnfitness = 0
    if(genome[6 - 1] == genome[11 - 1]):
        childUnfitness += 1
    if(genome[8 - 1] == genome[14 - 1]):
        childUnfitness += 1
    if(genome[13 - 1] == genome[16 - 1]):
        childUnfitness += 1
    if(genome[9 - 1] == genome[12 - 1]):
        childUnfitness += 1
    if(genome[15 - 1] == genome[20 - 1]):
        childUnfitness += 1
    if(genome[7 - 1] == genome[14 - 1]):
        childUnfitness += 1
    if(genome[11 - 1] == genome[18 - 1]):
        childUnfitness += 1
    if(genome[13 - 1] == genome[17 - 1]):
        childUnfitness += 1
    if(genome[8 - 1] == genome[15 - 1]):
        childUnfitness += 1
    if(genome[12 - 1] == genome[19 - 1]):
        childUnfitness += 1
    return childUnfitness

#Permet de sortir un nombre aléatoire dans la population
def pickRndParent(population : Population) -> int:
    rndNumber: int
    rndNumber = randint(0, generatedPopulation - 1)
    return rndNumber  

#Permet de choisir le parent avec le meileur (Plus bas) Fitness
def chooseParent(parentA, parentB) -> int:
    global pA
    global pB
    if(fitness[parentA] < fitness[parentB]):
        return parentA
    else:
        return parentB

#Génère un Mask binaire de la taille des genomes
def GenerateBinaryMask(length: int):   
    for i in range(length):
        mask[i] = randint(0, 1)  
    return mask

#Réinitialise(et initialise) le génome enfant avec des 0
def resetChild():
    theChildChosen.clear
    for i in range(20):
        theChildChosen.append(0)

#Utilise le Mask pour générer l'enfant depuis les deux parents
def TheChild(mask) -> Genome:
    global pA
    global pB
    for i in range(len(mask)):
        if(mask[i] == 0):
            theChildChosen[i] = Population[pA][i]
        else:
            theChildChosen[i] = Population[pB][i]
    return theChildChosen

#Effectue une mutation sur un gêne aléatoire respectant la contrainte d'exclusion
def RandomMutation(child: Genome) -> Genome:
    while(True):
        tmpRnd = randint(0, 19)
        tmpOld = child[tmpRnd]
        if(tmpRnd <= (5 - 1)):
            child[tmpRnd] = randint(1, 7)
        if(tmpRnd > (5 - 1) and tmpRnd <= (10 - 1)):
            child[tmpRnd] = randint(8, 14)
        if(tmpRnd > (10 - 1) and tmpRnd <= (15 - 1)):
            child[tmpRnd] = randint(8, 20)
        if(tmpRnd > (15 - 1) and tmpRnd <= (20 - 1)):
            child[tmpRnd] = randint(15, 20)
        if(child[tmpRnd] != tmpOld):
            return child

#Cherche le unfitness Maximum
def Umax()-> int:
    uMaxValue: int = 0
    for i in range(len(unfitness)):
        if(unfitness[i] > uMaxValue):
            uMaxValue = unfitness[i]
    return uMaxValue

#Cherche l'index de l'unfitness Maximum
def UmaxPos() -> int:
    uMaxPos: int = 0
    for i in range(len(unfitness)):
        if(unfitness[i] == Umax()):
            uMaxPos = i
    
    return uMaxPos

#Cherche le fitness maximum
def fMax()-> int:
    fMaxValue: int = 0
    for i in range(len(fitness)):
        if(fitness[i] > fMaxValue):
            fMaxValue = fitness[i]   
    return fMaxValue

#Cherche l'index de l'unfitness maximum
def FmaxPos() -> int:
    fMaxPos: int = 0
    for i in range(len(fitness)):
        if(fitness[i] == fMax()):
            fMaxPos = i
    return fMaxPos

#Reset l'unfitness de la population et le met à 0 
def resetUnfitness():
    for i in range(len(unfitness)):
        unfitness[i] = 0
    return unfitness

#Teste le fitness du genome selectionné
def test_childFitness(child: Genome) -> int:
    return len(set(child))

#Selectionne les deux parents 
def SelectionDesParents():
    global pA
    global pB

    while(True):
        pA = chooseParent(pickRndParent(Population), pickRndParent(Population))
        pB = chooseParent(pickRndParent(Population), pickRndParent(Population))
        if(pA != pB):
            break

#Effectue l'accouplement des deux parents
def Breeding(maskLength, mask) -> Genome:
    mask = GenerateBinaryMask(maskLength)
    return TheChild(mask)

#Retourne l'enfant muté
def Mutation() -> Genome: 
    return RandomMutation(theChildChosen)

#Remplace un élément faible de la population actuelle par l'enfant muté améliorant la qualité générale de la population
def InsertInPopulation(child, childFitness, childUnfitness, population):
    global StopBoucle
    if(child in population):  
        return
    if(childUnfitness > Umax()):
        return
    if(childUnfitness <= Umax() and childUnfitness > 0):
        population[UmaxPos()] = list(child) #JE ME SUIS ARRÊTE A CA 
        unfitness[UmaxPos()] = childUnfitness
        StopBoucle += 1
    if(childUnfitness == 0):
        if(childFitness > fMax()):
            return
        else:
            if(checkIfExists(child)):
                return
            population[FmaxPos()] = list(child)
            StopBoucle += 1

#Teste l'unfitness d'un genome
def childUnfitness(child) -> int:
    return (test_exclusionSingle(child) + test_inputOutputSingle(child, functions))

#Permet d'afficher la population actuelle
def printPopulation():
    for _ in range(len(Population)):       
        print("Population n°: ",str(_).zfill(2), Population[_], "   ||   Fitness : ", fitness[_], "   ||   Unfitness : ", unfitness[_])
        print(" ")

#PErmet de mettre à jours l'unfitness de la population
def UpdateUnfitness():
    resetUnfitness()
    test_inputOutput(Population, functions)
    test_exclusion(Population)

#Fait une vérification de l'éxistence d'un génome dans la population 
def checkIfExists(child) -> bool:
    tmp: bool = False
    for i in range(len(Population)):
        if(Population[i] == child):
            tmp = True
    return tmp



#-------------Public Variables------------------------------------------------------
generatedPopulation = 50        #Modify to change the number of population generated
showDebug_advanded = False      #Activate to see advanced Debug
numberOfGenomes = 20            #Do not Change
showDebug = False               #Change to see Debug
StopCondition = 1000            #Change up or down to change the number of changes
#-----------------------------------------------------------------------------------

#Chronomètre début
start = time.time()

functions = InitializeFunctions(functions)

#Boucle pour éviter les doublons dans la population initiale
while(True):
    Population = generate_population(generatedPopulation, numberOfGenomes)
    if test_same_genes(Population) == False:
        break

InitializeFitness(Population)

test_fitness(Population)

UpdateUnfitness()

print("Population Initiale")
print(" ")
printPopulation()

resetChild()
cpt: int = 0
while(True):
    cpt += 1
    SelectionDesParents()
    if(showDebug == True):
        print("Parent A: ", pA, Population[pA])
        print("Parent B: ", pB, Population[pB])
        print(" ")
    theChildChosen = Breeding(numberOfGenomes, mask)
    if(showDebug == True):
        print("Mask : ", mask)
        print(" ")
        print("Child Before Mutation : ", theChildChosen)
    theChildChosen = Mutation()
    if(showDebug == True):
        print("Child After Mutation : ", theChildChosen)
        print(" ")
        print(" ")
    InsertInPopulation(theChildChosen, test_childFitness(theChildChosen), childUnfitness(theChildChosen), Population)
    UpdateUnfitness()
    test_fitness(Population)
    if(StopBoucle == StopCondition):
        break

print("New population")
print(" ")
printPopulation()
print("Nombre d'itérations :", cpt)

#Chronomètre fin
end = time.time()
print("Time = ", end - start)