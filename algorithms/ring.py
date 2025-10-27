# file: algorithms/ring.py

import threading
import time
import random
from framework import Node

class RingNode(Node):
    def __init__(self, node_id, network, num_nodes, num_requests=2):
        super().__init__(node_id, network, num_nodes, num_requests)
        self.next_node = (self.node_id + 1) % self.num_nodes
        self.has_token = (self.node_id == 0)
        self.wants_to_enter = False

    def pass_token(self):
        print(f"[Node {self.node_id}] passing token to Node {self.next_node}.")
        self.has_token = False
        self.network.send(self.node_id, self.next_node, 'TOKEN')

    def run(self):
        if self.has_token:
            time.sleep(1)
            self.pass_token()

        listener = threading.Thread(target=self.message_listener, daemon=True)
        listener.start()
        
        for _ in range(self.num_requests):
            time.sleep(random.uniform(1, 3))
            print(f"🤔 [Node {self.node_id}] wants to enter the CS.")
            self.wants_to_enter = True
            while self.wants_to_enter:
                time.sleep(0.1)

    def message_listener(self):
        while True:
            msg = self.inbox.get()
            if msg['type'] == 'TOKEN':
                self.has_token = True
                if self.wants_to_enter:
                    self.enter_critical_section()
                    self.exit_critical_section()
                    self.wants_to_enter = False
                self.pass_token()