import time
from gwy01_testlib import *
import pytest

url = 'nats:'
topic = '>'
pubtopic = 'leds.in.on'
publed = b'{"color":"red","priority":10}\r\n' 
button_sub = 'button.>'
leds_sub = 'leds.>'
network = 'site.state..>'

@pytest.mark.asyncio
async def test_ws_status():
   
   nats = await GwyNats(url)
   
   await nats.pub('nrf.deviceid.request','','hi')
   await nats.subscribe(topic,10)
   
   #await nats.pub(pubtopic,publed)
   await nats.close()
   
   wsres, wsstat = nats.findfirst('websocket.status')
   assert wsres == True
   print(wsstat)
   assert '"connected"' in wsstat
   
   resled, retled = nats.findfirst('leds.in.on')
   assert resled == True
   assert 'red' in retled
   

   assert nats.is_closed
   
if __name__ == "__main__":
   asyncio.run(test_ws_status())
