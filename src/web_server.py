#!/usr/bin/env python3
"""
Simple web server to serve the CO2 emissions dashboard
"""
import http.server
import socketserver
import os
import json
import pandas as pd
from urllib.parse import urlparse, parse_qs

class CO2DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/dashboard.html':
            # Serve the HTML dashboard
            self.path = '/dashboard.html'
            return super().do_GET()
        elif self.path.startswith('/api/data'):
            # Serve data API
            self.serve_data()
        else:
            super().do_GET()
    
    def serve_data(self):
        try:
            # Load the CO2 data
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'owid-co2-data.csv')
            df = pd.read_csv(data_path)
            
            # Get query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Filter by countries if specified
            if 'countries' in query_params:
                countries = query_params['countries'][0].split(',')
                df = df[df['country'].isin(countries)]
            
            # Get unique countries and years
            countries = sorted(df['country'].unique().tolist())
            years = sorted(df['year'].unique().tolist())
            
            # Prepare response data
            response_data = {
                'countries': countries,
                'years': years,
                'data': {}
            }
            
            # Process data for each country
            for country in countries:
                country_df = df[df['country'] == country].copy()
                country_df = country_df.dropna(subset=['co2', 'year'])
                country_df = country_df.sort_values('year')
                
                response_data['data'][country] = {
                    'historical': []
                }
                
                for _, row in country_df.iterrows():
                    response_data['data'][country]['historical'].append({
                        'year': int(row['year']),
                        'co2': float(row['co2']) if pd.notna(row['co2']) else 0,
                        'population': float(row['population']) if pd.notna(row['population']) else 0,
                        'energy': float(row['primary_energy_consumption']) if pd.notna(row['primary_energy_consumption']) else 0
                    })
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def main():
    port = 8080
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
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