#################### BLACK JACK BOT
from random import shuffle
## possible moves
	#hit
	#stay
	#split
class Deck:
	def __init__(self):
		self.cards = []
		suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
		values = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']

		for suit in suits:
			for card in values:
				self.cards.append((card,suit))

	def shuffle(self):
		return shuffle(self.cards)
"""
Deck_of_cards = []

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']

for suit in suits:
	for card in values:
		Deck_of_cards.append((card,suit))



from random import shuffle
def shuffleDeck(deck):
	return shuffle(deck)

"""
def deal(deck, num_of_cards):
	cards = []
	for i in xrange(num_of_cards):
		cards.append(deck.pop())
		i-=1
	return cards ## taks a deck and deals out the specificed number of cards 
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


class player(object):
	def __init__(self, name = 'BOT', hand = None, money = 0):
		self.name = name
		self.money = money
		self.hand = hand


def point_value(hand):## Give it hand and it returns the point value of the hand 
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



newDeck = Deck()
print newDeck.cards
newDeck.shuffle()
print newDeck.cards

player1 = player
player1.hand = deal(newDeck.cards,2)
print player1.hand
print point_value(player1.hand)

"""
shuffleDeck(Deck_of_cards)
player1 = player
player1.hand = deal(Deck_of_cards,2)
print player1.hand
print point_value(player1.hand)

hit(player1,Deck_of_cards)

print player1.hand
print point_value(player1.hand)


"""
