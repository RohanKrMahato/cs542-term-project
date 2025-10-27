# file: framework.py

import threading
import queue
import time
import random

# --- Global state for safety verification ---
CRITICAL_SECTION_COUNTER = 0
LOCK = threading.Lock()

class Network:
    """Simulates the message-passing network."""
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.inboxes = {i: queue.Queue() for i in range(num_nodes)}
        print(f"Network initialized for {num_nodes} nodes.")

    def send(self, sender_id, recipient_id, message_type, **kwargs):
        message = {'sender': sender_id, 'type': message_type, **kwargs}
        self.inboxes[recipient_id].put(message)
        time.sleep(random.uniform(0.01, 0.05))

    def broadcast(self, sender_id, message_type, **kwargs):
        for i in range(self.num_nodes):
            if i != sender_id:
                self.send(sender_id, i, message_type, **kwargs)

    def get_inbox(self, node_id):
        return self.inboxes[node_id]

class Node(threading.Thread):
    """Base class for a node in the distributed system."""
    def __init__(self, node_id, network, num_nodes, num_requests=2):
        super().__init__()
        self.node_id = node_id
        self.network = network
        self.num_nodes = num_nodes
        self.inbox = network.get_inbox(node_id)
        self.num_requests = num_requests
        self.daemon = True

    def enter_critical_section(self):
        global CRITICAL_SECTION_COUNTER
        with LOCK:
            CRITICAL_SECTION_COUNTER += 1
            assert CRITICAL_SECTION_COUNTER == 1, f"MUTUAL EXCLUSION VIOLATED! Count: {CRITICAL_SECTION_COUNTER}"
        print(f"✅ [Node {self.node_id}] has entered the critical section.")
        time.sleep(random.uniform(0.1, 0.3))

    def exit_critical_section(self):
        global CRITICAL_SECTION_COUNTER
        print(f"❌ [Node {self.node_id}] is exiting the critical section.")
        with LOCK:
            CRITICAL_SECTION_COUNTER -= 1