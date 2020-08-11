import random


class Card():
    """A playing card replicator.

    """
    def __init__(self, value=None, suit=None):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __str__(self):
        card_map = {11: 'Jack',
                    12: 'Queen',
                    13: 'King',
                    14: 'Ace'}
        val_str = str(self.value)
        if self.value in card_map:
            val_str = card_map[self.value]
        return val_str + ' of ' + self.suit

    def __repr__(self):
        return self.__str__()


class Deck():
    """A card deck replicator.

    """

    def __init__(self):
        self.cards = []
        for suit in ('Clubs', 'Diamonds', 'Hearts', 'Spades'):
            for value in range(2, 15):
                self.cards.append(Card(value, suit))

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        """Shuffle the deck.

        """
        random.shuffle(self.cards)

    def pop(self):
        """Take the top car off the deck and return it.

        """
        return self.cards.pop()

    def __str__(self):
        ret = f'{len(self)} Cards:\n'
        for card in self.cards:
            ret += str(card) + '\n'
        return ret

    def __repr__(self):
        return self.__str__()


class Cube():
    """A cube game simulator.

    """
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.top = [self.deck.pop() for _ in range(9)]
        self.depths = [1] * 9
        self.lives = [True] * 9
        self.life_count = 9
        self.set_highest_lowest()

    def set_highest_lowest(self):
        """Set the highest and lowest cards in play.

        """
        self.highest = [-1, Card(-1, -1)]
        self.lowest = [-1, Card(15, 15)]
        for i in range(9):
            if not self.lives[i]:
                continue
            if self.top[i] > self.highest[1]:
                self.highest = [i, self.top[i]]
            if self.top[i] < self.lowest[1]:
                self.lowest = [i, self.top[i]]

    def bet(self, index, higher):
        if not self.lives[index]:
            return
        new_card = self.deck.pop()
        old_card = self.top[index]
        self.top[index] = new_card
        self.depths[index] += 1
        if higher and (new_card <= old_card):
            self.lives[index] = False
            self.life_count -= 1
            self.set_highest_lowest()
            return False
        if (not higher) and (new_card >= old_card):
            self.lives[index] = False
            self.life_count -= 1
            self.set_highest_lowest()
            return False
        self.set_highest_lowest()
        return True

    def get_most_extreme(self):
        """Return the most extreme card and its index.

        """
        hi_dist = abs(self.highest[1].value - 8)
        lo_dist = abs(self.lowest[1].value - 8)
        if hi_dist > lo_dist:
            return self.highest
        else:
            return self.lowest

    def __len__(self):
        return sum(self.depths)

    def __repr__(self):
        ret = f'{len(self.deck)} cards in deck\n'
        ret += f'{len(self)} cards in cube\n'
        ret += f'{sum(self.lives):.0f} alive, '
        ret += f'{9-sum(self.lives):.0f} dead:\n\n'
        for i in range(3):
            for j in range(3):
                idx = i*3 + j
                tmp = str(self.top[idx])
                if self.lives[idx]:
                    tmp += ' (A)'
                else:
                    tmp += ' (D)'
                ret += f'{tmp:<23}'
            ret += '\n'
        return ret

    def __str__(self):
        return self.__repr__()
