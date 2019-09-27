from .. import learn
from .. import fileinput
from .generate_file import generate_file
from os import remove
import pytest


def test_read():
    num_cards = 20
    filepath = generate_file(num_cards)
    cards = list(fileinput.read_cards(filepath))

    assert len(cards) == num_cards

    for i, card in enumerate(cards):
        assert card.description == f'front{i}'
        assert card.response == f'back{i}'

    remove(filepath)


def test_read_write():
    num_cards = 50
    filepath = generate_file(num_cards)
    cards = list(fileinput.read_cards(filepath))

    assert len(cards) == num_cards

    for i, card in enumerate(cards):
        assert card.description == f'front{i}'
        assert card.response == f'back{i}'

    fileinput.write_cards(filepath, cards)
    cards = list(fileinput.read_cards(filepath))
    for i, card in enumerate(cards):
        assert card.description == f'front{i}'
        assert card.response == f'back{i}'

    remove(filepath)


def test_is_reviewable_today():
    num_cards = 4
    filepath = generate_file(num_cards)
    cards = list(fileinput.read_cards(filepath))
    for card in cards:
        assert card.is_reviewable()


def test_learn():
    num_cards = 25
    filepath = generate_file(num_cards)
    cards = list(fileinput.read_cards(filepath))

    hard_cards = (2, 3, 10, 15, 16, 25)
    current_hard_cards = list(hard_cards)

    def rate_fn(card):
        for i in current_hard_cards:
            if str(i) in card.description:
                current_hard_cards.remove(i)
                return 0
        return 3

    learn.learn(cards, rate_fn=rate_fn)
    for i, card in enumerate(cards):
        if str(i) in hard_cards:
            assert card.easiness_factor - (2.5 - 0.8 + 0.1) < 0.0001
        else:
            assert card.easiness_factor - (2.5 + 0.1) < 0.0001
