# St. George Quest

A terminal text adventure set on the University of Toronto's St. George campus. Explore campus, talk to characters, and bring the required items back to the starting location before you run out of moves.

## Play

From the repository root, run `python adventure.py` with Python 3.10 or newer. The game uses only the standard library.

Type `look` to inspect your surroundings, follow a movement command listed on screen, or use `take <item>`, `drop <item>`, and `talk to <character>`. Use `save` and `restore` to manage a local save, or `quit` to exit.

## Structure

| File | Purpose |
| --- | --- |
| `adventure.py` | Terminal loop, game rules, and saving |
| `game_data.json` | Campus map, items, characters, and puzzles |
| `game_entities.py` | Game state and entity models |
| `event_logger.py` | Linked event log |
| `simulation.py` | Scripted walkthroughs |

The bundled walkthrough currently fails at a movement command that does not match the map. The interactive entry point runs independently.

Developed as a CSC111 course project at the University of Toronto. Course starter files retain their original attribution.
