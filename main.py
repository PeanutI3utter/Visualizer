from Base import window, element
from Button import Button

w = window(800, 600, "Test")
custom_button = Button(100, 50, 50, 50, text="Some button")
w.window_elements.add_child(custom_button)
w.start()