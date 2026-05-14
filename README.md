# Chess Engine Clone in Python

Credit: **Eddie Sharick (Eddie)**  
Tutorial Playlist: https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY

This repository reconstructs a Chess Engine using Python as an introductory Artificial Intelligence and game development project.

The project is designed for students and beginner developers who want to explore:

- Game state management
- Chess rule implementation
- Search algorithms in AI
- Decision-making systems
- Optimization techniques in game engines

The engine is fully playable and includes several classical Chess AI algorithms such as:

- MinMax
- NegaMax
- Alpha-Beta Pruning

---

# Tech Stack

- Python
- Pygame

---

# Project Overview

This project focuses on both game logic and AI search algorithms.

The repository contains two different implementations of check-detection systems:

| Version | Description |
|---|---|
| `main.py` + `engine.py` | Traditional piece-to-king threat detection |
| `main2.py` + `engine2.py` | King-origin scanning method |

The primary playable and fully completed version of the engine is:

```bash
main.py
```

which is supported by:

```bash
engine.py
```

The secondary version exists for experimentation and comparison between two different algorithmic approaches to detecting checks.

> Note: `main2.py` and `engine2.py` are still experimental and not fully completed yet.

---

# Highlight Features

## 1. Multiple Game Modes

The engine supports multiple gameplay configurations using simple boolean flags inside:

```bash
main.py
```

```python
playerOne = False
playerTwo = False
```

- `playerOne` controls the White side
- `playerTwo` controls the Black side

Configuration rules:

| Value | Meaning |
|---|---|
| `True` | Human player |
| `False` | AI player |

Examples:

| Configuration | Result |
|---|---|
| `True / True` | Human vs Human |
| `True / False` | Human vs AI |
| `False / True` | AI vs Human |
| `False / False` | AI vs AI |

This flag-based structure makes the engine easy to configure while demonstrating conditional execution systems in game development.

---

## 2. Adjustable AI Difficulty

The AI search depth can be adjusted in:

```bash
settings.py
```

through:

```python
DEPTH
```

Increasing depth allows the AI to search further into future positions, producing stronger moves at the cost of longer computation time.

General behavior:

| Depth | Result |
|---|---|
| Lower depth | Faster but weaker AI |
| Higher depth | Slower but stronger AI |

---

## 3. Two Different Check Detection Systems

One of the educational goals of this project is to demonstrate that the same problem can be solved using different algorithmic perspectives.

### Version 1 — Piece-to-King Detection

Files:

```bash
main.py
engine.py
```

This method evaluates all opposing pieces and determines whether any of them attack the king.

Conceptually:

```text
Enemy Pieces → King
```

This is the primary and currently used implementation.

---

### Version 2 — King-Origin Detection

Files:

```bash
main2.py
engine2.py
```

This method starts from the king’s position and scans outward in every direction to identify attacking enemy pieces.

Conceptually:

```text
King → Enemy Pieces
```

This alternative implementation was created to compare efficiency, structure, and readability between two different approaches to the same chess problem.

---

## 4. AI System

The AI logic is implemented inside:

```bash
SmartMoveFinder.py
```

This file contains:

- Move evaluation systems
- Board scoring
- Move ordering
- Recursive search algorithms
- Experimental AI implementations

Some algorithms inside the file are not actively used in the main gameplay loop anymore, but they are intentionally preserved to demonstrate the progression and development of the engine.

This allows learners to observe:

- Algorithm evolution
- Incremental optimization
- Different search strategies
- Tradeoffs between simplicity and performance

---

# AI Algorithms

## MinMax Algorithm

### Definition

MinMax is a classical decision-making algorithm used in turn-based two-player games.

The algorithm assumes:

- The AI attempts to maximize its advantage
- The opponent attempts to minimize the AI’s advantage

The engine recursively explores future positions and evaluates the best possible move.

---

### Application in Chess

The engine generates a move tree:

```text
Move → Countermove → Countermove → ...
```

Each position is evaluated using:

- Material count
- Piece values
- Board control
- Positional strength

The AI then chooses the move with the best evaluated outcome.

---

## NegaMax Algorithm

### Definition

NegaMax is a simplified variation of MinMax.

Instead of maintaining separate maximizing and minimizing functions, NegaMax uses score negation to represent the opponent’s perspective.

This significantly simplifies recursive search implementation.

---

### Why It Matters

Benefits include:

- Cleaner recursion
- Less duplicated code
- Easier maintenance
- Easier integration with Alpha-Beta Pruning

---

## Alpha-Beta Pruning

### Definition

Alpha-Beta Pruning optimizes MinMax/NegaMax by eliminating branches that cannot affect the final decision.

This reduces unnecessary calculations.

---

### Result

Benefits include:

- Faster move search
- Deeper search depth
- Better performance
- More efficient AI evaluation

Without pruning:

```text
Every possible branch is explored
```

With pruning:

```text
Irrelevant branches are skipped
```

---

# Move Logging

A move log panel is displayed beside the chessboard to track every move made during the game.

This feature demonstrates:

- State tracking
- UI synchronization
- Move history systems
- Interactive feedback design

---

# Directory Structure

```bash
Chess-Engine/
│
├── Chess-engine-clone/
│   ├── engine.py
│   ├── engine2.py
│   ├── main.py
│   ├── main2.py
│   ├── settings.py
│   ├── SmartMoveFinder.py
│   └── image/
│
├── .gitignore
├── LICENSE
└── README.md
```

---

# Important Files

## `main.py`

Primary executable file.

Responsibilities:

- Starts the game
- Handles the main game loop
- Processes player input
- Updates the display
- Connects the AI with the engine

This is the recommended and fully supported entry point for the project.

---

## `engine.py`

Primary chess engine implementation.

Responsibilities:

- Game state management
- Legal move generation
- Check/checkmate detection
- Piece movement rules
- Castling, en passant, promotion
- Move validation

Uses the:

```text
Piece → King
```

check-detection approach.

---

## `main2.py`

Alternative executable used for testing the second check-detection system.

Works together with:

```bash
engine2.py
```

This version is still incomplete and mainly exists for experimentation and learning purposes.

---

## `engine2.py`

Alternative engine implementation using:

```text
King → Piece
```

threat scanning.

Created mainly for experimentation, comparison, and learning purposes.

---

## `SmartMoveFinder.py`

Contains all AI-related logic.

Includes:

- Random move selection
- Basic board evaluation
- MinMax
- NegaMax
- Alpha-Beta Pruning
- Recursive search systems

Some functions are legacy or experimental implementations kept intentionally to demonstrate the engine’s development process.

---

## `settings.py`

Stores global constants and configuration values such as:

- Board dimensions
- Colors
- FPS
- AI depth settings
- Asset settings

---

## `image/`

Contains chess piece images and visual assets used by Pygame.

---

# Run Locally

Clone the repository:

```bash
git clone <your-repository-link>
```

Go to the project directory:

```bash
cd Chess-engine-clone
```

Install dependencies:

```bash
pip install pygame
```

Run the main version:

```bash
python main.py
```

Experimental alternative version:

```bash
python main2.py
```

---

# Educational Purpose

This project was built not only as a playable chess engine, but also as a learning platform for:

- Beginner AI programming
- Recursive algorithms
- Search optimization
- State management
- Game development
- Algorithmic thinking

By studying the repository, learners can observe how a chess engine evolves from:

```text
Random Moves
→ Board Evaluation
→ MinMax
→ NegaMax
→ Alpha-Beta Optimization
```


# Conclusion

This repository serves as both:

- A functional chess engine
- An educational AI project

It demonstrates how classical AI algorithms can be applied to a real interactive system while also introducing students to software architecture, optimization, and game logic design.

The project aims to make Chess AI approachable, understandable, and practical for beginners interested in Computer Science and Artificial Intelligence.
