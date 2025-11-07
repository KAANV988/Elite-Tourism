import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# --- App Configuration ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Database Setup ---
db = SQLAlchemy(app)

# --- Login Manager Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info' 

# --- Database Models ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

# RENAMED: from Destination to State
class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    # NEW: This links a State to its 'children' Cities
    # When a State is deleted, all its Cities are also deleted.
    cities = db.relationship('City', backref='state', lazy=True, cascade='all, delete-orphan')

# NEW: The City model
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    # NEW: This holds the detailed text for the city page
    details = db.Column(db.Text, nullable=True) 
    # NEW: This is the Foreign Key that links this City to its 'parent' State
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- User-Facing Page Routes ---

@app.route('/')
def home():
    # Now, this fetches all STATES to show on the homepage
    all_states = State.query.all()
    return render_template('index.html', states=all_states) # Renamed 'destinations' to 'states'

# NEW: This page shows the cities *inside* a state
@app.route('/state/<int:state_id>')
def state_detail(state_id):
    state = State.query.get_or_404(state_id)
    # The template will be able to access state.cities
    return render_template('state_detail.html', state=state)

# NEW: This page shows the details for a single city
@app.route('/city/<int:city_id>')
def city_detail(city_id):
    city = City.query.get_or_404(city_id)
    # The template will have access to city.name, city.details, etc.
    return render_template('city_detail.html', city=city)

# --- Auth Routes (Login, Register, Logout) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_panel'))
        else:
            return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user) 
            flash('Logged in successfully!', 'success')
            if user.is_admin:
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password') 
        if email.lower() == 'admin@gmail.com':
            flash('This email is reserved for administrative use.', 'danger')
            return redirect(url_for('register'))
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered.', 'warning')
            return redirect(url_for('register'))
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required 
def logout():
    logout_user() 
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required 
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_panel'))
    return render_template('dashboard.html')

# --- Admin Routes ---

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))
    return render_template('admin.html')

# RENAMED: from 'admin_destinations' to 'admin_states'
@app.route('/admin/states', methods=['GET', 'POST'])
@login_required
def admin_states():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        image_filename = request.form.get('image_filename')
        
        existing_state = State.query.filter_by(name=name).first()
        if existing_state:
            flash('A state with this name already exists.', 'danger')
        else:
            new_state = State(name=name, description=description, image_filename=image_filename)
            db.session.add(new_state)
            db.session.commit()
            flash('State added successfully!', 'success')
        
        return redirect(url_for('admin_states'))

    all_states = State.query.all()
    # RENAMED: 'admin_destinations.html' to 'admin_states.html'
    # RENAMED: 'destinations' to 'states'
    return render_template('admin_states.html', states=all_states) 

# RENAMED: from 'edit_destination' to 'edit_state'
@app.route('/admin/state/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_state(id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    state_to_edit = State.query.get_or_404(id)

    if request.method == 'POST':
        state_to_edit.name = request.form.get('name')
        state_to_edit.description = request.form.get('description')
        state_to_edit.image_filename = request.form.get('image_filename')
        
        db.session.commit()
        flash('State updated successfully!', 'success')
        return redirect(url_for('admin_states'))

    # RENAMED: 'edit_destination.html' to 'edit_state.html'
    return render_template('edit_state.html', state=state_to_edit) 

# RENAMED: from 'delete_destination' to 'delete_state'
@app.route('/admin/state/delete/<int:id>')
@login_required
def delete_state(id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
        
    state_to_delete = State.query.get_or_404(id)
    db.session.delete(state_to_delete)
    db.session.commit()
    flash('State deleted successfully.', 'success')
    return redirect(url_for('admin_states'))

# --- NEW: Admin Routes for CITIES ---

@app.route('/admin/state/<int:state_id>/cities', methods=['GET', 'POST'])
@login_required
def admin_cities(state_id):
    # THIS IS THE FIX: Changed 'is__admin' to 'is_admin'
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    state = State.query.get_or_404(state_id)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        image_filename = request.form.get('image_filename')
        details = request.form.get('details') # The new details field

        new_city = City(
            name=name, 
            description=description, 
            image_filename=image_filename,
            details=details,
            state_id=state_id # Link to the parent state
        )
        db.session.add(new_city)
        db.session.commit()
        flash('City added successfully!', 'success')
        return redirect(url_for('admin_cities', state_id=state_id))
    
    # Show the page with the state's info and its list of cities
    return render_template('admin_cities.html', state=state, cities=state.cities)

@app.route('/admin/city/edit/<int:city_id>', methods=['GET', 'POST'])
@login_required
def edit_city(city_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    city_to_edit = City.query.get_or_404(city_id)

    if request.method == 'POST':
        city_to_edit.name = request.form.get('name')
        city_to_edit.description = request.form.get('description')
        city_to_edit.image_filename = request.form.get('image_filename')
        city_to_edit.details = request.form.get('details')
        
        db.session.commit()
        flash('City updated successfully!', 'success')
        # Redirect back to the list of cities for that state
        return redirect(url_for('admin_cities', state_id=city_to_edit.state_id)) 

    return render_template('edit_city.html', city=city_to_edit)

@app.route('/admin/city/delete/<int:city_id>')
@login_required
def delete_city(city_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
        
    city_to_delete = City.query.get_or_404(city_id)
    state_id = city_to_delete.state_id # Save this before we delete!
    
    db.session.delete(city_to_delete)
    db.session.commit()
    flash('City deleted successfully.', 'success')
    return redirect(url_for('admin_cities', state_id=state_id))


# --- Main Entry Point ---
def create_admin_user():
    with app.app_context():
        db.create_all() # This now creates ALL 3 tables
        admin_user = User.query.filter_by(email='admin@gmail.com').first()
        if not admin_user:
            print("Creating admin user...")
            new_admin = User(
                name='Admin', 
                email='admin@gmail.com', 
                password='Admin@123',
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_admin_user()
    app.run(debug=True, port=5000)