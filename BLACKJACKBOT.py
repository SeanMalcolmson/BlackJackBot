#################### BLACK JACK BOT
from random import shuffle

class Deck:
	def __init__(self):
		self.cards = []
		suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
		values = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']

		for suit in suits:
			for card in values:
				self.cards.append((card,suit))

	def shuffle(self): ## shuffles the deck with "deckName.shuffle()""
		return shuffle(self.cards)

def deal(deck, num_of_cards): ## taks a deckname.cards and deals out the specificed number of cards 
	cards = []
	for i in xrange(num_of_cards):
		cards.append(deck.pop())
		i-=1
	return cards
#### move options ####
def hit(player,deck):
	player.hand += deal(deck,1)
## stay and double located in do_move

def bust(player): ## takes a player and returns true of they have busted 
	if point_value(player.hand) > 21:
		return True
	else:
		return False 

DealerDict ={2:0,3:1,4:2,5:3,6:4,7:5,8:6,9:7,'King':8,'Queen':8,'Jack':8,10:8,'Ace':9} ## note that king queen jack and 10 keys point to the same column as they all are valued 10 points 

PlayerDict ={21:0,20:0,19:0,18:0,17:0,16:1,15:2,14:3,13:4,12:5,11:6,10:7,9:8,8:9,7:10,6:11,5:12, ## note that 17-21 points will fallow same strat box to save evolution time
 'soft 21':13, 'soft 20':14, 'soft 19':15, 'soft 18':16, 'soft 17':17,'soft 16':18,'soft 15':19, 'soft 14':20, 'soft 13':21,
 ('Ace','Ace'):22,('King','King'):23,('Queen','Queen'):23,('Jack','Jack'):23,(10,10):23,(9,9):24,(8,8):25,(7,7):26,(6,6):27,(5,5):28,(4,4):29,(3,3):30,(2,2):31} ## (10,10) could be 10 card or 1 of jack king queen 


## create a 32 x 10 array
import random

class StratagyTable:
	def __init__(self):
		self.grid = []
		self.fitness = 0 ## this will be used to find most successfull stratagy
		typesOfMoves = ['Hit','Stay','Double']  ## excluding Split move to simplify code 
		for i in range(32): 
			row = []
			for j in range(10):
				row.append(random.choice(typesOfMoves))

			self.grid.append(row)
	def get_move(self,playerHand,dealerHand):
		## player shouldnt be able to hit again if they have doubled or decided to stay 
		## otherwise they may continue to hit while under 21 
		if point_value(playerHand) > 21:  
			return "Bust"

		playerCards = convert_format(playerHand) 
		dealer1stCard = dealerHand[0][0]
		
		rowNum = PlayerDict[playerCards]
		colNum = DealerDict[dealer1stCard]
		return self.grid[rowNum][colNum]

def hard_ace_count(hand): ## returns what the value of the hand would be with hard aces(1 point each)
	points = 0
	for cards in hand:
		if type(cards[0]) == int:
			points+=cards[0]
		elif cards[0] in ['Jack','Queen','King']:
			points+=10
		else: ## values hard aces at 1
			points +=1
	return points

def convert_format(hand): ## convits the format of the hand to somthing that the table/dict can use
	## check for double hands eg. (10,10)
	if len(hand) ==2 and hand[0][0] == hand[1][0]:
		return (hand[0][0],hand[1][0])

	## below check for soft vs hard hands
	elif point_value(hand) > hard_ace_count(hand):
		return "soft "+str(point_value(hand))
	else:
		return point_value(hand)

def print_array(array):
	rowNum = 0
	for rows in array:
		print str(rowNum)+": " + str(rows)
		rowNum+=1

def print_array_clean(array): ## a nicer format for the strat tables 
	print "-"*50+"Dealer Card Up" +'-'*50
	LAYOUT = "{!s:15} {!s:8} {!s:8} {!s:8} {!s:8} {!s:8} {!s:8} {!s:8} {!s:8} {!s:20} {!s:10}"
	print LAYOUT.format(' ',2,3,4,5,6,7,8,9,"10/Jack/Queen/King","Ace")
	columnheadings = ["Hard 17+ ","Hard 16","Hard 15","Hard 14","Hard 13","Hard 12","Hard 11","Hard 10","Hard 9","Hard 8","Hard 7","Hard 6","Hard 5",
	"Soft 21","Soft 20","Soft 19","Soft 18","Soft 17","Soft 16","Soft 15","Soft 14","Soft 13",
	"Ace, Ace","10 value pairs","9,9","8,8",'7,7',"6,6","5,5","4,4","3,3","2,2"]
	rowcount = 0
	for rows in array:
		print LAYOUT.format(columnheadings[rowcount],rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9])
		rowcount+=1

class Player(object):
	def __init__(self, name = 'BOT', hand = None, money = 0):
		self.name = name
		self.money = money
		self.hand = hand
		self.canHit = True
		self.betAmount = 5

def has_ace(hand): ## takes a hand of card and check if there is an ace in it
	has = False
	for cards in hand:
		if cards[0] == 'Ace':
			has = True
	return has

def point_value(hand):## Give it hand and it returns the point value of the hand 
	points = 0
	for cards in hand:
		if type(cards[0]) == int:
			points+=cards[0]
		elif cards[0] in ['Jack','Queen','King']:
			points+=10
		else: ## if there is an ace first assume to give the player the higher value (11)
			points +=11
	if points > 21 and has_ace(hand): ## but if by taking the higher value of the ace(11) it would cause a bust value ace at 1 
		aceCount = 0
		for cards in hand: ## added this to account for hands with multiple aces 
			if cards[0] == 'Ace':
				aceCount+=1
		while points > 21 and aceCount>=1:
			aceCount -= 1
			points -= 10
	return points


def who_winsV2(dealer,player):
	if point_value(player.hand) == 21: ## hitting blackjack has a payout of 3/2 * bet
		player.money += (3/2.0)*player.betAmount
		return player.name
	elif bust(player):
		player.money -=player.betAmount
		return dealer.name
	elif bust(dealer):
		player.money += player.betAmount
		return player.name
	elif point_value(dealer.hand) > point_value(player.hand):
		player.money -=player.betAmount
		return dealer.name
	elif point_value(dealer.hand) == point_value(player.hand):
		return "Tie Game"
	else:
		player.money +=player.betAmount
		return player.name


## Initialising single random Stratagy table and printing it out
"""
test = StratagyTable()
print "-"*25 + "StratagyTable" + "-"*25
print_array(test.grid)
print "-"*50
"""
def do_move(player,move,deck): ## little fuciton to perform the move read from the table 
	################ UN-Comment prints statemet to see whats going on ###############@
	if move == 'Stay':
		player.canHit = False
		##print 'Staying'
	elif move == 'Hit':
		hit(player,deck.cards)
		##print "hitting"

	elif move == 'Double': ## double
		hit(player,deck.cards)
		player.canHit = False 
		player.betAmount *=2
		##print "doubling"
	else:
		##print "busted"
		player.canHit = False

def play_using_strat(stratagytable, NumberOfTestingHands):  ## takes the random statatgy grid and number of hands you want to test with it 
	################ UN-Comment prints statemet to see whats going on ###############@
	dealer = Player()
	dealer.name = 'Dealer'

	player2 = Player()
	player2.name = 'player2'
	player2.money = 1000
	freshDeck = Deck()
	freshDeck.shuffle()

	numOfHandsPlayed = 0
	while numOfHandsPlayed < NumberOfTestingHands:
		numOfHandsPlayed+=1
		if len(freshDeck.cards) < 12:
			new = Deck()
			new.shuffle()
			freshDeck.cards += new.cards

		dealer.hand = deal(freshDeck.cards,2)
		player2.hand = deal(freshDeck.cards,2)
		player2.canHit = True
		player2.betAmount = 5
		##print "Dealer start hand:" + str(dealer.hand)
		##print "player2 start hand:" + str(player2.hand)
		##print "The Player should "+ str(stratagytable.get_move(player2.hand,dealer.hand))
		do_move(player2,stratagytable.get_move(player2.hand,dealer.hand),freshDeck)
		while player2.canHit == True:
			##print "do another move"
			do_move(player2,stratagytable.get_move(player2.hand,dealer.hand),freshDeck)
		while point_value(dealer.hand) < 17:
			hit(dealer,freshDeck.cards)
		##print "Dealer end hand:" + str(dealer.hand) + "its point value is:" + str(point_value(dealer.hand))
		##print "player2 end hand:" + str(player2.hand) + "its point value is:" + str(point_value(player2.hand))
		##print "the winner is: " +who_winsV2(dealer,player2)  ## need a new who_wins fuciton 
		who_winsV2(dealer,player2) ## Comment out this if you uncomment the above line
	##print "player 2 has this much money: " + str(player2.money)
	stratagytable.fitness = player2.money
	#print "the fitness of this player statatgy is: " + str(stratagytable.fitness) 

def play_using_stratPRINTABLE(stratagytable, NumberOfTestingHands):  ##  Just a printable version of the play testing fuction
	dealer = Player()
	dealer.name = 'Dealer'
	player2 = Player()
	player2.name = 'player2'
	player2.money = 1000
	freshDeck = Deck()
	freshDeck.shuffle()

	numOfHandsPlayed = 0
	while numOfHandsPlayed < NumberOfTestingHands:
		numOfHandsPlayed+=1
		if len(freshDeck.cards) < 12:
			new = Deck()
			new.shuffle()
			freshDeck.cards += new.cards

		dealer.hand = deal(freshDeck.cards,2)
		player2.hand = deal(freshDeck.cards,2)
		player2.canHit = True
		player2.betAmount = 5
		print "Dealer start hand:" + str(dealer.hand)
		print "player2 start hand:" + str(player2.hand)
		print "The Player should "+ str(stratagytable.get_move(player2.hand,dealer.hand))
		do_move(player2,stratagytable.get_move(player2.hand,dealer.hand),freshDeck)
		while player2.canHit == True:
			print "do another move"
			do_move(player2,stratagytable.get_move(player2.hand,dealer.hand),freshDeck)
		while point_value(dealer.hand) < 17:
			hit(dealer,freshDeck.cards)
		print "Dealer end hand:" + str(dealer.hand) + "its point value is:" + str(point_value(dealer.hand))
		print "player2 end hand:" + str(player2.hand) + "its point value is:" + str(point_value(player2.hand))
		print "the winner is: " +who_winsV2(dealer,player2)  ## need a new who_wins fuciton 
		##who_winsV2(dealer,player2) ## Comment out this if you uncomment the above line
	print "player 2 has this much money: " + str(player2.money)
	stratagytable.fitness = player2.money
	print "the fitness of this player statatgy is: " + str(stratagytable.fitness) 


print "-"*50 +'Example of Play Testing Random Table' + '-'*50 ### this is just to show you what is happening durring play testing
testStrat = StratagyTable()
play_using_stratPRINTABLE(testStrat,10)
print " "
print "-"*50 +'Example of a Random Strategy Table' + '-'*50 
print_array_clean(testStrat.grid)

def create_base_poputation(size):
	basePopulationStrats = []
	basePopSize = size
	while basePopSize > 0:
		new = StratagyTable()
		basePopulationStrats.append(new)
		##print_array(new.grid)
		play_using_strat(new,1000) ## test each strat with 1000 hands 
		basePopSize -=1
	return basePopulationStrats


workingPopulation = [] ## this will be a list contaiging the current populations of stratagy tables
## the list will be ammended as better stratagyies are found 
print "_"*50 + "Base Population Statagys" + '_'*50
workingPopulation+=create_base_poputation(100)

workingPopulation = sorted(workingPopulation, key=lambda StratagyTable: StratagyTable.fitness)
print "Sorted base pop" * 3
for strats in workingPopulation:
	##print '_' *100
	##print_array(strats.grid) ## uncomment this if you want to see the actual statagy tables 
	print "the fitness of this player statatgy is: " + str(strats.fitness)


def get_top_50(workingPop): 
	workingPop = sorted(workingPop, key=lambda StratagyTable: StratagyTable.fitness) ## sorts it in order of fittest first before slicing the list 
	tempList = workingPop[len(workingPop)/2:]
	return tempList



import copy

def mutate(stratagytable): ### Used by 'crossOver' fuction 
	chanceToMutate = 10 ## % chance of each element mutatating 
	typesOfMoves = ['Hit','Stay','Double']  ## excluding Split move to simplify code
	for row in range(32): 
			for col in range(10):
				if random.randint(0,100) < chanceToMutate:
					stratagytable.grid[row][col] = random.choice(typesOfMoves)
	return stratagytable

"""
print '-'*50 + 'mutate test' +'-'*50
testinMutate = mutate(best)
print_array(testinMutate.grid)
"""
def crossOver(table1,table2): ## Crosses overs to stratagies you give it ALSO mutates 
	rowNums = range(32)
	shuffle(rowNums)
	RandomRows = rowNums[:16]
	newStrat = copy.deepcopy(table1)
	for row in RandomRows:
		newStrat.grid[row] = table2.grid[row][:]
	return mutate(newStrat)
"""
testCrossOver = crossOver(best,testinMutate)
print '-'*50 + 'crossOver test' +'-'*50
print_array(testCrossOver.grid)

"""
def create_addtional_mutated50(workingpop50):
	newList =[]
	numToAdd = 50
	while numToAdd > 0:
		random2 = random.sample(workingpop50,2)
		newStrat = crossOver(random2[0],random2[1])
		play_using_strat(newStrat,1000)
		newList.append(newStrat)
		numToAdd-=1
	newList = sorted(newList, key=lambda StratagyTable: StratagyTable.fitness)
	return newList

##print 'new mutated 50' *5 
##for strats in create_addtional_mutated50(workingPopulation):
	#print "the fitness of this player statatgy is: " + str(strats.fitness)

def genetic_algorithem(numberOfGenerations,workingPopulation):
	while numberOfGenerations > 0:
		workingPopulation = get_top_50(workingPopulation)
		workingPopulation += create_addtional_mutated50(workingPopulation)
		workingPopulation = sorted(workingPopulation, key=lambda StratagyTable: StratagyTable.fitness)
		numberOfGenerations-=1
	return workingPopulation





print "-"*50 +'genetic_algorithem' + '-'*50
workingPopulation = genetic_algorithem(100,workingPopulation)
for strats in workingPopulation:
	print "the fitness of this player statatgy is: " + str(strats.fitness)
print " "
print "The Best Result in 10 Generations was :" +str(workingPopulation[-1].fitness)
print "-"*50 +'Best StratagyTable' + '-'*50
print_array_clean(workingPopulation[-1].grid)

print " "
play_using_strat(workingPopulation[-1],1000)
print "After retesting the final stratagy with another 1000 hands its success is: " + str(workingPopulation[-1].fitness)
print "Player retains "+ str(((workingPopulation[-1].fitness) / 1000.0 )*100) + "% of their money"