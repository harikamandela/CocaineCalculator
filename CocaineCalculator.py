# -*- coding: utf-8 -*-
"""
@author: mandela.harika
"""

import csv
import datetime
import os



mw_cocaine=339.8 #molecular weight of cocaine
totalCocaine=0

#Method to determine total cocaine usage and also write cocaine sessions to CSV for tracking purpose
def cocaineData(ratno,expno,coc_injection,coc_intake) :
    global totalCocaine
    totalCocaine=totalCocaine+coc_intake
    writer.writerow((ratno,expno,coc_injection,coc_intake))

def calculateCocaine(file) :
    f=open(file,'r')
    filerowcount=0
    startdate=''
    startyear=0
    weightofrat=0
    urowcount=0
    u15value=0
    ratno=0
    expno=0
    for line in f :
        
        #Increment the row count on reading each row. makes it easy to move to U10 row based on location of U row
        filerowcount=filerowcount+1 
        
        line=line.strip()
        #Rat No is stored in the format: BOX:  6 SUBJECT:      256
        if line.startswith('BOX') :
            #Extracting Rat no
            sessiondetails=line.split(':')
            ratno=sessiondetails[2].strip().split(" ")
            ratno=ratno[0]
            #Extracting Experiment no
            expno=sessiondetails[3].strip().split(" ")
            expno=expno[0]
        
        #Extract the startdate of experiment
        if line.startswith('START') :
            experimentdates=line.split(" ")
            startdate=experimentdates[1]
            startyear=datetime.strptime(startdate,'%m/%d/%y')
            
        #Calculate cocaine consumption only for experiments in the specified year
        if startyear.year>=year:
            #Extract the weight of rat
            if line.startswith('W:') :
                weightrow=line.split(':')
                weightofrat=weightrow[1].strip() 
                
            #Format of values in the file
            #U:
            #   0:      0.0      0.0      0.0      0.0      0.0      0.0      0.0      0.0      0.0      0.0
            #   10:   6000.0      0.0    500.0   1649.9      0.0   6000.0   2951.6    500.0      0.0      0.0
            #U15 value is the cocaine consumption
            if line.startswith('U:') :
                urowcount=filerowcount
            if filerowcount==urowcount+2 :#As U10 row is two rows after U row
                splitu10 =line.split(':')

                #Splits 10: and the remaining 11-20 values as 2 elements in the array        
                for x in splitu10 :
                    x=x.strip()
                    u11to20row=x
                
                countInU10Row=0#Tracks progress to U15
                #Split the string of values from U11to20 
                for i in u11to20row.split() :
                    #This counter helps to track reaching U15 row .In short execute the loop 5 times to reach U15
                    countInU10Row= countInU10Row=+1
                    if countInU10Row == 5:
                        u15value=i
                        break
                cocaineIntake=float(weightofrat) * mw_cocaine * float(u15value)
                cocaineData(ratno,expno,u15value,cocaineIntake)
                break
    f.close()

#Take from User the directory location of rat cocaine session files 
#and also the year to calculate for
directory = raw_input("Enter the directory: \n")
year=int(raw_input("Year ?"))

#Creating a CSV to record cocaine data
csvfile=open('CocaineConsumption'+year+'.xls','wb')
writer=csv.writer(csvfile)
writer.writerow(("Rat no.","Exp no.","Cocaine Injection","Cocaine Intake"))

for file in os.listdir(directory):
#Skip analyzing files of different type in the directory
    if not file.endswith(".xls") and not file.endswith(".py"):
        calculateCocaine(file)
        
print 'Cocaine usage of the year'+year+'is'+totalCocaine+'mg'
          
