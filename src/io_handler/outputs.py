from abc import ABC, abstractmethod


class OutputHandler(ABC):
    """
    Abstract base class for handling game outputs.
    """

    def __init__(self, player_names: dict[int:str]):
        self.player_names = player_names

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
    def show_stats(self, stats: list[dict[int, list[int]]], card_stack_count: int):
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

    def show_stats(self, stats: list[dict[int, list[int]]], card_stack_count: int):
        """
        Prints the player stats to the console.
        """
        max_len = max(len(name) for name in self.player_names.values())

        print(f"\nCards left: {card_stack_count}")
        for i in range(len(stats)):
            print(
                f"{self.player_names[stats[i]['player_idx']].ljust(max_len)} has -- {stats[i]['money']} money -- {stats[i]['cows']} cows -- {stats[i]['score']} score."
            )

    def show_final_score(self, scores: list[int]):
        """
        Prints the final score.
        """
        for score in scores:
            print(f"{self.player_names[scores.index(score)]} has {score} points.")
