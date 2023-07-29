"""
The Poker Hand Strength Evaluator is a Python program that allows users to 
input a poker hand and evaluates its strength based on the standard hand 
rankings in Texas Hold'em Poker. Texas Hold'em is one of the most popular 
variants of poker played worldwide, and understanding the strength of a hand 
is crucial in making strategic decisions during the game.

Features:
- User Input: The program prompts the user to input their poker hand, consisting of five cards represented by their ranks and suits (e.g., "2H" for 2 of hearts, "AD" for Ace of diamonds).
- Hand Evaluation: The program then evaluates the strength of the input hand and determines the best possible hand combination, such as straight flush, four of a kind, full house, etc.
- Hand Comparison: Users can compare their hands against each other, and the program will indicate which hand is stronger based on the standard hand rankings.
- Error Handling: The program includes error handling mechanisms to validate user input and ensure that a valid poker hand is provided.
- User-Friendly Output: After evaluating the hand, the program displays the user's hand and its strength, providing valuable insights into the potential of the hand during a poker game.

"""
from flask import Flask, render_template, request
import argparse
import collections
import random
class Card:
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        return f"{self.rank}{self.suit}"


ranks=['2','3','4','5','6','7','8','9','T','J','Q','K','A']
suits=['H','D','C','S']

deck=[Card(rank,suit) for rank in ranks for suit in suits]

random.shuffle(deck)

def get_hand_from_input(hand_input):
    hand_input=hand_input.upper().split()
    if len(hand_input)!=5:
        raise argparse.ArgumentTypeError("A hand must have 5 cards")
    hand=[]
    for card_input in hand_input:
        if len(card_input)!=2:
            raise argparse.ArgumentTypeError("Invalid card format. Please provide cards in the format: '2H 4D 6S 8C AD'")
        rank,suit=card_input[:-1],card_input[-1]
        if rank not in ranks or suit not in suits:
            raise argparse.ArgumentTypeError(f"Invalid card: {card_input}. Valid ranks: {ranks}, valid suits: {suits}")
        hand.append(Card(rank,suit))
    return hand

def is_straight_flush(hand):
    # Check for Straight Flush logic
    suits_set = set(card.suit for card in hand)
    if len(suits_set) == 1:
        for i in range(1, len(hand)):
            if ranks.index(hand[i].rank) != ranks.index(hand[i-1].rank) + 1:
                return False
        return True
    return False

def is_four_of_a_kind(hand):
    # Check for Four of a Kind logic
    rank_counts = [0] * len(ranks)
    for card in hand:
        rank_counts[ranks.index(card.rank)] += 1
    return any(count == 4 for count in rank_counts)

def is_full_house(hand):
    # Check for Full House logic
    rank_counts = [0] * len(ranks)
    for card in hand:
        rank_counts[ranks.index(card.rank)] += 1
    return any(count == 3 for count in rank_counts) and any(count == 2 for count in rank_counts)

def is_flush(hand):
    # Check for Flush logic
    suits_set = set(card.suit for card in hand)
    return len(suits_set) == 1

def is_straight(hand):
    # Check for Straight logic
    for i in range(1, len(hand)):
        if ranks.index(hand[i].rank) != ranks.index(hand[i-1].rank) + 1:
            return False
    return True

def is_three_of_a_kind(hand):
    # Check for Three of a Kind logic
    rank_counts = [0] * len(ranks)
    for card in hand:
        rank_counts[ranks.index(card.rank)] += 1
    return any(count == 3 for count in rank_counts)

def is_two_pair(hand):
    # Check for Two Pair logic
    rank_counts = collections.Counter(card.rank for card in hand)
    num_pairs = 0
    for count in rank_counts.items():
        if count == 2:
            num_pairs += 1
    return num_pairs == 2

def is_one_pair(hand):
    # Check for One Pair logic
    rank_counts = [0] * len(ranks)
    for card in hand:
        rank_counts[ranks.index(card.rank)] += 1
    return any(count == 2 for count in rank_counts)
def get_pair_and_high_card(hand):
    rank_counts = collections.Counter(card.rank for card in hand)
    pair_rank = None
    high_card_rank = None
    for rank, count in rank_counts.items():
        if count == 2:
            pair_rank = rank
        elif count == 1:
            high_card_rank = rank
    return pair_rank, high_card_rank
def get_three_of_a_kind_and_pair(hand):
    rank_counts = collections.Counter(card.rank for card in hand)
    three_of_a_kind_rank = None
    pair_rank = None
    for rank, count in rank_counts.items():
        if count == 3:
            three_of_a_kind_rank = rank
        elif count == 2:
            pair_rank = rank
    return three_of_a_kind_rank, pair_rank

def evaluate_hand_strength(hand):
    # Sort the hand by rank for easier evaluation
    sorted_hand = sorted(hand, key=lambda card: ranks.index(card.rank))

    if is_straight_flush(sorted_hand):
        return 9
    elif is_four_of_a_kind(sorted_hand):
        return 8
    elif is_full_house(sorted_hand):
        return 7
    elif is_flush(sorted_hand):
        return 6
    elif is_straight(sorted_hand):
        return 5
    elif is_three_of_a_kind(sorted_hand):
        return 4
    elif is_two_pair(sorted_hand):
        return 3
    elif is_one_pair(sorted_hand):
        return 2
    else:
        return 1
#Rank Hands:
def resolve_tie(hand1, hand2):
    hand1_strength = evaluate_hand_strength(hand1)
    hand2_strength = evaluate_hand_strength(hand2)

    if hand1_strength > hand2_strength:
        return "Hand 1 is stronger"
    elif hand1_strength < hand2_strength:
        return "Hand 2 is stronger"

    # Check for specific tie-breaking scenarios based on hand strength
    if hand1_strength == 2:  # One Pair
        hand1_pair_rank, hand1_high_card = get_pair_and_high_card(hand1)
        hand2_pair_rank, hand2_high_card = get_pair_and_high_card(hand2)
        if hand1_pair_rank > hand2_pair_rank:
            return "Hand 1 is stronger"
        elif hand1_pair_rank < hand2_pair_rank:
            return "Hand 2 is stronger"
        elif hand1_high_card > hand2_high_card:
            return "Hand 1 is stronger"
        elif hand1_high_card < hand2_high_card:
            return "Hand 2 is stronger"

    elif hand1_strength == 3:  # Two Pair
        hand1_high_pair, hand1_low_pair = sorted(get_pair_and_high_card(hand1), reverse=True)
        hand2_high_pair, hand2_low_pair = sorted(get_pair_and_high_card(hand2), reverse=True)
        if hand1_high_pair > hand2_high_pair:
            return "Hand 1 is stronger"
        elif hand1_high_pair < hand2_high_pair:
            return "Hand 2 is stronger"
        elif hand1_low_pair > hand2_low_pair:
            return "Hand 1 is stronger"
        elif hand1_low_pair < hand2_low_pair:
            return "Hand 2 is stronger"

    elif hand1_strength == 4:  # Three of a Kind
        hand1_three_of_a_kind, hand1_pair = get_three_of_a_kind_and_pair(hand1)
        hand2_three_of_a_kind, hand2_pair = get_three_of_a_kind_and_pair(hand2)
        if hand1_three_of_a_kind > hand2_three_of_a_kind:
            return "Hand 1 is stronger"
        elif hand1_three_of_a_kind < hand2_three_of_a_kind:
            return "Hand 2 is stronger"
        elif hand1_pair > hand2_pair:
            return "Hand 1 is stronger"
        elif hand1_pair < hand2_pair:
            return "Hand 2 is stronger"

    elif hand1_strength == 5:  # Straight
        if ranks.index(hand1[-1].rank) > ranks.index(hand2[-1].rank):
            return "Hand 1 is stronger"
        elif ranks.index(hand1[-1].rank) < ranks.index(hand2[-1].rank):
            return "Hand 2 is stronger"
        else:
            return "It's a tie!"

    elif hand1_strength == 6:  # Flush
        # Compare the highest cards of the flush hands
        for i in range(4, -1, -1):
            if ranks.index(hand1[i].rank) > ranks.index(hand2[i].rank):
                return "Hand 1 is stronger"
            elif ranks.index(hand1[i].rank) < ranks.index(hand2[i].rank):
                return "Hand 2 is stronger"
        return "It's a tie!"

    elif hand1_strength == 7:  # Full House
        hand1_three_of_a_kind, hand1_pair = get_three_of_a_kind_and_pair(hand1)
        hand2_three_of_a_kind, hand2_pair = get_three_of_a_kind_and_pair(hand2)
        if hand1_three_of_a_kind > hand2_three_of_a_kind:
            return "Hand 1 is stronger"
        elif hand1_three_of_a_kind < hand2_three_of_a_kind:
            return "Hand 2 is stronger"
        elif hand1_pair > hand2_pair:
            return "Hand 1 is stronger"
        elif hand1_pair < hand2_pair:
            return "Hand 2 is stronger"
        else:
            return "It's a tie!"

    elif hand1_strength == 8:  # Four of a Kind
        hand1_rank_counts = collections.Counter(card.rank for card in hand1)
        hand2_rank_counts = collections.Counter(card.rank for card in hand2)
        hand1_four_of_a_kind_rank = [rank for rank, count in hand1_rank_counts.items() if count == 4][0]
        hand2_four_of_a_kind_rank = [rank for rank, count in hand2_rank_counts.items() if count == 4][0]
        if ranks.index(hand1_four_of_a_kind_rank) > ranks.index(hand2_four_of_a_kind_rank):
            return "Hand 1 is stronger"
        elif ranks.index(hand1_four_of_a_kind_rank) < ranks.index(hand2_four_of_a_kind_rank):
            return "Hand 2 is stronger"
        else:
            return "It's a tie!"

    elif hand1_strength == 9:  # Straight Flush
        if ranks.index(hand1[-1].rank) > ranks.index(hand2[-1].rank):
            return "Hand 1 is stronger"
        elif ranks.index(hand1[-1].rank) < ranks.index(hand2[-1].rank):
            return "Hand 2 is stronger"
        else:
            return "It's a tie!"

    return "It's a tie!"


def rank_hands(hand1, hand2):
    hand1_strength = evaluate_hand_strength(hand1)
    hand2_strength = evaluate_hand_strength(hand2)

    if hand1_strength > hand2_strength:
        return "Hand 1 is stronger"
    elif hand1_strength < hand2_strength:
        return "Hand 2 is stronger"
    else:
        return resolve_tie(hand1, hand2)
def main():
    print("Welcome to the Poker Hand Strength Evaluator!")

    while True:
        try:
            # Get user input for hand 1
            hand1_input = input("Enter your first poker hand (e.g., '2H 4D 6S 8C AD'): ")
            hand1 = get_hand_from_input(hand1_input)

            # Get user input for hand 2
            hand2_input = input("Enter your second poker hand (e.g., '2H 4D 6S 8C AD'): ")
            hand2 = get_hand_from_input(hand2_input)

            # Evaluate and compare the hands
            result = rank_hands(hand1, hand2)
            print(result)

            play_again = input("Do you want to compare more hands? (yes/no): ").lower()
            if play_again != 'yes':
                break

        except argparse.ArgumentTypeError as e:
            print(f"Error: {e}")
            print("Please provide valid poker hands in the format: '2H 4D 6S 8C AD'")
            continue
app=Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get user input for hand 1
            hand1_input = request.form["hand1"]
            hand1 = get_hand_from_input(hand1_input)

            # Get user input for hand 2
            hand2_input = request.form["hand2"]
            hand2 = get_hand_from_input(hand2_input)

            # Evaluate and compare the hands
            result = rank_hands(hand1, hand2)
            return render_template("index.html", result=result, hand1_input=hand1_input, hand2_input=hand2_input)

        except argparse.ArgumentTypeError as e:
            error_message = f"Error: {e}"
            return render_template("index.html", error_message=error_message)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)