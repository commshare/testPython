class Car:
    def __init__(self):
        self.speed = 0
        self.odometer = 0
        self.time = 0

    def say_stat(self):
        print (" i am going {} kph ! ").format(self.speed)

    def accelerate(self):
        self.speed += 5
    def brake(self):
        self.speed = -5

    def step(self):
        self.odometer += self.speed
        self.time +=1
    def avrage_speed(self):
        return self.odometer / self.time

if __name__ == "__main__":
    my_car = Car()
    print("i am a car !")
    while True:
        action = input("what should i do ?  ABC").upper()
    if action not in "ABOS" or len(action) != 1:
        print(" i do not konw how to do ")
        continue
    if action == 'A' :
        my_car.accelerate()
    elif action == 'B' :
        my_car.brake
    elif action == '0' :
        print("the car has driven {} km ".format(my_car.odometer))
    elif action == 'S':
        print("the car avr speed is {} kph ".format(my_car.avrage_speed))
    my_car.step()
    my_car.say_state()