#################### BLACK JACK BOT

## possible moves
	#hit
	#stay
	#split


Deck_of_cards = []

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']

for suit in suits:
	for card in values:
		Deck_of_cards.append((card,suit))

card_point_values = {} ## create a key/value table for cards ie jack is 10 queen is 10 ...

from random import shuffle
def shuffleDeck(deck):
	return shuffle(deck)


def deal(deck, num_of_cards):
	cards = []
	for i in xrange(num_of_cards):
		cards.append(deck.pop())
		i-=1
	return cards ## taks a deck and deals out the specificed number of cards 
#### move options ####
def hit():
	pass
def stay():
	pass
def split():
	pass
def double():
	pass
######################	
def bet(): ## 
	pass

class player(object):
	def __init__(self, name = 'BOT', money = 0):
		self.name = name
		self.money = money


def point_value(hand):
	points = 0
	ace = ' '
	for cards in hand:
		if type(cards[0]) == int:
			points+=cards[0]
		elif cards[0] in ['Jack','Queen','King']:
			points+=10
		else:
			ace =" + 1 or 11"
	return str(points)+ace





shuffleDeck(Deck_of_cards)
hand1 = deal(Deck_of_cards,2)
print hand1
print point_value(hand1)


"""
print Deck_of_cards
shuffleDeck(Deck_of_cards)
print "-"*20 + "shuffled !!!" + "-"*20
print Deck_of_cards
"""
