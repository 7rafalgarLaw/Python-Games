#!/usr/bin/env python
# coding: utf-8

# # BlackJack

# In[1]:


class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
  
    def __str__(self):
        bg_color = ''
        if self.suit == 'Hearts' or self.suit == 'Diamonds':
            bg_color = Color.COLOR_RED
        else:
            bg_color = Color.COLOR_BLACK
        return bg_color + Color.BOLD + self.rank +' of ' + self.suit + Color.RESET
    
    def show_some(player_cards, dealer_cards):
        print()
        print('\tPlayer Cards : ', end = " ")
        for card in player_cards:
            print(card, end=' ')
        print()
        print('\tDealer Cards : ', end = " ")
        hcard = dealer_cards.pop()
        for card in dealer_cards:
            print(card, end=' ')
        print('-------------')
        dealer_cards.append(hcard)
    
    def show_all(player_cards, dealer_cards):
        print()
        print('\tPlayer Cards : ', end = " ")
        for card in player_cards:
            print(card, end=' ')
        print()
        print('\tDealer Cards : ', end = " ")
        for card in dealer_cards:
            print(card, end=' ')
        print()
    


# In[2]:


class Color:
    
    RESET = '\u001b[0m'
    COLOR_RED = '\u001b[31m'
    COLOR_BLACK = '\u001b[30m'
    BOLD = '\u001b[1m'


# In[3]:


import random

class Deck:
  
    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

    def __init__(self):
        self.deck = [] 
        for suit in Deck.suits:
            for rank in Deck.ranks:
                new_card = Card(suit, rank)
                self.deck.append(new_card)

    def __str__(self):
        string = ''
        for card in self.deck:
            string += card.rank + " of " + card.suit + ", "
        print(string)
        return string.rstrip(', ')

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        four_cards = self.deck[-4:]
        del self.deck[-4:]
        return four_cards

    def hit(self, hand):
        card = self.deck.pop()
        hand.add_card(card)
    


# In[4]:


class Hand:
  
    values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':1}
  
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        #self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        Hand.evaluate_hand(self)

    def evaluate_hand(self):
        value = 0
        has_ace = False
        # Evaluated again to adjust for Ace
        for c in self.cards:
            value += Hand.values[c.rank]
            if c.rank == 'Ace': has_ace = True
        
        self.value = value
        if has_ace and value + 10 < 22:
            self.value += 10

    def __str__(self):
        return str([str(x) for x in self.cards])
    


# In[5]:


class Chips:
    
    def __init__(self):
        self.total = 10000  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
    def take_bet(self):
        while True:
            try:
                bet_amt = int(input('Enter the amount you wish to bet : '))
            except: 
                print('Enter a number.')
            else:
                if bet_amt > self.total:
                    print('Your amount exceeds your current balance of '+str(self.total))
                elif bet_amt <= 0:  
                    print("Dont act smart.")
                else:
                    print(f'Your bet of amount {bet_amt} is placed.')
                    self.bet = bet_amt
                    break
        


# In[6]:


def hit_or_stand():
    global isPlaying

    player_input = ''

    while player_input.lower() != 'hit' and player_input.lower() != 'stand':
        player_input = input('\nWould you like to hit or stand : ')
        if player_input.lower() == 'hit':
            isPlaying = True
        elif player_input.lower() == 'stand':
            isPlaying = False
        else:
            print('Enter "hit" or "stand"')
            
def player_busts(hand, player_chips):
    
    if hand.value > 21:
        print('\nYour hand value has exceeded 21 points.')
    player_chips.lose_bet()
    print("\nYou have lost the game!")
    print("Bet Amount deducted : {}".format(player_chips.bet))
    print("Account balance : {}".format(player_chips.total))
    
def player_wins(player_chips):
    
    player_chips.win_bet()
    print("\nYou have won the game.")
    print("Bet Amount Credited : {}".format(player_chips.bet))
    print("Account balance : {}".format(player_chips.total))
    


# In[7]:


def play_again():

    global replay

    print()
    flag = input("Would you like to play again? Y for Yes N for No : ")
    if flag.lower() == 'n':
        replay = False


# In[ ]:


#show_some(['a','b','c'],['1','2','3'])
#show_all(['a','b','c'],['1','2','3'])

import time

print("\n"+Color.BOLD+"Welcome to BlackJack\n"+Color.RESET)

# Set up the Player's chips
player_chips = Chips()
print('Your account balance is : '+str(player_chips.total))

while True:

    isPlaying = True
    replay = True

    # Use new Deck and Shuffle it.
    new_deck = Deck()
    new_deck.shuffle()

    # Prompt the Player for their bet.
    player_chips.take_bet()

    initial_cards = new_deck.deal()

    # Hand creation
    player_hand = Hand()
    for c in initial_cards[:2]:
        player_hand.add_card(c)
    dealer_hand = Hand()
    for c in initial_cards[2:]:
        dealer_hand.add_card(c)

    # Show cards (but keep one dealer card hidden)
    Card.show_some(player_hand.cards, dealer_hand.cards)

    while isPlaying:
        # Prompt the Player to Hit or Stand
        hit_or_stand()

        # Player turns
        if isPlaying:
            new_deck.hit(player_hand)
            Card.show_some(player_hand.cards, dealer_hand.cards)

            # If player's hand exceeds 21 player has lost.
            if player_hand.value > 21:
                player_busts(player_hand, player_chips)
                if player_chips.total:
                    play_again()
                else:
                    print('\nYou have no account balance to play!')
                    replay = False
                isPlaying = False
        else:
            # Show Dealer's Hidden card
            Card.show_all(player_hand.cards, dealer_hand.cards)
    
    # Play dealer only if player has not lost
    if player_hand.value < 22:
        
        # Dealer's turn
        while dealer_hand.value <= 17:
            time.sleep(2)

            # Hit Dealer
            new_deck.hit(dealer_hand)

            Card.show_all(player_hand.cards, dealer_hand.cards)
            
        else:
        #Result
            if dealer_hand.value > 21 or dealer_hand.value < player_hand.value:
                player_wins(player_chips)

            elif dealer_hand.value == player_hand.value:
                print("\nIts a draw!")

            else:
                player_busts(player_hand, player_chips)

            isPlaying = False
            if player_chips.total:
                play_again()
            else:
                print('\nYou have no account balance to play!')
                replay = False

    # Replay
    if replay == False:
          break


# In[ ]:





# In[ ]:





# In[ ]:




