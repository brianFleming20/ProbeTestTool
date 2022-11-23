import unittest
import Datastore
import OnScreenKeys
import tkinter as ttk


DS = Datastore.Data_Store()
KEY = OnScreenKeys.Keyboard()


class KeysTests(unittest.TestCase):

    # Test for keystrokes is acknowledged by the system.
    def test_keystrokes_seen(self):
        print("Keystrokes case change")
        KEY.keys = ""
        KEY.get_keyboard()
        self.shift_lock = False
        
        KEY.press('t')
        
        result = KEY.keys
        print(f"press key {result}")
        
        self.assertEqual(result, "t")
        
        KEY.keys = ""
        
        KEY.shift()
        KEY.press('t')

        result1 = KEY.keys
        
        self.assertEqual(result1, "T")
    
    # Test that the keystrokes have been saved to file.
    def test_keystrokes_saved_to_file(self):
        print("Keystrokes saved to file")
    
        KEY.keys = ""
        self.shift_lock = False
    
        KEY.press('t')
        KEY.press('h')
        KEY.press('e')
        
        result = DS.get_keyboard_data()
        
        self.assertEqual(result, "the")


if __name__ == '__main__':
    unittest.main()