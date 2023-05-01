class RelatedTree:
    def __init__(self) -> None:
        self.tree = []

    def __del__(self) -> None:
        self = None

    def add(self, key, value) -> None:
        j = 0
        for i in range(len(self.tree)):
            if len(self.tree[i][j]) == 0: #если узел дерева пустой создаём узел
                self.tree[i][j].append(key)
                self.tree[i][j].append(value)
                return
            elif key == self.tree[i][j][0]:
                self.tree[i][j][1] = value #меняем значение если ключ такой же
                return
            elif key < self.tree[i][j][0]:
                j = 2 * j #сын слева
            else:   
                j = 2 * j + 1 #сын справа    

        self.tree.append([]) #если дошли до последнего уровня, добавляем уровень
        for k in range(2**(len(self.tree) - 1)):
            self.tree[len(self.tree) - 1].append([])

        self.tree[len(self.tree) - 1][j].append(key)
        self.tree[len(self.tree) - 1][j].append(value)
        return
    
    def _nodeLevelUp(self, i:int, j:int, toLeft:bool) -> None: #поднимаем узлы всего поддерева на уровень вверх, поднимаем поддерево на уровень вверх
        if i == len(self.tree): #ушли ниже глубины дерева
            return
        
        bias = 0
        if toLeft: #если смещаем влево вверх а не вправо вверх
            bias = -1

        self.tree[i - 1][j // 2 + j % 2 + bias] = self.tree[i][j]
        self._nodeLevelUp(i + 1, j * 2, toLeft) #также поднимаем брата слева
        self._nodeLevelUp(i + 1, j * 2 + 1, toLeft) #и справа

        if i == len(self.tree) - 1: #если узел находятся на последнем уровне обнулляем
            self.tree[i][j] = []
        elif len(self.tree[i + 1][j * 2]) == 0 and len(self.tree[i + 1][j * 2 + 1]) == 0: #если у узла нет сыновей удаляем узел
            self.tree[i][j] = []

    def remove(self, key) -> None:
        if len(self.tree) == 1:
            if self.tree[0][0][0] == key:
                self.clear()
                return

        j = 0
        for i in range(len(self.tree)):
            if key == self.tree[i][j][0]:
                if i == len(self.tree) - 1:
                    self.tree[i][j] = []
                    return
                else:
                    if len(self.tree[i + 1][j * 2 + 1]) == 0: #нет правого сына у удаляемого узла
                        self._nodeLevelUp(i + 1, j * 2, False) #на место узла который нужно удалить ставим его левого брата и поднимаем всё поддерево    
                        return    
                    else: #есть правый сын значит ищем крайний левый узел в правом поддереве
                        k = i + 1 #создаем две новых переменных чтобы сохранить индекс узла который нужно удалить
                        q = j * 2 + 1
                        while (len(self.tree[k + 1][q * 2]) != 0): #если у узла нет левого брата, то мы нашли крайний левый узел
                            k += 1
                            q *= 2
                       
                        self.tree[i][j] = self.tree[k][q] #ставим крайний левый узел на место удаляемого узла
                        self._nodeLevelUp(k + 1, 2 * q + 1, True) #ставим на место левого крайнего узла его правого сына если есть и подднимаем всё поддерего влево вверх 
                        return
            elif key < self.tree[i][j][0]:
                j = 2 * j #сын слева
            else:
                j = 2 * j + 1 #сын справа

        raise KeyError("node is not in tree")
                               
    def clear(self) -> None:
        self.tree = []

    def get(self, key): #получение значения узла по ключу
        j = 0
        for i in range(len(self.tree)):
            if len(self.tree[i][j]) == 0:
                raise KeyError("node is not in tree")
            elif key == self.tree[i][j][0]:
                return self.tree[i][j][1]
            elif key < self.tree[i][j][0]:
                j *= 2
            else:
                j = j * 2 + 1

        raise KeyError("node is not in tree")           
 
    def _find(self, i, j, value): #вспомогательная функция для нахождения ключа по значению
        if i == len(self.tree):
            return
        elif len(self.tree[i][j]) == 0:
            return
        elif self.tree[i][j][1] == value:
            return self.tree[i][j][0]
        
        key = self._find(i + 1, j * 2, value)

        if key is None:    
            key = self._find(i + 1, j * 2 + 1, value)

        return key    

    def find(self, value): #нахождения ключа узла по значению
        key = self._find(0, 0, value)
        if key is not None:
            return key
        
        raise ValueError("node is not in tree")
    
    def _indexOf(self, key) -> list: #вспомогательная функция для нахождения индекса узла
        j = 0
        for i in range(len(self.tree)):
            if len(self.tree[i][j]) == 0:
                return None, None
            elif key == self.tree[i][j][0]:
                return i, j
            elif key < self.tree[i][j][0]:
                j *= 2
            elif key > self.tree[i][j][0]:
                j = j * 2 + 1    

        return None, None

    def max(self, key_root = None): #нахождение максимума
        if len(self.tree) == 0: #пустое деревоо
            raise ValueError("tree is empty")
        
        if key_root is None:
            key_root = self.tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            j_root_right = j_root_left   
        
        max = None
        for i in range(i_root, len(self.tree)):
            for j in range(j_root_left, j_root_right + 1):
                if len(self.tree[i][j]) == 0: #если узла нет пропускаем проверку
                    pass
                elif type(self.tree[0][0][1]) not in (int, float): #если значение узла не числовой тип пропускаем проверку
                    pass
                elif max is None: #первый встретившийся числовой тип
                    max = self.tree[i][j][1]
                elif self.tree[i][j][1] > max: #если значение узла больше максимального значения
                    max = self.tree[i][j][1]

            j_root_left *= 2
            j_root_right = j_root_right * 2 + 1        

        if max is None: #если макс до сих пор None значит числовой тип не найден
            raise TypeError("tree with key root " + str(key_root) + " doesn't have any int or float type node")

        return max                

    def min(self, key_root = None): #работа аналогична def max
        if len(self.tree) == 0:
            raise ValueError("tree is empty")
        
        if key_root is None:
            key_root = self.tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            j_root_right = j_root_left
        
        min = None
        for i in range(i_root, len(self.tree)):
            for j in range(j_root_left, j_root_right + 1):
                if len(self.tree[i][j]) == 0:
                    pass
                elif type(self.tree[0][0][1]) not in (int, float):
                    pass
                elif min is None:
                    min = self.tree[i][j][1]
                elif self.tree[i][j][1] < min:
                    min = self.tree[i][j][1]

            j_root_left *= 2
            j_root_right = j_root_right * 2 + 1        

        if min == None:
            raise TypeError("tree with key root " + str(key_root) + " doesn't have any int or float type node")

        return min                     
    
    def depth(self) -> int:
        return len(self.tree)
    
    def nodesCount(self, key_root = None) -> int:
        if self.isEmpty(key_root) is True:
            return 0

        if key_root is None:
            key_root = self.tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            j_root_right = j_root_left

        nodes_count = 0
        for i in range(i_root, len(self.tree)):
            for j in range(j_root_left, j_root_right + 1):
                if len(self.tree[i][j]) != 0:
                    nodes_count += 1

            j_root_left *= 2
            j_root_right = j_root_right * 2 + 1        

        return nodes_count

    def isEmpty(self, key_root = None) -> bool:
        #если корень всего дерева отсуствует
        if len(self.tree) == 0:
            return True
        
        #если корень всего дерева отсуствует
        if len(self.tree[0]) == 0:
            return True

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            key_root = self.tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            j_root_right = j_root_left
        
        #если корневой узел пустой то и дерево пустое
        if len(self.tree[i_root][j_root_left]) == 0:
            return True
        else: #иначе проверяем каждый узел, если находится хотя бы один не пустой возвращаем False
            for i in range(i_root, len(self.tree)):
                for j in range(j_root_left, j_root_right + 1): #радиус от крайнего левого узла до крайнего права узла текущего уровня i дерева
                    if len(self.tree[i][j]) != 0:
                        return False

                j_root_left *= 2
                j_root_right = j_root_right * 2 + 1

            return True  

    def _preOrderTraversal(self, i:int, j:int, pre_order_traversal:list) -> None: #вспомогательная рекурсивная функция для прямого обхода
        if i == self.depth(): #если упёрлись в последний уровень
            return
        if len(self.tree[i][j]) == 0: #если узел пустой
            return
        
        pre_order_traversal.append(self.tree[i][j][1]) #добавляем значение эллемента
        
        self._preOrderTraversal(i + 1, j * 2, pre_order_traversal) #повторяем для левого сына
        self._preOrderTraversal(i + 1, j * 2 + 1, pre_order_traversal) #повторяем для правого сына

    def preOrderTraversal(self, key_root = None) -> list: #прямой обход
        if self.isEmpty(key_root) is True: #если дерево с корнем key_root пустое возрващаем пустой массив обхода
            return []

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            i_root = 0
            j_root = 0
        else:
            i_root, j_root = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            
        pre_order_traversal = []

        self._preOrderTraversal(i_root, j_root, pre_order_traversal)

        return pre_order_traversal
    
    def _postOrderTraversal(self, i:int, j:int, post_order_traversal:list) -> None: #вспомогательная рекурсивная функция для обратного обхода
        if i == self.depth(): #если упёрлись в последний уровень
            return
        if len(self.tree[i][j]) == 0: #если узел пустой
            return
        
        self._postOrderTraversal(i + 1, j * 2, post_order_traversal)
        self._postOrderTraversal(i + 1, j * 2 + 1, post_order_traversal)

        post_order_traversal.append(self.tree[i][j][1])

    def postOrderTraversal(self, key_root = None) -> list: #обратный обход
        if self.isEmpty(key_root) is True: #если дерево с корнем key_root пустое возрващаем пустой массив обхода
            return []

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            i_root = 0
            j_root = 0
        else:
            i_root, j_root = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            
        post_order_traversal = []

        self._postOrderTraversal(i_root, j_root, post_order_traversal)

        return post_order_traversal
    
    def _inOrderTraversal(self, i:int, j:int, in_order_traversal:list) -> None: #вспомогательная рекурсивная функция для симметричного обхода
        if i == self.depth(): #если упёрлись в последний уровень
            return
        if len(self.tree[i][j]) == 0: #если узел пустой
            return
        
        self._inOrderTraversal(i + 1, j * 2, in_order_traversal)
        in_order_traversal.append(self.tree[i][j][1])
        self._inOrderTraversal(i + 1, j * 2 + 1, in_order_traversal)

    def inOrderTraversal(self, key_root = None) -> list: #симметричный обход дерева
        if self.isEmpty(key_root) is True: #если дерево с корнем key_root пустое возрващаем пустой массив обхода
            return []

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            i_root = 0
            j_root = 0
        else:
            i_root, j_root = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            
        in_order_traversal = []

        self._inOrderTraversal(i_root, j_root, in_order_traversal)

        return in_order_traversal    

        
    def printTree(self, key_root = None):
        if self.isEmpty(key_root) is True:
            print("tree is empty")
            return

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            key_root = self.tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self._indexOf(key_root)
            if i_root == None:
                raise KeyError("node is not in tree")
            j_root_right = j_root_left

        max_length_node = len(str(self.max(key_root))) #длина максимального эллемента
        count_node_last_level = 2**(self.depth() - 1) // 2**i_root #количество узлов последнего уровня поддерева, так как с каждым нижне уровнем сын является корнем поддерева с узлами в 2 раза меньше на последнем уровне
        count_node = 0 #количество узлов на текущем уровне плюс все предыдующие уровни
        length_last_level = (2 * count_node_last_level - 1) * max_length_node #длина вывода последнего уровня, состоит из длины всех узлов (количество элементво на длину максмимального узла) + расстояния между узлами равное длине максимального узла
        space_before_node_current_level = 0 #расстоянние между эллемента текущего уровня равно длине последнего уровня - длине всех узлов текущего уровня и эту разница делить на удвоенное количество узлов текущего уровня (так как для каждого узла нужны пробелы слевы и справа)

        #печатаем структуру дерева
        for i in range(i_root , len(self.tree)):
            count_node += j_root_right - j_root_left + 1   
            space_before_node_current_level = (length_last_level - max_length_node * count_node) // (2 * (j_root_right - j_root_left + 1))
            if i == len(self.tree) - 1:
                space_before_node_current_level = 0 #убираем расстояние для последнего уровня, так как у него нет сыновей
                
            for j in range(j_root_left, j_root_right + 1):
                if len(self.tree[i][j]) == 0:
                    print(" "*(space_before_node_current_level) + " "*max_length_node + " "*(space_before_node_current_level + max_length_node), end="")
                else:
                    print(" "*(space_before_node_current_level)+ " "*(max_length_node - len(str(self.tree[i][j][1]))) + str(self.tree[i][j][1]) + " "*(space_before_node_current_level + max_length_node), end="")
            
            #рисуем ветки
            print()
            for j in range(j_root_left, j_root_right + 1):
                flag_last_max = 0 #для корректного вывода если у узла на предпоследнем уровне, длина значения которого равна длине максимального числа, есть левый сын и/или правый сын то в конце и в начале нужно на одни пробел меньше выводить перед веткой
                if i != len(self.tree) - 1: #рисуем ветки для всех кроме последнего уровня
                    if len(self.tree[i][j]) != 0: #если есть узел рисуем для его сыновей ветки

                        if i == len(self.tree) - 2 and len(str(self.tree[i][j][1])) != 1:
                                flag_last_max = -1
                        
                        if len(self.tree[i + 1][j * 2]) != 0: #если есть левый сын рисуем для него ветки
                            print(" "*((space_before_node_current_level - max_length_node) // 2 + max_length_node + flag_last_max) + "/" + "-"*((space_before_node_current_level - max_length_node) // 2 - 1  + max_length_node - len(str(self.tree[i][j][1]))), end=(" "*(len(str(self.tree[i][j][1])))))  
                        else: #если нет рисуем пробелы равные расстоянию до родительского узла
                            print(" "*space_before_node_current_level, end = (" "*max_length_node))
 
                        if len(self.tree[i + 1][j * 2 + 1]) != 0: #если есть правый сын рисуем для него ветки
                            print("-"*((space_before_node_current_level - max_length_node) // 2 - 1 + max_length_node - len(str(self.tree[i + 1][j * 2 + 1][1]))) + "\\", end = (" "*(len(str(self.tree[i + 1][j * 2 + 1][1])) + (space_before_node_current_level - max_length_node) // 2 + max_length_node + flag_last_max)))
                        else: #если нет рисуем пробелы равные расстоянию после родительского узла
                            print(" "*space_before_node_current_level, end = (" "*max_length_node))
                    else: #если нет узла то рисуем пробелы равные расстоянию до родительского эллемента и после него
                        print(" "*(space_before_node_current_level + max_length_node + space_before_node_current_level), end = (" "*(max_length_node)))    

            print()
        
            #увеличиваем диапозон индексов левого крайнего узла уровня дерева и крайнего правого
            j_root_left *= 2 
            j_root_right = j_root_right * 2 + 1  

tree = RelatedTree()

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
tree.printTree()

print("Глубина дерева: " + str(tree.depth()))
print("Количество узло в дереве " + str(tree.nodesCount()))

print("Значение узла с ключом 10: " + str(tree.get(10)))
print("Нахождение значения узла с ключом 3: " + str(tree.find(3)))
print("Максимум всего дерева: " + str(tree.max()))
print("Максимум поддерва с корнем ключа 9: " + str(tree.max(9)))
print("Прямой обход дерева: " + str(tree.preOrderTraversal()))
print("Обратный обход дерева: " + str(tree.postOrderTraversal()))
print("Симметричный обход дерева: " + str(tree.inOrderTraversal()))


print("3 изменения дерева: ")
tree.remove(50)
tree.printTree()
print("Глубина дерева после удаления: " + str(tree.depth()))
print("Количество узло в дереве " + str(tree.nodesCount()))

print("Значение узла с ключом 10: " + str(tree.get(10)))
print("Нахождение значения узла с ключом 3: " + str(tree.find(3)))
print("Максимум всего дерева: " + str(tree.max()))
print("Максимум поддерва с корнем ключа 9: " + str(tree.max(9)))
print("Прямой обход дерева c корнем с ключом 60: " + str(tree.preOrderTraversal(60)))
print("Симметричный обход с корнем 60: " + str(tree.inOrderTraversal(60)))


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
print("Количество узло в поддереве с корнем 60: " + str(tree.nodesCount(60)))

print("Значение узла с ключом 10: " + str(tree.get(10)))
print("Максимум поддерева с корнем 50: " + str(tree.max(50)))
print("Минимум поддерева с корнем 50: " + str(tree.min(50)))
print("Обратный обход дерева с корнем 6: " + str(tree.postOrderTraversal(6)))
print("Симметричный обход дерева: " + str(tree.inOrderTraversal()))

print()
print("5 изменения дерева: ")
print("Очищаем дерево")
tree.clear()
tree.printTree()

print("Глубина дерева после очищения: " + str(tree.depth()))
print("Количество узло в дереве " + str(tree.nodesCount()))

print("6 изменения дерева: ")
tree.add(30, 30)
tree.printTree()
print("Глубина дерева после добавления 30: " + str(tree.depth()))
print("Количество узло в дереве " + str(tree.nodesCount()))
print("Пустое ли дерево " + str(tree.isEmpty()))
print("Обратный обход дерева: " + str(tree.postOrderTraversal()))
print("Симметричный обход дерева: " + str(tree.inOrderTraversal()))

print("7 изменения дерева: ")
tree.remove(30)
print("Пустое ли дерево после удаления 30 " + str(tree.isEmpty()))

print("Прямой обход дерева: " + str(tree.preOrderTraversal()))
