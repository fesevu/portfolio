class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        
class BinaryTree:
    def __init__(self):
        self.root = None
        
    def insert(self, key):
        if not self.root:
            self.root = Node(key)
        else:
            self._insert(key, self.root)
            
    def _insert(self, key, node):
        if key < node.val:
            if node.left:
                self._insert(key, node.left)
            else:
                node.left = Node(key)
        else:
            if node.right:
                self._insert(key, node.right)
            else:
                node.right = Node(key)
    
    def delete(self, key):
        if self.root:
            self.root = self._delete(key, self.root)
    
    def _delete(self, key, node):
        if not node:
            return node
        
        if key < node.val:
            node.left = self._delete(key, node.left)
        elif key > node.val:
            node.right = self._delete(key, node.right)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            temp = self._min_value_node(node.right)
            node.val = temp.val
            node.right = self._delete(temp.val, node.right)
        
        return node
    
    def search(self, key):
        return self._search(key, self.root) is not None
    
    def _search(self, key, node):
        if not node or node.val == key:
            return node
        
        if key < node.val:
            return self._search(key, node.left)
        return self._search(key, node.right)
    
    def _min_value_node(self, node):
        current = node
        
        while current.left:
            current = current.left
            
        return current
        
    def pre_order_traversal(self):
        if self.root:
            self._pre_order_traversal(self.root)
            print("")
            
    def _pre_order_traversal(self, node):
        if node:
            print(node.val, end=" ")
            self._pre_order_traversal(node.left)
            self._pre_order_traversal(node.right)
            
    def post_order_traversal(self):
        if self.root:
            self._post_order_traversal(self.root)
            print("")
            
    def _post_order_traversal(self, node):
        if node:
            self._post_order_traversal(node.left)
            self._post_order_traversal(node.right)
            print(node.val, end=" ")
    
    def in_order_traversal(self):
        if self.root:
            self._in_order_traversal(self.root)
            print("")
            
    def _in_order_traversal(self, node):
        if node:
            self._in_order_traversal(node.left)
            print(node.val, end=" ")
            self._in_order_traversal(node.right)
            
    def count_nodes(self):
        return self._count_nodes(self.root)
    
    def _count_nodes(self, node):
        if not node:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
    
    def depth(self):
        return self._depth(self.root)
    
    def _depth(self, node):
        if not node:
            return 0
        
        left_depth = self._depth(node.left)

        right_depth = self._depth(node.right)
        
        return max(left_depth, right_depth) + 1
        
    def is_empty(self):
        return self.root is None
    
    def clear(self):
        self.root = None
        
    def print_tree(self):
        if self.root:
            self._print_tree(self.root, 0)
    
    def _print_tree(self, node, level):
        if node:
            self._print_tree(node.right, level + 1)
            print(f"{' ' * 4 * level}{node.val}")
            self._print_tree(node.left, level + 1)

tree = BinaryTree()
tree.insert(50)
tree.insert(30)
tree.insert(20)
tree.insert(40)
tree.insert(70)
tree.insert(60)
tree.insert(80)

tree.print_tree()

# Вывод:
#        80
#    70
#        60
#50
#        40
#    30
#        20

tree.delete(20)
tree.delete(30)

tree.print_tree()

# Вывод:
#        80
#    70
#        60
#50
#        40

print(tree.search(50))  # True
print(tree.search(100)) # False

tree.pre_order_traversal()   # 50 40 70 60 80 
tree.post_order_traversal()  # 40 60 70 80 50
tree.in_order_traversal()    # 40 50 60 70 80

print(tree.count_nodes()) # 5
print(tree.depth())       # 3

tree.clear()

print(tree.is_empty()) # True
