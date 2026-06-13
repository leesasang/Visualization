class Student:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age      # Name mangling

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    # property object를 이용한 구현
    name = property(get_name, set_name)

    # Decorator를 이용한 구현
    @property
    def age(self):
        return f"[{self.__age}]"

    @age.setter
    def age(self, age):
        if age < 0:
            self.__age = 0
        else:
            self.__age = age

    def display(self):
        print(f"{self.__name}'s age is {self.__age}")


if __name__ == "__main__":
    s = Student("김 아무개", 21)

    s.name = "박 아무개"
    s.age = -10

    print(s.age)

    print("------------")
    s.display()

    print("------------")
    print(s.__dict__)  # instance attribute 확인

    print("------------")
    print(dir(s))      # 접근 가능한 attribute 이름 확인
