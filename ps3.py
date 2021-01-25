# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>
import os
os.chdir("/Users/alandeutsch/Documents/Python/OCW/PS3")

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """


    word2 = word.lower()

    values = []
    for l in word2:
        if l != "*":
            values.append(SCRABBLE_LETTER_VALUES[l])
        else:
            values.append(0)

    comp2 = 7*len(word2) - 3*(n - len(word2))

    if comp2 > 1:
        return sum(values)*comp2
    else:
        return sum(values)*1

# print(get_word_score("BOB",2))
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
# display_hand({'e': 2, 'a': 1, '*': 1, 't': 2, 'n': 1, 'l': 1, 'e': 2, 'p':1, 'h':1})

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand={}
    num_vowels = int(math.ceil(n / 3))-1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1 # Adds entry in dictionary with value -> number of times it appears

    for i in range(num_vowels, n-1):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand["*"] = 1

    return hand

# print(deal_hand(1))
#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    word2 = word.lower()
    new_hand = {}

    for l in hand.keys():
        count = word2.count(l)
        if hand[l] > 1: #If value is more than 1
            if l in word2: #If letter in word
                if hand[l]-count >= 1:
                    new_hand[l] = hand[l]-count
            if l not in word2:
                new_hand[l] = hand[l]
        elif hand[l] == 1:
            if l not in word2:
                new_hand[l] = hand[l]

    return new_hand

# print(update_hand({'b':2, 'o':1, 'l':1, 'w':1, 'n':2},'BOB'))

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word2 = word.lower()

    flag = []
    for l in word2:
        if l in hand.keys():
            if hand[l] >= word2.count(l):
                flag.append(1)
            else:
                flag.append(0)
        else:
            flag.append(0)

    new_words = []
    flag2=[]
    if "*" in word2:
        for v in VOWELS:
            new_word = word2.replace("*",v)
            new_words.append(new_word)
        for new_word in new_words:
            if new_word in word_list:
                flag2.append(1)
            else:
                flag2.append(0)

        if 0 not in flag and 1 in flag2:
            return True
        else:
            return False
    else:
        if 0 not in flag and word2 in word_list:
            return True
        else:
            return False

# print(is_valid_word('elephant',{'e': 2, 'a': 1, '*': 1, 't': 2, 'n': 1, 'l': 1, 'e': 2, 'p':1, 'h':1},load_words()))

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """

    length = []
    for l in hand.keys():
        length.append(hand[l])
    return sum(length)

# print(calculate_handlen({'a':1, 'b':2, 'z': 3}))

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """
    total_points = 0
    while calculate_handlen(hand) > 0:
        print()
        print("Current hand: ")
        display_hand(hand)
        word = input('Enter word, or "!!" to indicate that you are finished: ')
        if word == "!!":
            break
        else:
            if is_valid_word(word, hand, word_list):
                total_points += get_word_score(word,HAND_SIZE)
                print(word + " earned " + str(get_word_score(word,HAND_SIZE)) + " points. Total: " + str(total_points) + " points")
            else:
                print("That is not a valid word. Please choose another word.")
            new_hand = update_hand(hand, word)
            hand = new_hand

    print("Total score for this hand: " + str(total_points) + " points")
    return total_points

    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score

    # As long as there are still letters left in the hand:

        # Display the hand

        # Ask user for input

        # If the input is two exclamation points:

            # End the game (break out of the loop)


        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)

            # update the user's hand by removing the letters of their inputted word


    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

# play_hand({'e': 2, 'a': 1, '*': 1, 't': 2, 'n': 1, 'l': 1, 'e': 2, 'p':1, 'h':1},load_words())

#
# Problem #6: Playing a game
#


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    alphabet = ''.join(sorted(VOWELS + CONSONANTS))
    new_hand = hand

    if letter in hand.keys():
        new_letter = random.choice(alphabet)
        while new_letter in hand.keys():
            print(new_letter)
            new_letter = random.choice(alphabet)

        value = new_hand[letter]
        new_hand.pop(letter, None)
        new_hand[new_letter] = value

    return new_hand

# print(substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l'))


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    print()
    try:
        num_hands = int(input("How many hands would you like to play? "))
    except ValueError:
        print("Value Error")
        exit()

    print()

    total_points = []
    hands = []
    substituded = 0
    replayed = 0

    hand = deal_hand(HAND_SIZE)
    print("Current Hand: ")
    display_hand(hand)
    sub = input("Would you like to substitute a letter? [y/n] ")
    if sub.lower() == 'y':
        substituded = 1
        letter_replace = input("Which letter would you like to replace? ")
        new_hand = substitute_hand(hand, letter_replace)
    else:
        new_hand = hand
    hands.append(new_hand)

    total_score = play_hand(new_hand, word_list)
    total_points.append(total_score)
    print("--------")

    for i in range(1, num_hands):
        sub_temp = 0
        replay_temp = 0
        if replayed != 1:
            replay = input("Would you like to replay the hand? [y/n] ")
            if replay == 'y':
                replayed = 1
                replay_temp = 1
                sub_temp = 1
                hand = hands[i-1]
            else:
                hand = deal_hand(HAND_SIZE)
        else:
            hand = deal_hand(HAND_SIZE)

        if substituded != 1 and sub_temp != 1:
            print("Current Hand: ")
            display_hand(hand)
            sub = input("Would you like to substitute a letter? [y/n] ")
            if sub.lower() == 'y':
                substituded = 1
                letter_replace = input("Which letter would you like to replace? ")
                new_hand = substitute_hand(hand, letter_replace)
            else:
                new_hand = hand
        else:
            new_hand = hand

        total_score = play_hand(new_hand, word_list)
        if replay_temp == 1:
            if total_score > total_points[i-1]:
                del total_points[i-1]
                total_points.append(total_score)
        else:
            total_points.append(total_score)
        print("--------")

    print("Total score for all hands: " + str(sum(total_points)))


    # print("play_game not implemented.") # TO DO... Remove this line when you implement this function

# play_game("hello")

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
