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

from game_entities import Location, Item, NPC
from event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - self.current_location_id: the id of the player's current location in the game
        - ongoing: whether the game is ongoing
        - inventory: a list of item names currently held by the player
        - score: the player's current score based on deposited items
        - moves_used: the number of moves the player has made
        - max_moves: the maximum number of moves allowed before losing
        - deposited: a set of normalized item names that have been correctly placed
        - required items: a list of item which requires to win

    Representation Invariants:
        - self.current_location_id in self._locations
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.
    #   - _npcs: some none human characters

    _locations: dict[int, Location]
    _items: list[Item]
    _npcs: list[NPC]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    inventory: list[str]
    score: int
    moves_used: int
    max_moves: int
    deposited: set[str]
    required_items: set[str] = {"usb drive", "laptop charger", "lucky mug"}

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
        self._locations, self._items, self._npcs = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.inventory = []
        self.score = 0
        self.moves_used = 0
        self.max_moves = 200
        self.deposited = set()

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item], list[NPC]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)
        all_loc_items = set()
        for loc in locations.values():
            all_loc_items.update(AdventureGame.normalize_item_name(x) for x in loc.items)

        for itm in items:
            if AdventureGame.normalize_item_name(itm.name) not in all_loc_items:
                print(f"The item '{itm.name}' doesn't exist.")
        npcs = []
        for npc_data in data['NPC']:
            npc = NPC(npc_data['name'], npc_data['location_id'], npc_data.get['message'],
                      npc_data['required_item'], npc_data['success_message'], npc_data['given_hint'])
            npcs.append(npc)

        return locations, items, npcs

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
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
        for itm in self._items:
            if self.normalize_item_name(itm.name) == target:
                return itm
        return None

    def _find_in_location_items(self, curr_location: Location, loc_item: str) -> Optional[str]:
        """Return the actual item name stored in location.items matching user input, or None."""
        target = self.normalize_item_name(loc_item)
        for name in curr_location.items:
            if self.normalize_item_name(name) == target:
                return name
        return None

    def _find_in_inventory(self, inv_item: str) -> Optional[str]:
        """Return the actual item name stored in inventory matching user input, or None."""
        target = self.normalize_item_name(inv_item)
        for name in self.inventory:
            if self.normalize_item_name(name) == target:
                return name
        return None

    def take_item(self, avail_item: str) -> str:
        """Return a message about whether the item is available to be taken."""
        avail_item = avail_item.strip()
        if avail_item == "":
            return "You did not enter an item."
        curr_location = self.get_location()
        actual_name = self._find_in_location_items(curr_location, avail_item)
        if actual_name is None:
            return f"The {avail_item} isn't here."
        curr_location.items.remove(actual_name)
        self.inventory.append(actual_name)
        self.moves_used += 1
        return f"You got the {actual_name}!"

    def drop_item(self, avail_item: str) -> str:
        """Return whether you successfully dropped the item at the current position."""
        avail_item = avail_item.strip()
        if avail_item == "":
            return "You did not enter an item."
        curr_location = self.get_location()
        actual_name = self._find_in_inventory(avail_item)
        if actual_name is None:
            return f"You can't drop '{avail_item}'. You don't have it yet."

        self.inventory.remove(actual_name)
        curr_location.items.append(actual_name)
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

    def log_action(self, curr_log: EventList, cmd: str) -> None:
        """Record one chronological event after executing command."""
        loc = self.get_location()
        curr_log.add_event(Event(loc.id, loc.long_description), command=cmd)

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

    def location_format(self, loc: Location, visited: bool) -> str:
        """Return a string representation of the location's description based on whether
        it has been visited before.
        """
        header = f"LOCATION {loc.id}\n"
        if visited:
            return header + loc.long_description
        else:
            return header + loc.brief_description

    def update_item_description(self, item_name: str, new_description: str) -> None:
        """Find the item and modify its description"""
        item_obj = self.get_item(item_name)
        if item_obj:
            item_obj.description = new_description

    def undo(self, curr_game_log: EventList) -> str:
        """
        Reverts the game state to the previous event, including position,
        inventory, and score synchronization.
        """
        if curr_game_log.is_empty() or curr_game_log.first == curr_game_log.last:
            return "Nothing to undo."

        # 1. Get the current state being removed
        current_event = curr_game_log.last
        cmd = current_event.prev_command

        # 2. Reverse the logic based on the command type
        if cmd:
            if cmd.startswith("take "):
                item_name = cmd[5:].strip()
                actual_name = self._find_in_inventory(item_name)
                if actual_name:
                    self.inventory.remove(actual_name)
                    self.get_location().items.append(actual_name)

            elif cmd.startswith("drop "):
                item_name = cmd[5:].strip()
                actual_name = self._find_in_location_items(self.get_location(), item_name)
                if actual_name:
                    self.get_location().items.remove(actual_name)
                    self.inventory.append(actual_name)
                    # Revert score if the item was dropped at target
                    norm_name = self.normalize_item_name(actual_name)
                    if norm_name in self.deposited:
                        item_obj = self.get_item(actual_name)
                        if item_obj:
                            self.score -= item_obj.target_points
                            self.deposited.remove(norm_name)

        # 3. Remove the state from the linked list
        curr_game_log.remove_last_event()

        # 4. Move player back to the new 'last' event ID
        self.current_location_id = curr_game_log.last.id_num
        if self.moves_used > 0:
            self.moves_used -= 1

        return f"Undone! You are back at: {self.get_location().name}"

    def save_game(self, filename: str = "savegame.json") -> str:
        """Serializes the core game state into a JSON file."""
        state = {
            "current_location_id": self.current_location_id,
            "inventory": self.inventory,
            "score": self.score,
            "moves_used": self.moves_used,
            "deposited": list(self.deposited),
            "ongoing": self.ongoing
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
        return "Game progress saved to savegame.json."

    def restore_game(self, filename: str = "savegame.json") -> str:
        """Loads and overwrites current game attributes from a save file."""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            self.current_location_id = state["current_location_id"]
            self.inventory = state["inventory"]
            self.score = state["score"]
            self.moves_used = state["moves_used"]
            self.deposited = set(state["deposited"])
            self.ongoing = state["ongoing"]
            return "Game restored from file!"
        except FileNotFoundError:
            return "No save file found."

    def _find_npc_here(self, npcs_name: str) -> NPC | None:
        """Return the NPC with this name at the current location, if there is no such NPC, return None."""
        target_npc = self.normalize_item_name(npcs_name)
        for npc in self._npcs:
            if npc.location_id == self.current_location_id and self.normalize_item_name(npc.name) == target_npc:
                return npc
        return None

    def talk_to(self, npcs_name: str) -> str:
        """Interact with the NPC at the current location."""
        npcs_name = npcs_name.strip()
        if npcs_name == "":
            return "Who do you want to talk to?"

        npc = self._find_npc_here(npcs_name)
        if npc is None:
            return f"There is no one here named '{npcs_name}'."

        if npc.given_hint:
            return f"{npc.name}: We've already talked."

        if npc.required_item:
            required_item = self.normalize_item_name(npc.required_item)
            have_it = any(self.normalize_item_name(x) == required_item for x in self.inventory)
            if not have_it:
                return f"{npc.name}: {npc.message}"

            npc.given_hint = True
            if npc.success_message:
                return f"{npc.name}: {npc.success_message}"
            return f"{npc.name}: Thanks!"
        else:
            npc.given_hint = True
            return f"{npc.name}: {npc.message}"


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        #  Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event

        # Depending on whether it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        print(game.location_format(location, visited=location.visited))
        location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        executed = False

        if choice.startswith("take "):
            item = choice[5:]
            message = game.take_item(item)
            print(message)
            executed = True

        elif choice.startswith("drop "):
            item = choice[5:]
            message = game.drop_item(item)
            print(message)
            executed = True

        elif choice.startswith("talk to "):
            npc_name = choice[8:]
            message = game.talk_to(npc_name)
            print(message)
            executed = True

        if not executed:
            while choice not in location.available_commands and choice not in menu:
                print("That was an invalid option; try again.")
                choice = input("\nEnter action: ").lower().strip()

            print("========")
            print("You decided to:", choice)

            if choice in menu:
                # Handle each menu command as appropriate
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
                executed = True
            elif choice in location.available_commands:
                # Handle non-menu actions
                result = location.available_commands[choice]
                game.current_location_id = result
                game.moves_used += 1
                executed = True
            else:
                print("That was an invalid option, please try again.")
                continue
        if executed:
            game.log_action(game_log, choice)
            end_message = game.check_end()
            if end_message is not None:
                print(end_message)

            # Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # Add in code to deal with special locations (e.g. puzzles) as needed for your game
