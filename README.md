# Chess Engine Clone in Python

Credit by: ***Eddie Sharick (Eddie)*** (link: https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY)

This repository aims to reconstruct Chess engine clone using Python as an introductory project to a high-school student
to get familiar with the concept of ***AI algorithms*** (such as Minimax, NegaMax, AlphaBeta Pruning).

## Instructions
Clone the repository: 

Install dependencies (if any):

Run the game: python main.py
## Highlight Features

#### 1. **Flag-Based Execution**
The chess engine is run by flags, allowing flexible control over different modes (human vs. human, human vs. AI, or AI vs. AI). This design teaches students how to build configurable applications that adapt to different scenarios.

#### 2. **Check Detection Engines**
Two different approaches are implemented to detect checks:
* **Piece-to-King Method:** Evaluates all opposing pieces to see if they threaten the king.
* **King-Origin Method:** Starts from the king’s position and checks outward for threats.  
This dual-engine design illustrates multiple algorithmic solutions to the same problem.

#### 3. **AI Move Trigger**
The AI is triggered programmatically to make moves by coding the materials (piece values, board evaluation, and move generation). This shows how logical evaluation connects with automated decision-making.

#### 4. **MinMax Algorithm (Spotlight)**
* **Definition:** MinMax is a decision-making algorithm used in two-player games. It explores all possible moves, assuming both players play optimally. The AI tries to **maximize its advantage** while the opponent tries to **minimize it**.
* **Application in Chess:** The engine generates a tree of possible moves and counter-moves, then evaluates the best outcome for the AI based on piece values and board position.

#### 5. **NegaMax Algorithm (Spotlight)**
* **Definition:** NegaMax is a streamlined version of MinMax that leverages the symmetry of two-player games. Instead of separately maximizing and minimizing, it uses a single evaluation function with negation to represent the opponent’s perspective.
* **Application in Chess:** This reduces code complexity while maintaining the same decision-making power as MinMax, making the AI logic more elegant and efficient.

#### 6. **Alpha-Beta Pruning (Spotlight)**
* **Definition:** Alpha-Beta Pruning is an optimization of MinMax. It eliminates branches of the move tree that cannot possibly affect the final decision, drastically reducing the number of positions the AI needs to evaluate.
* **Application in Chess:** This allows the AI to “think deeper” within the same time constraints, improving performance without sacrificing accuracy.

#### 7. **Move Logging**
A move log window is displayed on the right side of the chessboard. This feature tracks all moves made during the game, reinforcing the importance of state management and user feedback in interactive applications.

## Conclusion
This project is both a learning tool and a playable chess engine.  
By exploring the code, students will:
* Learn how to run applications with flags for flexible configuration
* Understand multiple approaches to detecting checks in chess
* See how AI is triggered to make moves based on coded materials
* Explore how **MinMax, NegaMax, and Alpha-Beta Pruning** simulate strategic thinking
* Gain confidence in building interactive applications with move logging and state tracking

 