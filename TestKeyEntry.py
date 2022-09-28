import unittest
import Datastore
import OnScreenKeys
import tkinter as ttk


DS = Datastore.Data_Store()
KEY = OnScreenKeys


class KeysTests(unittest.TestCase):

    def setUp(self):
        self.canvas = ttk.Canvas(width=20, height=20)
        self.name_text = self.canvas.create_text(10,10,text="none")

    # Test for keystrokes is acknowledged by the system.
    def test_keystrokes_seen(self):
        print("Keystrokes seen")
        self.keys = ""
        self.shift_lock = False
        
        KEY.Keyboard.press(self,'t')
        
        result = self.keys
        
        self.assertEqual(result, "t")
        
        self.keys = ""
        
        KEY.Keyboard.shift(self)
        KEY.Keyboard.press(self,'t')

        result1 = self.keys
        
        self.assertEqual(result1, "T")
    
    # Test that the keystrokes have been saved to file.
    def test_keystrokes_saved_to_file(self):
        print("Keystrokes saved to file")
    
        self.keys = ""
        self.shift_lock = False
    
        KEY.Keyboard.press(self,'t')
        KEY.Keyboard.press(self,'h')
        KEY.Keyboard.press(self,'e')
        
        result = DS.get_keyboard_data()
        
        self.assertEqual(result, "the")
    
    
    
if __name__ == '__main__':
    unittest.main()