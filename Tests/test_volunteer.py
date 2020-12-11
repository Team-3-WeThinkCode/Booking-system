import unittest
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import volunteer
import quickstart

class Test(unittest.TestCase):

    def test_convert_90_min_slot_into_min_slot(self):
        slot = ('13:00', '14:30')
        result = volunteer.convert_90_min_slot_into_30_min_slots(slot)
        self.assertEqual(result, [('13:00', '13:30'), ('13:30', '14:00'), ('14:00', '14:30')], "Error in converting 90min slot to 30min slot.")
        
        slot = ('13:30', '15:00')
        result = volunteer.convert_90_min_slot_into_30_min_slots(slot)
        self.assertEqual(result, [('13:30', '14:00'), ('14:00', '14:30'), ('14:30', '15:00')], "Error in converting 90min slot to 30min slot.")
        

if __name__ == "__main__":
    unittest.main()