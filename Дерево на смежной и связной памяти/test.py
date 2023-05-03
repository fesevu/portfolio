class Node:
    def __init__(self, data:float, key:int) -> None:
        if isinstance(data, (float, int)) is False:
            raise TypeError("data must be float or int")
        if isinstance(key, int) is False:
            raise TypeError("key must be int")
        
        self.data = data
        self.key = key
        self.right:Node = None
        self.left:Node = None
    
    def __str__(self) -> str:
        return str(self.data)     

class LinkedTree:
    max_data_length = 0
    def __init__(self, root:Node = None) -> None:
        if (isinstance(root, Node) is False) and (root is not None):
            raise TypeError("tree accepts only Node type")
        self.root = root  

    def __del__(self) -> None:
        self = None    

    def add(self, data:float, key:int) -> None: #добавляем в правое поддерево узел с большим ключом и в левое поддерево - с меньшим или если нет корня создаем корень
        if isinstance(data, (float, int)) is False:
            raise TypeError("data must be float or int")
        if isinstance(key, int) is False:
            raise TypeError("key must be int")
        
        if len(str(data)) > self.max_data_length:
            self.max_data_length = len(str(data))
        
        new_node = Node(data, key)
        if self.root == None:
            self.root = new_node
            return
        
        prev_node:Node = None
        current_node:Node = self.root  

        while (current_node):
            if current_node.key == key:
                current_node.data = data
                return
            elif current_node.key > key:
                prev_node = current_node
                current_node = current_node.left
            elif current_node.key < key:
                prev_node = current_node
                current_node = current_node.right

        if prev_node.key > key:
          prev_node.left = new_node
        elif prev_node.key < key:
          prev_node.right = new_node            

    def get(self, key:int) -> float:
        if isinstance(key, int) is False:
            raise TypeError("key must be int")
        
        current_node:Node = self.root

        while (current_node):
            if current_node.key == key:
                return current_node
            elif current_node.key > key:
                current_node = current_node.left
            elif current_node.key < key:
                current_node = current_node.right      

        raise KeyError("no such element in tree")
    
    def remove(self, key:int) -> None:
        if isinstance(key, int) is False:
            raise TypeError("key must be int")
        if self.root == None:
            raise ValueError("tree is empty")
        
        prev_node:Node = None
        current_node:Node = self.root
        
        while(current_node):
            if current_node.key == key:
                break
            elif current_node.key > key:
                prev_node = current_node
                current_node = current_node.left
            elif current_node.key < key:
                prev_node = current_node
                current_node = current_node.right

        if current_node.right == None:
            if prev_node == None:
                self.root = current_node.left
            else:
                if current_node == prev_node.left:
                    prev_node.left = current_node.left
                else:
                    prev_node.right = current_node.left
        else:
            prev_far_left:Node = current_node
            far_left:Node = current_node.right

            while (far_left.left): #ищем крайний левый элемент, а значит самый маленький элемент в правом поддереве элемента, который нужно удалить
                prev_far_left = far_left
                far_left = far_left.left

            far_left.left = current_node.left #присваеваем крайнему левому левого сына узла который нужно удалить
            

            if prev_node == None:
                self.root = far_left  
            elif current_node == prev_node.left:
                prev_node.left = far_left 
            else:
                prev_node.right = far_left     
    """""
    Доработать вертикальный вывод дерева
    def printTreeVert(self) -> None:
        if self.root == None:
            print("Tree is empty")    

        levels:list = []

        queue:list = [[self.root]] #очередь чтобы пройтись по каждому узлу
        level:int = 0
        while len(queue) > 0:  
            level_elements:list = queue[0]
          
            levels_temp:list = []
            queue_temp:list = []
            j = 0          
            while len(level_elements) > 0:
                current_node:Node = level_elements.pop(0)
                
                if current_node is not None:
                   queue_temp.append(current_node.left)
                   queue_temp.append(current_node.right)
                elif j <= 2**level:   
                   queue_temp.append(current_node)

                if current_node is not None: 
                   levels_temp.append(current_node.data)
                else:
                   levels_temp.append(current_node) 

                j += 1         

            queue.pop(0)
            if len(queue_temp) > 0:
               queue.append(queue_temp)

            for i in range(2**level):
                try:
                    levels_temp[i]
                except IndexError:
                    levels_temp.append(None)           

            levels.append(levels_temp)

            level += 1

        print(levels)    

        levels.pop(len(levels) - 1) #удаление последней строки она всегда будет пустая
   
        length_last_level = self.max_data_length * (2*(len(levels[len(levels) - 1])) - 1)
        #длина строки необходима на последний уровень дерева = длина самого большего числа * количество элементов в том числе None + количество пробелов

        for i in range(len(levels)):
            max_length = (2*(2**(len(levels) - 1 - i))) * self.max_data_length #максимальная длина выделяемая на узел
            start = max_length // 2 - self.max_data_length
            ended = max_length - start - self.max_data_length
            for j in range(len(levels[i])):
                if (i == len(levels) - 1): #нижний уровень дерева
                    start:int = 0
                    ended = self.max_data_length            

                if levels[i][j] is not None:
                    print(" "*(start + self.max_data_length - len(str(levels[i][j]))) + str(levels[i][j]), end=" "*ended)
                else:
                    print(" "*(start + self.max_data_length), end=" "*ended)
            
            #print() 
            max_length1 = (2*(2**(len(levels) - 2 - i))) * self.max_data_length #максимальная длина выделяемая на узел следующего уровня
            start1 = max_length1 // 2 - self.max_data_length
            ended1 = max_length1 - start1 - self.max_data_length
            print(levels[i])
            if (i != len(levels) - 1):
                for j in range(len(levels[i])):
                    if levels[i + 1][2*j] is not None:
                        print(" "*(start1 + self.max_data_length) + "/" + "-"*(start- start1 - self.max_data_length - 1), end="")
                    else:
                        print(" "*(start1 + self.max_data_length) + " "*(start - start1 - self.max_data_length), end="")  

                    if levels[i + 1][2*j + 1] is not None:
                        print(" "*self.max_data_length + "-"*(start - start1 - self.max_data_length - 1) + "\\", end=(ended1 + self.max_data_length)*" ")
                    else:
                        print(" "*self.max_data_length + " "*(start - start1 - self.max_data_length - 1) + " ", end=ended1*" ")      

            print()
        """    
       
class Trunk:
    def __init__(self, prev=None, str=None):
        self.prev = prev
        self.str = str
 
def showTrunks(p):
    if p is None:
        return
    showTrunks(p.prev)
    print(p.str, end='')
 
def printTree(root, prev, isLeft):
    if root is None:
        return
 
    prev_str = '    '
    trunk = Trunk(prev, prev_str)
    printTree(root.right, trunk, True)
 
    if prev is None:
        trunk.str = '———'
    elif isLeft:
        trunk.str = '.———'
        prev_str = '   |'
    else:
        trunk.str = '`———'
        prev.str = prev_str
 
    showTrunks(trunk)
    print(' ' + str(root.data))
    if prev:
        prev.str = prev_str
    trunk.str = '   |'
    printTree(root.left, trunk, False)

lt = LinkedTree()
lt.add(33, 33)
lt.add(5, 5)
lt.add(3, 3)
lt.add(35, 35)
lt.add(20, 20)
lt.add(99, 99)
lt.add(31, 31)
lt.add(17, 17)
lt.add(4, 4)
lt.add(18, 18)

printTree(lt.root, None, False)
#lt.printTreeVert()

print(lt.get(31))
lt.remove(20)
lt.remove(33)
lt.add(10000, 10000)
lt.add(96, 96)
lt.add(95, 95)
lt.add(110, 110)
lt.add(105, 105)
lt.add(101, 101)
lt.add(106, 106)
#lt.printTreeVert()

printTree(lt.root, None, False)
