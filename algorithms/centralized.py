# file: algorithms/centralized.py

import queue
import time
import random
from framework import Node

class CentralizedCoordinator(Node):
    def __init__(self, node_id, network, num_nodes, num_requests=0):
        super().__init__(node_id, network, num_nodes, num_requests)
        self.token_held = False
        self.request_queue = queue.Queue()

    def run(self):
        print(f"[Coordinator {self.node_id}] is running.")
        while True:
            try:
                msg = self.inbox.get(timeout=1)
                sender = msg['sender']
                if msg['type'] == 'REQUEST':
                    if not self.token_held:
                        self.token_held = True
                        self.network.send(self.node_id, sender, 'GRANT')
                    else:
                        self.request_queue.put(sender)
                elif msg['type'] == 'RELEASE':
                    if not self.request_queue.empty():
                        next_node = self.request_queue.get()
                        self.network.send(self.node_id, next_node, 'GRANT')
                    else:
                        self.token_held = False
            except queue.Empty:
                pass

class CentralizedClient(Node):
    def run(self):
        for _ in range(self.num_requests):
            time.sleep(random.uniform(0.5, 1.5))
            print(f"🤔 [Node {self.node_id}] wants to enter the CS.")
            self.network.send(self.node_id, 0, 'REQUEST') # Coordinator is node 0
            grant_msg = self.inbox.get()
            if grant_msg['type'] == 'GRANT':
                self.enter_critical_section()
                self.exit_critical_section()
                self.network.send(self.node_id, 0, 'RELEASE')