from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name[1:]} should be an integer.")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"{self.protected_name[1:]} "
                             f"should be between {self.min_amount} "
                             f"and {self.max_amount}.")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: IntegerRange,
                 weight: IntegerRange,
                 height: IntegerRange) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(4, 14)
        weight = IntegerRange(20, 50)
        height = IntegerRange(80, 120)
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(14, 60)
        weight = IntegerRange(50, 120)
        height = IntegerRange(120, 220)
        super().__init__(age, weight, height)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            limitation = self.limitation_class()
            limitation.age.__set__(visitor, visitor.age)
            limitation.weight.__set__(visitor, visitor.weight)
            limitation.height.__set__(visitor, visitor.height)
            return True
        except (TypeError, ValueError) as e:
            print(f"Access Denied: {e}")
            return False
