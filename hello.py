from typing import Protocol

class Quacker(Protocol):
    def quack(self) -> None:
        pass

class Duck:
    def quack(self) -> None:
        print("Quack, quack!")

class Person:
    def quack(self) -> None:
        print("I'm quacking like a duck!")

def make_it_quack(quacker: Quacker) -> None:
    quacker.quack()

duck = Duck()
person = Person()
make_it_quack(duck)  # Works because Duck implements the quack method
make_it_quack(person)  # Works because Person also implements the quack method
