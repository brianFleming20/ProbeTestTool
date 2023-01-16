import OnScreenKeys
from tkinter import Canvas, messagebox
import Datastore

KEY = OnScreenKeys
DS = Datastore.Data_Store()
FONT_NAME = "Courier"


class TestKeyboard:

    def test_convert_key(self):
        key = "h"
        expected = "H"
        result = KEY.convert_key(key)
        assert result == expected

    def test_wait_for_response(self, capsys):
        test_canvas = Canvas(width=1100, height=280)
        name_text = test_canvas.create_text(70, 18, text="lower case", fill="black", font=(FONT_NAME, 12, "bold"))
        test_canvas.pack()
        expected = "h"
        with capsys.disabled():
            print('Press the letter "H"')
        KEY.Keyboard().get_keyboard()
        result = KEY.wait_for_response(test_canvas, name_text)
        assert result == expected


    def test_get_keyboard(self):
        KEY.Keyboard().get_keyboard()
        result = messagebox.askyesno(title="Keys", message="Is the keyboard showing?")
        assert result is True

    def test_end_keyboard(self):
        K = KEY.Keyboard()
        expected = "h+"
        DS.write_to_from_keys("")
        result_keys1 = K.keys
        assert result_keys1 == ""
        K.keys = "h"
        K.end_keyboard("+")
        result = DS.get_keyboard_data()
        assert result == expected

    def test_clear(self):
        K = KEY.Keyboard()
        K.keys = "once"
        expected = "onc"
        K.clear()
        result = K.keys
        assert result == expected

    def test_shift(self):
        K = KEY.Keyboard()
        K.get_keyboard()
        K.shift()
        result1 = K.shift_lock
        assert result1 is True
        K.shift()
        result2 = K.shift_lock
        assert result2 is False

    def test_press(self):
        K = KEY.Keyboard()
        expected1 = "the"
        K.press('t')
        K.press('h')
        K.press('e')
        result = DS.get_keyboard_data()
        assert result == expected1
        K.keys = ""

        K.shift_lock = True
        expected2 = "THE"
        K.press('t')
        K.press('h')
        K.press('e')
        result1 = DS.get_keyboard_data()
        assert result1 == expected2


