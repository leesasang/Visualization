class Student:
    def __init__(self, name, age):
        self.name = name
        self.__age = age      # Name mangling
        self._job = "test"    # 관례적으로 외부에서 직접 접근하지 말 것을 _로 표시

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.__age = age

    def set_job(self, job):
        self._job = job       # 관례상 _가 앞에 있으면 직접 접근하지 말라는 의미

    def display(self):
        print(f"{self.name}'s age is {self.__age}")
        print(f"{self.name}'s job is {self._job}")


if __name__ == "__main__":
    s = Student("김 아무개", 21)

    s.name = "박 아무개"
    s._job = "학생"  # 관례일 뿐이므로 강제력은 약함. 실제 접근 가능.

    s.display()
    print(dir(s))
    # print(s.__dict__)  # instance attribute들을 출력해줌.
