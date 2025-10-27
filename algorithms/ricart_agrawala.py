# file: algorithms/ricart_agrawala.py

import threading
import time
import random
import queue
from framework import Node

class RicartAgrawalaNode(Node):
    def __init__(self, node_id, network, num_nodes, num_requests=2):
        super().__init__(node_id, network, num_nodes, num_requests)
        self.state = 'RELEASED'
        self.my_timestamp = 0
        self.logical_clock = 0
        self.replies_needed = 0
        self.deferred_queue = []

    def handle_message(self, msg):
        self.logical_clock = max(self.logical_clock, msg.get('timestamp', 0)) + 1
        sender = msg['sender']
        if msg['type'] == 'REQUEST':
            if (self.state == 'HELD' or 
               (self.state == 'WANTED' and (self.my_timestamp, self.node_id) < (msg['timestamp'], sender))):
                self.deferred_queue.append(sender)
            else:
                self.network.send(self.node_id, sender, 'REPLY', timestamp=self.logical_clock)
        elif msg['type'] == 'REPLY':
            self.replies_needed -= 1

    def run(self):
        listener = threading.Thread(target=self.message_listener, daemon=True)
        listener.start()
        for _ in range(self.num_requests):
            time.sleep(random.uniform(0.5, 2))
            self.state = 'WANTED'
            self.logical_clock += 1
            self.my_timestamp = self.logical_clock
            self.replies_needed = self.num_nodes - 1
            print(f"🤔 [Node {self.node_id}] wants CS with timestamp {self.my_timestamp}.")
            self.network.broadcast(self.node_id, 'REQUEST', timestamp=self.my_timestamp)
            while self.replies_needed > 0:
                time.sleep(0.05)
            self.state = 'HELD'
            self.enter_critical_section()
            self.exit_critical_section()
            self.state = 'RELEASED'
            for node_id in self.deferred_queue:
                self.network.send(self.node_id, node_id, 'REPLY', timestamp=self.logical_clock)
            self.deferred_queue.clear()
    
    def message_listener(self):
        while True:
            try:
                msg = self.inbox.get(timeout=1)
                self.handle_message(msg)
            except queue.Empty:
                pass