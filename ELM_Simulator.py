import os
import serial
import serial.tools.list_ports


class InvalidSerialPort(Exception):
    pass

def serial_ports():
    return [p.device for p in serial.tools.list_ports.comports(include_links=True)]


if __name__ == '__main__':
    try:
        port_found = False
        
        while not port_found:
            port = input('Specify Arduino Serial Port: ')
            
            for p in serial_ports():
                if p == port or os.path.split(p)[-1] == port:
                    port_found = True
                    break
            
            if not port_found:
                print('Invalid serial port specified. Valid options are:\n\n\t{ports},\n\nbut {port} was provided'.format(
                       **{'ports': serial_ports(), 'port': port}))
                exit()
        
        connection = serial.Serial()
        connection.port = port
        connection.baudrate = 115200
        
        try:
            connection.open()
        except serial.SerialException as e:
            print(e)
            exit()
        
        while True:
            if connection.in_waiting:
                query = connection.read_until(terminator='\r')
                
                if query.endswith('>'):
                    query = query.split('>')[0]
                    
                    if query.startswith('AT '):
                        command = query.split('AT ')[1]
                        
                        print('Received command: '.format(command))
                        
                    elif len(query) >= 6:
                        service = int(query[0:2], 16)
                        pid     = int(query[2:],  16)
                        
                        if service == 1:
                            if pid == 12:
                                connection.write('410C0101>\r')
                            elif pid == 13:
                                connection.write('410D02>\r')
                        
                        elif service == 34:
                            if pid == 4906:
                                connection.write('62132A0303>\r')
                            elif pid == 8434:
                                connection.write('6220F200>\r')
                            elif pid == 12345:
                                connection.write('6230390505>\r')
                            elif pid == 13162:
                                connection.write('62336A06>\r')
                else:
                    print('Timeout')
        
    except KeyboardInterrupt:
        try:
            connection.close()
        except NameError:
            pass
    
    
