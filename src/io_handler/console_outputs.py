from abc import ABC, abstractmethod
from game.player_view import PlayerView

class OutputHandler(ABC):
    """
    Abstract base class for handling game outputs.
    """

    @abstractmethod
    def show_message(self, message: str):
        """
        Displays a generic message to the user.
        """
        pass

    @abstractmethod
    def show_cow_draw(self, cow_value: int):
        """
        Displays the current cow card up for auction.
        """
        pass

    @abstractmethod
    def show_donkey_event(self, money_value: int):
        """
        Displays the event when a donkey card is drawn.
        """
        pass

    @abstractmethod
    def show_last_card_drawn(self):
        """
        Displays the event when the last card is drawn from the stack.
        """
        pass

    @abstractmethod
    def show_stats(self, player_view: PlayerView, card_stack_count: int):
        """
        Displays the player stats.
        """
        pass

    @abstractmethod
    def show_final_score(self, scores: list[int]):
        """
        Displays the final scores.
        """
        pass


class ConsoleOutputHandler(OutputHandler):
    """
    Concrete implementation of OutputHandler for the console.
    """

    def show_message(self, message: str):
        """
        Prints a generic message to the console.
        """
        print(message)

    def show_cow_draw(self, cow_value: int):
        """
        Prints the current cow card up for auction to the console.
        """
        print(f"Bid for COW {cow_value}!")

    def show_donkey_event(self, money_value: int):
        """
        Prints the donkey event to the console.
        """
        print(f"It's a donkey! The bank will give each player {money_value} money.")

    def show_last_card_drawn(self):
        """
        Prints the last card drawn event to the console.
        """
        print("Last card was drawn.")

    def show_stats(self, player_view: PlayerView, card_stack_count: int):
        """
        Prints the player stats to the console.
        """
        max_len = max(len(pub_view.player_name) for pub_view in player_view.public)

        print(f"\nCards left: {card_stack_count}")
        for pub_view in player_view.public:
            print(f"{pub_view.player_name.ljust(max_len)} has -- {pub_view.money_cards_count} money cards -- {pub_view.cow_cards} cows -- {pub_view.score} score.")
        
        print(f"Your money cards: {player_view.private.money_card_values}\n")

    def show_final_score(self, player_view: PlayerView):
        """
        Prints the final score.
        """
        for view in player_view.public:
            print(f"{view.player_name} has {view.score} points.")  