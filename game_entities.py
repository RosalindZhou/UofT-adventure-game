"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: A unique integer identifier for this location.
        - name: The short name of the location.
        - brief_description: A one-line description shown when the user has visited before.
        - long_description: A detailed description shown when the user presses "look".
        - available_commands: A dictionary mapping direction/command strings to the destination location ID.
        - items: A list of item names currently present at this location.
        - visited: A boolean indicating if the player has been to this location before.

    Representation Invariants:
        - self.id_num >= 0
        - all(dest >= 0 for dest in self.available_commands.values())
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    id: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool

    def look(self) -> str:
        """Return the current location's long description."""
        return self.long_description


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item, used for picking up and dropping.
        - description: A short description of the item.
        - start_position: The ID of the location where the item is initially placed.
        - target_position: The ID of the location where the item should be delivered for points.
        - target_points: The number of points awarded when the item is at its target position.

    Representation Invariants:
        - self.start_position >= 0
        - self.target_position >= 0
        - self.target_points >= 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int

    def is_at_target(self, current_location_id: int) -> bool:
        """Check if this item is at the target location."""
        return current_location_id == self.target_position

    def get_score_if_target(self, current_location_id: int) -> int:
        """If this item is at the target location, return its score."""
        if self.is_at_target(current_location_id):
            return self.target_points
        else:
            return 0


@dataclass
class Player:
    """A class representing the player in the game.

    Instance Attributes:
        - current_location: The ID of the location where the player is currently.
        - inventory: A list of item names that the player is carrying.
        - score: The player's current total score.
        - moves_left: The number of moves remaining before the game ends.

    Representation Invariants:
        - self.current_location >= 0
        - self.score >= 0
        - self.moves_left >= 0
        - len(set(self.inventory)) == len(self.inventory)
    """
    current_location: int
    inventory: list[str]
    score: int = 0
    moves_left: int = 40

    def move(self, new_location_id: int) -> None:
        """Update the player's current location and score."""
        self.current_location = new_location_id
        self.moves_left -= 1

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.moves_left <= 0


@dataclass
class Puzzle:
    """A special location that requires a puzzle to be solved before proceeding.

    Instance Attributes:
        - answer: The correct string or ID needed to solve the puzzle.
        - solved: A boolean indicating whether the puzzle has been completed.
        - puzzle_prompt: The question or hint displayed to the player.
        - reward_item: An item name given to the player upon solving (optional).

    Representation Invariants:
        - len(self.answer) > 0
    """
    location: Location
    answer: str
    puzzle_prompt: str
    solved: bool
    reward_item: str

    def attempt_solve(self, player_guess: str) -> bool:
        """Check if the player can solve the puzzle."""
        if player_guess.lower() == self.answer.lower():
            self.solved = True
            return True
        return False


@dataclass
class NPC:
    """A non-player character in the text adventure game.

    Instance Attributes:
        - name: The name of the NPC.
        - location_id: The ID of the location where this NPC is currently located.
        - message: The dialogue the NPC speaks when the player talks to them.
        - required_item: The name of an item the player must have to trigger a special
          interaction (e.g., 't-card' for rb).
        - given_hint: A boolean tracking if the NPC has already provided their hint/reward.

    Representation Invariants:
        - self.name != ""
        - self.location_id >= 0
    """
    name: str
    location_id: int
    message: str
    required_item: str = ""
    given_hint: bool = False

    def interact(self, player_inventory: list[str]) -> str:
        """Return the dialogue if the player shows their item"""
        if not self.required_item or self.required_item in player_inventory:
            return f"{self.name}: {self.message}"
        return f"{self.name} seems to waiting for some item..."
# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })
