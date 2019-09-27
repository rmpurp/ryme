from random import shuffle
from operator import attrgetter


class CardBag:
    def __init__(self, cards, num_cards, shuffle=True):
        """
        Create a new CardBag with the given set of cards, limited by num_cards.

        Uses a bag system, where 10 cards will be put into a bag and shuffled
        (if shuffle is true, which is default). When there are fewer than
        3 cards, the bag will be refilled to 10 cards.
        """
        eligible_cards = list(filter(lambda x: x.is_reviewable(), cards))

        if num_cards < 0 or num_cards >= len(eligible_cards):
            self.cards = eligible_cards
        else:
            eligible_cards.sort(key=attrgetter('next_review'))
            self.cards = eligible_cards[:num_cards]
        self.total_num = len(self.cards)
        

        self.last_card = None
        self.current_bag = []
        self.shuffle = shuffle

    def refill_bag(self):
        """Refill the bag to 10 cards, if possible."""
        new_cards = self.cards[:10 - len(self.current_bag)]
        del self.cards[:10 - len(self.current_bag)]

        if self.shuffle:
            shuffle(new_cards)

        self.current_bag.extend(new_cards)

    def __len__(self):
        """Get the number of cards remaining in the bag"""
        return len(self.cards) + len(self.current_bag)

    def recycle_last(self):
        """Place the most recent card back into the bag."""
        self.current_bag.append(self.last_card)

    def __next__(self):
        """Get the next card to review."""
        if self.cards and len(self.current_bag) < 3:
            self.refill_bag()

        if not self.current_bag:
            raise StopIteration

        self.last_card = self.current_bag.pop(0)

        return self.last_card

    def __iter__(self):
        """Return iterator over cards, which here is the object per se."""
        return self


def learn(cards, show_fn=None, rate_fn=None, write_fn=None, num_cards=-1):
    """Learn the given cards.

    show_fn is intended to be used to prompt the user for an answer,
    and rate_fn is used to prompt the user for a result. If show_fn is not
    given, nothing will occur, and if rate_fn is not given, "3" will be the
    rating given.
    """
    if not show_fn:
        def show_fn(card, remaining, total): pass

    if not rate_fn:
        def rate_fn(card): return 3

    bag = CardBag(cards, num_cards)

    for card in bag:
        show_fn(card, len(bag), bag.total_num)
        rating = rate_fn(card)
        card.rate(rating)
        if rating < 2:
            bag.recycle_last()
        if write_fn:
            write_fn()
