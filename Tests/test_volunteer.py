import unittest
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import volunteer
import quickstart

class Test(unittest.TestCase):


    def test_get_open_volunteer_slots_of_the_day(self):
        result = True
        slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
        open_slots = volunteer.get_open_volunteer_slots_of_the_day('2020-11-13', quickstart.create_service('codeclinic'))
        if len(open_slots) == 0:
            pass
        else:
            for open_slot in open_slots:
                if open_slot not in slots:
                    result = False
        self.assertTrue(result)


    def test_convert_to_digital_time_format_1(self):
        result = volunteer.convert_to_digital_time_format(8,30)
        self.assertEqual(result, '08:30')


    def test_convert_to_digital_time_format_2(self):
        result = volunteer.convert_to_digital_time_format(14,00)
        self.assertEqual(result, '14:00')


    def test_convert_slot_into_30_min_slots(self):
        slot = ('08:30', '10:00')
        result = volunteer.convert_slot_into_30_min_slots(slot)
        self.assertEqual(result, [('08:30', '09:00'), ('09:00', '09:30'), ('09:30', '10:00')])
        

if __name__ == "__main__":
    unittest.main()