from dataclasses import dataclass


@dataclass
class PublicView:
    """Defines the attributes which each player is allowed to see publicly"""

    player_idx: int
    player_name: str
    cow_cards: list[int] | None
    money_cards_count: int
    score: int


@dataclass
class PrivateView:
    """Defines the attributes which only the current player is allowed to see"""

    money_card_values: list[int]
    money_value: int
    joint_cows: dict[int, list[int]] | None = (
        None  # cows which other players also own. This attribute is not actually private but needed here for convenience
    )


@dataclass
class PlayerView:
    """Defines the visible and not visible player attributes"""

    current_player_idx: int
    public: list[PublicView]
    private: PrivateView
