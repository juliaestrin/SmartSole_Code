import asyncio
import platform
import sys
import pandas as pd
from bleak import BleakClient
import io
import time
import datetime

FILENAME = "./output.xlsx"
address = (
    "CA:EE:38:A5:33:4E"
    #"DA:D3:CD:7E:F0:A8"
    # "EC:54:1B:8A:8C:6B"
    # "C8:14:2A:19:65:5F"
    # "E6:94:DD:E9:72:E9"
    if platform.system() != "SparkFun_nRF52840"
    else "00001523-1212-EFDE-1523-785FEABCD123"
)

# LED_UUID = "00001525-1212-EFDE-1523-785FEABCD123"
# BUTTON_UUID = "00001524-1212-EFDE-1523-785FEABCD123"
TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

pressPoints = []
stringpressPoints = []
lenlist = 0
buflen = 666
# f = io.open("test.txt", mode="w", encoding="utf-8")

def callback(sender: int, data: bytearray):
    # print(f"{sender}: {data}")
    # f.write(data)
    pressPoints.append(data)
    datastring = data.decode("utf-8")
    # print(datastring[0:2])
    stringpressPoints.append(datastring)
    global lenlist
    lenlist = len(stringpressPoints)
    # lenlist = len(stringpressPoints)
    # print(lenlist)
    # print('Prev: '+ stringpressPoints[lenlist - 2])
    # print('Datastring:' + datastring)

   # print(stringpressPoints)
    errlist = ['11', 'xx', '00', '01', '02', '03', '04', '05', '06', '07']
    # for i in range(1,9):
    if lenlist > 1:
        if datastring[0:2] in errlist:
            if datastring == errlist[0]:
                if stringpressPoints[lenlist - 2][0:2] != errlist[9]:
                    print('value to be replaced: ')
                    print(stringpressPoints[lenlist - 2])
                    newstring = errlist[9] + ' 0'
                    stringpressPoints.insert(lenlist- 1, newstring)
            for i in range(1,10):
                if datastring[0:2] == errlist[i]:
                   # print(errlist[i])
                    if stringpressPoints[lenlist -2][0:2] != errlist[i-1]:
                        print('Packet Dropped!')
                        print(i)
                        print(errlist[i-1])
                        print(stringpressPoints[lenlist - 2])
                        print(stringpressPoints[lenlist -1])
                        print(datastring)
                        newstring = errlist[i-1] + ' 0'
                        stringpressPoints.insert(lenlist - 1 , newstring)


async def main(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        await client.start_notify(TX_UUID, callback)

        # points = 0
        # t_end = time.time() + 60
        global lenlist
        list_end = buflen * 10
        while lenlist < list_end:
            await client.read_gatt_char(TX_UUID)
            if lenlist > 0:
                print(lenlist)
          #  points = points + 1
           # print("-")

        print(stringpressPoints)
            #print(pressPoints)
        #stringdata = [str(pressPoints)]
        #print(stringdata)
        #print(stringpressPoints)
        #df = pd.DataFrame(stringpressPoints, columns=['x', 'y'])
        # print(df.dtypes)
        #print(df)
        # df.to_excel(FILENAME)
        #print(pressPoints)


        targetindex = stringpressPoints.index('11')
        finallist = stringpressPoints[targetindex:]
        print(finallist)
        finallist = [finallist[i:i+10] for i in range(0,len(finallist), 10)]
        print(finallist)
        df = pd.DataFrame(finallist, columns=['Del', 'time', 'chanel 0', 'channel 1', 'channel 2', 'channel 3', 'channel 4', 'channel 5', 'channel 6', 'channel 7'])

        x = datetime.datetime.now()
        date = str(x.date())
        time = str(x.time())
        filename = str('SmartSole' + date + '_' + time[0:2] + 'h' + time[3:5] + 'm.csv')

        print(df)
        df.to_csv(filename)



if __name__ == "__main__":
   asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else address))