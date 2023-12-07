CARD_ORDER = "23456789TJQKA"
CARD_ORDER_WITH_JOKERS = "J23456789TQKA"

HAND_ORDER = [
    [1,1,1,1,1],
    [2,1,1,1],
    [2,2,1],
    [3,1,1],
    [3,2],
    [4,1],
    [5]
]

def parse_hands(data):
    for line in data.splitlines():
        parts = line.split()
        yield (parts[0], int(parts[1]))

def get_card_totals(hand, use_jokers=False):
    card_totals = [hand.count(item) for item in set(hand)]
    card_totals.sort(reverse=True)

    if use_jokers:
        # If jokers are present, add to the maximum count present
        n_jokers = hand.count("J")
        if n_jokers and n_jokers < 5:
            card_totals.remove(n_jokers)
            card_totals[0] += n_jokers

    return card_totals

def sort_hands(hands, use_jokers=False):
    if use_jokers:
        card_order = CARD_ORDER_WITH_JOKERS
    else:
        card_order = CARD_ORDER

    # Sort by cards (secondary)
    for i in reversed(range(5)):
        hands.sort(key=lambda hand: card_order.index(hand[0][i]))

    # Sort by rank (primary)
    hands.sort(
        key=lambda hand: HAND_ORDER.index(
            get_card_totals(hand[0], use_jokers=use_jokers)
        )
    )

    return hands

def score_hands(hands):
    return sum(
        [(k+1) * bid for k,(_,bid) in enumerate(hands)]
    )

def run(data):
    hands = list(parse_hands(data))
    
    sorted_hands = sort_hands(hands.copy())
    sorted_hands_with_jokers = sort_hands(hands.copy(), use_jokers=True)
    
    return (
        score_hands(sorted_hands),
        score_hands(sorted_hands_with_jokers)
    )

# Running script
fp = "2023/inputs/day7"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
