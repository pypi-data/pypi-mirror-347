import json
import logging
import socket
import time
from itertools import cycle
from queue import Queue
from threading import Thread
from decimal import Decimal
import requests
_LOGGER = logging.getLogger(__name__)

crcTable = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5,
    0x60c6, 0x70e7, 0x8108, 0x9129, 0xa14a, 0xb16b,
    0xc18c, 0xd1ad, 0xe1ce, 0xf1ef, 0x1231, 0x0210,
    0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
    0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c,
    0xf3ff, 0xe3de, 0x2462, 0x3443, 0x0420, 0x1401,
    0x64e6, 0x74c7, 0x44a4, 0x5485, 0xa56a, 0xb54b,
    0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
    0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6,
    0x5695, 0x46b4, 0xb75b, 0xa77a, 0x9719, 0x8738,
    0xf7df, 0xe7fe, 0xd79d, 0xc7bc, 0x48c4, 0x58e5,
    0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
    0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969,
    0xa90a, 0xb92b, 0x5af5, 0x4ad4, 0x7ab7, 0x6a96,
    0x1a71, 0x0a50, 0x3a33, 0x2a12, 0xdbfd, 0xcbdc,
    0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
    0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03,
    0x0c60, 0x1c41, 0xedae, 0xfd8f, 0xcdec, 0xddcd,
    0xad2a, 0xbd0b, 0x8d68, 0x9d49, 0x7e97, 0x6eb6,
    0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
    0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a,
    0x9f59, 0x8f78, 0x9188, 0x81a9, 0xb1ca, 0xa1eb,
    0xd10c, 0xc12d, 0xf14e, 0xe16f, 0x1080, 0x00a1,
    0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
    0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c,
    0xe37f, 0xf35e, 0x02b1, 0x1290, 0x22f3, 0x32d2,
    0x4235, 0x5214, 0x6277, 0x7256, 0xb5ea, 0xa5cb,
    0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
    0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447,
    0x5424, 0x4405, 0xa7db, 0xb7fa, 0x8799, 0x97b8,
    0xe75f, 0xf77e, 0xc71d, 0xd73c, 0x26d3, 0x36f2,
    0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
    0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9,
    0xb98a, 0xa9ab, 0x5844, 0x4865, 0x7806, 0x6827,
    0x18c0, 0x08e1, 0x3882, 0x28a3, 0xcb7d, 0xdb5c,
    0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
    0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0,
    0x2ab3, 0x3a92, 0xfd2e, 0xed0f, 0xdd6c, 0xcd4d,
    0xbdaa, 0xad8b, 0x9de8, 0x8dc9, 0x7c26, 0x6c07,
    0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
    0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba,
    0x8fd9, 0x9ff8, 0x6e17, 0x7e36, 0x4e55, 0x5e74,
    0x2e93, 0x3eb2, 0x0ed1, 0x1ef0
]


class TISCONTROL():
    """Tiscontrol provides a communication link with the IP com port hub."""

    SOCKET_TIMEOUT = 4.0
    RX_PORT = 6000
    TX_PORT = 6000

    link_ip = "255.255.255.255"
    proxy_ip = None
    proxy_port = None
    transaction_id = cycle(range(1, 1000))
    the_queue = Queue()
    thread = None

    def __init__(self, link_ip=None):
        """Initialise the component."""
        if link_ip is not None:
            TISCONTROL.link_ip = link_ip
    def connect(self):
         print ("where are the nuclear wessels?")

    def _send_message(self, msg):
        """Add message to queue and start processing the queue."""
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSock.sendto(bytes.fromhex(msg), (TISCONTROL.link_ip, self.TX_PORT))
        return "success"

    def crc16(self,payload):
        crc = 0x0000
        for i in range(len(payload)):
            tmp = (crc >> 8)
            crc = (crc << 8) & 0xFFFF
            index= int(payload[i], 16) ^ tmp
            crc = crcTable[index] ^ crc
        return f'{crc:04x}'  # Always return 4-digit hex 

    def payload(self,string):
        result = []
        for i in range(0, len(string), 2):
            result.append("0x"+string[i : i + 2])
        return self.crc16(result)

    def fullPacket(self,packet):
        constant="C0A8018B534D415254434C4F5544AAAA"
        return constant+packet

    def turn_on_light(self, device_id,level):
        """Create the message to turn light on."""
        con_packet="0f01fefffe0031"+device_id+level+"0000"
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
        
    def curtain_motor(self, device_id,level):
        """Create the message to turn curtain on."""
        con_packet="0d01fefffee3e0"+device_id+level
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
        
    def universal_switch(self, device_id,mode):
        """Create the message to universal switch."""
        con_packet="0d01fefffee01c"+device_id+mode
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)

    def hsb_on_light(self, device_id,level,hue,saturation):
        """Create the message to hsb light on."""
        con_packet="1001fefffe2034"+device_id+level+hue+"02"+saturation
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
        
    def scene_switch(self, device_id,scene_no):
        """Create the message to scene switch."""
        con_packet="0d01fefffe0002"+device_id+scene_no
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
    # floor Heater
    def floorheater_mode(self, device_id,mode):
        """Create the message to floor heater mode."""
        con_packet="0e01fefffee3d8"+device_id+"2214"+mode
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)

    def security_mode(self, device_id,mode):
        """Create the message to security mode."""
        con_packet="0d01fefffe0104"+device_id+mode
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
    
    def security_mode_panic(self, device_id):
        """Create the message to security panic."""
        con_packet="0f01fefffe010c"+device_id+"040000"
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
    
    def floorheater_temperature(self, device_id,setpoint):
        """Create the message to floor heater mode."""
        con_packet="0e01fefffee3d8"+device_id+"2218"+setpoint
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
    def tv_box(self, command):
        """Byte to hex data"""
        if(command=="on"):return 126
        elif(command==1):return 127
        elif(command==2):return 128
        elif(command==3):return 129
        elif(command==4):return 130
        elif(command==5):return 131
        elif(command==6):return 132
        elif(command==7):return 133
        elif(command==8):return 134
        elif(command==9):return 135
        elif(command=="guide"):return 136
        elif(command==0):return 137
        elif(command=="back"):return 138
        elif(command=="up"):return 139
        elif(command=="left"):return 140
        elif(command=="confirm"):return 141
        elif(command=="right"):return 142
        elif(command=="down"):return 143
        elif(command=="voladd"):return 144
        elif(command=="volred"):return 145
        elif(command=="chadd"):return 146
        elif(command=="chred"):return 147
        elif(command=="mute"):return 148
    def ir_tv(self, command):
        """Byte to hex data"""
        if(command=="on"):return 106
        elif(command==1):return 108
        elif(command==2):return 109
        elif(command==3):return 110
        elif(command==4):return 111
        elif(command==5):return 112
        elif(command==6):return 113
        elif(command==7):return 114
        elif(command==8):return 115
        elif(command==9):return 116
        elif(command=="res"):return 117
        elif(command==0):return 118
        elif(command=="av"):return 119
        elif(command=="back"):return 120
        elif(command=="up"):return 122
        elif(command=="left"):return 123
        elif(command=="confirm"):return 121
        elif(command=="right"):return 124
        elif(command=="down"):return 125
        elif(command=="voladd"):return 101
        elif(command=="volred"):return 105
        elif(command=="chadd"):return 102
        elif(command=="chred"):return 104
        elif(command=="mute"):return 107 
        elif(command=="menu"):return 103 
    def projector(self, command):
        """Byte to hex data"""
        if(command=="on"):return 168
        elif(command=="off"):return 169
        elif(command=="computer"):return 170
        elif(command=="video"):return 171
        elif(command=="single source"):return 172
        elif(command=="focusadd"):return 173
        elif(command=="focusred"):return 174
        elif(command=="pictureadd"):return 175
        elif(command=="picturered"):return 176
        elif(command=="menu"):return 177
        elif(command=="confirm"):return 178
        elif(command=="up"):return 179
        elif(command=="left"):return 180
        elif(command=="right"):return 181
        elif(command=="down"):return 182
        elif(command=="quit"):return 183
        elif(command=="voladd"):return 184
        elif(command=="volred"):return 185
        elif(command=="mute"):return 186
        elif(command=="auto"):return 187
        elif(command=="pause"):return 188
        elif(command=="mcd"):return 189

    def thermostat_mode(self, device_id,ac_status,cool_temp,ac_mode,heat_temp,auto_temp,auto_dry):
        """Create the message to turn thermostat on."""
        con_packet="1401fefffee0ee"+device_id+ac_status+cool_temp+ac_mode+"01"+heat_temp+auto_temp+auto_dry+"00"
        get_crc=self.payload(con_packet)
        packet=con_packet+get_crc
        send_packet=self.fullPacket(packet)
        return self._send_message(send_packet)
    def rgbtohsb(self,r, g, b):
        rabs = r / 255
        gabs = g / 255
        babs = b / 255
        v = max(rabs, gabs, babs)
        diff = v - min(rabs, gabs, babs)
        
        def diffc(c):
            return (v - c) / 6 / diff + 1 / 2
        
        def percentRoundFn(num):
            return round(num * 100) / 100
        
        if diff == 0:
            h = s = 0
        else:
            s = diff / v
            rr = diffc(rabs)
            gg = diffc(gabs)
            bb = diffc(babs)
            
            if rabs == v:
                h = bb - gg
            elif gabs == v:
                h = (1 / 3) + rr - bb
            elif babs == v:
                h = (2 / 3) + gg - rr
            
            if h < 0:
                h += 1
            elif h > 1:
                h -= 1
        
        s = percentRoundFn(s * 400)
        
        if s > 240:
            print(s)
            s = s - 160
        
        return {
            'h': round(h * 240),
            's': round(s),
            'v': round(v * 100)
    }
    def get_status_of_device(self, device_id,device_type):
        """Create the message to turn light on."""
        if(device_type=="light"):
            con_packet="0b01fefffe0033"+device_id
            get_crc=self.payload(con_packet)
            packet=con_packet+get_crc
            send_packet=self.fullPacket(packet)
            return send_packet
        elif(device_type=="thermostat"):
            print("Thermostat Feedback")
            con_packet="0c01fefffee0ec"+device_id
            get_crc=self.payload(con_packet)
            packet=con_packet+get_crc
            send_packet=self.fullPacket(packet)
            return send_packet
        elif(device_type=="floorheater"):
            print("FloorHeater Feedback")
            con_packet="0c01fefffe1944"+device_id
            get_crc=self.payload(con_packet)
            packet=con_packet+get_crc
            send_packet=self.fullPacket(packet)
            return send_packet
        elif(device_type=="hsb"):
            print("hsb Feedback")
            con_packet="0c01fefffe2036"+device_id
            get_crc=self.payload(con_packet)
            packet=con_packet+get_crc
            send_packet=self.fullPacket(packet)
            return send_packet
        elif(device_type=="security"):
            print("security Feedback")
            con_packet="0c01fefffe011e"+device_id
            get_crc=self.payload(con_packet)
            packet=con_packet+get_crc
            send_packet=self.fullPacket(packet)
            return send_packet
        elif(device_type=="sensor"):
            print("security sensor Feedback")
            con_packet="0b01fefffe012c"+device_id
            get_crc=self.payload(con_packet)
            packet=con_packet+get_crc
            send_packet=self.fullPacket(packet)
            return send_packet
        else:
            print("FloorHeater Feedback")

    def set_trv_proxy(self, proxy_ip, proxy_port):
        """Set TIS Control proxy ip/port."""
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port

    def add_space(self,a):
        # split address to 6 character
        pac=' '.join([a[i:i+2] for i in range(0, len(a), 2)])
        # format to 00:00:00:00:00:00
        return pac
    
    def byte_to_hex(self, data):
        """Byte to hex data"""
        res = ""
        for b in data:
            res += "%02x" % b
        return res

    def number_to_hex(self, number):
    
     return str(format(number, '02x'))

    def datagram_received(self, data):
        """Manage receipt of a UDP packet from TIS Control."""
        # print(self.add_space(self.byte_to_hex(data)))
        # _LOGGER.info(self.add_space(self.byte_to_hex(data)))
        #self.store_data(self.convert_hex(data))
        packet=self.byte_to_hex(data)
        print(packet[8:28])
        if packet[8:28]=="534d415254434c4f5544":
            # return self.byte_to_hex(data)
            packet_check=packet[32:]
            return packet[32:]
        else:
          _LOGGER.info("wrong gateway received")
          return "Wrong"

    def read_trv_status(self,device_id,device_type):
        """Read TIS Control status from the proxy."""
        #targ = temp = battery = trv_output = None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(("0.0.0.0", self.RX_PORT))
                sock.settimeout(4.0)
                msg = self.get_status_of_device(device_id,device_type)
                sock.sendto(bytes.fromhex(msg), (self.link_ip, self.TX_PORT))
                response, dummy = sock.recvfrom(65565)
                # print(response)
                data_is=self.datagram_received(response)
                print("dsd"+data_is)
                if (data_is[10:14]=="0034" or data_is[10:14]=="0032" or data_is[10:14]=="1945" or data_is[10:14]=="e0ed" or data_is[10:14]=="2037" or data_is[10:14]=="011f" or data_is[10:14]=="012d" or data_is[10:14]=="0040"):
                    return self.datagram_received(response)
        except socket.timeout:
            _LOGGER.warning("TIS control proxy not responing")

        except socket.error as ex:
            _LOGGER.warning("TIS control proxy error %s", ex)

        return "Success"

    def _send_queue(self):
        """If the queue is not empty, process the queue."""
        while not TISCONTROL.the_queue.empty():
            self._send_reliable_message(TISCONTROL.the_queue.get_nowait())

    def _auth(self,email,password):
        print(email)
        url = 'https://tissmarthome-webcontrol.web.app/homeassistant/auth'
        myobj = {'email': email,'password':password}
        x = requests.post(url, json = myobj)
        return x.json()
    def _getdevices(self,email,password):
        print(email)
        url = 'https://tissmarthome-webcontrol.web.app/homeassistant/get_devices'
        myobj = {'email': email,'password':password}
        x = requests.post(url, json = myobj)
        return x.json()
    def _send_reliable_message(self,device_id,device_type):
        """Send msg to TIS Control hub."""
        result = False
        max_retries = 15
        trans_id = next(TISCONTROL.transaction_id)
        err = None
        msg=""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) \
                    as write_sock, \
                    socket.socket(socket.AF_INET, socket.SOCK_DGRAM) \
                    as read_sock:
                write_sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                read_sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                read_sock.setsockopt(socket.SOL_SOCKET,
                                     socket.SO_BROADCAST, 1)
                read_sock.settimeout(self.SOCKET_TIMEOUT)
                read_sock.bind(('0.0.0.0', self.RX_PORT))
                while max_retries:
                    max_retries -= 1
                    msg = self.get_status_of_device(device_id,device_type)
                    write_sock.sendto(bytes.fromhex(msg), (TISCONTROL.link_ip, self.TX_PORT))
                    result = False
                    while True:
                        response, dummy = read_sock.recvfrom(65565)
                        _LOGGER.info(self.datagram_received(response))
                        data_is=self.datagram_received(response)
                        print("dsd"+data_is)
                        if (data_is[10:14]=="0034" or data_is[10:14]=="0032" or data_is[10:14]=="1945" or data_is[10:14]=="e0ed" or data_is[10:14]=="2037" or data_is[10:14]=="011f" or data_is[10:14]=="012d" or data_is[10:14]=="0040"):
                        #return self.datagram_received(response)
                         result = True
                         return self.datagram_received(response)
                        
        except socket.timeout:
            _LOGGER.error("TIS Control timeout!")

            # return result
            return "timeout"

        except Exception as ex:
            _LOGGER.error(ex)
            #raise
            return "Exception error"

        if result:
            _LOGGER.info("TIS Control OK!")
        else:
            if err:
                _LOGGER.error("TIS Control fail (%s)!", err)
            else:
                _LOGGER.error("TIS Control fail!")
        # return result
        return "Connection fail"