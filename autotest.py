from serial import Serial
import serial.tools.list_ports
from time import sleep

commands = {
    'close' : b'\x01\x10\x00', 
    'open'  : b'\x01\x0f\x00',
    'stop'  : b'\x01\x13\x00',
    'close_pwm' : b'\x01\x12\x01',
    'open_pwm'  :  b'\x01\x11\x01'
}

def crcCalc(data):
    crc_table = [
        0, 94,188,226, 97, 63,221,131,194,156,126, 32,163,253, 31, 65,
        157,195, 33,127,252,162, 64, 30, 95,  1,227,189, 62, 96,130,220,
        35,125,159,193, 66, 28,254,160,225,191, 93,  3,128,222, 60, 98,
        190,224,  2, 92,223,129, 99, 61,124, 34,192,158, 29, 67,161,255,
        70, 24,250,164, 39,121,155,197,132,218, 56,102,229,187, 89,  7,
        219,133,103, 57,186,228,  6, 88, 25, 71,165,251,120, 38,196,154,
        101, 59,217,135,  4, 90,184,230,167,249, 27, 69,198,152,122, 36,
        248,166, 68, 26,153,199, 37,123, 58,100,134,216, 91,  5,231,185,
        140,210, 48,110,237,179, 81, 15, 78, 16,242,172, 47,113,147,205,
        17, 79,173,243,112, 46,204,146,211,141,111, 49,178,236, 14, 80,
        175,241, 19, 77,206,144,114, 44,109, 51,209,143, 12, 82,176,238,
        50,108,142,208, 83, 13,239,177,240,174, 76, 18,145,207, 45,115,
        202,148,118, 40,171,245, 23, 73,  8, 86,180,234,105, 55,213,139,
        87,  9,235,181, 54,104,138,212,149,203, 41,119,244,170, 72, 22,
        233,183, 85, 11,136,214, 52,106, 43,117,151,201, 74, 20,246,168,
        116, 42,200,150, 21, 75,169,247,182,232, 10, 84,215,137,107, 53
    ]
    result = 0
    for i in data: 
        result = crc_table[result ^ i]  
    return bytes([result])

def send_command(ser, data, value = None):
    if (value is not None):
        data += value
    data += crcCalc(data)
    ser.write(data)

def main():
    ports = list(serial.tools.list_ports.comports())
    for i,port in enumerate(ports):
        print(f'{i} :{port.name}')
    port_name = ""
    if len(ports) == 1:
        port_name = ports[0].name
    else:
        port_num = int(input("enter port num: "))
        port_name = ports[port_num].name
    print(f'Open port {port_name}')
    
    baudrate = 115200
    ser = Serial(port_name, baudrate=baudrate)
    print(f'Serial open {ser.is_open}')
    #pwm_cycle(ser)
    i = 0
    while 1:
        send_command(ser, commands['open_pwm'], bytes([i]))
        send_command(ser, commands['open_pwm'], bytes([i]))


def pwm_cycle(ser):
    i = 0
    pwm_sleep = 0.35
    max_pwm = 30
    while 1:
        for i in range(max_pwm):
            print(f'{i} +  close')
            data = close_pwm + bytes([i])
            #print (data)
            data +=  crcCalc(data)
            #print (crc)
            #data += crc
            print (data)
            ser.write(data)
            sleep(pwm_sleep)
        ser.write(stop)
        sleep(1)
        for i in range(max_pwm):
            print(f'{i} +  open')
            data = open_pwm + bytes([i])
            #print (data)
            data += crcCalc(data)
            print (data)
            ser.write(data)
            sleep(pwm_sleep)
        ser.write(stop)
        sleep(1)
        

def open_close(ser): 
    move_time = 5
    stop_time = 0   
    i = 0
    while 1:
        i+=1
        print(f'---{i}----')
        print("open")
        ser.write(open)
        sleep(move_time)
        print("stop")
        #ser.write(stop)
        sleep(stop_time)
        print("close")
        ser.write(close)
        sleep(move_time)
        print("stop")
        #ser.write(stop)
        sleep(stop_time)

if __name__ == '__main__':
    main()