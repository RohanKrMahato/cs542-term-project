# file: algorithms/maekawa.py

import threading
import time
import random
import math
import queue
from framework import Node

def generate_voting_sets(N):
    side = int(math.sqrt(N))
    if side * side != N:
        raise ValueError("Maekawa's algorithm requires N to be a perfect square.")
    voting_sets = {}
    for i in range(N):
        row, col = i // side, i % side
        row_set = {r * side + col for r in range(side)}
        col_set = {row * side + c for c in range(side)}
        voting_sets[i] = row_set.union(col_set)
    return voting_sets

class MaekawaNode(Node):
    def __init__(self, node_id, network, num_nodes, voting_set, num_requests=2):
        super().__init__(node_id, network, num_nodes, num_requests)
        self.state = 'RELEASED'
        self.voting_set = voting_set
        self.votes_received = 0
        self.has_voted = False
        self.request_queue = queue.Queue()

    def handle_message(self, msg):
        sender = msg['sender']
        if msg['type'] == 'REQUEST':
            if self.state == 'HELD' or self.has_voted:
                self.request_queue.put(sender)
            else:
                self.has_voted = True
                self.network.send(self.node_id, sender, 'REPLY')
        elif msg['type'] == 'REPLY':
            self.votes_received += 1
        elif msg['type'] == 'RELEASE':
            if not self.request_queue.empty():
                next_node = self.request_queue.get()
                self.network.send(self.node_id, next_node, 'REPLY')
            else:
                self.has_voted = False
    
    def run(self):
        listener = threading.Thread(target=self.message_listener, daemon=True)
        listener.start()
        for _ in range(self.num_requests):
            time.sleep(random.uniform(0.5, 2))
            self.state = 'WANTED'
            self.votes_received = 0
            print(f"🤔 [Node {self.node_id}] wants CS, requesting from {self.voting_set}.")
            for voter_id in self.voting_set:
                self.network.send(self.node_id, voter_id, 'REQUEST')
            while self.votes_received < len(self.voting_set):
                time.sleep(0.05)
            self.state = 'HELD'
            self.enter_critical_section()
            self.exit_critical_section()
            self.state = 'RELEASED'
            for voter_id in self.voting_set:
                self.network.send(self.node_id, voter_id, 'RELEASE')

    def message_listener(self):
        while True:
            try:
                msg = self.inbox.get(timeout=1)
                self.handle_message(msg)
            except queue.Empty:
                pass