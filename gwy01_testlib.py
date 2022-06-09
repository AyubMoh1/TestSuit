import asyncio
from async_class import AsyncClass, AsyncObject, task, link
from nats.aio.client import Client, _SPC_, _CRLF_
import time
import serial
import re
import smbus2
import sys


SUB_OP = b'SUB'

data = []



class GwyPower:
    """Writes to bus for rpi-relay hat power control for switch and gwy.

    Libraries
    ----------
    smbus2 and time.
    """

    DEVICE_BUS = 1
    DEVICE_ADDR = 0x10
    bus = smbus2.SMBus(DEVICE_BUS)
        
    def __init__(self):
        pass
    
    def gwy(self, action):
        """GWY power control.

        Parameters
        ----------
        action : string
            The action to take: 'on', 'off', or 'reboot'.
        """
        action = action
        if action == 'on':
            self.bus.write_byte_data(self.DEVICE_ADDR,0x02,0xFF)
        elif action == 'off':
            self.bus.write_byte_data(self.DEVICE_ADDR,0x02,0x00)
        elif action == 'reboot':
            self.bus.write_byte_data(self.DEVICE_ADDR,0x02,0x00)
            time.sleep(2)
            self.bus.write_byte_data(self.DEVICE_ADDR,0x02,0xFF)

    def switch(self, action):
        """Eth switch power control.

        Parameters
        ----------
        action : string
            The action to take: 'on' or 'off'.
        """        
        action = action
        if action == 'on':
            self.bus.write_byte_data(self.DEVICE_ADDR,0x04,0xFF)
        elif action == 'off':
            self.bus.write_byte_data(self.DEVICE_ADDR,0x04,0x00)
          

class GwySerial:
    """Creates a serial connection .

    Libraries
    ----------
    pyserial, time and re.
    """

    def __init__(self):
        """Instance of ser, hardcoded port and baudrate uses python serial library.
        """

        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=0)
        self.read_pos = 0

        
    def find(self, regex, timeout):
        """ Takes in a string and timeout from main using the serial instance finds a matching string.
        starts as false, becomes true if match is found(match object). returns true and the matched string.
        
        Parameters
        ----------
        match : string
            Finds string from serial output.
        timeout : int
            Sets timeout.
        """
        time_start = time.time()
        is_match = False
        buffer = ""
        while ((time.time() - time_start) < timeout) and not is_match:
            one = self.ser.read().decode('ASCII', "replace")
            buffer += one
            print(one, end ="")
            if one == "\n":
                match = re.search(regex, buffer)
                if match:
                    return (True, match.string)
                else:
                    buffer = ""
        return (False, "")
            
    def cmd(self, serialcmd):
        """Writes to serial connection.

        Parameters
        ----------
        serialcdm : string.
            String that gets encoded with ASCII and written over serial connection.
        """
        self.ser.write(serialcmd.encode('ASCII'))


class plejd_client(Client):
    """Special class modification for accepting messages which contains an extra blank space.
    """
    async def _send_subscribe(self, sub):

        sub_cmd = b''.join([
            SUB_OP, _SPC_,
            sub.subject.encode(), _SPC_, ("%d" % sub._id).encode(), _CRLF_
        ])
        await self._send_command(sub_cmd)
        await self._flush_pending()



async def text_handler(msg):
    """Receives the callback object from subscriptions, uses a global data-list to append callback objects into list.

    Parameters
    ----------
    msg : object
       Object split into subject, data and reply.
    """
    try:
        text = msg.subject + ':"' + msg.data.decode(encoding='utf-8') + '"'
        data.append(text)        
    except:
        print("Cannot decode: " + msg.subject)
        text = msg.subject + ':""'
        data.append(text)
        
        

class GwyNats(AsyncObject, plejd_client):
    """Creates sub and pub coroutines with modified plejd_client class.

    Libraries
    ----------
    async-class and asyncio
    """

    async def __ainit__(self, url):
        """Async-init from async-class.

        Parameters
        ----------
        url : string.
        Connection ip to gwy.
        """
        self.client = plejd_client()
        await self.client.connect(url)


    async def subscribe(self, topic, time):
        """Subscribes to passed topic.
        Callback to text_handler for decoding.
        When finished returns message data back to main as a list via text_handler.

        Parameters
        ----------
        topic : string.
        time : int.
            Subscribe to topic, async.sleep time.
        """
        await self.client.subscribe(topic, cb=text_handler)        
        try:
            await asyncio.sleep(time)
        except:
            pass
            
    async def pub(self, topic, payload='', rtopic='reply2topic'):
        """Publishes to topic with message.

        Parameters
        ----------
        topic : string.
        payload : default empty string.
        rtopic : default replay2topic string.
        """
        await self.client.publish(topic, payload.encode() + b'\r\n', rtopic)

    
    def findfirst(self, search):
        """Find a received NATS message matching regex. Return TRUE + message if found, false if not found.

        Parameters
        ----------
        search : string.
        data : global list
        """
        r = re.compile(search)
        newlist = list(dict.fromkeys(filter(r.match, data)))
        if len(newlist) > 0:
            return True, newlist[0]
        else:
            return False, ""

    async def __adel__(self):
        """Drains subscriptions and closes nats connection
        """
        await self.client.drain()
        await self.client.close()
        
