"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - self.current_location_id: the id of the player's current location in the game
        - ongoing: whether the game is ongoing
        - inventory: TODO: handle these instance attributes
        - score:
        - moves_used:
        - max_moves:
        - deposited:

    Representation Invariants:
        - self.current_location_id in self._locations
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    inventory: list[str]
    score: int
    moves_used: int
    max_moves: int
    deposited: set[str]

    required_items = {"usb drive", "laptop charger", "lucky mug"}

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.inventory = []
        self.score = 0
        self.moves_used = 0
        self.max_moves = 200
        self.deposited = set()

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW
        for item_data in data["items"]:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)
        all_loc_items = set()
        for loc in locations.values():
            all_loc_items.update(AdventureGame.normalize_item_name(x) for x in loc.items)

        for item in items:
            if AdventureGame.normalize_item_name(item.name) not in all_loc_items:
                print(f"The item '{item.name}' doesn't exist.")
        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]

    def game_lost(self) -> bool:
        """Return whether the player has used up the maximum number of moves."""
        return self.moves_used >= self.max_moves

    def game_won(self) -> bool:
        """Return whether all required items have been deposited at the target position."""
        return self.required_items.issubset(self.deposited) and self.current_location_id == 101

    @staticmethod
    def normalize_item_name(s: str) -> str:
        """Return a normalized item name for matching user input.
        """
        parts = s.strip().lower().split()
        return " ".join(parts)

    def get_item(self, name: str) -> Optional[Item]:
        """Return the Item object with the given name, or None if not found."""
        target = self.normalize_item_name(name)
        for item in self._items:
            if self.normalize_item_name(item.name) == target:
                return item
        return None

    def _find_in_location_items(self, location: Location, item: str) -> Optional[str]:
        """Return the actual item name stored in location.items matching user input, or None."""
        target = self.normalize_item_name(item)
        for name in location.items:
            if self.normalize_item_name(name) == target:
                return name
        return None

    def _find_in_inventory(self, item: str) -> Optional[str]:
        """Return the actual item name stored in inventory matching user input, or None."""
        target = self.normalize_item_name(item)
        for name in self.inventory:
            if self.normalize_item_name(name) == target:
                return name
        return None

    def take_item(self, item: str) -> str:
        """Return a message about whether the item is available to to be taken."""
        item = item.strip()
        if item == "":
            return "You did not enter an item."
        location = self.get_location()
        actual_name = self._find_in_location_items(location, item)
        if actual_name is None:
            return f"The {item} isn't here."
        location.items.remove(actual_name)
        self.inventory.append(actual_name)
        self.moves_used += 1
        return f"You got the {actual_name}!"

    def drop_item(self, item: str) -> str:
        """Return whether you successfully dropped the item at the current position."""
        item = item.strip()
        if item == "":
            return "You did not enter an item."
        location = self.get_location()
        actual_name = self._find_in_inventory(item)
        if actual_name is None:
            return f"You can't drop '{item}'. You don't have it yet."

        self.inventory.remove(actual_name)
        location.items.append(actual_name)
        self.moves_used += 1

        item_obj = self.get_item(actual_name)
        if item_obj is not None and location.id == item_obj.target_position:
            norm = self.normalize_item_name(actual_name)
            if norm not in self.deposited:
                self.score += item_obj.target_points
                self.deposited.add(norm)
                return f"You dropped {actual_name} at the right place! +{item_obj.target_points} points."
            else:
                return f"You dropped {actual_name}, but it is already there — no extra points."

        return f"You dropped {actual_name}."

    def log_action(self, game_log: EventList, command: str) -> None:
        """Record one chronological event after executing command."""
        loc = self.get_location()
        game_log.add_event(Event(loc.id, loc.long_description), command=command)

    def check_end(self) -> Optional[str]:
        """Return a message if the game ends, otherwise return None."""
        if self.game_lost():
            self.ongoing = False
            return "Time's up! You ran out of moves. The game is over. Take another try."
        if self.game_won():
            self.ongoing = False
            return ("You found all the missing items and brought them back to your dorm!\n"
                    "You submitted the project just in time. You win!")
        return None

if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        if choice.startswith("take "):
            item = choice[5:]
            message = game.take_item(item)
            print(message)
            game.log_action(game_log, choice)
            end_message = game.check_end()
            if end_message is not None:
                print(end_message)
            continue

        elif choice.startswith("drop "):
            item = choice[5:]
            message = game.drop_item(item)
            print(message)
            game.log_action(game_log, choice)
            end_message = game.check_end()
            if end_message is not None:
                print(end_message)
            continue

        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            elif choice == "look":
                print(location.long_description)
            elif choice == "quit":
                game.ongoing = False
            elif choice == "inventory":
                if game.inventory == []:
                    print("Your inventory is empty.")
                else:
                    print("You are carrying:")
                    for item in game.inventory:
                        print("-", item)
            elif choice == "score":
                print("Your current score is", game.score)
                game.log_action(game_log, choice)
        elif choice in location.available_commands:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result
            game.moves_used += 1
            game.log_action(game_log, choice)
        else:
            print("That was an invalid option, please try again.")
            continue
        end_message = game.check_end()
        if end_message is not None:
            print(end_message)

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game