import unittest
import os
from pathlib import Path
from ..nmea_parser import NMEAParser

class TestNMEAParserWithRealFiles(unittest.TestCase):
    def setUp(self):
        self.parser = NMEAParser()
        self.test_files_dir = Path(__file__).parent.parent.parent / 'testfiles'
        
    def test_parse_all_files(self):
        """Test parsing all NMEA files in the testfiles directory."""
        for file_path in self.test_files_dir.glob('*.nmea'):
            with self.subTest(file=file_path.name):
                # Parse the file
                gps_data = self.parser.parse_file(str(file_path))
                
                # Basic validation
                self.assertIsNotNone(gps_data, f"Failed to parse {file_path.name}")
                self.assertGreater(len(gps_data), 0, f"No GPS data found in {file_path.name}")
                
                # Validate data structure
                for point in gps_data:
                    self.assertIsNotNone(point.timestamp)
                    self.assertIsNotNone(point.latitude_decimal)
                    self.assertIsNotNone(point.longitude_decimal)
                    self.assertIsNotNone(point.speed_knots)
                    self.assertIsNotNone(point.course_degrees)
                    self.assertIsNotNone(point.fix_quality)
                    self.assertIsNotNone(point.num_satellites)
                    self.assertIsNotNone(point.hdop)
                    self.assertIsNotNone(point.altitude)
                
                # Test coordinate conversion
                coordinates = self.parser.get_coordinates()
                self.assertEqual(len(coordinates), len(gps_data))
                
                # Test timestamp extraction
                timestamps = self.parser.get_timestamps()
                self.assertEqual(len(timestamps), len(gps_data))
                
                # Test distance calculation
                distances = self.parser.get_distances()
                self.assertEqual(len(distances), len(gps_data) - 1)
                
                # Validate coordinate ranges
                for lat, lon in coordinates:
                    self.assertTrue(-90 <= lat <= 90, f"Invalid latitude in {file_path.name}")
                    self.assertTrue(-180 <= lon <= 180, f"Invalid longitude in {file_path.name}")
                
                # Validate speed and course ranges
                for point in gps_data:
                    self.assertTrue(0 <= point.speed_knots, f"Invalid speed in {file_path.name}")
                    self.assertTrue(0 <= point.course_degrees <= 360, f"Invalid course in {file_path.name}")
                
                # Validate fix quality
                for point in gps_data:
                    self.assertTrue(0 <= point.fix_quality <= 8, f"Invalid fix quality in {file_path.name}")
                
                # Validate number of satellites
                for point in gps_data:
                    self.assertTrue(0 <= point.num_satellites <= 32, f"Invalid number of satellites in {file_path.name}")
                
                # Validate HDOP
                for point in gps_data:
                    self.assertTrue(point.hdop >= 0, f"Invalid HDOP in {file_path.name}")
                
                print(f"Successfully parsed {file_path.name}: {len(gps_data)} points")

if __name__ == '__main__':
    unittest.main()