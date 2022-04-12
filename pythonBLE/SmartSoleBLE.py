import asyncio
import platform
import sys
import pandas as pd
from bleak import BleakClient
import io
import time
import datetime
import math

pd.options.mode.chained_assignment = None

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
buflen = 300
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
       # df.to_csv(filename)

        """
        Created on Wed Mar 30 15:54:08 2022

        @author: tamarakahhale

        This script is going to take in a CSV of data points and anaylze them
        needs to output a csv for the html to take in
        """


        data = df
        # fix channel 1 spelling on both ends
        columns = ['channel 1', 'channel 2', 'channel 3', 'channel 4', 'channel 5', 'channel 6', 'channel 7']
        final_col = ['channel 7', 'channel 6', 'channel 1', 'channel 5', 'channel 2', 'channel 3', 'channel 4']
        limit = [60, 68, 64, 66, 59, 70]
        needed = {}
        final = {}
        val = {}
        rad = {}

        data = data.astype(str)  # change all data points to strings

        data['time'] = data['time'].str[2:]  # remove the xx from the time values
        data['time'] = data['time'].astype(int)
        totaltime = (data['time'][len(data['time']) - 1] - data['time'][0]) / 1000  # total time in seconds

        '''
        time packets that get lost need to be 110
        '''

        # use this for loop to take the channel values off each number so we have just the data left
        for x in columns:
            data[x] = data[x].str[3:]
            for y in range(len(data[x])):
                data[x][y] = float(data[x][y])

        # above is only possible if the channel is retained even when a 0 is placed
        find_start = data['time'][0] + 4700
        cutoff = (data.iloc[(data['time'] - find_start).abs().argsort()[:1]]).index  # about 4.7 seconds in
        data = data.drop(data.index[0:cutoff[0]])  # cut first 5 seconds
        # print(data)

        first = (data['channel 4'] >= 66).idxmax()  # get index of start of step 1

        # get index of first num >70 in channel 6
        for index, item in enumerate(data['channel 6']):
            if (item > 70):
                if ((index + cutoff[0]) > first):
                    break
                if ((index + cutoff[0]) < first):
                    pass

        print(data)
        # get index (x) of last num >70 in channel 6 --> for usage, need last -1
        for last in range((index + cutoff[0]), (index + cutoff[0] + 35)):
            print(data['channel 6'][last])
            if data['channel 6'][last] < 70:
                break
        # print(first)
        # print(last)

        drange = (last + 1) - first
        div1 = math.ceil(drange / 3)
        div3 = math.ceil((drange - div1) / 2)
        div2 = drange - (div1 + div3)
        # print(drange, div1, div2, div3)

        # get dictionary of only necessary values
        for x in columns:
            needed.setdefault(x, [])
            for y in range(first, last + 1):
                needed[x].append(data[x][y])

        # get the average for each of the three phases
        for x in columns:
            final.setdefault(x, [])
            final[x].append(((sum(needed[x][0:div1])) / div1))
            final[x].append((sum(needed[x][div1:div1 + div2]) / div2))
            final[x].append(((sum(needed[x][div1 + div2:div1 + div2 + div3])) / div3))
        # print(final)

        send = pd.DataFrame(columns=['x', 'y', 'd', 'r'])
        send['x'] = [170, 90, 180, 80, 150, 80, 120, 350, 420, 350, 420, 380, 420, 390,
                     170, 90, 180, 80, 150, 80, 120, 350, 420, 350, 420, 380, 420, 390,
                     170, 90, 180, 80, 150, 80, 120, 350, 420, 350, 420, 380, 420, 390]
        send['y'] = [60, 120, 200, 270, 350, 420, 510, 60, 120, 200, 270, 350, 420, 510,
                     60, 120, 200, 270, 350, 420, 510, 60, 120, 200, 270, 350, 420, 510,
                     60, 120, 200, 270, 350, 420, 510, 60, 120, 200, 270, 350, 420, 510]

        # print(send)

        # set values according to their property
        for x in columns:
            val.setdefault(x, [])
            rad.setdefault(x, [])
            for y in range(0, 3):
                if final[x][y] >= 95:
                    val[x].append(100)
                    rad[x].append(85)
                if 80 <= final[x][y] < 95:
                    val[x].append(95)
                    rad[x].append(70)
                if 72 <= final[x][y] < 80:
                    val[x].append(87)
                    rad[x].append(65)
                if 65 <= final[x][y] < 72:
                    val[x].append(80)
                    rad[x].append(60)
                if 60 <= final[x][y] < 65:
                    val[x].append(80)
                    rad[x].append(55)
                if final[x][y] < 60:
                    val[x].append(75)
                    rad[x].append(50)

        print(val)
        # print(rad)

        # left foot data
        c = 14
        i = 0
        for col in final_col:
            for x in range(0, 3):
                send['d'][x * c + i] = val[col][x]
                send['r'][x * c + i] = rad[col][x]
            i = i + 1

        # right foot data
        c = 14
        i = 7
        for col in final_col:
            for x in range(0, 3):
                send['d'][x * c + i] = val[col][x]
                send['r'][x * c + i] = rad[col][x]
            i = i + 1

        print(send)

        send.to_csv("finaltest_1.csv")

        '''
        calc the total number of steps using the example step
        see how long it takes, and suppose the steps were that many times
        '''

        # pronation
        # if sensor pronate excxeeds baseline, you pronate
        # calculate how many total steps taken
        # how many times sensor 6/7 change?
        # calculate how much time was taken
        # use time
        # calculate average pace
        # time/total steps

        # based on the one average step, equate a sensor reading to a radius and value number
        # for all three phases of the step

        '''
        channel 4 - upwards of 66  is a step
        channel 3 - upwards of 64 (maybe 63?)
        channel 5 - inconclusive (58/59?? Maybe 57? Pretty stable)
        channel 2 - upwards of 68 ** use as benchmark for a good step
        channel 6 - upwards of 70
        channel 1 - 60 ish


        >95 == red and big
        80 - 95 == orange and big
        72 - 80 == yellow and big
        65 - 72 == yellow and small
        60 - 65 == green and big
        <60 = green/blue and small
        '''



if __name__ == "__main__":
   asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else address))