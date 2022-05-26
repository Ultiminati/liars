import math

# name of cards are written as a tuple. Their indexes are indicative of their game value.
cards = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")


# liars function returns the probability of "x" desired cards being present randomly in "n" unknown cards
# while there are "maxx" unknown desired cards in "t" unknown cards in total.

def liars(n, x, t, m):
    return math.comb(n, x) * math.comb(m, x) * math.comb(t - m, n - x) / (math.comb(t, x) * math.comb(t - x, n - x))


# conditional_p function returns "p", the probability of "x" or more desired cards being present randomly in "n" cards
# while there are "k" known cards present and "b" known desired cards present
# which there are total of "t" cards and "m" desired cards.

def conditional_p(n, x, k, b, t=52, m=8):
    p = 0
    for i in range(x, m + 1):
        if i - b > n - k:
            continue
        if i - b < 0:
            return 1
        p += liars(n - k, i - b, t - k, m - b)
    return p


# claim_p returns the probability of the claim "c"
# with "t" being the dictionary of known cards and there are "n" cards on the table.
# dictionary of known cards has keys as the name of a card and values as number of that card known.
# a claim is a tuple whose first element is number of the card in question and second element is the name of the card.

def claim_p(n, t, c):
    k = 0
    for i in t.values():
        k += i
    if c[1] == "2":
        return conditional_p(n, c[0], k, t.get(c[1], 0))
    return conditional_p(n, c[0], k, t.get(c[1], 0) + t.get("2", 0))


# this function returns all the possible legal claims with "c" being the previous claim.
# if c is not specified, output will be the whole list.

def legal_claims(c=(2, "2")):
    card_values = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "10": 8, "J": 9, "Q": 10, "K": 11,
                   "A": 12}
    list_of_legal_claims = []
    initial_value = card_values[c[1]]
    for i in range(c[0], 9):
        for j in range(initial_value + 1, card_values["A"] + 1):
            list_of_legal_claims.append((i, cards[j]))
        initial_value = 0
    return list_of_legal_claims


# this function handles a string claim input and turns it to a proper tuple claim.

def claim_handler(claim_input):
    claim = claim_input.upper().split()
    claim[0] = int(claim[0])
    return tuple(claim)


# this function handles string card information and turns it to a proper known cards dictionary.

def card_handler(cards_input):
    cards_dictionary = {}
    for i in cards_input.upper().split():
        cards_dictionary[i] = cards_dictionary.get(i, 0) + 1
    return cards_dictionary


# claims_and_probs function returns the list of legal claims and their probabilities
# given "n", number of cards in the game; "t", the dictionary of known cards and the previous claim. the list is sorted,
# starting from the most probable.

def claims_and_probabilities(n, t, previous_claim):
    claims = legal_claims(previous_claim)
    claims_and_probs = []
    for i in claims:
        claims_and_probs.append([i, claim_p(n, t, i)])
    return sorted(claims_and_probs, key=lambda x: x[1])[::-1]


#

def top_x_most_probable_claims(x, claims_and_probs):
    for i in range(x):
        print("There are {} {}'s => {}".format(claims_and_probs[i][0][0],
                                               claims_and_probs[i][0][1],
                                               str(round(claims_and_probs[i][1] * 100, 2)) + "%"))


# action_of_choice returns the best move given the most probable claim and its probability
# and the probability of the previous claim.

def action_of_choice(claim_and_its_probability, p_of_previous_claim):
    if claim_and_its_probability[1] > 1 - p_of_previous_claim:
        return "claim that there are {} {}'s since this is likelier than the previous being false". \
            format(claim_and_its_probability[0][0], claim_and_its_probability[0][1])
    else:
        return "open the cards since your best claim is not likely than the previous being false"


# this function takes a probability as an input, rounds it and returns as visually nice percentage.

def goodformat(p):
    return str(round(p * 100, 2)) + "%"


# the never ending game mode in which the player will need to give the necessary informations needed
# every time they want to know the probability of a specific claim in a specific scenario.

def infinite_claims():
    while True:
        print("How many cards are there in the game?")
        a = input().lower()
        if a == "":
            return
        n = int(a)
        print("Which cards do you have?")
        your_cards_input = input()
        print("Which other cards do you think are on the table?")
        other_cards_input = input()
        print("What do you claim?")
        claim = claim_handler(input())

        all_cards_dict = card_handler(your_cards_input)
        your_cards_dict = card_handler(your_cards_input + " " + other_cards_input)
        print("If what you think about the other cards are true, the probability of the claim is",
              goodformat(claim_p(n, your_cards_dict, claim)))
        print("Based just on your own cards, the probability is", goodformat(claim_p(n, all_cards_dict, claim)))

        best_claim_and_p_based_on_all = claims_and_probabilities(n, all_cards_dict, claim)
        best_claim_and_p_based_on_yours = claims_and_probabilities(n, your_cards_dict, claim)

        print("\nTop 10 claims you can make")
        print("\nIf you are right about the cards:")
        top_x_most_probable_claims(10, best_claim_and_p_based_on_all)

        print("\nIf we consider only the cards you have:")
        top_x_most_probable_claims(10, best_claim_and_p_based_on_yours)


# "liars: the game". keeps all the information about how the game progresses.
# probabilities are calculated for two scenarios:
# in the first one, your guesses for the other cards in the game along with your own cards are considered.
# in the second one, only your cards are considered.
# "n" is the initial number of cards there are.

def game(n):
    n = int(n)
    previous_claim = (2, "2")
    print("There are total of {} cards in the game.".format(n))

    print("Which cards do you have?")
    your_cards_input = input()

    print("Which other cards do you think are on the table?")
    other_cards_input = input()

    print("What was the last claim?")
    last_claim_input = input()

    print("Do you have any specific claim you want to know about?")
    special_claim_input = input()

    your_cards_dict = card_handler(your_cards_input)
    all_cards_dict = card_handler(your_cards_input + " " + other_cards_input)

    if last_claim_input != "":
        previous_claim = claim_handler(last_claim_input)

    if special_claim_input != "":
        special_claim = claim_handler(special_claim_input)
        print("The probability of your claim is {} if you are right about the other cards. If not, it is {}".format(
            goodformat(claim_p(n, all_cards_dict, special_claim)),
            goodformat(claim_p(n, your_cards_dict, special_claim))))

    prev_claim_probs = (claim_p(n, all_cards_dict, previous_claim), claim_p(n, your_cards_dict, previous_claim))
    print("The probability of the previous claim is {} if you are right about the other cards. If not, it is {}".format(
        goodformat(prev_claim_probs[0]), goodformat(prev_claim_probs[1])))

    best_claim_and_p_based_on_all = claims_and_probabilities(n, all_cards_dict, previous_claim)
    best_claim_and_p_based_on_yours = claims_and_probabilities(n, your_cards_dict, previous_claim)

    print("\nTop 10 claims you can make")

    print("\nIf you are right about the cards:")
    top_x_most_probable_claims(10, best_claim_and_p_based_on_all)

    print("\nIf we consider only the cards you have:")
    top_x_most_probable_claims(10, best_claim_and_p_based_on_yours)

    print(
        "\nYour best action would be to {} if you are right about the cards. \nIf not, best action would be to {}."
        .format(
            action_of_choice(best_claim_and_p_based_on_all[0], prev_claim_probs[0]),
            action_of_choice(best_claim_and_p_based_on_yours[0], prev_claim_probs[1])))

    finisher = input().lower()
    while True:
        if finisher == "n":
            return game(n + 1)
        if finisher == "l":
            print("How many cards are removed?")
            return game(n - int(input()))
        if finisher == "f":
            return
        print("Please write: (without the quotation marks)")
        print("\"n\" if game continued with someone having one more card.")
        print("\"l\" if game continued with someone eliminated.")
        print("\"f\" if game is finished.")


print("Please select your what you want:")
print("write 'g' if you want to play the normal game")
print("write 'i' if you want to know about a specific claim in a specific scenario")
while True:
    wanted_game_mode = input().lower()
    if wanted_game_mode == "g":
        print("To play the game, please provide the number of cards in the game.")
        game(int(input()))
        break
    if wanted_game_mode == "i":
        infinite_claims()
        break
    else:
        print("Your input was invalid.")
