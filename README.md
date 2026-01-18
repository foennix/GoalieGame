# Neuer: The Goalkeeper Game

Welcome to **Neuer: The Goalkeeper Game**! Put yourself in the shoes of the legendary Manuel Neuer and defend your goal against a barrage of penalty shots.

## Features
- **Pixel Art Graphics**: Retro style visuals.
- **Simple Controls**: Play with just the keyboard.
- **High Scores**: Compete with yourself or friends.
- **Progressive Difficulty**: The game gets faster as you score more points.

## Requirements
- MacOSX (or any OS that supports Python and Pygame)
- Python 3.8+
- Pygame

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Set up a virtual environment (Recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## How to Play

1.  **Run the game**:
    ```bash
    python3 main.py
    ```

2.  **Controls**:
    - **Left Arrow**: Dive Left
    - **Right Arrow**: Dive Right
    - **Up Arrow**: Jump / Block High Center
    - **Down Arrow**: Stay Low / Ready Center
    - **Space**: Restart Game (on Game Over screen)

3.  **Objective**:
    - Block the incoming balls!
    - Each save earns you 100 points.
    - If a ball enters the goal, you lose a life.
    - Game Over after 3 goals allowed.

## Troubleshooting

If you encounter issues running the game on Mac:
- Ensure you have the latest version of Python installed.
- If you see no window or errors about video drivers, ensure your terminal has permissions to record screen/access windows (System Preferences -> Security & Privacy).

Enjoy the game!
