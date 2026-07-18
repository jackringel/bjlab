from bjlab import Hand, Rank

A, T = Rank.ACE, Rank.TEN


def hand(*cards):
    return Hand.from_cards(cards)


def test_empty_hand():
    h = Hand()
    assert h.is_empty
    assert h.n_cards == 0
    assert h.hard_total == 0


def test_add_is_pure():
    h = hand(T)
    h2 = h.add(Rank.SIX)
    assert h.cards == (T,)
    assert h2.cards == (T, Rank.SIX)


def test_hard_and_soft_totals():
    h = hand(A, Rank.SIX)  # soft 17
    assert h.hard_total == 7
    assert h.soft_total == 17
    assert h.best_total == 17
    assert h.is_soft

    h = h.add(T)  # A,6,T = hard 17 (this case caught the old soft_total bug)
    assert h.hard_total == 17
    assert h.soft_total is None
    assert h.best_total == 17
    assert not h.is_soft

    h = hand(A, A)  # soft 12
    assert h.hard_total == 2
    assert h.soft_total == 12
    assert h.best_total == 12


def test_blackjack():
    assert hand(A, T).is_blackjack
    assert hand(T, A).is_blackjack
    assert not hand(A, A).is_blackjack
    assert not hand(T, T).is_blackjack
    assert not hand(A, Rank.FIVE, Rank.FIVE).is_blackjack  # 3-card 21


def test_pairs():
    assert hand(Rank.EIGHT, Rank.EIGHT).is_pair
    assert hand(Rank.EIGHT, Rank.EIGHT).pair_rank is Rank.EIGHT
    assert hand(T, T).is_pair
    assert not hand(A, Rank.SIX).is_pair
    assert hand(A, Rank.SIX).pair_rank is None
    assert not hand(T, T, T).is_pair


def test_bust():
    h = hand(T, T, Rank.FIVE)
    assert h.is_bust
    assert h.best_total == 25
    assert not hand(T, T).is_bust
