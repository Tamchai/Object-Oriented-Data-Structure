# data_structures.py
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return temp.data
    
    def peek(self):
        return self.front.data if self.front else None
    
    def get_all(self):
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items

class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.down = None
        self.left = None
        self.up = None

class Menu2DLinkedList:
    def __init__(self):
        self.root = None
        self.current = None
        self.all_nodes = []
    
    def create_battle_menu(self):
        fight = LinkedListNode("Fight")
        bag = LinkedListNode("Bag")
        pokemon = LinkedListNode("Pokémon")
        run = LinkedListNode("Run")
        
        fight.right = bag
        bag.left = fight
        bag.right = pokemon
        pokemon.left = bag
        pokemon.right = run
        run.left = pokemon
        
        self.root = fight
        self.current = fight
        self.all_nodes = [fight, bag, pokemon, run]
        return fight
    
    def create_move_menu(self, moves):
        if not moves:
            return None
        
        nodes = [LinkedListNode(move.name if hasattr(move, 'name') else move) for move in moves]
        self.all_nodes = nodes
        
        if len(nodes) >= 1:
            self.root = nodes[0]
        
        if len(nodes) >= 2:
            nodes[0].right = nodes[1]
            nodes[1].left = nodes[0]
        
        if len(nodes) >= 3:
            nodes[0].down = nodes[2]
            nodes[2].up = nodes[0]
        
        if len(nodes) >= 4:
            nodes[1].down = nodes[3]
            nodes[3].up = nodes[1]
            nodes[2].right = nodes[3]
            nodes[3].left = nodes[2]
        
        self.current = self.root
        return self.root
    
    def move_right(self):
        if self.current and self.current.right:
            self.current = self.current.right
            return True
        return False
    
    def move_left(self):
        if self.current and self.current.left:
            self.current = self.current.left
            return True
        return False
    
    def move_down(self):
        if self.current and self.current.down:
            self.current = self.current.down
            return True
        return False
    
    def move_up(self):
        if self.current and self.current.up:
            self.current = self.current.up
            return True
        return False
    
    def get_current_data(self):
        return self.current.data if self.current else None
    
    def get_current_index(self):
        if not self.current or not self.all_nodes:
            return 0
        try:
            return self.all_nodes.index(self.current)
        except ValueError:
            return 0
    
    def reset_to_first(self):
        self.current = self.root

class TreeNode:
    def __init__(self, area_name, stage_range):
        self.area_name = area_name
        self.stage_range = stage_range
        self.children = []
        self.parent = None
    
    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

class AreaTree:
    def __init__(self):
        self.root = None
        self.current_node = None
        self.build_tree()
    
    def build_tree(self):
        # Root
        self.root = TreeNode("Start", (0, 0))
        
        # Level 1: Stages 1-10
        forest = TreeNode("Forest", (1, 10))
        self.root.add_child(forest)
        
        # Level 2: Stages 11-20
        cave = TreeNode("Cave", (11, 20))
        forest.add_child(cave)
        
        # Level 3: Stages 21-30
        tower1 = TreeNode("Tower", (21, 30))
        cave.add_child(tower1)
        
        # Level 4: Stages 31-40
        beach = TreeNode("Beach", (31, 40))
        tower1.add_child(beach)
        
        # Level 5: Stages 41-50
        tower2 = TreeNode("Tower", (41, 50))
        beach.add_child(tower2)
        
        self.current_node = self.root
    
    def get_available_areas(self):
        if not self.current_node:
            return []
        return [(child.area_name, child.stage_range) for child in self.current_node.children]
    
    def select_area(self, index):
        if self.current_node and 0 <= index < len(self.current_node.children):
            self.current_node = self.current_node.children[index]
            return self.current_node.area_name
        return None
    
    def get_area_for_stage(self, stage_number):
        def find_area(node, stage):
            if node.stage_range[0] <= stage <= node.stage_range[1]:
                return node.area_name
            for child in node.children:
                result = find_area(child, stage)
                if result:
                    return result
            return None
        
        result = find_area(self.root, stage_number)
        return result if result else "Forest"