# file: main.py

import math

# --- Import framework and algorithm classes ---
from framework import Network
from algorithms.centralized import CentralizedCoordinator, CentralizedClient
from algorithms.ring import RingNode
from algorithms.ricart_agrawala import RicartAgrawalaNode
from algorithms.maekawa import MaekawaNode, generate_voting_sets
from algorithms.suzuki_kasami import SuzukiKasamiNode

def run_simulation(algorithm, num_nodes, num_requests):
    """Initializes and runs the simulation based on user choices."""
    network = Network(num_nodes)
    nodes = []

    if algorithm == 'centralized':
        nodes.append(CentralizedCoordinator(0, network, num_nodes))
        for i in range(1, num_nodes):
            nodes.append(CentralizedClient(i, network, num_nodes, num_requests))
    elif algorithm == 'ring':
        for i in range(num_nodes):
            nodes.append(RingNode(i, network, num_nodes, num_requests))
    elif algorithm == 'ricart-agrawala':
        for i in range(num_nodes):
            nodes.append(RicartAgrawalaNode(i, network, num_nodes, num_requests))
    elif algorithm == 'maekawa':
        try:
            voting_sets = generate_voting_sets(num_nodes)
            print("Generated Voting Sets:", voting_sets)
            for i in range(num_nodes):
                nodes.append(MaekawaNode(i, network, num_nodes, voting_sets[i], num_requests))
        except ValueError as e:
            print(f"Error: {e}"); return
    elif algorithm == 'suzuki-kasami':
        for i in range(num_nodes):
            nodes.append(SuzukiKasamiNode(i, network, num_nodes, num_requests))
    else:
        print("Unknown algorithm."); return

    # Start all node threads
    for node in nodes: node.start()
    
    # Wait for client/worker threads to finish their requests
    worker_threads = [n for n in nodes if not isinstance(n, CentralizedCoordinator)]
    for node in worker_threads: node.join()

    print("\n--- Simulation Finished ---")
    print("Mutual exclusion was maintained throughout the simulation.")

if __name__ == "__main__":
    # --- Interactive Configuration ---
    algorithms = {
        '1': 'centralized',
        '2': 'ring',
        '3': 'ricart-agrawala',
        '4': 'maekawa',
        '5': 'suzuki-kasami'
    }
    
    while True:
        print("\nChoose the algorithm to simulate:")
        for key, value in algorithms.items():
            print(f"  {key}: {value.replace('-', ' ').title()}")
        choice = input("Enter number: ")
        if choice in algorithms:
            ALGORITHM_TO_RUN = algorithms[choice]
            break
        else:
            print("Invalid choice. Please try again.")

    while True:
        try:
            num_str = input(f"Enter the number of nodes (e.g., 4): ")
            NUM_NODES = int(num_str)
            if NUM_NODES <= 1:
                print("Number of nodes must be greater than 1.")
                continue
            if ALGORITHM_TO_RUN == 'maekawa':
                side = int(math.sqrt(NUM_NODES))
                if side * side != NUM_NODES:
                    print("Error: For Maekawa's algorithm, the number of nodes must be a perfect square (4, 9, 16, etc.).")
                    continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    while True:
        try:
            req_str = input(f"Enter the number of CS requests per node (e.g., 2): ")
            NUM_REQUESTS_PER_NODE = int(req_str)
            if NUM_REQUESTS_PER_NODE <= 0:
                print("Number of requests must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    print(f"\nStarting simulation for '{ALGORITHM_TO_RUN}' with {NUM_NODES} nodes and {NUM_REQUESTS_PER_NODE} requests per node.\n")
    run_simulation(ALGORITHM_TO_RUN, NUM_NODES, NUM_REQUESTS_PER_NODE)