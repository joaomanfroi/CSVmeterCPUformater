import csv
import datetime
import os

serial_numbers = []

user_id = 'manfroij'
time = (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime('%H:%M')
date =  datetime.date.today().strftime("%m/%d/%y")
service_location = 'ped'
# serviceTimeZone = ''
service_timezone = '-3:00/NoDST'

def load_serial_numbers() -> bool:
    global serial_numbers
    if not os.path.exists('files/serial_numbers.txt'):
        with open('files/serial_numbers.txt', 'w') as file:
            file.write("# Add serial numbers here, one per line, hex format\n")
            print("serial_numbers.txt created. Please add serial numbers.")
            return False
    try:
        with open('files/serial_numbers.txt', 'r') as file:
            if len(file.readlines()) == 0:
                print("Error: serial_numbers.txt is empty. Please add serial numbers.")
                return False
            for line in file:
                if not line.startswith('#') and line.strip():
                    if len(line.strip()) != 8 or not all(c in '0123456789ABCDEFabcdef' for c in line.strip()):
                            print("Invalid serial number: %s" % line.strip())
                            continue
                    if line.strip() not in serial_numbers:
                        serial_numbers.append(line.strip())
        print("Serial numbers loaded successfully.")
        return True
    except IOError:
        print("Error: Unable to read serial_numbers.txt file.")
        return False
    except Exception as e:
        print("An unexpected error occurred: %s" % str(e))
        return False


def create_csv():
    global manufacture_writer, installation_writer
    try:
        manufacture_writer = csv.writer(open('files/manufacture_data.csv', 'w', newline=""), dialect='excel')
        installation_writer = csv.writer(open('files/installation_data.csv', 'w', newline=""), dialect='excel')

        manufacture_header = ("manufacturer","customer","shippedTo","shippedToState","shippedDate","custMeterNo",
                          "mfgSerialNumber","amrSerialnumber","kH","numDials","form","base","class","detentMode",
                          "KM","KMh","edgeSerialNumber")
        installation_header = ("UserID","InstallationDate","InstallationTime","ChangeOutMeterNo","ChangeOutMeterkWh", 
                           "InstalledMeterNo","InstalledEndpointSN","InstalledMeterkWh","ServiceLatitude","ServiceLongitude",
                           "ServiceLocation","ServiceTimeZone","TenantGroup")
        
        manufacture_writer.writerow(manufacture_header)
        installation_writer.writerow(installation_header)
        print('CSV files created successfully.')
    except FileNotFoundError:
        print('Error: Unable to create CSV files.')
    except IOError:
        print('Error: Unable to write to CSV files.')
    except Exception as e:
        print('An unexpected error occurred: %s' % str(e))
    

def generate_files():
    global manufacture_writer, installation_writer

    for serial in serial_numbers:
        manufacture_vector = ('', '', '', '', '', serial, int(serial, 16), int(serial, 16), '', '', '', '', '', '', '', '')
        installation_vector = (user_id, date, time, serial, '', serial, int(serial, 16), '', '', '', service_location, service_timezone, '')

        manufacture_writer.writerow(manufacture_vector)
        installation_writer.writerow(installation_vector)
    print('Manufature and Installation files generated successfully.')

if load_serial_numbers():
    create_csv()
    generate_files()
    print('Ending program...')

