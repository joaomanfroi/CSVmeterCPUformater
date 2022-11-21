import pathlib as path
import os
import csv
import datetime

metertxtpath = 'files/meterSN.txt'
cputxtpath = 'files/cpuSN.txt'
csvmeterMM = 'files/meterMM.csv'
csvmeterMI = 'files/meterMI.csv'
csvcpuMM = 'files/cpuMM.csv'
csvcpuMI = 'files/cpuMI.csv'

fileMTMM = open(csvmeterMM, 'w', newline="")
fileMTMI = open(csvmeterMI, 'w', newline="")
fileCPUMM = open(csvcpuMM, 'w', newline="")
fileCPUMI = open(csvcpuMI, 'w', newline="")

csvWriterMTMM = csv.writer(fileMTMM, dialect='excel')
csvWriterMTMI = csv.writer(fileMTMI, dialect='excel')
csvWriterCPUMM = csv.writer(fileCPUMM, dialect='excel')
csvWriterCPUMI = csv.writer(fileCPUMI, dialect='excel')

userID = 'rompkoh'
timeVal = '14:55'

def openCSV():
    MMinitVector = ("manufacturer","customer","shippedTo","shippedToState","shippedDate","custMeterNo",
                    "mfgSerialNumber","amrSerialnumber","kH","numDials","form","base","class","detentMode",
                    "KM","KMh","edgeSerialNumber")

    MInitVector = ("UserID","InstallationDate","InstallationTime","ChangeOutMeterNo","ChangeOutMeterkWh",
                   "InstalledMeterNo","InstalledEndpointSN","InstalledMeterkWh","ServiceLatitude","ServiceLongitude",
                   "ServiceLocation","ServiceTimeZone","TenantGroup")

    try:
        csvWriterMTMM.writerow(MMinitVector)
        csvWriterMTMI.writerow(MInitVector)
        csvWriterCPUMM.writerow(MMinitVector)
        csvWriterCPUMI.writerow(MInitVector)
        print('Arquivos CSV carregados!')
    except FileNotFoundError or IOError:
        print('Error durante gravação do CSV!!')

def opentxtFile():
    with open(metertxtpath, "r") as meterFD:
        global meters
        try:
            meters = meterFD.readlines()
        except FileNotFoundError:
            print("Error during open file or file not exists -> Meter file")
    print("File opened -> meters")


    with open(cputxtpath, "r") as cpuFD:
        global cpus
        try:
            cpus = cpuFD.readlines()
        except FileNotFoundError:
            print("Error during open file or file not exists -> CPU file")
    print("File opened -> cpus")

def checkCPUMeter():
    for aux in range(len(meters)):
        if cpus.__contains__(meters[aux]) and (aux <= len(cpus)):
            print('Erro CPU contem meters:', meters[aux])
            return True
            break

        meters[aux] = meters[aux].rstrip()

    for aux in range(len(cpus)):
        if meters.__contains__(cpus[aux]) and (aux <= len(cpus)):
            print('Erro meters contem cpus:', cpus[aux])
            return True
            break

        cpus[aux] = cpus[aux].strip()

    print("Não temos CPU e meters misturados nos arquivos!!")
    return False

def genMIfile():
    for aux in range(len(meters)):
        decVal = int(meters[aux], 16)
        data = datetime.date.today().strftime("%m/%d/%y")

        vector = (userID, data, timeVal, meters[aux], '', meters[aux], decVal, '', '', '', '', '', '')

        csvWriterMTMI.writerow(vector)

    print('Arquivos MI gerados -> Meters')

    for aux in range(len(cpus)):
        decVal = int(cpus[aux], 16)
        data = datetime.date.today().strftime("%m/%d/%y")

        vector = (userID, data, timeVal, cpus[aux], '', cpus[aux], decVal, '', '', '', '', '', '')

        csvWriterCPUMI.writerow(vector)

    print('Arquivos MI gerados -> CPUS')

def genMMfile():
    for aux in range(len(meters)):
        decVal = int(meters[aux], 16)
        vector = ('', '', '', '', '', meters[aux], decVal, decVal, '', '', '', '', '', '', '', '')

        csvWriterMTMM.writerow(vector)

    print('Arquivos MM gerados -> Meters')

    for aux in range(len(cpus)):
        decVal = int(cpus[aux], 16)
        vector = ('', '', '', '', '', cpus[aux], decVal, decVal, '', '', '', '', '', '', '', '')

        csvWriterCPUMM.writerow(vector)

    print('Arquivos MM gerados -> CPUs')

opentxtFile()

if checkCPUMeter() is False:
    openCSV()
    genMIfile()
    genMMfile()
else:
    print('             CPUs e Meters misturados!!!!')


# hex = '400A29D4'
# dec = int(hex, 16)
#
# print('valor:->', dec)

# print(datetime.date.today().strftime("%m/%d/%y"))
