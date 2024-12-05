import obd
import csv
import time

# Connect to the vehicle
connection = obd.OBD(portstr="COM3")

if connection.is_connected():
    print("Successfully connected to the vehicle.\n")

    # Commands to query
    commands = {
        "Engine RPM": obd.commands.RPM,
        "Battery Voltage": obd.commands.ELM_VOLTAGE,
        "Coolant Temperature": obd.commands.COOLANT_TEMP,
        "Speed": obd.commands.SPEED,
        "MAF Sensor": obd.commands.MAF,
        "O2 Sensor": obd.commands.O2_B1S1,
    }

    # File setup
    csv_file = "obd_realtime_data.csv"
    fieldnames = [
        "Timestamp",
        "Control Module Voltage",
        "Engine RPM",
        "Battery Voltage",
        "Coolant Temperature",
        "Speed",
        "MAF Sensor",
        "O2 Sensor",
    ]

    # Write headers to the CSV file if not already written
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    try:
        while True:
            print("Fetching data...")
            data_row = {"Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

            # Fetch real-time data
            for name, command in commands.items():
                response = connection.query(command)
                if response is not None and response.value is not None:
                    data_row[name] = response.value
                else:
                    data_row[name] = "N/A"

            # Save to CSV
            with open(csv_file, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(data_row)

            print(data_row)
            print("\n--- Waiting for 2 seconds before the next fetch ---\n")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nData fetching stopped by user.")
else:
    print("Failed to connect to the vehicle. Check the COM port.")

# Close the connection
connection.close()
