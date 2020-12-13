import os, sys, unittest
import json
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from utilities import file_utilities


class test_file_utilities(unittest.TestCase): 


    def test_read_data_from_json_file_existing_file(self):
        temp = {'test': ["this", "is", "a", "test"]}
        with open('data_files/temp.json', 'w') as json_file:
                json.dump(temp, json_file, sort_keys=True, indent=4)
        executed, read_data = file_utilities.read_data_from_json_file('data_files/temp.json')
        self.assertEqual(read_data, temp)
        os.remove('data_files/temp.json')


    def test_read_data_from_json_file_non_existing_file(self):
        executed, read_data = file_utilities.read_data_from_json_file('data_files/temp.json')
        self.assertFalse(executed)
        self.assertEqual(read_data, {})


    def test_is_non_zero_file_true(self):
        temp = {'test': ["this", "is", "a", "test"]}
        with open('data_files/temp.json', 'w') as json_file:
                json.dump(temp, json_file, sort_keys=True, indent=4)
        file_has_contents = file_utilities.is_non_zero_file('data_files/temp.json')
        self.assertTrue(file_has_contents)
        os.remove('data_files/temp.json')

    
    def test_is_non_zero_file_false(self):
        file_has_contents = file_utilities.is_non_zero_file('data_files/temp.json')
        self.assertFalse(file_has_contents)
        

if __name__ == "__main__":
    unittest.main()