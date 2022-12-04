from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup

Window.size = (400, 600)

class MainMenu(Widget):
    val_x = StringProperty('0')
    x_set = False
    val_y = StringProperty('0')
    y_set = False
    op = StringProperty(None)
    operand = None
    selected = StringProperty('0')
    previous = StringProperty('')
    expression = StringProperty('')
    reset_display = False
    expr_2 = ''


    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def size_check(self, val, disp='main'):
        '''Checks the length of a selected display string
        and adjusts the font size if the string is past
        a certain length. This ensures that the displayed
        number always fits within the screen boundaries.

        The "disp" variable determines which display is
        checked. A value of "main" will check the main
        number display, whereas a value of "exp" will
        cause the expression display to be checked.'''
        if disp == 'main':
            if len(str(val)) >= 20:
                self.ids.display.font_size = self.width/16
            elif len(str(val)) >= 12:
                self.ids.display.font_size = self.width/12
            else:
                self.ids.display.font_size = self.width/8
        elif disp == 'exp':
            if len(str(val)) >= 20:
                self.ids.show_expression.font_size = self.width/30
            elif len(str(val)) >= 12:
                self.ids.show_expression.font_size = self.width/25
            else:
                self.ids.show_expression.font_size = self.width/20


    def zero(self):
        '''Appends a zero to the display string. Will not
        append a zero if it would result in an unnecesary
        leading zero.

        If self.reset_display is True, entering any value will
        clear the currently displayed number, allowing input of
        a fresh value.'''
        if self.reset_display:
            self.selected = '0'
            self.expression = ''
            self.expr_2 = ''
            self.reset_display = False
        if len(self.selected) < 20 and self.selected[0] != '0':
            self.selected = (self.selected + '0')
            self.size_check(self.selected)

    def num_in(self, x):
        '''Appends string x to the end of the display string.
        Use with numbers from 1 to 9. Automatically strips
        uneccesary leading zeroes from the string.

        If self.reset_display is True, entering any value will
        clear the currently displayed number, allowing input of
        a fresh value.'''
        if self.reset_display:
            self.selected = '0'
            self.expression = ''
            self.expr_2 = ''
            self.reset_display = False
        if len(self.selected) < 20:
            self.selected = (self.selected + x).lstrip('0')
            self.size_check(self.selected)


    def deci(self):
        '''Appends a decimal point to the end of the display string.
        Will do nothing if the display string already contains a
        decimal point.

        If self.reset_display is True, entering any value will
        clear the currently displayed number, allowing input of
        a fresh value.'''
        if self.reset_display:
            self.selected = '0'
            self.expression = ''
            self.expr_2 = ''
            self.reset_display = False
        if len(self.selected) < 20 and '.' not in self.selected:
            self.selected = (self.selected + '.')           
            self.size_check(self.selected)

    def nega(self):
        '''Appends a - to the beginning of the display string, or
        removes it if one is already present.

        If self.reset_display is True, entering any value will
        clear the currently displayed number, allowing input of
        a fresh value.'''
        if self.reset_display:
            self.selected = '0'
            self.expression = ''
            self.expr_2 = ''
            self.reset_display = False
        if self.selected[0:2] != '0.':
            self.selected = self.selected.lstrip('0')
        if len(self.selected) < 20 and '-' not in self.selected:
            self.selected = ('-' + self.selected)           
        else:
            self.selected = self.selected.removeprefix('-')
        self.size_check(self.selected)


    def clear_input(self):
        '''Clears the currently inputted number in the display.'''
        self.selected = '0'
        self.size_check(self.selected)

    def clear_all(self):
        '''Clears all values stored in memory.'''
        self.val_x = '0'
        self.val_y = '0'
        self.selected = '0'
        self.operand = None
        self.previous = ''
        self.size_check(self.selected)
        self.x_set = False
        self.y_set = False
        self.expression = ''
        self.expr_2 = ''
        self.reset_display = False

    def operate(self, oper, opname):
        '''Appends the operater "oper" to the current string and
        defines the current operation as entered under "opname",
        from addition, multiplication, etc. Additionally stores
        the current display value into self.val_x if self.val_x
        is currently empty, else calls self.calc().'''
        if not self.x_set:
            if self.selected == '.' or self.selected == '-' or not self.selected or self.selected == '-.':
                self.selected = '0'
            if self.reset_display:
                self.expression = ''
                self.selected = self.expr_2
                self.reset_display = False 
            self.operand = opname
            self.selected += oper
            self.val_x = self.selected
            self.previous = self.val_x
            self.expression += self.selected
            self.selected = self.val_y
            self.x_set = True
            self.size_check(self.expression, 'exp')


    def bspace(self):
        '''Deletes the last character in the current display string,
        if any characters are present. If the display string is empty,
        does nothing.'''
        if len(str(self.selected)):
            self.selected = self.selected.removesuffix(self.selected[-1])
            self.size_check(self.selected)
            if not self.selected:
                self.selected = '0'

    def calc(self):
        '''Based on the operator stored in self.operator, performs a
        mathematical operation on self.val_x and self.val_y. Currently,
        addition, subtraction, multiplication, and division are
        possible.'''
        if self.x_set and self.selected:
            self.val_x = self.val_x.rstrip('+-*÷.') 
            self.selected.rstrip('+-*÷.')
            self.val_y = self.selected
            if self.val_y == '.' or self.val_y == '-' or not self.val_y or self.val_y == '-.':
                self.val_y = '0'            
            self.expression = self.expression + self.val_y + '='
            if self.operand == 'add':
                self.ans = str(float(self.val_x) + float(self.val_y))
            elif self.operand == 'subtract':
                self.ans = str(float(self.val_x) - float(self.val_y))
            elif self.operand == 'multiply':
                self.ans = str(float(self.val_x) * float(self.val_y))
            elif self.operand == 'divide':
                try:
                    self.ans = str(round(float(self.val_x) / float(self.val_y),3))
                except ZeroDivisionError:
                    self.ans = 'Err'
            self.ans = self.ans.rstrip('0').rstrip('.')
            if self.ans != 'Err':
                try:
                    self.ans = int(self.ans)
                except ValueError:
                    self.ans = float(self.ans)
            self.size_check(self.ans)
            self.size_check(self.expression, 'exp')
            self.selected = str(self.ans)
            self.val_x = ''
            self.x_set = False
            self.val_y = ''
            self.previous = ''
            self.op = ''
            self.expr_2 = self.selected
            self.reset_display = True



    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == '1' or keycode[1] == 'numpad1':
            self.num_in('1')
        elif keycode[1] == '2' or keycode[1] == 'numpad2':
            self.num_in('2')
        elif keycode[1] == '3' or keycode[1] == 'numpad3':
            self.num_in('3')
        elif keycode[1] == '4' or keycode[1] == 'numpad4':
            self.num_in('4')
        elif keycode[1] == '5' or keycode[1] == 'numpad5':
            self.num_in('5')
        elif keycode[1] == '6' or keycode[1] == 'numpad6':
            self.num_in('6')
        elif keycode[1] == '7' or keycode[1] == 'numpad7':
            self.num_in('7')
        elif 'shift' not in modifiers and keycode[1] == '8' or keycode[1] == 'numpad8':
            self.num_in('8')
        elif keycode[1] == '9' or keycode[1] == 'numpad9':
            self.num_in('9')
        elif keycode[1] == '0' or keycode[1] == 'numpad0':
            self.zero()
        elif 'shift' in modifiers and keycode[1] == '=' or keycode[1] == 'numpadadd' or keycode[1] == '+' or 'rshift' in modifiers and keycode[1]:
            self.operate('+', 'add')
        elif keycode[1] == '-' or keycode[1] == 'numpadsubtract' or keycode[1] == 'numpadsubstract':
            self.operate('-', 'subtract')
        elif 'shift' in modifiers and keycode[1] == '8' or keycode[1] == 'numpadmul' or keycode[1] == 'x':
            self.operate('*', 'multiply')
        elif keycode[1] == '/' or keycode[1] == 'numpaddivide':
            self.operate('÷', 'divide')
        elif keycode[1] == '=' or keycode[1] == 'enter' or keycode[1] == 'numpadenter':
            self.calc()
        elif keycode[1] == '.' or keycode[1] == 'numpaddecimal':
            self.deci()
        elif keycode[1] == 'backspace':
            self.bspace()
        elif keycode[1] == 'c':
            self.clear_input()
        elif keycode[1] == 'delete':
            self.clear_all()



        return True

class SettingsMenu(Popup):

    def change_resolution(self, x, y):
        '''Changes the screen resolution to be
        x by y pixels in size.'''
        Window.size = (x, y)


class Calculator(App):

    def build(self):
        window = MainMenu()
        return window
        


if __name__ == '__main__':
    Calculator().run()