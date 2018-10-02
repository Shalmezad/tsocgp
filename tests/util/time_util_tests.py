from tsocgp.util import TimeUtil
import unittest

class TimeUtilTests(unittest.TestCase):
    def test_ddi_conversion_minutes(self):
        s = "PT3M"
        t = TimeUtil.ddi_duration_to_seconds(s)
        self.assertEqual(180, t)

    def test_ddi_conversion_seconds(self):
        s = "PT53S"
        t = TimeUtil.ddi_duration_to_seconds(s)
        self.assertEqual(53, t)
    
    def test_ddi_conversion_mixed(self):
        # This appears in problem 5:
        s = "PT2M30S"
        t = TimeUtil.ddi_duration_to_seconds(s)
        self.assertEqual(150, t)

    def test_seconds_since_midnight_to_hms_seconds_single_digit(self):
        s = 2
        t = TimeUtil.seconds_since_midnight_to_hms(s)
        self.assertEqual("00:00:02", t)

    def test_seconds_since_midnight_to_hms_seconds_double_digits(self):
        s = 25
        t = TimeUtil.seconds_since_midnight_to_hms(s)
        self.assertEqual("00:00:25", t)

    def test_seconds_since_midnight_to_hms_minutes_single_digits(self):
        s = 120
        t = TimeUtil.seconds_since_midnight_to_hms(s)
        self.assertEqual("00:02:00", t)
    
    def test_seconds_since_midnight_to_hms_minutes_seconds_single_digits(self):
        s = 125
        t = TimeUtil.seconds_since_midnight_to_hms(s)
        self.assertEqual("00:02:05", t)

    def test_seconds_since_midnight_to_hms_minutes_double_digits(self):
        s = 720
        t = TimeUtil.seconds_since_midnight_to_hms(s)
        self.assertEqual("00:12:00", t)

    def test_seconds_since_midnight_to_hms_full(self):
        s = 73840
        t = TimeUtil.seconds_since_midnight_to_hms(s)
        self.assertEqual("20:30:40", t)

    def test_hms_to_seconds_since_midnight_full(self):
        t = "20:30:40"
        s = TimeUtil.hms_to_seconds_since_midnight(t)
        self.assertEqual(73840, s)