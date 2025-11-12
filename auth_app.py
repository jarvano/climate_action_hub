#!/usr/bin/env python3
"""
Climate Action Hub - User Authentication and Preferences System
A comprehensive Flask application with user authentication, session management, and personalized preferences.
"""

import os
import json
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np

# Initialize Flask app
app = Flask(__name__, template_folder='.', static_folder='.')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'climate-action-hub-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///climate_users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Database Models
class User(UserMixin, db.Model):
    """User model for authentication and preferences"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, cascade='all, delete-orphan')
    saved_analyses = db.relationship('SavedAnalysis', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

class UserPreferences(db.Model):
    """User preferences for personalized experience"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Climate preferences
    preferred_countries = db.Column(db.Text, default='[]')  # JSON array
    preferred_regions = db.Column(db.Text, default='[]')  # JSON array
    preferred_sectors = db.Column(db.Text, default='[]')  # JSON array
    
    # Display preferences
    theme = db.Column(db.String(20), default='light')
    chart_type = db.Column(db.String(20), default='line')
    data_granularity = db.Column(db.String(20), default='annual')
    
    # Notification preferences
    email_notifications = db.Column(db.Boolean, default=True)
    data_updates = db.Column(db.Boolean, default=True)
    forecast_alerts = db.Column(db.Boolean, default=False)
    
    # Analysis preferences
    default_forecast_years = db.Column(db.Integer, default=8)
    confidence_level = db.Column(db.Float, default=0.95)
    
    # Privacy settings
    share_analyses = db.Column(db.Boolean, default=False)
    public_profile = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_preferred_countries(self):
        try:
            return json.loads(self.preferred_countries)
        except:
            return []
    
    def set_preferred_countries(self, countries):
        self.preferred_countries = json.dumps(countries)
    
    def get_preferred_regions(self):
        try:
            return json.loads(self.preferred_regions)
        except:
            return []
    
    def set_preferred_regions(self, regions):
        self.preferred_regions = json.dumps(regions)
    
    def get_preferred_sectors(self):
        try:
            return json.loads(self.preferred_sectors)
        except:
            return []
    
    def set_preferred_sectors(self, sectors):
        self.preferred_sectors = json.dumps(sectors)

class SavedAnalysis(db.Model):
    """Saved analysis results for users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False)  # 'forecast', 'comparison', 'trend'
    description = db.Column(db.Text)
    
    # Analysis data
    countries = db.Column(db.Text, default='[]')  # JSON array
    parameters = db.Column(db.Text, default='{}')  # JSON object
    results = db.Column(db.Text, default='{}')  # JSON object
    chart_data = db.Column(db.Text, default='{}')  # JSON object for chart configuration
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=False)
    
    def get_countries(self):
        try:
            return json.loads(self.countries)
        except:
            return []
    
    def set_countries(self, countries):
        self.countries = json.dumps(countries)
    
    def get_parameters(self):
        try:
            return json.loads(self.parameters)
        except:
            return {}
    
    def set_parameters(self, parameters):
        self.parameters = json.dumps(parameters)
    
    def get_results(self):
        try:
            return json.loads(self.results)
        except:
            return {}
    
    def set_results(self, results):
        self.results = json.dumps(results)
    
    def get_chart_data(self):
        try:
            return json.loads(self.chart_data)
        except:
            return {}
    
    def set_chart_data(self, chart_data):
        self.chart_data = json.dumps(chart_data)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication decorators
def require_active_user(f):
    """Decorator to ensure user is active"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_active:
            flash('Please log in to access this feature.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Home page with authentication status"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            user.update_last_login()
            flash('Welcome back! You have been logged in successfully.', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password, or account is inactive.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required.', 'warning')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'warning')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'warning')
            return render_template('register.html')
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # Create default preferences
            preferences = UserPreferences(user_id=new_user.id)
            db.session.add(preferences)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with personalized content"""
    user_preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    recent_analyses = SavedAnalysis.query.filter_by(user_id=current_user.id).order_by(SavedAnalysis.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         preferences=user_preferences, 
                         recent_analyses=recent_analyses)

@app.route('/profile')
@login_required
def profile():
    """User profile management"""
    return render_template('profile.html')

@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    """User preferences management"""
    user_preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        # Update preferences
        user_preferences.theme = request.form.get('theme', 'light')
        user_preferences.chart_type = request.form.get('chart_type', 'line')
        user_preferences.data_granularity = request.form.get('data_granularity', 'annual')
        user_preferences.default_forecast_years = int(request.form.get('forecast_years', 8))
        user_preferences.confidence_level = float(request.form.get('confidence_level', 0.95))
        user_preferences.email_notifications = request.form.get('email_notifications') == 'on'
        user_preferences.data_updates = request.form.get('data_updates') == 'on'
        user_preferences.forecast_alerts = request.form.get('forecast_alerts') == 'on'
        user_preferences.share_analyses = request.form.get('share_analyses') == 'on'
        user_preferences.public_profile = request.form.get('public_profile') == 'on'
        
        # Handle multi-select fields
        preferred_countries = request.form.getlist('preferred_countries')
        preferred_regions = request.form.getlist('preferred_regions')
        preferred_sectors = request.form.getlist('preferred_sectors')
        
        user_preferences.set_preferred_countries(preferred_countries)
        user_preferences.set_preferred_regions(preferred_regions)
        user_preferences.set_preferred_sectors(preferred_sectors)
        
        try:
            db.session.commit()
            flash('Preferences updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to update preferences.', 'danger')
    
    return render_template('preferences.html', preferences=user_preferences)

@app.route('/save_analysis', methods=['POST'])
@login_required
def save_analysis():
    """Save analysis results"""
    data = request.get_json()
    
    analysis = SavedAnalysis(
        user_id=current_user.id,
        title=data.get('title', 'Untitled Analysis'),
        analysis_type=data.get('analysis_type', 'forecast'),
        description=data.get('description', ''),
        countries=json.dumps(data.get('countries', [])),
        parameters=json.dumps(data.get('parameters', {})),
        results=json.dumps(data.get('results', {})),
        chart_data=json.dumps(data.get('chart_data', {})),
        is_public=data.get('is_public', False)
    )
    
    try:
        db.session.add(analysis)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Analysis saved successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to save analysis.'})

@app.route('/my_analyses')
@login_required
def my_analyses():
    """User's saved analyses"""
    analyses = SavedAnalysis.query.filter_by(user_id=current_user.id).order_by(SavedAnalysis.created_at.desc()).all()
    return render_template('my_analyses.html', analyses=analyses)

@app.route('/api/user/preferences')
@login_required
def get_user_preferences():
    """API endpoint for user preferences"""
    preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()
    if preferences:
        return jsonify({
            'theme': preferences.theme,
            'chart_type': preferences.chart_type,
            'data_granularity': preferences.data_granularity,
            'preferred_countries': preferences.get_preferred_countries(),
            'preferred_regions': preferences.get_preferred_regions(),
            'preferred_sectors': preferences.get_preferred_sectors(),
            'default_forecast_years': preferences.default_forecast_years,
            'confidence_level': preferences.confidence_level,
            'email_notifications': preferences.email_notifications,
            'data_updates': preferences.data_updates,
            'forecast_alerts': preferences.forecast_alerts
        })
    return jsonify({})

# Template context processors
@app.context_processor
def inject_user_status():
    """Inject user authentication status into all templates"""
    return dict(
        current_user=current_user,
        is_authenticated=current_user.is_authenticated
    )

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize database
@app.before_first_request
def create_tables():
    """Create database tables"""
    db.create_all()

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)