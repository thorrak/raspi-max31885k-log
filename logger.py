# Set up the imports
import os
import glob
import time
import datetime
import RPi.GPIO as GPIO

# When the script launches, make sure that the one wire modules are loaded
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

 # Then find all of the DS18B20 devices hooked up
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


# Now set up the pins for our power detection mechanism
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def outlet_powered():
    return GPIO.input(6)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Ok, now let's set up the main loop
i = 0
fname = "{0}.txt".format(datetime.date.today().strftime("%Y%m%d-%H%M%S"))
f = open(fname, 'w')
f.write("Loop,Date,Time,Temp_C,Temp_F,Powered\n")
while True:
    temp_c, temp_f = read_temp()

    today_date = datetime.date.today()

    # The log string is {Loop},{Date},{Time},{Temp_C},{Temp_F},{Powered}
    log_string = "{0},{1},{2},{3},{4},{5}\n".format(i, today_date.strftime("%Y-%m-%d"), today_date.strftime("%H:%M:%S"),
                                                  temp_c, temp_f, outlet_powered())
    f.write(log_string)
    print(log_string[:(log_string.__len__()-1)])
    time.sleep(1)

f.close()