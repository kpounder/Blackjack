import random
import pandas as pd


class Deck:
    deck = []
    values = [str(_) for _ in range(2, 11)] + ['J', 'Q', 'K', 'A']
    suits = ['D', 'H', 'S', 'C']
    for value in values:
        for suit in suits:
            deck.append((value, suit))

    def __init__(self):
        self.cards_in_play = []
        self.available_cards = self.deck[:]
        for card in self.cards_in_play:
            self.available_cards.remove(card)

    def deal_card(self):
        dealt_card = random.choice(self.available_cards)
        self.cards_in_play.append(dealt_card)
        self.available_cards.remove(dealt_card)
        return dealt_card


class Player:
    def __init__(self, deck, hand=[]):
        self.deck = deck
        self.hand = hand[:]
        self.n_aces_as_eleven = 0
        self.score = 0

    def calc_hand_score(self):
        values = [card[0] for card in self.hand]
        values = [int(value) if value.isdigit() else value for value in values]
        values = [10 if value in ['J', 'Q', 'K'] else value for value in values]
        values = [11 if value == 'A' else value for value in values]
        n_aces = values.count(11)
        score = sum(values)
        while score > 21 and n_aces >= 1:
            score -= 10
            n_aces -= 1
        return score

    def get_card(self):
        new_card = self.deck.deal_card()
        self.hand.append(new_card)
        if new_card[0] in ['J', 'Q', 'K']:
            self.score += 10
        elif new_card[0] == 'A':
            self.score += 11
            self.n_aces_as_eleven += 1
        else:
            self.score += int(new_card[0])
        while self.score > 21 and self.n_aces_as_eleven >= 1:
            self.score -= 10
            self.n_aces_as_eleven -= 1


class Dealer(Player):
    def play_hand(self):
        while self.score < 17:
            self.get_card()


class Human(Player):
    pass


def main():
    game_nums = []
    human_starting_score = []
    human_final_score = []
    human_hit_once = []
    dealer_starting_score = []
    dealer_final_score = []
    human_won = []

    for game_num in range(500000):
        deck = Deck()
        dealer = Dealer(deck)
        human = Human(deck)
        dealer.get_card()
        dealer.get_card()
        human.get_card()
        human.get_card()

        game_nums.append(game_num)
        human_starting_score.append(human.score)
        dealer_starting_score.append(dealer.score)

        if game_num % 2 == 0:
            human.get_card()
            human_hit_once.append(True)
        else:
            human_hit_once.append(False)

        dealer.play_hand()

        human_final_score.append(human.score)
        dealer_final_score.append(dealer.score)
        if dealer.score > 21 or human.score > dealer.score:
            human_won.append(True)
        else:
            human_won.append(False)

    df = pd.DataFrame({
        'game_nums': game_nums,
        'human_starting_score': human_starting_score,
        'human_hit_once': human_hit_once,
        'human_final_score': human_final_score,
        'dealer_starting_score': dealer_starting_score,
        'dealer_final_score': dealer_final_score,
        'human_won': human_won
    })
    df = df.set_index('game_nums')
    df.to_csv('game_data.csv')


main()