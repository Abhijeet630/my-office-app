from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_super_secret_key_here' # IMPORTANT: Change this to a strong, random, and secret key in production!

# Initialize SQLAlchemy object
db = SQLAlchemy(app)

# Make the datetime object globally available in Jinja2 templates
@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

# Database Model: ComputerSystem 
class ComputerSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.String(100))
    department = db.Column(db.String(100))
    host_name = db.Column(db.String(100), nullable=False)
    employee_name = db.Column(db.String(100))
    ip_address = db.Column(db.String(100))
    operating_system = db.Column(db.String(100))
    product_model = db.Column(db.String(100))
    pc_type = db.Column(db.String(100))
    processor = db.Column(db.String(100))
    price = db.Column(db.String(100))
    ram_size = db.Column(db.String(100))
    hard_disk_type = db.Column(db.String(100))
    hard_disk_size = db.Column(db.String(100))
    hard_disk_sn = db.Column(db.String(100))
    ssd_disk_type = db.Column(db.String(100))
    ssd_disk_size = db.Column(db.String(100))
    ssd_hard_disk_sn = db.Column(db.String(100))
    adapter_mac_address = db.Column(db.String(100))
    external_lancard = db.Column(db.String(100))
    display_make_model = db.Column(db.String(100))
    display_serial_number = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<ComputerSystem {self.host_name}>'

# Updated Database Model: Router (Sr. No. removed)
class Router(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # sr_no = db.Column(db.String(50)) # REMOVED: Sr. No. is now handled by loop.index in table display
    department = db.Column(db.String(100))
    router_name = db.Column(db.String(100))
    router_model_name = db.Column(db.String(100))
    serial_no = db.Column(db.String(100))
    router_connected = db.Column(db.String(100))
    price_list = db.Column(db.String(100))

    def __repr__(self):
        return f'<Router {self.router_name}>'

# Create database tables within the application context
# IMPORTANT: Since Router model changed, you MUST delete 'database.db' again!
with app.app_context():
    db.create_all()

# --- Route Definitions (ComputerSystem routes remain unchanged) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/system_info')
def system_info_list():
    systems = ComputerSystem.query.all()
    return render_template('system_info.html', systems=systems)

@app.route('/system_info/add', methods=['GET', 'POST'])
def add_system_info():
    # ... (unchanged) ...
    if request.method == 'POST':
        floor = request.form.get('floor')
        department = request.form.get('department')
        host_name = request.form['host_name']
        employee_name = request.form.get('employee_name')
        ip_address = request.form.get('ip_address')
        operating_system = request.form.get('operating_system')
        product_model = request.form.get('product_model')
        pc_type = request.form.get('pc_type')
        processor = request.form.get('processor')
        price = request.form.get('price')
        ram_size = request.form.get('ram_size')
        hard_disk_type = request.form.get('hard_disk_type')
        hard_disk_size = request.form.get('hard_disk_size')
        hard_disk_sn = request.form.get('hard_disk_sn')
        ssd_disk_type = request.form.get('ssd_disk_type')
        ssd_disk_size = request.form.get('ssd_disk_size')
        ssd_hard_disk_sn = request.form.get('ssd_hard_disk_sn')
        adapter_mac_address = request.form.get('adapter_mac_address')
        external_lancard = request.form.get('external_lancard')
        display_make_model = request.form.get('display_make_model')
        display_serial_number = request.form.get('display_serial_number')

        if not host_name:
            flash('Host Name is required!', 'danger')
            return redirect(url_for('add_system_info'))

        new_system = ComputerSystem(
            floor=floor, department=department, host_name=host_name, employee_name=employee_name,
            ip_address=ip_address, operating_system=operating_system, product_model=product_model,
            pc_type=pc_type, processor=processor, price=price, ram_size=ram_size,
            hard_disk_type=hard_disk_type, hard_disk_size=hard_disk_size, hard_disk_sn=hard_disk_sn,
            ssd_disk_type=ssd_disk_type, ssd_disk_size=ssd_disk_size, ssd_hard_disk_sn=ssd_hard_disk_sn,
            adapter_mac_address=adapter_mac_address, external_lancard=external_lancard,
            display_make_model=display_make_model, display_serial_number=display_serial_number
        )
        try:
            db.session.add(new_system)
            db.session.commit()
            flash('System Information added successfully!', 'success')
            return redirect(url_for('system_info_list'))
        except Exception as e:
            flash(f'Error adding system information: {e}', 'danger')
            db.session.rollback()

    return render_template('system_info_form.html', title='Add System Information')

@app.route('/system_info/edit/<int:id>', methods=['GET', 'POST'])
def edit_system_info(id):
    # ... (unchanged) ...
    system = ComputerSystem.query.get_or_404(id)
    if request.method == 'POST':
        system.floor = request.form.get('floor')
        system.department = request.form.get('department')
        system.host_name = request.form['host_name']
        system.employee_name = request.form.get('employee_name')
        system.ip_address = request.form.get('ip_address')
        system.operating_system = request.form.get('operating_system')
        system.product_model = request.form.get('product_model')
        system.pc_type = request.form.get('pc_type')
        system.processor = request.form.get('processor')
        system.price = request.form.get('price')
        system.ram_size = request.form.get('ram_size')
        system.hard_disk_type = request.form.get('hard_disk_type')
        system.hard_disk_size = request.form.get('hard_disk_size')
        system.hard_disk_sn = request.form.get('hard_disk_sn')
        system.ssd_disk_type = request.form.get('ssd_disk_type')
        system.ssd_disk_size = request.form.get('ssd_disk_size')
        system.ssd_hard_disk_sn = request.form.get('ssd_hard_disk_sn')
        system.adapter_mac_address = request.form.get('adapter_mac_address')
        system.external_lancard = request.form.get('external_lancard')
        system.display_make_model = request.form.get('display_make_model')
        system.display_serial_number = request.form.get('display_serial_number')

        if not system.host_name:
            flash('Host Name is required!', 'danger')
            return redirect(url_for('edit_system_info', id=id))

        try:
            db.session.commit()
            flash('System Information updated successfully!', 'success')
            return redirect(url_for('system_info_list'))
        except Exception as e:
            flash(f'Error updating system information: {e}', 'danger')
            db.session.rollback()

    return render_template('system_info_form.html', system=system, title='Edit System Information')

@app.route('/system_info/delete/<int:id>', methods=['POST'])
def delete_system_info(id):
    # ... (unchanged) ...
    system = ComputerSystem.query.get_or_404(id)
    try:
        db.session.delete(system)
        db.session.commit()
        flash('System Information deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting system information: {e}', 'danger')
        db.session.rollback()
    return redirect(url_for('system_info_list'))

# --- New Routes for Router Information (Sr. No. handling updated) ---

# List Router Information Route
@app.route('/router_info')
def router_info_list():
    routers = Router.query.all()
    return render_template('router_info.html', routers=routers)

# Add New Router Information Route
@app.route('/router_info/add', methods=['GET', 'POST'])
def add_router_info():
    if request.method == 'POST':
        # Removed 'sr_no' from form retrieval
        department = request.form.get('department')
        router_name = request.form.get('router_name')
        router_model_name = request.form.get('router_model_name')
        serial_no = request.form.get('serial_no')
        router_connected = request.form.get('router_connected')
        price_list = request.form.get('price_list')

        new_router = Router(
            department=department, router_name=router_name, # sr_no is not passed here
            router_model_name=router_model_name, serial_no=serial_no,
            router_connected=router_connected, price_list=price_list
        )
        try:
            db.session.add(new_router)
            db.session.commit()
            flash('Router Information added successfully!', 'success')
            return redirect(url_for('router_info_list'))
        except Exception as e:
            flash(f'Error adding router information: {e}', 'danger')
            db.session.rollback()
    return render_template('router_info_form.html', title='Add Router Information')

# Edit Existing Router Information Route
@app.route('/router_info/edit/<int:id>', methods=['GET', 'POST'])
def edit_router_info(id):
    router = Router.query.get_or_404(id)
    if request.method == 'POST':
        # Removed 'sr_no' from form update
        router.department = request.form.get('department')
        router.router_name = request.form.get('router_name')
        router.router_model_name = request.form.get('router_model_name')
        router.serial_no = request.form.get('serial_no')
        router.router_connected = request.form.get('router_connected')
        router.price_list = request.form.get('price_list')

        try:
            db.session.commit()
            flash('Router Information updated successfully!', 'success')
            return redirect(url_for('router_info_list'))
        except Exception as e:
            flash(f'Error updating router information: {e}', 'danger')
            db.session.rollback()
    return render_template('router_info_form.html', router=router, title='Edit Router Information')

# Delete Router Information Route
@app.route('/router_info/delete/<int:id>', methods=['POST'])
def delete_router_info(id):
    router = Router.query.get_or_404(id)
    try:
        db.session.delete(router)
        db.session.commit()
        flash('Router Information deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting router information: {e}', 'danger')
        db.session.rollback()
    return redirect(url_for('router_info_list'))

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) # debug=True is for development, set to False in production