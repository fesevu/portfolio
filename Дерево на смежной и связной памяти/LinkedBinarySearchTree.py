"""Структура бинарного дерева должна иметь следующие функции:

1) Добавление нового элемента в дерево +

2) Удаление элемента из дерева +

3) Поиск элемента в дереве +

4) Обход дерева в прямом порядке (префиксном) +

5) Обход дерева в обратном порядке (постфиксном) +

6) Обход дерева в симметричном порядке (инфиксном) +

7) Получение количества элементов в дереве +

8) Вычисление глубины дерева +

9) Проверка дерева на пустоту +

10) Очистка дерева от всех элементов. +

Напиши класс бинарного дерева со всеми этими функциями на языке Python"""

class Node:
    def __init__(self, key, data = None) -> None:
        self.key = key
        if data is None:
            self.data = key
        else:
            self.data = data    
        self.left:Node = None
        self.right:Node = None

class Trunk: #класс веток, хранит префикс который выводится на экран для каждой строчки. Для этого хранит ссылку на ветку для предыдующего элемента и строку самого элемента        
    def __init__(self, prev=None, str=None):
        self.prev = prev
        self.str = str
 
    def showTrunks(trunk): #печатаем ветку
        if trunk is None: #если уперлись до "роидтельского элеммента" для ветки корнего узла
            return
        Trunk.showTrunks(trunk.prev) #чтобы начать печатать с ветки для корнего узла для текущего уровня
        print(trunk.str, end="")    

class LinkedBinaryTree:
    def __init__(self, key = None, data = None) -> None:
        if key is None:
            self.root = None
        else:
            self.root = Node(key, data)    

    def __del__(self) -> None:
        self = None

    def __add(self, new_node, root):
        if root is None:
            return
        
        if new_node.key == root.key: #если ключи совпадают перезаписываем
            root.data = new_node.data
        elif new_node.key < root.key:
            if root.left: #если левый сын то переходим в левое поддерево
                self.__add(new_node, root.left)
            else: #иначе записываем новый узел в левого сына
                root.left = new_node
        else: #ключ больше ключа текущего узла
            if root.right:
                self.__add(new_node, root.right)
            else:
                root.right = new_node    

        return                 

    def add(self, key, data = None) -> None: #добавляем узел
        new_node = Node(key, data)
        if self.root is None: #если нет корня
            self.root = new_node
            return
        else: #корень есть
            self.__add(new_node, self.root)

    def remove(self, key) -> None:
        node, prev_node, isLeft = self.__findNode(key, self.root)

        if node:  #если сущетсвует узел
            if node.right: #если у узла есть правый сын
                leftmost_element, prev_leftmost_element = self.__minimum(node.right, node)
                if prev_node is None: #предудщий узел отсутсвует то есть удаляем корень дерева
                    self.root = leftmost_element #в корень ставим найденный левый узел
                    if prev_leftmost_element != node: #если крайний левый узел не является правым сыном удаляемого узла
                        prev_leftmost_element.left = leftmost_element.right #правое поддерево найденного узла поднимаем в левое поддерево родителя
                        leftmost_element.left = node.left #левый узел удаляемого узла становится левым узлом крайнего левого узла
                        leftmost_element.right = node.right #правый узел удаляемого узла становится правым узлом крайнего левого узла
                    
                else: #общий случай
                    if isLeft:
                        prev_node.left = leftmost_element #заменяем ссылку на удаляемый узел на крайний левый узел в левом поддереве
                    else:
                        prev_node.right = leftmost_element #в правом поддереве

                    if prev_leftmost_element != node: #если крайний левый узел не является правым сыном удаляемого узла
                        prev_leftmost_element.left = leftmost_element.right #правое поддерево найденного узла поднимаем в левое поддерево родителя
                        leftmost_element.left = node.left #левый узел удаляемого узла становится левым узлом крайнего левого узла
                        leftmost_element.right = node.right #правый узел удаляемого узла становится правым узлом крайнего левого узла
            else: #в других случая
                if prev_node is None: #предудщий узел отсутсвует то есть удаляем корень дерева
                    self.root = self.root.left
                elif isLeft: #если узел левый тогда заменяем ссылку левого сына родительского узла на левую ссылку узла, если у узла нет ни правого ни левого сына, то node.left будет None и соответсвенно просто удалиться ссылку у родительского узла на удаляемый узел
                    prev_node.left = node.left
                else:
                    prev_node.right = node.left   
        else: #если не существует такого узла
            raise KeyError("node is not in tree")    

    def clear(self, key_root = None) -> None: #очищаем дерево / поддерево
        if self.root is None:
            return
        if key_root is None:
            key_root = self.root.key

        current_node:Node = self.__findNode(key_root, self.root)[0] #находим узел, который ялвяется корнем дерева / поддеревва

        if current_node is None:
            raise KeyError("node is not in tree")
        
        if current_node == self.root:
            self.root = None
        else:
            prev_node:Node = self.root
            while(prev_node):
                if prev_node.right == current_node:
                    prev_node.right = None
                    return
                elif prev_node.left == current_node:   
                    prev_node.left = None
                    return
                elif current_node.key < prev_node.key:
                    prev_node = prev_node.left
                elif current_node.key > prev_node.key:
                    prev_node = prev_node.right    

    def __findNode(self, key, root:Node): #-> list(Node, Node, bool): #находит узел, родителя узла и определяет левый или правый сын
        prevNode:Node = None
        isLeft = None
        current_node:Node = root
        while(current_node and key != current_node.key):
            if key < current_node.key:
                isLeft = True
                prevNode = current_node
                current_node = current_node.left
            elif key > current_node.key:
                isLeft = False
                prevNode = current_node
                current_node = current_node.right

        return current_node, prevNode, isLeft 
    
    def __findKey(self, value, root:Node):
        if value == root.data:
            return root.key
        
        key = self.__findKey(value, root.left)
        if key is None:
            key = self.__findKey(value, root.right)

    def findKey(self, value, key_root = None): #получаем ключ по значению, возваращет None если нет такого узла
        if key_root is None: #если не указан ключ корня, то ставим по умолчанию ключ кореня дерева
            key_root = self.root.key
        
        root:Node = self.__findNode(key_root, self.root)[0] #находим корневой элеммента дерева / поддерева
        key = self.__findKey(value, root)

        return key
        
    def find(self, key, key_root = None): #получаем значение по ключу, если нет ключа возвращает None
        if self.root is None:
            raise ValueError("tree is empty")
        if key_root is None:
            key_root = self.root.key

        root:Node = self.__findNode(key_root, self.root)[0] #находим узел корня которого подали в функцию
        node:Node = self.__findNode(key, root)[0] #нахоим узел значение которого нужно получить
        if node is None:
            return None
        else:
            return node.data

    def isEmpty(self, key_root = None) -> bool: #проверяем пустое ли дерево/поддерево
        if self.root is None:
            return True
        if key_root is None:
            key_root = self.root.key

        current_node:Node = self.__findNode(key_root, self.root)[0]

        if current_node is None:
            raise KeyError("node is not in tree")

        if self.root is None: #если корень дерево пустой, то дерево пустое
            return True
        else:
            return False        
    
    def __nodeCount(self, root:Node) -> None: #рекурсивная функция для нахождения кол-во узлов в дереве
        if root is None:
            return 0 
        #если корень сущетствует увеличиться счётчик
        node_count = 1
        node_count += self.__nodeCount(root.left) #переходим к левому сыну
        node_count += self.__nodeCount(root.right) #переходим к правому сыну

        return node_count

    def nodeCount(self, key_root = None) -> int: #количество узлов в дереве / поддереве
        if self.root is None:
            return 0
        if key_root is None:
            key_root = self.root.key

        root:Node = self.__findNode(key_root, self.root)[0] #находим узел по ключу

        return self.__nodeCount(root)
    
    def __depth(self, root:Node):
        if root is None:
            return 0

        left_depth = self.__depth(root.left) #глубина левого поддерева

        right_depth = self.__depth(root.right) #глубина правого поддерева
        
        return max(left_depth, right_depth) + 1 #возвращаем глубину поддерева учитывая корень поддерева

    def depth(self, key_root = None) -> int: #глубина дерева / поддерева
        if self.root is None:
            return 0
        if key_root is None:
            key_root = self.root.key

        root:Node = self.__findNode(key_root, self.root)[0] #находим узел по ключу 

        return self.__depth(root)
    
    def __maximum(self, root:Node, prev_node):
        maximum = root
        if root.right:
            maximum, prev_node = self.__maximum(root.right, root)
        
        return maximum, prev_node

    def maximum(self, key_root = None):
        if self.root is None:
            raise ValueError("tree is empty")
        if key_root is None:
            key_root = self.root.key

        root, prev_node = self.__findNode(key_root, self.root)[0:2] #находим узел по ключу

        if root: #если узел найден в дереве
            return self.__maximum(root, prev_node)[0].data
        else:
            raise KeyError("node is not in tree") 
    
    def __minimum(self, root:Node, prev_node:Node):
        minimum = root
        if root.left:
            minimum, prev_node = self.__minimum(root.left, root)
        
        return minimum, prev_node

    def minimum(self, key_root = None):
        if self.root is None:
            raise ValueError("tree is empty")
        if key_root is None:
            key_root = self.root.key

        root, prev_node = self.__findNode(key_root, self.root)[0:2] #находим узел по ключу

        if root: #если нйаден узел в дереве
            return self.__minimum(root, prev_node)[0].data
        else:
            raise KeyError("node is not in tree")
    
    def __preOrderTraversal(self, root:Node, pre_order_traversal):
        if root is None:
            return
        
        pre_order_traversal.append(root.data)
        self.__preOrderTraversal(root.left, pre_order_traversal)
        self.__preOrderTraversal(root.right, pre_order_traversal)

    
    def preOrderTraversal(self, key_root = None):
        pre_order_traversal = []

        if self.root is None:
            return pre_order_traversal
        if key_root is None:
            key_root = self.root.key

        root:Node = self.__findNode(key_root, self.root)[0] #находим узел по ключу

        self.__preOrderTraversal(root, pre_order_traversal)

        return pre_order_traversal
    
    def __postOrderTraversal(self, root:Node, post_order_traversal):
        if root is None:
            return
        
        self.__postOrderTraversal(root.left, post_order_traversal)
        self.__postOrderTraversal(root.right, post_order_traversal)
        post_order_traversal.append(root.data)

    
    def postOrderTraversal(self, key_root = None):
        post_order_traversal = []

        if self.root is None:
            return post_order_traversal
        if key_root is None:
            key_root = self.root.key

        root:Node = self.__findNode(key_root, self.root)[0] #находим узел по ключу

        self.__postOrderTraversal(root, post_order_traversal)

        return post_order_traversal
    
    def __inOrderTraversal(self, root:Node, in_order_traversal):
        if root is None:
            return
        
        self.__inOrderTraversal(root.left, in_order_traversal)
        in_order_traversal.append(root.data)
        self.__inOrderTraversal(root.right, in_order_traversal)

    def inOrderTraversal(self, key_root = None):
        in_order_traversal = []

        if self.root is None:
            return in_order_traversal
        if key_root is None:
            key_root = self.root.key

        root:Node = self.__findNode(key_root, self.root)[0] #находим узел по ключу

        self.__inOrderTraversal(root, in_order_traversal)

        return in_order_traversal

    def __printTree(self, node:Node, prev:Trunk, trunk_length, isLeft): #принимает корневой узел для которого рисуем, предыдущую ветку, длинну ветки, является ли ветка узел вверхним или нижним и отрисовывает дерево с переданным корнем
        if node is None: #если узел пустой для него нечего рисовать
            return
        
        prev_str = "    "
        trunk = Trunk(prev, prev_str) #сохраняем ветку для текущего узла текущего уровня
        self.__printTree(node.right, trunk, trunk_length, True) #идем по правой ветке

        if prev is None: #если текущий узел корневой печатаем указатель на корневой узел
            trunk.str = "———"       
        elif isLeft: #правая ветка, islLeft для того чтобы расширять дерево вниз, чтобы крайние правые ветки "стилились" по верху как и нижние левые
            trunk.str = ".———" #печатаем ветку вверх 
            prev_str = "   |" #чтобы нарисовать ветку которая идёт ниже узла, то есть для левого сына
        else: #левая ветка
            trunk.str = "`———" #печатаем ветку вниз
            prev.str = prev_str

        Trunk.showTrunks(trunk) #печатаем ветку для текущего узла
        print(" " + str(node.data))
        
        if prev:
            prev.str = prev_str #если есть предудущая ветка, то либо расширяем её вниз (палочка вертикальная), так как ветка была для правого поддерева либо пробелы, чтобы выделить место для ветки

        trunk.str = "   |"   
        self.__printTree(node.left, trunk, trunk_length, False)

    def printTree(self, key_root = None): #печатаем дерево с вершиной key_root
        if self.root is None:
            return print("tree is empty")
        if key_root is None:
            key_root = self.root.key

        root = self.__findNode(key_root, self.root)[0] #ищем по всему дереву узел 

        self.__printTree(root, None, len(str(self.maximum(key_root))), False)

        print()     
      
tree = LinkedBinaryTree()

print("1 изменение дерева: ")
tree.add(7, 7)
tree.add(50, 50)
tree.add(2, 2)
tree.add(3, 3)
tree.add(1, 1)
tree.printTree()

print("2 изменение дерева: ")
tree.add(40, 40)
tree.add(60, 60)
tree.add(5, 5)
tree.add(9, 9)
tree.add(10, 10)
tree.add(70, 70)
tree.add(53, 53)
tree.add(54, 54)
tree.printTree()

print("Глубина дерева: " + str(tree.depth()))
print("Количество узлов в дереве " + str(tree.nodeCount()))
print("Глубина дерева с корнем 40: " + str(tree.depth(40)))
print("Количество узлов в дереве с корнем 40 " + str(tree.nodeCount(40)))
print("Глубина дерева с корнем 60: " + str(tree.depth(60)))
print("Количество узлов в дереве с корнем 60 " + str(tree.nodeCount(60)))
print("Значение узла с ключом 10: " + str(tree.find(10)))
print("Нахождение значения узла с ключом 3: " + str(tree.find(3)))
print("Максимум всего дерева: " + str(tree.maximum()))
print("Максимум поддерва с корнем ключа 9: " + str(tree.maximum(9)))
print("Прямой обход дерева: " + str(tree.preOrderTraversal()))
print("Обратный обход дерева: " + str(tree.postOrderTraversal()))
print("Симметричный обход дерева: " + str(tree.inOrderTraversal()))


print()
print("3 изменения дерева: ")
tree.remove(50)
tree.printTree()
print("Глубина дерева после удаления: " + str(tree.depth()))
print("Количество узло в дереве " + str(tree.nodeCount()))

print("Значение узла с ключом 10: " + str(tree.find(10)))
print("Нахождение значения узла с ключом 3: " + str(tree.find(3)))
print("Максимум всего дерева: " + str(tree.maximum()))
print("Максимум поддерва с корнем ключа 9: " + str(tree.maximum(9)))
print("Прямой обход дерева c корнем с ключом 60: " + str(tree.preOrderTraversal(60)))
print("Симметричный обход с корнем 60: " + str(tree.inOrderTraversal(60)))

print()
print("4 изменения дерева: ")
tree.remove(7)
tree.remove(2)
tree.add(90, 90)
tree.add(80, 80)
tree.add(50, 50)
tree.add(55, 55)
tree.add(65, 65)
tree.add(63, 63)
tree.add(6, 6)
tree.add(66, 66)
tree.printTree()
tree.printTree(70)
tree.printTree(5)
print("Глубина дерева после изменений: " + str(tree.depth()))
print("Количество узло в поддереве с корнем 60: " + str(tree.nodeCount(60)))
print("Минимум поддерева с корнем 60: " + str(tree.minimum(60)))

print("Значение узла с ключом 10: " + str(tree.find(10)))
print("Максимум поддерева с корнем 50: " + str(tree.maximum(50)))
print("Минимум поддерева с корнем 50: " + str(tree.minimum(50)))
print("Обратный обход дерева с корнем 6: " + str(tree.postOrderTraversal(6)))
print("Симметричный обход дерева: " + str(tree.inOrderTraversal()))

print()
print("5 изменения дерева: ")
tree.clear(70)
tree.printTree()
print("Симметричный обход дерева: " + str(tree.inOrderTraversal()))
print("Пустое ли дерево " + str(tree.isEmpty()))
print("Пустое ли дерево с корнем 60 " + str(tree.isEmpty()))

print()
print("6 изменения дерева: ")
print("Очищаем дерево")
tree.clear()
tree.printTree()
print("Пустое ли дерево " + str(tree.isEmpty()))

print("Глубина дерева после очищения: " + str(tree.depth()))
print("Количество узло в дереве " + str(tree.nodeCount()))

print()
print("7 изменения дерева: ")
tree.add(30, 30)
tree.printTree()
print("Глубина дерева после добавления 30: " + str(tree.depth()))
print("Количество узло в дереве " + str(tree.nodeCount()))
print("Пустое ли дерево " + str(tree.isEmpty()))
print("Обратный обход дерева: " + str(tree.postOrderTraversal()))
print("Симметричный обход дерева: " + str(tree.inOrderTraversal()))

print()
print("8 изменения дерева: ")
tree.remove(30)
print("Пустое ли дерево после удаления 30 " + str(tree.isEmpty()))
print("Прямой обход дерева: " + str(tree.preOrderTraversal()))


