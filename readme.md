# Distributed Mutual Exclusion Algorithms Simulator

This project provides a Python-based simulation framework for visualizing and comparing classical distributed mutual exclusion algorithms. The simulator allows users to interactively choose an algorithm, set the number of participating nodes, and specify the number of critical section requests per node.

The primary goal of this project is to offer a hands-on demonstration of the core concepts, trade-offs, and mechanics behind different approaches to achieving mutual exclusion in a distributed system without shared memory.

## Features

- **Interactive CLI:** A simple command-line interface to configure and run simulations.
- **Concurrent Simulation:** Utilizes Python's `threading` module to simulate concurrent processes (nodes).
- **Message Passing Model:** A `Network` class with message queues (`queue.Queue`) simulates asynchronous message passing between nodes.
- **Safety Verification:** Includes a runtime assertion to verify that the safety property (at most one process in the critical section at a time) is never violated.
- **Modular and Extensible:** The code is structured with a clear separation between the simulation framework and the algorithm implementations, making it easy to add new algorithms.

## Algorithms Implemented

The simulator includes implementations of the following five classical algorithms:

1.  **Centralized Algorithm:** A simple coordinator-based approach.
2.  **Ring-Based Algorithm:** A token-passing approach on a logical ring.
3.  **Ricart-Agrawala Algorithm:** A fully decentralized, permission-based algorithm using Lamport timestamps.
4.  **Maekawa's Algorithm:** A more efficient, quorum-based optimization.
5.  **Suzuki-Kasami Algorithm:** A token-based broadcast algorithm.

## Project Structure

The project is organized into a framework and an `algorithms` package for clarity and modularity.

```
mutual_exclusion_project/
├── main.py                     # Main script to run the simulation (handles user input)
├── framework.py                # Core simulation classes (Node, Network) and safety checks
├── algorithms/
│   ├── __init__.py           # Makes 'algorithms' a Python package
│   ├── centralized.py        # Implements the Centralized algorithm
│   ├── ring.py               # Implements the Ring-Based algorithm
│   ├── ricart_agrawala.py    # Implements the Ricart-Agrawala algorithm
│   ├── maekawa.py            # Implements Maekawa's algorithm
│   └── suzuki_kasami.py      # Implements the Suzuki-Kasami algorithm
└── README.md                   # This file
```

## Prerequisites

- Python 3.x

No external libraries are required to run this simulation.

## Setup

1. **Navigate to the project directory:**
    ```bash
    cd mutual_exclusion_project
    ```

## How to Run

1.  Execute the main script from the root directory of the project:
    ```bash
    python main.py
    ```

2.  Follow the interactive prompts in your terminal:
    - First, you will be asked to **choose an algorithm** by entering its corresponding number.
    - Next, you will be prompted to enter the **number of nodes** for the simulation.
    - Finally, you will enter the **number of critical section requests** each node should make.

    **Note for Maekawa's Algorithm:** The number of nodes must be a perfect square (e.g., 4, 9, 16) for the voting set generation to work. The program will validate this.

## Example Usage

Here is an example of a terminal session to run Maekawa's algorithm with 4 nodes:

```bash
$ python main.py
```

## Sample Terminal Output (For Maekawa algorithm)

Choose the algorithm to simulate:  
  1: Centralized  
  2: Ring  
  3: Ricart Agrawala  
  4: Maekawa  
  5: Suzuki Kasami  
Enter number: 4  
Enter the number of nodes (e.g., 4): 4  
Enter the number of CS requests per node (e.g., 2): 2  

Starting simulation for 'maekawa' with 4 nodes and 2 requests per node.  

Network initialized for 4 nodes.  
Generated Voting Sets: {0: {0, 1, 2}, 1: {0, 1, 3}, 2: {0, 2, 3}, 3: {1, 2, 3}}  
🤔 [Node 3] wants CS, requesting from {1, 2, 3}.  
✅ [Node 3] has entered the critical section.  
🤔 [Node 2] wants CS, requesting from {0, 2, 3}.  
❌ [Node 3] is exiting the critical section.  
✅ [Node 2] has entered the critical section.  
🤔 [Node 0] wants CS, requesting from {0, 1, 2}.  
❌ [Node 2] is exiting the critical section.  
🤔 [Node 1] wants CS, requesting from {0, 1, 3}.  
✅ [Node 0] has entered the critical section.  
❌ [Node 0] is exiting the critical section.  
✅ [Node 1] has entered the critical section.  
❌ [Node 1] is exiting the critical section.  
🤔 [Node 2] wants CS, requesting from {0, 2, 3}.  
✅ [Node 2] has entered the critical section.  
❌ [Node 2] is exiting the critical section.  
🤔 [Node 3] wants CS, requesting from {1, 2, 3}.  
🤔 [Node 1] wants CS, requesting from {0, 1, 3}.  
🤔 [Node 0] wants CS, requesting from {0, 1, 2}.  
✅ [Node 3] has entered the critical section.  
❌ [Node 3] is exiting the critical section.  
✅ [Node 1] has entered the critical section.  
❌ [Node 1] is exiting the critical section.  
✅ [Node 0] has entered the critical section.  
❌ [Node 0] is exiting the critical section.  

--- Simulation Finished ---  
Mutual exclusion was maintained throughout the simulation.  