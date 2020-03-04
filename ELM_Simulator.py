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
        
        query = ''
        
        while True:
            if connection.in_waiting:
                query += connection.read().decode("utf-8")
                
                if query[-1] == '\r':
                    query = query[:-1]
                    
                    if query.startswith('AT '):
                        print('\nCommand: {}'.format(query))
                        command = query.split('AT ')[1]
                        connection.write(b'OK>\r')
                        print('\tSent: OK')
                        
                    elif len(query) >= 4:
                        try:
                            service = int(query[0:2], 16)
                            pid     = int(query[2:],  16)
                            
                            print('\nQuery: {}'.format(query))
                            
                            if service == 1:
                                if pid == 12:
                                    connection.write(b'410C0101>\r')
                                    print('Sent: 410C0101\n')
                                elif pid == 13:
                                    connection.write(b'410D02>\r')
                                    print('Sent: 410D02\n')
                            
                            elif service == 34:
                                if pid == 4906:
                                    connection.write(b'62132A0303>\r')
                                    print('Sent: 62132A0303\n')
                                elif pid == 8434:
                                    connection.write(b'6220F200>\r')
                                    print('Sent: 6220F200\n')
                                elif pid == 12345:
                                    connection.write(b'6230390505>\r')
                                    print('Sent: 6230390505\n')
                                elif pid == 13162:
                                    connection.write(b'62336A06>\r')
                                    print('Sent: 62336A06\n')
                        except ValueError:
                            print('**** Debug: {}'.format(query))
                    query = ''
        
    except KeyboardInterrupt:
        try:
            connection.close()
        except NameError:
            pass
    
    
