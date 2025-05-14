import unittest
from datetime import datetime
from ..nmea_parser import NMEAParser, GPSData

class TestNMEAParser(unittest.TestCase):
    def setUp(self):
        self.parser = NMEAParser()
        
    def test_ddmm_to_decimal(self):
        # Test latitude conversion
        lat = self.parser._ddmm_to_decimal("1234.5678", "N")
        self.assertAlmostEqual(lat, 12.57613, places=5)
        
        # Test longitude conversion
        lon = self.parser._ddmm_to_decimal("12345.6789", "W")
        self.assertAlmostEqual(lon, -123.761315, places=5)
        
    def test_parse_gprmc(self):
        # Test valid GPRMC sentence
        line = "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"
        self.parser._parse_gprmc(line)
        
        # Check if data was stored in temp_data
        self.assertTrue(len(self.parser.temp_data) > 0)
        
    def test_parse_gpgga(self):
        # Test valid GPGGA sentence
        line = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
        self.parser._current_date = datetime.now().date()  # Set current date
        self.parser._parse_gpgga(line)
        
        # Check if data was stored in temp_data
        self.assertTrue(len(self.parser.temp_data) > 0)

if __name__ == '__main__':
    unittest.main() 