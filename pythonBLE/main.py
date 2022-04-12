

stringpressPoints =[]

def errorhandle(datastring):
    stringpressPoints.append(datastring)
    lenlist = len(stringpressPoints)
    errlist = ['11', 'xx', '00', '01', '02', '03', '04', '05', '06', '07']
    if lenlist > 1:
        if datastring[0:2] in errlist:
            if datastring == errlist[0]:
                if stringpressPoints[lenlist - 2][0:2] != errlist[9]:
                    print('value to be replaced: ')
                    print(stringpressPoints[lenlist - 2])
                    newstring = errlist[9] + ' 0'
                    stringpressPoints.insert(lenlist - 1, newstring)
            for i in range(1, 10):
                if datastring[0:2] == errlist[i]:
                    # print(errlist[i])
                    if stringpressPoints[lenlist - 2][0:2] != errlist[i - 1]:
                        print('Packet Dropped!')
                        print(errlist[i - 1])
                        newstring = errlist[i - 1] + ' 0'

                        stringpressPoints.insert(lenlist - 1, newstring)

def main():
    array = ['11', 'xx1694499', '00   0', '01  73', '02  60', '03  75', '04  61', '05  82', '07  56', '11']

    for i in range(len(array)):
        errorhandle(array[i])

    print(stringpressPoints)


if __name__ == "__main__":
    main()