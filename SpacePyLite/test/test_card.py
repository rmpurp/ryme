from .. import card

def test_card():
    cd = card.Card('d', 'r')
    assert cd.easiness_factor == 2.5
    cd.easiness_factor = 2.3
    assert cd.easiness_factor == 2.3

