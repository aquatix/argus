"""Read S.M.A.R.T. disk information and raise alarms where needed"""
import pySMART
import tabulate


def get_smart_attribute(drive, attribute):
    for driveattribute in drive.attributes:
        if not driveattribute:
            continue
        if driveattribute.name == attribute:
            return float(driveattribute.raw)


def get_drive_age(drive):
    hours = get_smart_attribute(drive, 'Power_On_Hours')
    if not hours:
        return 'n/a'
    return str("%8.2f" % (hours / 24 / 365)) + ' years'


def get_drive_temperature(drive):
    temp = get_smart_attribute(drive, 'Temperature_Celsius')
    if temp:
        temp = f'{temp}C'
    else:
        temp = get_smart_attribute(drive, 'Airflow_Temperature_Cel')
        if temp:
            temp = f'{temp}C'
    return temp


def get_drive_reallocated_sectors(drive):
    return get_smart_attribute(drive, 'Reallocated_Sector_Ct')


def get_drive_information(drive):
    temp = get_drive_temperature(drive)
    age = get_drive_age(drive)
    reallocated_sectors = get_drive_reallocated_sectors(drive)
    data = [drive.name, drive.assessment, drive.model, drive.serial, drive.capacity, temp, age, reallocated_sectors]
    return data


def get_information_on_drives(devlist):
    header = ['Name', 'Health', 'Model', 'Serial', 'Capacity', 'Temperature', 'Age (on)', 'Reallocated Sectors']
    data = []
    for device in devlist.devices:
        data.append(get_drive_information(device))
    return header, data


def get_devices():
    return pySMART.DeviceList()


def format_drive_info(header, drive_info):
    return '{} has health status: {}\nModel: {}\nTemperature: {}, {} reallocated sectors.\nIts age is {} years.'.format(
        drive_info[header.index('Name')],
        drive_info[header.index('Health')],
        drive_info[header.index('Model')],
        drive_info[header.index('Temperature')],
        drive_info[header.index('Reallocated Sectors')],
        drive_info[header.index('Age (on)')].strip()
    )


def main():
    devlist = get_devices()
    header, data = get_information_on_drives(devlist)
    print(tabulate.tabulate(data, header, 'rst'))

if __name__ == "__main__":
    main()
