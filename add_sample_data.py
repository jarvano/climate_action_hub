#!/usr/bin/env python3
"""
Script to add sample data to the database for testing the user dashboard
"""

import json
from simple_auth_app import app, db, User, SavedAnalysis

# Create sample data within the app context
with app.app_context():
    # Get the admin user
    admin_user = User.query.filter_by(username='admin').first()
    
    if admin_user:
        # Add sample saved analyses
        sample_analyses = [
            {
                'title': 'Global CO2 Emissions Forecast 2024',
                'analysis_type': 'forecast',
                'description': 'Comprehensive analysis of global CO2 emissions trends and future projections',
                'countries': ['United States', 'China', 'India', 'Germany', 'Japan'],
                'parameters': {'forecast_years': 10, 'confidence_level': 0.95},
                'results': {'total_emissions': 35000, 'growth_rate': 2.3, 'peak_year': 2028},
                'chart_data': {'type': 'line', 'x_axis': 'years', 'y_axis': 'emissions'},
                'is_public': True
            },
            {
                'title': 'European Union Climate Targets Analysis',
                'analysis_type': 'comparison',
                'description': 'Comparative analysis of EU climate targets vs current progress',
                'countries': ['Germany', 'France', 'Italy', 'Spain', 'Netherlands'],
                'parameters': {'target_year': 2030, 'reduction_target': 0.55},
                'results': {'current_progress': 0.42, 'gap_to_target': 0.13, 'required_effort': 'high'},
                'chart_data': {'type': 'bar', 'x_axis': 'countries', 'y_axis': 'reduction_percentage'},
                'is_public': False
            },
            {
                'title': 'Renewable Energy Adoption Trends',
                'analysis_type': 'trend',
                'description': 'Analysis of renewable energy adoption rates across major economies',
                'countries': ['China', 'United States', 'India', 'Japan', 'Germany'],
                'parameters': {'time_period': '2015-2024', 'energy_types': ['solar', 'wind', 'hydro']},
                'results': {'total_capacity': 2800, 'growth_rate': 12.5, 'leading_country': 'China'},
                'chart_data': {'type': 'area', 'x_axis': 'years', 'y_axis': 'capacity_gw'},
                'is_public': True
            }
        ]
        
        for analysis_data in sample_analyses:
            # Check if analysis already exists
            existing = SavedAnalysis.query.filter_by(
                user_id=admin_user.id,
                title=analysis_data['title']
            ).first()
            
            if not existing:
                analysis = SavedAnalysis(
                    user_id=admin_user.id,
                    title=analysis_data['title'],
                    analysis_type=analysis_data['analysis_type'],
                    description=analysis_data['description'],
                    countries=json.dumps(analysis_data['countries']),
                    parameters=json.dumps(analysis_data['parameters']),
                    results=json.dumps(analysis_data['results']),
                    chart_data=json.dumps(analysis_data['chart_data']),
                    is_public=analysis_data['is_public']
                )
                db.session.add(analysis)
        
        db.session.commit()
        print("Sample data added successfully!")
        
        # Show current analyses
        analyses = SavedAnalysis.query.filter_by(user_id=admin_user.id).all()
        print(f"Total analyses for admin user: {len(analyses)}")
        for analysis in analyses:
            print(f"  - {analysis.title} ({analysis.analysis_type})")
    else:
        print("Admin user not found!")

print("Sample data script completed!")