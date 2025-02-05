class Dog:
    def __init__(self, name, breed):
        self.name = name  # 'self.name' refers to the instance's name attribute
        self.breed = breed  # 'self.breed' refers to the instance's breed attribute

    def bark(self):
        print(f"{self.name} says Woof!")  # Accessing the instance's name

# Create an instance of Dog
my_dog = Dog("Buddy", "Golden Retriever")

# Call the bark method
my_dog.bark()