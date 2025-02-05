class TextProcessor: #class is a blueprint for creating objects
    #initialize the constructor
    def __init__(self, text):
        self.text = text

    def word_count(self):
        return len(self.text.split())

    def summarize(self, max_length=50):
        return self.text[:max_length] + "..." if len(self.text) > max_length else self.text

    def to_uppercase(self):
        return self.text.upper()