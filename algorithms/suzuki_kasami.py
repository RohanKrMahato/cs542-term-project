# file: algorithms/suzuki_kasami.py

import threading
import time
import random
from framework import Node

class SuzukiKasamiNode(Node):
    def __init__(self, node_id, network, num_nodes, num_requests=2):
        super().__init__(node_id, network, num_nodes, num_requests)
        self.RN = [0] * self.num_nodes
        self.has_token = (self.node_id == 0)
        self.token = {'Q': [], 'LN': [0] * self.num_nodes} if self.has_token else None

    def run(self):
        listener = threading.Thread(target=self.message_listener, daemon=True)
        listener.start()
        for i in range(self.num_requests):
            time.sleep(random.uniform(1, 3))
            print(f"🤔 [Node {self.node_id}] wants to enter the CS.")
            request_sn = self.RN[self.node_id] + 1
            self.RN[self.node_id] = request_sn
            self.network.broadcast(self.node_id, 'REQUEST', sn=request_sn)
            while not self.has_token:
                time.sleep(0.1)
            self.enter_critical_section()
            self.exit_critical_section()
            self.token['LN'][self.node_id] = self.RN[self.node_id]
            for j in range(self.num_nodes):
                if j not in self.token['Q'] and self.RN[j] == self.token['LN'][j] + 1:
                    self.token['Q'].append(j)
            if self.token['Q']:
                next_node = self.token['Q'].pop(0)
                print(f"[Node {self.node_id}] passing token to Node {next_node}.")
                self.has_token = False
                self.network.send(self.node_id, next_node, 'TOKEN', token_data=self.token)
                self.token = None

    def message_listener(self):
        while True:
            msg = self.inbox.get()
            sender = msg['sender']
            if msg['type'] == 'REQUEST':
                self.RN[sender] = max(self.RN[sender], msg['sn'])
            elif msg['type'] == 'TOKEN':
                self.has_token = True
                self.token = msg['token_data']