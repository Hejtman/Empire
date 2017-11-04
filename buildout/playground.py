class Base1:
    def __init__(self):
        print('Base1')

    def get_from_parent(self):
        return self.get_child_var()


class Base2:
    def __init__(self):
        print('Base2')


class Child(Base1, Base2):
    def __init__(self):
        Base1.__init__(self)
        Base2.__init__(self)
        print('init child')
        self.a = 8

    def get_child_var(self):
        return self.a


a = Child()
print(a.get_from_parent())
