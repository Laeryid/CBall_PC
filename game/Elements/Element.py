import logger
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

class Element(Widget):
    input_data_line = ListProperty(None)
    size = NumericProperty(None)
    size_letter = StringProperty(None)
    initial_count = NumericProperty(None)
    count_left = NumericProperty(None)

    def __init__(self, *args, **kwargs):
        super(Element, self).__init__(*args, **kwargs)
        if not self.input_data_line is None:
            self.size_letter = self.input_data_line[1]
            self.size = int(self.input_data_line[2])
            self.initial_count = int(self.input_data_line[3])
            self.count_left = self.initial_count