#!/usr/bin/env python3
"""
Simple web server to serve the CO2 emissions dashboard with real CSV data
"""
import http.server
import socketserver
import os
import json
import sys

# Add the src directory to the path so we can import data_processor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from data_processor import get_major_countries_data
    REAL_DATA_AVAILABLE = True
except ImportError:
    REAL_DATA_AVAILABLE = False

class CO2DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/api/data':
            self.serve_data()
            return
        elif self.path == '/dashboard.html':
            self.path = '/dashboard.html'
        
        # Serve static files
        if self.path.endswith('.html') or self.path.endswith('.js') or self.path.endswith('.css'):
            try:
                with open(self.path[1:], 'rb') as f:
                    self.send_response(200)
                    if self.path.endswith('.html'):
                        self.send_header('Content-type', 'text/html')
                    elif self.path.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
                    elif self.path.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            super().do_GET()
    
    def serve_data(self):
        try:
            # Try to load real data first
            if REAL_DATA_AVAILABLE:
                real_data = get_major_countries_data()
                if real_data and real_data.get('countries'):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(real_data).encode())
                    print(f"Served real data for {len(real_data['countries'])} countries")
                    return
            
            # Fallback to sample data
            self.serve_sample_data()
            
        except Exception as e:
            print(f"Error serving data: {e}")
            self.serve_sample_data()
    
    def serve_sample_data(self):
        try:
            # Sample data for demonstration
            sample_data = {
                "countries": ["Kenya", "China", "United States", "India", "Germany", "Japan", "Brazil"],
                "years": list(range(2000, 2023)),
                "data": {
                    "Kenya": {
                        "historical": [
                            {"year": 2000, "co2": 8.5, "population": 30.7, "energy": 15.2},
                            {"year": 2005, "co2": 12.3, "population": 35.1, "energy": 18.7},
                            {"year": 2010, "co2": 15.8, "population": 40.5, "energy": 22.1},
                            {"year": 2015, "co2": 19.2, "population": 46.1, "energy": 26.8},
                            {"year": 2020, "co2": 22.1, "population": 53.8, "energy": 31.5},
                            {"year": 2022, "co2": 24.3, "population": 56.2, "energy": 33.7}
                        ]
                    },
                    "China": {
                        "historical": [
                            {"year": 2000, "co2": 3405.5, "population": 1267.4, "energy": 1250.3},
                            {"year": 2005, "co2": 5323.7, "population": 1307.6, "energy": 1987.2},
                            {"year": 2010, "co2": 8236.8, "population": 1340.9, "energy": 2875.6},
                            {"year": 2015, "co2": 9785.2, "population": 1371.2, "energy": 3421.8},
                            {"year": 2020, "co2": 10667.9, "population": 1411.8, "energy": 3654.2},
                            {"year": 2022, "co2": 10877.3, "population": 1412.6, "energy": 3712.5}
                        ]
                    },
                    "United States": {
                        "historical": [
                            {"year": 2000, "co2": 5847.9, "population": 282.2, "energy": 2456.8},
                            {"year": 2005, "co2": 5953.4, "population": 295.5, "energy": 2521.3},
                            {"year": 2010, "co2": 5434.3, "population": 309.3, "energy": 2287.9},
                            {"year": 2015, "co2": 5172.3, "population": 320.7, "energy": 2154.2},
                            {"year": 2020, "co2": 4713.2, "population": 331.0, "energy": 1987.6},
                            {"year": 2022, "co2": 4854.7, "population": 333.3, "energy": 2054.3}
                        ]
                    },
                    "India": {
                        "historical": [
                            {"year": 2000, "co2": 1028.5, "population": 1053.9, "energy": 385.2},
                            {"year": 2005, "co2": 1428.7, "population": 1134.4, "energy": 487.6},
                            {"year": 2010, "co2": 1812.3, "population": 1234.3, "energy": 612.8},
                            {"year": 2015, "co2": 2311.2, "population": 1311.1, "energy": 798.4},
                            {"year": 2020, "co2": 2654.3, "population": 1380.0, "energy": 912.5},
                            {"year": 2022, "co2": 2831.7, "population": 1406.6, "energy": 987.2}
                        ]
                    },
                    "Germany": {
                        "historical": [
                            {"year": 2000, "co2": 856.7, "population": 82.2, "energy": 387.5},
                            {"year": 2005, "co2": 819.3, "population": 82.4, "energy": 365.2},
                            {"year": 2010, "co2": 793.4, "population": 81.8, "energy": 342.8},
                            {"year": 2015, "co2": 778.2, "population": 81.4, "energy": 335.6},
                            {"year": 2020, "co2": 644.3, "population": 83.2, "energy": 287.4},
                            {"year": 2022, "co2": 675.8, "population": 84.4, "energy": 298.7}
                        ]
                    },
                    "Japan": {
                        "historical": [
                            {"year": 2000, "co2": 1184.7, "population": 126.8, "energy": 512.3},
                            {"year": 2005, "co2": 1214.6, "population": 127.8, "energy": 521.7},
                            {"year": 2010, "co2": 1170.8, "population": 128.1, "energy": 498.4},
                            {"year": 2015, "co2": 1148.9, "population": 127.1, "energy": 487.2},
                            {"year": 2020, "co2": 1027.8, "population": 125.8, "energy": 434.6},
                            {"year": 2022, "co2": 1054.3, "population": 125.1, "energy": 445.8}
                        ]
                    },
                    "Brazil": {
                        "historical": [
                            {"year": 2000, "co2": 342.8, "population": 174.5, "energy": 187.6},
                            {"year": 2005, "co2": 412.3, "population": 186.1, "energy": 221.4},
                            {"year": 2010, "co2": 456.7, "population": 195.5, "energy": 245.8},
                            {"year": 2015, "co2": 478.2, "population": 204.5, "energy": 258.3},
                            {"year": 2020, "co2": 421.7, "population": 212.6, "energy": 228.9},
                            {"year": 2022, "co2": 438.5, "population": 214.8, "energy": 237.4}
                        ]
                    }
                }
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(sample_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def main():
    port = 8080
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    with socketserver.TCPServer(("", port), CO2DashboardHandler) as httpd:
        print(f"CO2 Dashboard server running at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            httpd.shutdown()

if __name__ == "__main__":
    main()