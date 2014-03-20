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

def stay():
	pass
def split():
	pass
def double():
	pass
######################	
def bet(): ## 
	pass

def bust(player): ## takes a player and returns true of they have busted 
	if point_value(player.hand) > 21:
		return True
	else:
		return False 


class Player(object):
	def __init__(self, name = 'BOT', hand = None, money = 0):
		self.name = name
		self.money = money
		self.hand = hand




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


"""
## NOTE maybe switch all fuctions to take player as the argument instead of player.hand to make things cleaner 
newDeck = Deck()
print newDeck.cards
newDeck.shuffle()
print newDeck.cards

player1 = Player()
player1.hand = deal(newDeck.cards,2)
print player1.hand
print point_value(player1.hand)
#print player1.has_ace()

hit(player1,newDeck.cards)
print player1.hand
print point_value(player1.hand)
#print player1.has_ace()
print "Do they have an ace? :" + str(has_ace(player1.hand))
print "Did they bust? :" + str( bust(player1) )

"""

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


### working on below 
def test2Player(): ## Player vs Dealer both using dealer stratagy 
	dealer =  Player()
	dealer.name = 'Dealer'
	# assuming the dealer has unlimted money
	player2 = Player()
	player2.name = 'Player2'
	player2.money = 100
	freshDeck  = Deck()
	freshDeck.shuffle()
	while len(freshDeck.cards) > 8:
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




test2Player()