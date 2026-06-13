class Car:

  def __init__(self, name="Anony"):
    self.name = name
    self.speed = 0

  def start(self,speed=30):
    self.speed = speed

  def stop(self):
    self.speed = 0

  def accelerate(self,speed):
    self.speed = self.speed + speed

  def __str__(self):
    return f"{self.name}:speed={self.speed}"

if __name__ == "__main__":
  a = Car("붕붕이")
  a.start()
  print(a)
  a.accelerate(20)
  print(a)
  a.stop()
  print(a)
