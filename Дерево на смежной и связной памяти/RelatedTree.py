class RelatedTree:
    def __init__(self) -> None:
        self.__tree = []

    def __del__(self) -> None: #удаляем экземпляр класса
        self = None

    def add(self, key, value) -> None:
        j = 0
        for i in range(len(self.__tree)):
            if len(self.__tree[i][j]) == 0: #если узел дерева пустой создаём узел
                self.__tree[i][j].append(key)
                self.__tree[i][j].append(value)
                return
            elif key == self.__tree[i][j][0]:
                self.__tree[i][j][1] = value #меняем значение если ключ такой же
                return
            elif key < self.__tree[i][j][0]:
                j = 2 * j #сын слева
            else:   
                j = 2 * j + 1 #сын справа    

        self.__tree.append([]) #если дошли до последнего уровня, добавляем уровень
        for k in range(2**(len(self.__tree) - 1)):
            self.__tree[len(self.__tree) - 1].append([])

        self.__tree[len(self.__tree) - 1][j].append(key)
        self.__tree[len(self.__tree) - 1][j].append(value)
        return
    
    def __nodeLevelUp(self, i:int, j:int, toLeft:bool) -> None: #поднимаем узлы всего поддерева на уровень вверх, поднимаем поддерево на уровень вверх
        if i == len(self.__tree): #ушли ниже глубины дерева
            return
        
        bias = 0
        if toLeft: #если смещаем влево вверх а не вправо вверх
            bias = -1

        self.__tree[i - 1][j // 2 + j % 2 + bias] = self.__tree[i][j]
        self.__nodeLevelUp(i + 1, j * 2, toLeft) #также поднимаем брата слева
        self.__nodeLevelUp(i + 1, j * 2 + 1, toLeft) #и справа

        if i == len(self.__tree) - 1: #если узел находятся на последнем уровне обнулляем
            self.__tree[i][j] = []
        elif len(self.__tree[i + 1][j * 2]) == 0 and len(self.__tree[i + 1][j * 2 + 1]) == 0: #если у узла нет сыновей удаляем узел
            self.__tree[i][j] = []

    def remove(self, key) -> None: #удаляем узел по ключу
        if len(self.__tree) == 1:
            if self.__tree[0][0][0] == key: #если удаляем первый и единственный элемент просто очищяем дерево
                self.clear()
                return
            
        i, j = self.__indexOf(key) #находим индекс удаляемого узла
        if i == None: #значит такого узла нет
            raise KeyError("node is not in tree")
            
        if i == len(self.__tree) - 1: #если узел на последнем уровне, то просто удаляем один узел
            self.__tree[i][j] = []
            return
        else: #если есть сыновья у узла
            if len(self.__tree[i + 1][j * 2 + 1]) == 0: #нет правого сына у удаляемого узла
                self.__nodeLevelUp(i + 1, j * 2, False) #на место узла который нужно удалить ставим его левого брата и поднимаем всё поддерево    
                return    
            else: #есть правый сын значит ищем крайний левый узел в правом поддереве
                k = i + 1 #создаем две новых переменных чтобы сохранить индекс узла который нужно удалить
                q = j * 2 + 1
                while (len(self.__tree[k + 1][q * 2]) != 0): #если у узла нет левого брата, то мы нашли крайний левый узел
                    k += 1
                    q *= 2
                       
                self.__tree[i][j] = self.__tree[k][q] #ставим крайний левый узел на место удаляемого узла
                self.__nodeLevelUp(k + 1, 2 * q + 1, True) #ставим на место левого крайнего узла его правого сына если есть и подднимаем всё поддерего влево вверх 
                return

    def __isLevelEmpty(self, i:int, key_root = None) -> bool: #принимаем индекс уровня и проверяем пустой ли уровень, индекс относительный (внутренний для поддерева)
        if self.isEmpty(key_root) is True:
            raise KeyError("node is not in tree")
        
        #находим индексы относительно всего дерева
        if key_root is None:
            i_in_main_root = 0
            j_in_main_root_left = j_in_main_root_right = 0
        else:
            i_in_main_root, j_in_main_root_left = self.__indexOf(key_root)
            j_in_main_root_right = j_in_main_root_left
        
        j_in_main_root_left = int(j_in_main_root_left * 2**i) #крайний левый узел в поддереве / дереве для уровня i
        for j in range(1, i + 1):
            j_in_main_root_right = j_in_main_root_right * 2 + 1 #крайний правый узел в поддереве / дереве для уровня i
        i = i_in_main_root + i #i - индекс внутри поддерева, i_in_main_root - индекс уровня во всем дереве
        for j in range(j_in_main_root_left, j_in_main_root_right + 1):
            if len(self.__tree[i][j]) != 0:
                return False #нашли один не пустой узел значит уровень не пустой
                
        return True #если ничего не нашли поддерево пустое

    def __delVoidLevel(self) -> None: #удаляем пустые уровни всего дерева
        for i in range(self.depth() - 1, -1, -1): #начинаем с послежнего уровня
            if self.__isLevelEmpty(i) is True: #если уровень пустой удаляем уровень
                del self.__tree[i]
            else: #иначе ничего удалять не надо начиная с этого уровня и выше
                return    

    def clear(self, key_root = None) -> None: #очищение дерева с корнем с ключом key_root
        if self.isEmpty(key_root) is True:
            raise KeyError("node is not in tree")
        
        #получаем индексы узла
        if key_root is None:
            i_root = 0
            j_root = 0
        else:
            i_root, j_root = self.__indexOf(key_root)
        
        if i_root == 0: #если удаляем всё дерево
            self.__tree = []
        else:
            j_root_left = j_root_right = j_root
            for i in range(i_root, self.depth()): #проходимяс по поддереву и удаляем его сыновей
                for j in range(j_root_left, j_root_right + 1):
                    self.__tree[i][j] = []

                j_root_left *= 2
                j_root_right = j_root_right * 2 + 1 

            self.__delVoidLevel() #если только это поддерево занимало уровень удаляем образоващийся пустой уровень          


    def get(self, key): #получение значения узла по ключу
        j = 0
        i, j = self.__indexOf(key)
        if i is None:
            raise KeyError("node is not in tree")
        else:
            return self.__tree[i][j][1]           
 
    def __find(self, i, j, value): #вспомогательная функция для нахождения ключа по значению
        if i == len(self.__tree):
            return
        elif len(self.__tree[i][j]) == 0:
            return
        elif self.__tree[i][j][1] == value:
            return self.__tree[i][j][0]
        
        key = self.__find(i + 1, j * 2, value)

        if key is None:    
            key = self.__find(i + 1, j * 2 + 1, value)

        return key    

    def find(self, value): #нахождения ключа узла по значению
        key = self.__find(0, 0, value)
        if key is not None:
            return key
        
        raise ValueError("node is not in tree")
    
    def __indexOf(self, key) -> list: #вспомогательная функция для нахождения индекса узла
        j = 0
        for i in range(len(self.__tree)):
            if len(self.__tree[i][j]) == 0:
                return None, None
            elif key == self.__tree[i][j][0]:
                return i, j
            elif key < self.__tree[i][j][0]:
                j *= 2
            elif key > self.__tree[i][j][0]:
                j = j * 2 + 1    

        return None, None

    def maximum(self, key_root = None): #нахождение максимума
        if self.isEmpty(key_root) is True: #пустое деревоо
            raise ValueError("tree is empty")
        
        if key_root is None:
            i_root = 0
            j_root_right = 0
        else:
            i_root, j_root_right = self.__indexOf(key_root)   

        maximum = self.__tree[i_root][j_root_right][1]
        for i in range(i_root + 1, len(self.__tree)):
            j_root_right = j_root_right * 2 + 1 #передвигаемся на крайний правый узел
            if len(self.__tree[i][j_root_right]) != 0: #если найден новый крайний правый узел
                 maximum = self.__tree[i][j_root_right][1]
            else: #если нет то уже найден крайний правый узел
                return maximum     
            
        return maximum                

    def minimum(self, key_root = None): #работа аналогична def maximum
        if self.isEmpty(key_root) is True:
            raise ValueError("tree is empty")
        
        if key_root is None:
            i_root = 0
            j_root_left = 0
        else:
            i_root, j_root_left = self.__indexOf(key_root)
        
        j_root_left = j_root_left * 2 ** (len(self.__tree) - 1 - i_root) #индекс крайнего левого элемента для поддерева
        for i in range(len(self.__tree) - 1, i_root - 1, -1):
            if len(self.__tree[i][j_root_left]) != 0: #если найден новый крайний левый узел
                 return self.__tree[i][j_root_left][1] 
            j_root_left = j_root_left // 2 #передвигаемся на предпоследнйи левый узел   

        return self.__tree[i_root][j_root_left][1] #до сюда никогда не дойдёт                 
    
    def depth(self, key_root = None) -> int: #глубина дерева /поддерева
        if self.isEmpty(key_root) is True:
            return 0
        
        if key_root is None:
            return len(self.__tree)
        else:
            i_root = self.__indexOf(key_root)[0]
        
        depth = 1
        for i in range(1, len(self.__tree) - i_root):
            if self.__isLevelEmpty(i, key_root) is True:
                return depth
            else:
                depth += 1

        return depth
    
    def nodeCount(self, key_root = None) -> int: #количество элементов в дереве / поддереве
        if self.isEmpty(key_root) is True:
            return 0

        if key_root is None:
            key_root = self.__tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self.__indexOf(key_root)
            j_root_right = j_root_left

        nodes_count = 0
        for i in range(i_root, len(self.__tree)):
            for j in range(j_root_left, j_root_right + 1):
                if len(self.__tree[i][j]) != 0:
                    nodes_count += 1

            j_root_left *= 2
            j_root_right = j_root_right * 2 + 1        

        return nodes_count

    def isEmpty(self, key_root = None) -> bool: #пустое ли дерево
        #если корень всего дерева отсуствует
        if len(self.__tree) == 0:
            return True

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            key_root = self.__tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self.__indexOf(key_root)
            if i_root == None: #если нет такого узла нет и поддерева
                return True
            j_root_right = j_root_left
        
        #иначе дерево не пустое
        return False  

    def __preOrderTraversal(self, i:int, j:int, pre_order_traversal:list) -> None: #вспомогательная рекурсивная функция для прямого обхода
        if i == self.depth(): #если упёрлись в последний уровень
            return
        if len(self.__tree[i][j]) == 0: #если узел пустой
            return
        
        pre_order_traversal.append(self.__tree[i][j][1]) #добавляем значение эллемента
        
        self.__preOrderTraversal(i + 1, j * 2, pre_order_traversal) #повторяем для левого сына
        self.__preOrderTraversal(i + 1, j * 2 + 1, pre_order_traversal) #повторяем для правого сына

    def preOrderTraversal(self, key_root = None) -> list: #прямой обход
        if self.isEmpty(key_root) is True: #если дерево с корнем key_root пустое возрващаем пустой массив обхода
            return []

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            i_root = 0
            j_root = 0
        else:
            i_root, j_root = self.__indexOf(key_root)
            
        pre_order_traversal = []

        self.__preOrderTraversal(i_root, j_root, pre_order_traversal)

        return pre_order_traversal
    
    def __postOrderTraversal(self, i:int, j:int, post_order_traversal:list) -> None: #вспомогательная рекурсивная функция для обратного обхода
        if i == self.depth(): #если упёрлись в последний уровень
            return
        if len(self.__tree[i][j]) == 0: #если узел пустой
            return
        
        self.__postOrderTraversal(i + 1, j * 2, post_order_traversal)
        self.__postOrderTraversal(i + 1, j * 2 + 1, post_order_traversal)

        post_order_traversal.append(self.__tree[i][j][1])

    def postOrderTraversal(self, key_root = None) -> list: #обратный обход
        if self.isEmpty(key_root) is True: #если дерево с корнем key_root пустое возрващаем пустой массив обхода
            return []

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            i_root = 0
            j_root = 0
        else:
            i_root, j_root = self.__indexOf(key_root)
            
        post_order_traversal = []

        self.__postOrderTraversal(i_root, j_root, post_order_traversal)

        return post_order_traversal
    
    def __inOrderTraversal(self, i:int, j:int, in_order_traversal:list) -> None: #вспомогательная рекурсивная функция для симметричного обхода
        if i == self.depth(): #если упёрлись в последний уровень
            return
        if len(self.__tree[i][j]) == 0: #если узел пустой
            return
        
        self.__inOrderTraversal(i + 1, j * 2, in_order_traversal)
        in_order_traversal.append(self.__tree[i][j][1])
        self.__inOrderTraversal(i + 1, j * 2 + 1, in_order_traversal)

    def inOrderTraversal(self, key_root = None) -> list: #симметричный обход дерева
        if self.isEmpty(key_root) is True: #если дерево с корнем key_root пустое возрващаем пустой массив обхода
            return []

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            i_root = 0
            j_root = 0
        else:
            i_root, j_root = self.__indexOf(key_root)
            
        in_order_traversal = []

        self.__inOrderTraversal(i_root, j_root, in_order_traversal)

        return in_order_traversal    

    def printTree(self, key_root = None): #рисуем дерево вертикально с псевдографикой с корнем с ключом key_root
        if self.isEmpty(key_root) is True:
            print("tree is empty")
            return

        #находим индекс корня для дерева/поддерева
        if key_root is None:
            key_root = self.__tree[0][0][0]
            i_root = 0
            j_root_left = j_root_right = 0
        else:
            i_root, j_root_left = self.__indexOf(key_root)
            j_root_right = j_root_left

        max_length_node = len(str(self.maximum(key_root))) #длина максимального эллемента
        count_node_last_level = 2**(self.depth() - 1) // 2**i_root #количество узлов последнего уровня поддерева, так как с каждым нижне уровнем сын является корнем поддерева с узлами в 2 раза меньше на последнем уровне
        count_node = 0 #количество узлов на текущем уровне плюс все предыдующие уровни
        length_last_level = (2 * count_node_last_level - 1) * max_length_node #длина вывода последнего уровня, состоит из длины всех узлов (количество элементво на длину максмимального узла) + расстояния между узлами равное длине максимального узла
        space_before_node_current_level = 0 #расстоянние между эллемента текущего уровня равно длине последнего уровня - длине всех узлов текущего уровня и эту разница делить на удвоенное количество узлов текущего уровня (так как для каждого узла нужны пробелы слевы и справа)

        #печатаем структуру дерева
        for i in range(i_root , len(self.__tree)):
            count_node += j_root_right - j_root_left + 1   
            space_before_node_current_level = (length_last_level - max_length_node * count_node) // (2 * (j_root_right - j_root_left + 1))
            if i == len(self.__tree) - 1:
                space_before_node_current_level = 0 #убираем расстояние для последнего уровня, так как у него нет сыновей
                
            for j in range(j_root_left, j_root_right + 1):
                if len(self.__tree[i][j]) == 0:
                    print(" "*(space_before_node_current_level) + " "*max_length_node + " "*(space_before_node_current_level + max_length_node), end="")
                else:
                    print(" "*(space_before_node_current_level)+ " "*(max_length_node - len(str(self.__tree[i][j][1]))) + str(self.__tree[i][j][1]) + " "*(space_before_node_current_level + max_length_node), end="")
            
            #рисуем ветки
            print()
            for j in range(j_root_left, j_root_right + 1):
                flag_last_max = 0 #для корректного вывода если у узла на предпоследнем уровне, длина значения которого равна длине максимального числа, есть левый сын и/или правый сын то в конце и в начале нужно на одни пробел меньше выводить перед веткой
                if i != len(self.__tree) - 1: #рисуем ветки для всех кроме последнего уровня
                    if len(self.__tree[i][j]) != 0: #если есть узел рисуем для его сыновей ветки

                        if i == len(self.__tree) - 2 and len(str(self.__tree[i][j][1])) != 1:
                                flag_last_max = -1
                        
                        if len(self.__tree[i + 1][j * 2]) != 0: #если есть левый сын рисуем для него ветки
                            print(" "*((space_before_node_current_level - max_length_node) // 2 + max_length_node + flag_last_max) + "/" + "-"*((space_before_node_current_level - max_length_node) // 2 - 1  + max_length_node - len(str(self.__tree[i][j][1]))), end=(" "*(len(str(self.__tree[i][j][1])))))  
                        else: #если нет рисуем пробелы равные расстоянию до родительского узла
                            print(" "*space_before_node_current_level, end = (" "*max_length_node))
 
                        if len(self.__tree[i + 1][j * 2 + 1]) != 0: #если есть правый сын рисуем для него ветки
                            print("-"*((space_before_node_current_level - max_length_node) // 2 - 1 + max_length_node - len(str(self.__tree[i + 1][j * 2 + 1][1]))) + "\\", end = (" "*(len(str(self.__tree[i + 1][j * 2 + 1][1])) + (space_before_node_current_level - max_length_node) // 2 + max_length_node + flag_last_max)))
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
tree.add(53, 53)
tree.add(54, 54)
tree.printTree()

print("Глубина дерева: " + str(tree.depth()))
print("Количество узлов в дереве " + str(tree.nodeCount()))
print("Глубина дерева с корнем 40: " + str(tree.depth(40)))
print("Количество узлов в дереве с корнем 40 " + str(tree.nodeCount(40)))
print("Глубина дерева с корнем 60: " + str(tree.depth(60)))
print("Количество узлов в дереве с корнем 60 " + str(tree.nodeCount(60)))
print("Значение узла с ключом 10: " + str(tree.get(10)))
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

print("Значение узла с ключом 10: " + str(tree.get(10)))
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

print("Значение узла с ключом 10: " + str(tree.get(10)))
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
