# Blackjack Python
import random

def PrintHand(cards):
	for i in range(len(cards)):
		cards[i].PrintCard()
		
def HandUnder21(cards):
	return (HandPointTotal(cards) <= 21)
	
def HandPointTotal(cards):
	total = 0
	aces = 0
	for i in range(len(cards)):
		total = total + cards[i].PointValue()
		if cards[i].value == "Ace":
			aces = aces + 1
	total = total + (aces * 10)
	while total > 21 and aces > 0:
		total = total - 10
		aces = aces - 1
	return total
	
def BlackjackHand(cards):
	return (HandPointTotal(cards) == 21)
	
def AskPlayBlackjack(again):
	response = ""
	tries = 0
	play = "maybe"
	prompt = ""
	if again:
		prompt = "Keep playing Blackjack? (yes/no) "
	else:
		prompt = "Do you want to play Blackjack? (yes/no) "
	while (len(response) <= 0 or not response.isalpha()) and play == "maybe":
		response = input(prompt)
		tries = tries + 1
		if response.lower() == "yes":
			print ("Alright! Let's play!")
			play = "yes"
		elif response.lower() == "no":
			print ("Okay. Maybe another time.")
			play = "no"
		else:
			print ("I didn't understand that.")
			response = ""
			if tries == 3:
				play = "no"
				print ("There seems to be a failure to communicate between us. Perhaps we'll play another time.")
	return play
	
def HitOrStay():
	print ("\r\nHit or Stay?")
	response = "Stay"
	print (response)
	return response

class Card(object):
	suit = ""
	value = ""
	
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value
		
	def PrintCard(self):
		print (self.value + " of " + self.suit)
		
	def PointValue(self):
		if self.value == "King":
			return 10
		elif self.value == "Queen":
			return 10
		elif self.value == "Jack":
			return 10
		elif self.value == "Ace":
			return 1
		else:
			return int(self.value)
			
class Player(object):
	
	def __init__(self, name):
		self.name = name
		self.hand = []
	
	def HitOrStay(self):
		response = input("\r\nHit or Stay? ")
		if response.lower() == "hit" or response.lower() == "stay":
			print ("I'll " + response)
		else:
			print ("That didn't make any sense... I'll stay")
			response = "Stay"
		return response
	
	def AddToHand(self, card):
		self.hand.append(card)
		#print (self.name + " Hand: ")
		#self.PrintHand()
	
	def DiscardHand(self):
		discardPile = self.hand
		self.hand = []
		return discardPile
		
	def PrintHand(self):
		for i in range(len(self.hand)):
			self.hand[i].PrintCard()
		#print ("\r\n")
			
	def HandUnder21(self):
		return (self.HandPointTotal() <= 21)
		
	def HandPointTotal(self):
		total = 0
		aces = 0
		for i in range(len(self.hand)):
			total = total + self.hand[i].PointValue()
			if self.hand[i].value == "Ace":
				aces = aces + 1
		total = total + (aces * 10)
		while total > 21 and aces > 0:
			total = total - 10
			aces = aces - 1
		return total
	
	def BlackjackHand(self):
		return (self.HandPointTotal() == 21 and len(self.hand) == 2)
		
class Dealer(Player):
	def __init__(self):
		self.name = "Dealer"
		self.hand = []
		
	def HitOrStay(self):
		if HandPointTotal(self.hand) >= 17:
			print ("Dealer stays")
			return "Stay"
		else:
			print ("Dealer hits")
			return "Hit"

class Deck(object):
	cards = []
	suits = ["Diamonds","Clubs","Hearts","Spades"]
	
	def __init__(self):
		self.FillDeck()
		
	def FillDeck(self):
		for s in range(4):
			for i in range(1,14):
				if i == 1:
					self.cards.append(Card(self.suits[s],"Ace"))
				elif i == 11:
					self.cards.append(Card(self.suits[s],"Jack"))
				elif i == 12:
					self.cards.append(Card(self.suits[s],"Queen"))
				elif i == 13:
					self.cards.append(Card(self.suits[s],"King"))
				else:
					self.cards.append(Card(self.suits[s],str(i)))
	
	def Shuffle(self):
		for i in range(4):
			cardsShuffled = []
			while len(self.cards) > 0:
				cardsShuffled.append(self.cards.pop(random.randint(0,len(self.cards)-1)))
			self.cards = cardsShuffled
		print ("\r\nDeck has been shuffled\r\n")
		
	def PrintDeck(self):
		for i in range(len(self.cards)):
			self.cards[i].PrintCard()
			
	def CollectPlayedCards(self, cards):
		for i in range(len(cards)):
			self.cards.append(cards[i])
			
	def DealCard(self):
		return self.cards.pop(0)

def StartGame():
	deck = Deck()
	#deck.PrintDeck()
	#deck.Shuffle()
	#deck.PrintDeck()
	play = AskPlayBlackjack(False)

	while play == "yes":
		dealerPlay = "yes"
		dealer = Dealer()
		player = Player("Player 1")
		print ("Shuffling the deck")
		deck.Shuffle()
		print ("Dealing cards")
		player.AddToHand(deck.DealCard())
		dealer.AddToHand(deck.DealCard())
		player.AddToHand(deck.DealCard())
		dealer.AddToHand(deck.DealCard())
		#print ("\r\nDeck: \r\n")
		#deck.PrintDeck()
		while play == "yes":
			if player.HandUnder21():
				if player.BlackjackHand():
					if dealer.BlackjackHand():
						print("PUSH!")
					else:
						print ("You got BLACKJACK!!! YOU WIN!!!")
					dealerPlay = "no"
					play = "no"
				elif dealer.BlackjackHand():
					print ("Dealer got BLACKJACK!!! Dealer WINS!!!")
					dealerPlay = "no"
					play = "no"
				else:
					print ("\r\nHand: \r\n")
					player.PrintHand()
					choice = player.HitOrStay()
					if choice.lower() == "hit":
						player.AddToHand(deck.DealCard())
					else:
						print ("Player Total: %d\r\n" % player.HandPointTotal())
						play = "no"
			else:
				print ("Player Total: %d\r\n" % player.HandPointTotal())
				print ("\r\nBUST! You lost this round.\r\n")
				play = "no"
				dealerPlay = "no"
				
		while dealerPlay == "yes":
			if dealer.HandUnder21():
				if dealer.BlackjackHand():
					print ("Dealer got BLACKJACK!!! Dealer WINS!!!???")
					dealerPlay = "no"
				else:
					choice = dealer.HitOrStay()
					if choice.lower() == "hit":
						dealer.AddToHand(deck.DealCard())
					else:
						print ("Dealer Total: %d\r\n" % dealer.HandPointTotal())
						dealerPlay = "no"
						if dealer.HandPointTotal() > player.HandPointTotal():
							print ("Dealer WINS!!!")
						elif dealer.HandPointTotal() < player.HandPointTotal():
							print ("YOU WIN!!!")
						else:
							print ("PUSH!")
						
			else:
				print ("Dealer Total: %d\r\n" % dealer.HandPointTotal())
				print ("\r\nDealer BUSTS! You win this round!\r\n")
				dealerPlay = "no"
		
		print ("\r\nPlayer Hand: \r\n")
		player.PrintHand()
		print ("\r\nDealer Hand: \r\n")
		dealer.PrintHand()
		deck.CollectPlayedCards(player.DiscardHand())
		deck.CollectPlayedCards(dealer.DiscardHand())
		
		#print ("\r\nDeck: \r\n")
		#deck.PrintDeck()
		play = AskPlayBlackjack(True)
		
# hand = [Card("Spades","King"),Card("Clubs","5"),Card("Hearts","2")]
# print (HandPointTotal(hand))
# print (BlackjackHand(hand))
# print (HandUnder21(hand))

StartGame()
