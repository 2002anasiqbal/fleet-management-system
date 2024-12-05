from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# File paths for storing data
VEHICLES_FILE = 'vehicles.csv'
DRIVERS_FILE = 'drivers.csv'
SCHEDULES_FILE = 'schedules.csv'
FINANCE_FILE = 'finance.csv'  # New file for finance data

# Utility function to load data from a CSV file
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

# Utility function to save data to a CSV file
def save_data(filename, fieldnames, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Route: Home
@app.route('/')
def home():
    vehicles = load_data(VEHICLES_FILE)
    drivers = load_data(DRIVERS_FILE)
    schedules = load_data(SCHEDULES_FILE)
    finances = load_data(FINANCE_FILE)
    
    # Aggregate finance data for all vehicles
    total_revenue = sum(float(f['revenue']) for f in finances)
    total_fuel_cost = sum(float(f['fuel_cost']) for f in finances)
    total_maintenance_cost = sum(float(f['maintenance_cost']) for f in finances)

    # Aggregate vehicle data
    total_vehicles = len(vehicles)
    active_vehicle_count = total_vehicles  # Replace with actual condition if needed
    
    # Assuming drivers have a field 'status' to check availability
    available_driver_count = len([d for d in drivers if d.get('status') == 'available'])
    
    # Upcoming routes
    upcoming_routes = [s for s in schedules if s.get('departure_time')]  # Add your condition for upcoming routes
    
    return render_template('home.html', total_revenue=total_revenue,
                           total_fuel_cost=total_fuel_cost, total_maintenance_cost=total_maintenance_cost,
                           vehicles=vehicles, total_vehicles=total_vehicles,
                           active_vehicle_count=active_vehicle_count, 
                           available_driver_count=available_driver_count,
                           upcoming_routes=upcoming_routes)

# ====================== Vehicles ======================
@app.route('/view_vehicles', methods=['GET', 'POST'])
def view_vehicles():
    vehicles = load_data(VEHICLES_FILE)
    return render_template('view_vehicles.html', vehicles=vehicles)

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        vehicles = load_data(VEHICLES_FILE)
        new_vehicle = {
            'registration_number': request.form['registration_number'],
            'model': request.form['model'],
            'seats': request.form['seats'],
            'driver': request.form['driver']
        }
        vehicles.append(new_vehicle)
        save_data(VEHICLES_FILE, ['registration_number', 'model', 'seats', 'driver'], vehicles)
        return redirect(url_for('view_vehicles'))
    drivers = load_data(DRIVERS_FILE)
    return render_template('add_vehicle.html', drivers=drivers)

@app.route('/edit_vehicle/<registration_number>', methods=['GET', 'POST'])
def edit_vehicle(registration_number):
    vehicles = load_data(VEHICLES_FILE)
    vehicle_to_edit = next((v for v in vehicles if v['registration_number'] == registration_number), None)

    if request.method == 'POST' and vehicle_to_edit:
        vehicle_to_edit['model'] = request.form['model']
        vehicle_to_edit['seats'] = request.form['seats']
        vehicle_to_edit['driver'] = request.form['driver']
        save_data(VEHICLES_FILE, ['registration_number', 'model', 'seats', 'driver'], vehicles)
        return redirect(url_for('view_vehicles'))

    drivers = load_data(DRIVERS_FILE)
    return render_template('edit_vehicle.html', vehicle=vehicle_to_edit, drivers=drivers)

@app.route('/delete_vehicle/<registration_number>')
def delete_vehicle(registration_number):
    vehicles = load_data(VEHICLES_FILE)
    vehicles = [v for v in vehicles if v['registration_number'] != registration_number]
    save_data(VEHICLES_FILE, ['registration_number', 'model', 'seats', 'driver'], vehicles)
    return redirect(url_for('view_vehicles'))

# ====================== Drivers ======================
@app.route('/view_drivers', methods=['GET', 'POST'])
def view_drivers():
    drivers = load_data(DRIVERS_FILE)
    return render_template('view_drivers.html', drivers=drivers)

@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if request.method == 'POST':
        drivers = load_data(DRIVERS_FILE)
        new_driver = {
            'driver_name': request.form['driver_name'],
            'driver_id': request.form['driver_id'],
            'license_number': request.form['license_number'],
            'driver_contact': request.form['driver_contact']
        }
        drivers.append(new_driver)
        save_data(DRIVERS_FILE, ['driver_name', 'driver_id', 'license_number', 'driver_contact'], drivers)
        return redirect(url_for('view_drivers'))
    return render_template('add_driver.html')

@app.route('/edit_driver/<driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id):
    drivers = load_data(DRIVERS_FILE)
    driver_to_edit = next((d for d in drivers if d['driver_id'] == driver_id), None)

    if request.method == 'POST' and driver_to_edit:
        driver_to_edit['driver_name'] = request.form['driver_name']
        driver_to_edit['license_number'] = request.form['license_number']
        driver_to_edit['driver_contact'] = request.form['driver_contact']
        save_data(DRIVERS_FILE, ['driver_name', 'driver_id', 'license_number', 'driver_contact'], drivers)
        return redirect(url_for('view_drivers'))

    return render_template('edit_driver.html', driver=driver_to_edit)

@app.route('/delete_driver/<driver_id>')
def delete_driver(driver_id):
    drivers = load_data(DRIVERS_FILE)
    drivers = [d for d in drivers if d['driver_id'] != driver_id]
    save_data(DRIVERS_FILE, ['driver_name', 'driver_id', 'license_number', 'driver_contact'], drivers)
    return redirect(url_for('view_drivers'))

# ====================== Schedules ======================
@app.route('/view_schedules', methods=['GET', 'POST'])
def view_schedules():
    schedules = load_data(SCHEDULES_FILE)
    return render_template('view_schedules.html', schedules=schedules)

@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    if request.method == 'POST':
        schedules = load_data(SCHEDULES_FILE)
        new_schedule = {
            'start_city': request.form['start_city'],
            'stop_city': request.form['stop_city'],
            'assigned_bus': request.form['assigned_bus'],
            'departure_time': request.form['departure_time'],
            'arrival_time': request.form['arrival_time']
        }
        schedules.append(new_schedule)
        save_data(SCHEDULES_FILE, ['start_city', 'stop_city', 'assigned_bus', 'departure_time', 'arrival_time'], schedules)
        return redirect(url_for('view_schedules'))

    vehicles = load_data(VEHICLES_FILE)
    return render_template('add_schedule.html', vehicles=vehicles)

@app.route('/edit_schedule/<start_city>/<stop_city>', methods=['GET', 'POST'])
def edit_schedule(start_city, stop_city):
    schedules = load_data(SCHEDULES_FILE)
    schedule_to_edit = next((s for s in schedules if s['start_city'] == start_city and s['stop_city'] == stop_city), None)

    if request.method == 'POST' and schedule_to_edit:
        schedule_to_edit['assigned_bus'] = request.form['assigned_bus']
        schedule_to_edit['departure_time'] = request.form['departure_time']
        schedule_to_edit['arrival_time'] = request.form['arrival_time']
        save_data(SCHEDULES_FILE, ['start_city', 'stop_city', 'assigned_bus', 'departure_time', 'arrival_time'], schedules)
        return redirect(url_for('view_schedules'))

    vehicles = load_data(VEHICLES_FILE)
    return render_template('edit_schedule.html', schedule=schedule_to_edit, vehicles=vehicles)

@app.route('/delete_schedule/<start_city>/<stop_city>')
def delete_schedule(start_city, stop_city):
    schedules = load_data(SCHEDULES_FILE)
    schedules = [s for s in schedules if not (s['start_city'] == start_city and s['stop_city'] == stop_city)]
    save_data(SCHEDULES_FILE, ['start_city', 'stop_city', 'assigned_bus', 'departure_time', 'arrival_time'], schedules)
    return redirect(url_for('view_schedules'))

# ====================== Finance ======================
@app.route('/view_finance', methods=['GET', 'POST'])
def view_finance():
    finances = load_data(FINANCE_FILE)
    return render_template('view_finance.html', finances=finances)

@app.route('/add_finance', methods=['GET', 'POST'])
def add_finance():
    if request.method == 'POST':
        finances = load_data(FINANCE_FILE)
        new_finance = {
            'month': request.form['month'],
            'bus_registration_number': request.form['bus_registration_number'],
            'revenue': request.form['revenue'],
            'fuel_cost': request.form['fuel_cost'],
            'maintenance_cost': request.form['maintenance_cost']
        }
        finances.append(new_finance)
        save_data(FINANCE_FILE, ['month', 'bus_registration_number', 'revenue', 'fuel_cost', 'maintenance_cost'], finances)
        return redirect(url_for('view_finance'))
    vehicles = load_data(VEHICLES_FILE)
    return render_template('add_finance.html', vehicles=vehicles)

# Start the app
if __name__ == '__main__':
    app.run()
