class Pyt:
    def __init__(self, tree, key, root) -> None:
        self.__tree = tree
        self.key = key
        self.root = root
    
    """@property
    def tree(self):
        print("Не доступно для чтения")

    @tree.setter
    def tree(self, value):
        print("Не доступно для записи")

    @tree.deleter
    def tree(self):
        print("Не доступно для удаления") """

    def ht(self):
        print(self.__tree)    

a = Pyt(1, 3, 4)
#print(a.__tree)
a.ht()

