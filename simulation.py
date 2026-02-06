"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate
an entire playthrough of the game. Please consult the project handout for
instructions and details.

You can copy/paste your code from Assignment 1 into this file, and modify it as
needed to work with your game.

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
from event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """
        Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from the location at initial_location_id
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)
        init_location = self._game.get_location()
        first_event = Event(init_location.id, init_location.long_description)
        self._events.add_event(first_event, None)
        self.generate_events(commands, init_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """
        Generate events in this simulation, based on current_location and commands, a valid list of commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from current_location
        """
        curr = current_location
        for command in commands:
            cmd = command.lower().strip()
            if cmd in curr.available_commands:
                next_id = curr.available_commands[cmd]
                self._game.current_location_id = next_id
                curr = self._game.get_location()
            elif cmd.startswith("take "):
                item = cmd[5:].strip()
                self._game.take_item(item)
            elif cmd.startswith("drop "):
                item = cmd[5:].strip()
                self._game.drop_item(item)
            elif cmd.startswith("talk to "):
                npc_name = cmd[8:].strip()
                self._game.talk_to(npc_name)
            elif cmd in {"look", "inventory", "score", "log", "quit"}:
                pass
            else:
                raise ValueError(f"Invalid command in simulation: {command!r}.")
            new_event = Event(curr.id, curr.long_description)
            self._events.add_event(new_event, cmd)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """
        return self._events.get_id_log()

    def run(self) -> None:
        """
        Run the game simulation and log location descriptions.
        """
        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    # provide a walkthrough of commands needed to win and lose the game
    win_walkthrough = ["take t-card",  # 101
                       "go south",  # 102
                       "go south",  # 103
                       "take spare room key",  # 103
                       "go south",  # 104
                       "pull",  # 105
                       "take usb drive",  # 105
                       "go north",  # 103
                       "go north",  # 102
                       "go east",  # 1
                       "go east",  # 10
                       "go west",  # 3
                       "show/drop t-card",  # 3
                       "go north",  # 301
                       "go west",  # 302
                       "up",  # 312
                       "go east",  # 311
                       "go north",  # 314
                       "take lucky mug",  # 314
                       "talk to the cafeteria staff",  # 314
                       "go south",  # 311
                       "go west",  # 312
                       "down",  # 302
                       "go east",  # 301
                       "go north",  # 3
                       "go west",  # 10
                       "go south",  # 11
                       "go south",  # 12
                       "go east",  # 4
                       "go east",  # 401
                       "take left note",  # 401 some puzzle here
                       "go north",  # 402
                       "take laptop charger",  # 402
                       "go south",  # 401
                       "go west",  # 4
                       "go west",  # 12
                       "go south",  # 6
                       "go south",  # 601
                       "take toonie",  # 601
                       "go east",  # 603
                       "talk to Professor Paul He",  # 603
                       "go west",  # 601
                       "go west",  # 602
                       "up",  # 612
                       "go east",  # 611 some puzzle here
                       "take a python reference book",  # 611
                       "go west",  # 612
                       "down",  # 602
                       "go east",  # 601
                       "go north",  # 6
                       "go north",  # 12
                       "go north",  # 11
                       "go north",  # 10
                       "go west",  # 1
                       "go west",  # 102
                       "go north",  # 101 some puzzle here
                       ]  # Create a list of all the commands needed to walk through your game to win it

    expected_log = [101, 101,  # 101, take t-card
                    102, 103, 103,  # go, go, take spare key
                    104, 105, 105,  # go, pull, take usb
                    103, 102, 1, 10, 3, 301, 302, 312, 311, 314, 314,  # move to 314, take mug
                    311, 312, 302, 301, 3, 10, 11, 12, 4, 401, 401,  # move 401, take note
                    402, 402,  # go north, take charger
                    401, 4, 12, 6, 601, 601,  # move to 601, take toonie
                    603, 601, 602, 612, 611, 611,  # move to 611, take book
                    612, 602, 601, 6, 12, 11, 10, 1, 102, 101  # go back to dorm room
                    ]  # Update this log list to include the IDs of all locations that would be visited

    sim = AdventureGameSimulation('game_data.json', 101, win_walkthrough)
    assert expected_log == sim.get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = ["go south", "go north"] * 101  # 202 moves
    expected_lose_log = [101] + [102,
                                 101] * 101  # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your demo
    sim = AdventureGameSimulation('game_data.json', 101, lose_demo)
    assert expected_log == sim.get_id_log()

    # Add code below to provide walkthroughs that show off certain features of the game
    # Create a list of commands involving visiting locations, picking up items, and then
    # checking the inventory, your list must include the "inventory" command at least once
    inventory_demo = ["take t-card", "inventory", "go south", "inventory"]
    expected_log = [101, 101, 101, 102, 102]
    sim = AdventureGameSimulation(AdventureGameSimulation('game_data.json', 101, inventory_demo))
    assert expected_log == sim.get_id_log()

    scores_demo = ["take t-card", "go south", "go east", "go east", "go west", "drop t-card", "score"]
    expected_log = [101, 101, 102, 1, 10, 3, 3, 3]
    sim = AdventureGameSimulation('game_data.json', 101, scores_demo)
    assert expected_log == sim.get_id_log()

    # Add more enhancement_demos if you have more enhancements
    # enhancement1_demo = [...]
    # expected_log = []
    # sim = AdventureGameSimulation(...)
    # assert expected_log == sim.get_id_log()
    print("All simulations passed!")

    # Note: You can add more code below for your own testing purposes
