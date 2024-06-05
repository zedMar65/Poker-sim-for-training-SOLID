class Person(object):
    def __init__(self):
        self.name = "{} {}".format("First","Last")

class Employee(Person):
    def introduce(self):
        print("Hi! My name is {}".format(self.name))

e = Employee()
e.introduce()