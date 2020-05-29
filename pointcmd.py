##The following code connects to a DXR and then command damper position open adn readys flow back
#The following modules need to be enabled via [pip python "module"]
import BAC0
from time import sleep
import csv
import pandas as pd
import numpy as np


dxr_name = []
#dxr_addresses = []
#dxr_instance = []
dxr_damper = []
dxr_valve = []
dxr_temp = []
position = []


# get computer's IP address

myIp = input("Insert Your ip address     ")
dxr_addresses = input("Input your DXR ip     ")
dxr_instance = input("Input your DXR instance #     ")
cmd_length = int(input('Input the test sample time     '))

myIp = "169.254.199.100"
dxr_addresses = "169.254.199.10"
dxr_instance = "1601"

# create an instance of BAC0
bacnet = BAC0.connect(ip=myIp)

# connect to the dxr
dxr = BAC0.device(dxr_addresses,dxr_instance,bacnet)

# read the objectList

dxr_objlist = dxr_addresses + " device " + dxr_instance + " objectList"
points = bacnet.read(dxr_objlist)

# points = bacnet.read('10.73.4.55 device 700015 objectList')


# run tests on boxes listed in boxes.csv
with open("boxes.csv",'r') as f:
    boxes = csv.reader(f)
    for row in boxes:
        # initialize performance arrays for cooling and heating tests

        cooling = dict(air_vol_stpt=0,air_volume=0,damper_pos=0,supply_temp=0,valve_pos=0)
        heating = dict(air_vol_stpt=0,air_volume=0,damper_pos=0,supply_temp=0,valve_pos=0)
        damper_command_present = False
        valve_command_present = False
        supply_temp_present = False
        air_stpt_present = False
        air_volume_present = False
        comments = ""

        # connect to the dxr
        dxr = BAC0.device(row[1],row[2],bacnet)

        # read the objectList

        dxr_objlist = row[1] + " device " + row[2] + " objectList"
        points = bacnet.read(dxr_objlist)

        # points = bacnet.read('10.73.4.55 device 700015 objectList')

        # list points by name as key/value pairs
        # additionally, find the long string that contains floor and segment info
        # -- we will use this to identify the name of VavSuBalSta

        point_strings = []
        for point in dxr.points:
            # print(point)
            point_strings.append(str(point))

        #print points in array
        cmd_iteration = 10
        #cmd_length = 1
        i=0
        #the damper is commanded (number) of times here.
        #dxr holds the name of the controller, row[] holds the point name
        dmpr_command = [0]*cmd_iteration     #initialize command array
        dmpr_position = [0]*cmd_iteration    #initialize position array
        air_volume = [0]*cmd_iteration       #initialize air volume array
        while i < 10:
            dmpr_command[i] = i*10
            dxr[row[3]] = dmpr_command[i]  #command the damper to position of 10*iteration (10 -> 100%)
            print(str(row[3]) + ' commanded at ' + str(i*10) + ' for ' + str(cmd_length) + ' seconds')
            
            dmpr_position[i] = dxr[row[3]]                      #read position of damper   
            air_volume[i] = str(dxr[row[7]]) + ' at ' + str(dmpr_command[i]) + ' pct command'   #read air flow
             
            
            sleep(cmd_length)   #wait [cmd_length] seconds between commands
            i = i+1

        i=0
        while i < 10:
            print(air_volume[i])
            i = i+1
            



        

