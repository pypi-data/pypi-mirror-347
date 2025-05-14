import unittest
import os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from ..nmea_parser import NMEAParser

class TestNMEAVisualization(unittest.TestCase):
    def setUp(self):
        self.parser = NMEAParser()
        self.test_files_dir = Path(__file__).parent.parent.parent / 'testfiles'
        self.output_dir = Path(__file__).parent.parent.parent / 'visualization_output'
        self.output_dir.mkdir(exist_ok=True)
        
    def test_visualize_tracks(self):
        """Test parsing and visualizing all NMEA files."""
        # Create a figure for all tracks
        plt.figure(figsize=(15, 10))
        
        # Create a colormap for different files
        colors = plt.cm.rainbow(np.linspace(0, 1, len(list(self.test_files_dir.glob('*.nmea')))))
        
        for i, (file_path, color) in enumerate(zip(sorted(self.test_files_dir.glob('*.nmea')), colors)):
            # Parse the file
            gps_data = self.parser.parse_file(str(file_path))
            
            if not gps_data:
                print(f"Warning: No data found in {file_path.name}")
                continue
                
            # Get coordinates
            coordinates = self.parser.get_coordinates()
            lats, lons = zip(*coordinates)
            
            # Plot the track
            plt.plot(lons, lats, color=color, label=file_path.name, linewidth=2, alpha=0.7)
            
            # Plot start and end points
            plt.plot(lons[0], lats[0], 'o', color=color, markersize=8)
            plt.plot(lons[-1], lats[-1], 's', color=color, markersize=8)
            
            # Create individual track plot
            plt.figure(figsize=(10, 8))
            plt.plot(lons, lats, color='blue', linewidth=2)
            plt.plot(lons[0], lats[0], 'go', markersize=10, label='Start')
            plt.plot(lons[-1], lats[-1], 'ro', markersize=10, label='End')
            
            # Add speed as color gradient
            speeds = [point.speed_knots for point in gps_data]
            points = plt.scatter(lons, lats, c=speeds, cmap='viridis', s=50, alpha=0.6)
            plt.colorbar(points, label='Speed (knots)')
            
            # Add labels and title
            plt.title(f'GPS Track: {file_path.name}')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.legend()
            plt.grid(True)
            
            # Save individual track plot
            plt.savefig(self.output_dir / f'{file_path.stem}_track.png')
            plt.close()
            
            print(f"Processed {file_path.name}: {len(gps_data)} points")
            print(f"Track bounds: Lat [{min(lats):.4f}, {max(lats):.4f}], Lon [{min(lons):.4f}, {max(lons):.4f}]")
            print(f"Average speed: {np.mean(speeds):.2f} knots")
            print("-" * 50)
        
        # Finalize the combined plot
        plt.title('All GPS Tracks')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        
        # Save the combined plot
        plt.savefig(self.output_dir / 'all_tracks.png', bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"\nVisualization complete! Check the 'visualization_output' directory for the plots.")

if __name__ == '__main__':
    unittest.main() 