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

def stay(): ## technically stay you dont need to perform an aciton for
	pass
def split():### this will not be implamented 
	pass
def double(): ## double hits you player once and doubles initial bet
	pass       ## can recive no more cards after 


def bust(player): ## takes a player and returns true of they have busted 
	if point_value(player.hand) > 21:
		return True
	else:
		return False 

############################ NEW STUFFF ###############################################
#######################################################################################
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
		####### working on this#######
		## player shouldnt be able to hit again if they have doubled or decided to stay 
		## otherwise they may continue to hit while under 21 
		if point_value(playerHand) > 21: ## testing this part 
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
########################################################### END OF NEW STUFF ########################################################
#####################################################################################################################################
def print_array(array):
	for rows in array:
		print rows

class Player(object):
	def __init__(self, name = 'BOT', hand = None, money = 0):
		self.name = name
		self.money = money
		self.hand = hand
		## maybe add a currentBet variable here for implementing double 
		self.canHit = True
		self.betAmount = 5
		## and a hasdouble or has stayed variable 

class Dealer(object):
	def __init__(self,hand = None):
		self.hand = hand 

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


def who_wins(dealer,player):
	if bust(player):
		player.money -=5
		return dealer.name
	elif bust(dealer):
		player.money += 5
		return player.name
	elif point_value(dealer.hand) > point_value(player.hand):
		player.money -=5
		return dealer.name
	elif point_value(dealer.hand) == point_value(player.hand):
		return "Tie Game"
	else:
		player.money +=5
		return player.name

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


def test2Player(): ## Player vs Dealer both using dealer stratagy 
	dealer =  Player()
	dealer.name = 'Dealer'
	# assuming the dealer has unlimted money
	player2 = Player()
	player2.name = 'Player2'
	player2.money = 100
	freshDeck  = Deck()
	freshDeck.shuffle()
	while len(freshDeck.cards) > 8: ## keep going until the deck has about 8 cards left just in case they might run out mid game 
		dealer.hand = deal(freshDeck.cards,2)
		player2.hand = deal(freshDeck.cards,2)
		print "Dealer start hand:" + str(dealer.hand)
		print "player2 start hand:" + str(player2.hand)
		while point_value(dealer.hand) < 17:
			hit(dealer,freshDeck.cards)
		while point_value(player2.hand) < 17:
			hit(player2,freshDeck.cards)
		print "Dealer end hand:" + str(dealer.hand) + "its point value is:" + str(point_value(dealer.hand))
		print "player2 end hand:" + str(player2.hand) + "its point value is:" + str(point_value(player2.hand))

		print "the winner is: " +who_wins(dealer,player2)
	print "player 2 has this much money: " + str(player2.money)

##test2Player() ## Uncomment this to test 2players using dealer strat testing 

## Initialising single random Stratagy table and printing it out
test = StratagyTable()
print "-"*25 + "StratagyTable" + "-"*25
print_array(test.grid)
print "-"*50

def do_move(player,move,deck): ## little fuciton to perform the move read from the table 
	if move == 'Stay':
		player.canHit = False
		print 'Staying'
	elif move == 'Hit':
		hit(player,deck.cards)
		print "hitting"

	elif move == 'Double': ## double
		hit(player,deck.cards)
		player.canHit = False 
		player.betAmount *=2
		print "doubling"
	else:
		print "busted"
		player.canHit = False

def play_using_strat(stratagytable, NumberOfTestingHands):  ## takes the random statatgy grid and number of hands you want to test with it 
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
		if len(freshDeck.cards) < 8:
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
	print "player 2 has this much money: " + str(player2.money)
	stratagytable.fitness = player2.money
	print "the finess of this player statatgy is: " + str(stratagytable.fitness) 



#play_using_strat(test,1000)


def create_base_poputation(size):

	basePopSize = size
	while basePopSize > 0:
		new = StratagyTable()
		print_array(new.grid)
		play_using_strat(new,10)
		basePopSize -=1


create_base_poputation(10)