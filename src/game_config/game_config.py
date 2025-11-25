class GameConfig:
    # Kartenwerte
    COW_CARD_VALUES = [10]  # , 20, 40, 70, 100]  # z. B.
    DONKEY_COW = COW_CARD_VALUES[0]

    # Geldkarten
    MONEY_CARD_VALUES = [0, 10, 50, 100, 200, 500]
    STARTING_MONEY = [3, 3, 5, 0, 0, 0]  # Anzahl pro Wert

    # Spielregeln
    COPIES_PER_COW = 4
    MAX_PLAYERS = 4
    MIN_PLAYERS = 2
