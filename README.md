*This project has been created as part of the 42 curriculum by kmathuri, ysimonne.*

# Description

This project is a modern recreation of the 1980 Namco classic, **Pac-Man**, developed in Python 3.10+. The goal is to navigate Pac-Man through a maze, eating all pacgums while avoiding four unique ghosts. This version emphasizes modular software architecture, robust error handling, and professional project management standards.

# Features

* **Dynamic Maze Generation:** Every level (except the first) is randomly generated using an external module.
* **Progressive Difficulty:** At least 10 levels of increasing challenge.
* **Cheat Mode:** Special keys for evaluation:
* `i`: Invincibility.
* `l`: Level skip.
* `e`: Extra life.


* **UI/HUD:** Real-time display of score, lives, level, and remaining time.

# Instructions

## Installation

Install the required dependencies using the Makefile:

```bash
make install

```

## Execution

Launch the game by providing a configuration file:

```bash
python3 pac-man.py config.json

```

## Other Commands

* `make run`: Run the game with the default config.
* `make lint`: Run `flake8` and `mypy` for code quality.
* `make clean`: Remove temporary caches and files.

# Implementation Section

The game is built using **Pygame** to handle the graphical loop and user inputs. We focused on a non-crashing experience by implementing extensive `try-except` blocks and context managers for file handling, ensuring no Python tracebacks are ever shown to the user.

# General Software Architecture

The project follows an Object-Oriented approach with four primary modules:

* **Engine:** Manages the main game loop, event handling, and high-level state transitions.
* **Game:** Handles the logic of the current level, including collision detection and timing.
* **Menu:** Controls the Main Menu, Highscore view, and Pause screens.
* **GameSprite:** The base class for all moving entities (Pac-Man and Ghosts), managing movement and animations.

# Configuration

The game is configured via a JSON file that supports comments (lines starting with `#`).
**Key Parameters:**

* `lives`: Number of starting lives (Default: 3).
* `points_per_pacgum`: Score for small dots.
* `seed`: Fixed seed for the first level (Default: 42).
* `level_max_time`: Seconds allowed per level.

# Highscore System

Scores are stored in a local `highscores.json` file.

* **Why:** We chose JSON for its human-readability and ease of integration with Python's standard library.
* **Logic:** It stores the Top 10 players. If the file is missing or corrupted, the system initializes a new empty record to prevent crashes.

# Maze Generation

The project integrates an external **A-Maze-ing** package from another group via Git:
`git@vogsphere.42nice.fr:vogsphere/intra-uuid-9600eecf-bbb3-4caf-8dfb-dba26de66eed-7292331-kmathuri`
Our loader adapts to their interface to fetch a maze grid with the `PERFECT` parameter set to `False` to ensure open corridors.

# Project Management

We used **Linear** for task tracking and progress monitoring.
Detailed evidence, including Kanban view and progress logs, can be found in the [project-management](./project-management) directory.

## Resources & AI Usage

* **Pygame Documentation:** [https://www.pygame.org/docs/](https://www.pygame.org/docs/)

**AI Usage Statement:**
AI tools were utilized to:

1. Generate compliant **docstrings** following Google style.
2. Draft this **README** structure based on the subject requirements.
3. Automate **linting** fixes and static type hint suggestions for `mypy`.
4. Generate initial technical **documentation** for the internal modules.

---

**Play the game on [Itch.io](https://itch.io)**