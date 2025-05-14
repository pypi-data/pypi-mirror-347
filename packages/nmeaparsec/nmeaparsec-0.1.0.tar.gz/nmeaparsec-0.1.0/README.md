# NmeaParseC

A Python package for parsing NMEA data from GPS devices. This package provides tools to read and process NMEA sentences from GPS log files, with support for common NMEA message types like GPRMC and GPGGA.

## Features

- Parse NMEA sentences from files
- Support for GPRMC and GPGGA message types
- Convert coordinates between DDMM.MMMMM and decimal degrees
- Calculate distances between GPS points using the Haversine formula
- Extract timestamps, coordinates, and other GPS data
- Type hints and dataclass support for better code organization

## Installation

```bash
pip install nmeaparsec
```

## Usage

```python
from nmeaparsec import NMEAParser

# Create a parser instance
parser = NMEAParser()

# Parse a NMEA file
gps_data = parser.parse_file("path/to/your/nmea/file.nmea")

# Get coordinates
coordinates = parser.get_coordinates()

# Get timestamps
timestamps = parser.get_timestamps()

# Calculate distances between consecutive points
distances = parser.get_distances()
```

## Supported NMEA Sentences

- GPRMC (Recommended Minimum Navigation Information)
- GPGGA (Global Positioning System Fix Data)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 