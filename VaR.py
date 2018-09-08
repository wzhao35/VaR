
##############################################################################################
#User Interface
import Tkinter as tk
from Tkinter import *

class User:
    def __init__(self, master):
        self._name = "" 
        frame = Frame(master)
        frame.grid()
        master.title("FUTURES MARGIN INPUT")
        self.locator_label1 = Label(frame, text="Choose methodology (1 as historical simulation, 2 as parametric VaR):",width=100, height=2)
        self.locator_label2 = Label(frame, text="Enter confidence interval(%):",width=100, height=2)
        self.locator_label3 = Label(frame, text="Choose number of days:",width=100, height=2)
        self.locator_label1.grid(row=0, sticky=E)
        self.locator_label2.grid(row=1, sticky=E)
        self.locator_label3.grid(row=2, sticky=E)
        self.entry1 = Entry(frame)
        self.entry2 = Entry(frame)
        self.entry3 = Entry(frame)
        self.entry1.grid(row=0, sticky=E)
        self.entry2.grid(row=1, sticky=E)
        self.entry3.grid(row=2, sticky=E)
        self.button1 = Button(frame, text="Confirm", command=self.context, pady=2)
        self.button1.grid(row=3)
        self.button2 = Button(frame, text="Exit", command=master.destroy, pady=2)
        self.button2.grid(row=4, sticky=E)
    def context(self):
        self._context1 = self.entry1.get()
        self._context2 = self.entry2.get()
        self._context3 = self.entry3.get()


root = Tk()
Input = User(root)
root.mainloop()

model=int(Input._context1)
CI=int(Input._context2)/100.0
days=int(Input._context3)

##############################################################################################
#Main Code - EWMA
import pandas as pd
from pandas import DataFrame, read_csv
from scipy.stats import norm
import numpy as np
import math
import sys
import os

s=0.94
location1 = r'.../ICE-SBV2016.csv'
location2 = r'.../ICE-SFU2016.csv'
location3 = r'.../ICE-CCU2016.csv'
location4 = r'.../ICE-KCU2016.csv'
location5 = r'.../ICE-CTV2016.csv'
data1 = pd.read_csv(location1)
data2 = pd.read_csv(location2)
data3 = pd.read_csv(location3)
data4 = pd.read_csv(location4)
data5 = pd.read_csv(location5)

data1 = data1.sort_values(['Date'],ascending=[True])
data2 = data2.sort_values(['Date'],ascending=[True])
data3 = data3.sort_values(['Date'],ascending=[True])
data4 = data4.sort_values(['Date'],ascending=[True])
data5 = data5.sort_values(['Date'],ascending=[True])

data1=data1[~np.isnan(data1['Settle'])]
data2=data2[~np.isnan(data2['Settle'])]
data3=data3[~np.isnan(data3['Settle'])]
data4=data4[~np.isnan(data4['Settle'])]
data5=data5[~np.isnan(data5['Settle'])]

price1=data1['Settle'].values[:]
price2=data2['Settle'].values[:]
price3=data3['Settle'].values[:]
price4=data4['Settle'].values[:]
price5=data5['Settle'].values[:]
length=[len(price1),len(price2),len(price3),len(price4),len(price5)]

change1=np.zeros(len(price1)-1)
change2=np.zeros(len(price2)-1)
change3=np.zeros(len(price3)-1)
change4=np.zeros(len(price4)-1)
change5=np.zeros(len(price5)-1)

error=np.zeros(5)

for i in range(0,len(price1)-1):
    change1[i]=price1[i+1]/price1[i]-1


for i in range(0,len(price2)-1):
    change2[i]=price2[i+1]/price2[i]-1


for i in range(0,len(price3)-1):
    change3[i]=price3[i+1]/price3[i]-1


for i in range(0,len(price4)-1):
    change4[i]=price4[i+1]/price4[i]-1


for i in range(0,len(price5)-1):
    change5[i]=price5[i+1]/price5[i]-1


num=len(change1)-days
var_ewma1=np.zeros(days)
actual1=np.zeros(days)
variance=np.zeros(days)
count1=0
if model==1:
    ###############################
    #Historical Simulation
    '''
    for i in range(0,days):
        contract_value1=1120*price1[num+i]
        change=np.zeros(num)
        for j in range(0,num):
            change[j]=change1[i+j]
            variance[i]=variance[i]+pow(s,num-j-1)*(change[j]**2)
        
        variance[i]=(1-s)*variance[i]
        pastvar=np.zeros(num)
        normr=np.zeros(num)
        value=np.zeros(num)
        pastvar[0]=(1-s)*pow(change[0],2)
        for j in range(1,num):
            pastvar[j]=s*pastvar[j-1]+(1-s)*(change[j-1]**2)
        for k in range(0,num):
            normr[k]=np.sqrt(variance[i]/pastvar[k])*change[k]
            value[k]=normr[k]*contract_value1
        
        value=np.sort(value, axis=None)
        var_ewma1[i]=value[num*(1-CI)-1]
        actual1[i]=contract_value1*change1[num+i]
        if actual1[i]<var_ewma1[i]:
            count1=count1+1
    error[0]=float(count1)/days
    var_ewma1=abs(var_ewma1)
    actual1=(-1)*actual1
    '''
    pastvar=np.zeros(len(change1))
    pastvar[0]=(1-s)*pow(change1[0],2)
    for i in range(1,len(change1)):
        pastvar[i]=s*pastvar[i-1]+(1-s)*(change1[i-1]**2)
    for i in range(0,days):
        contract_value1=1120*price1[num+i]
        change=np.zeros(num)
        for j in range(0,num):
            change[j]=change1[i+j]
            variance[i]=variance[i]+pow(s,num-j-1)*(change[j]**2)
        
        variance[i]=(1-s)*variance[i]
        normr=np.zeros(num)
        value=np.zeros(num)
        for j in range(0,num):
            normr[j]=np.sqrt(variance[i]/pastvar[i+j])*change[j]
            value[j]=normr[j]*contract_value1
        value=np.sort(value, axis=None)
        var_ewma1[i]=value[num*(1-CI)-1]
        actual1[i]=contract_value1*change1[num+i]
        if actual1[i]<var_ewma1[i]:
            count1=count1+1
    error[0]=float(count1)/days
    var_ewma1=abs(var_ewma1)
    actual1=(-1)*actual1
else:
    ##############################
    #Parametric VaR
    for i in range(0,days):
        contract_value1=1120*price1[num+i]
        change=np.zeros(num)
        for j in range(0,num):
           change[j]=change1[i+j]
           variance[i]=variance[i]+pow(s,num-j-1)*(change[j]**2)
        
        variance[i]=(1-s)*variance[i]
        mean1=np.mean(change)
        std1=np.sqrt(variance[i])
        var_ewma1[i]=contract_value1*(mean1-norm.ppf(CI)*std1)
        actual1[i]=contract_value1*change1[num+i]
        if actual1[i]<var_ewma1[i]:
            count1=count1+1
    error[0]=float(count1)/days
    var_ewma1=abs(var_ewma1)
    actual1=(-1)*actual1

##############################################################################################
#Output
from Tkinter import *

lst = var_ewma1.astype(str)
day=np.asarray(range(1, days+1))
day=day.astype(str)

root = Tk()
root.title("FUTURES MARGIN RESULT")
def close_window (): 
    root.destroy()

label_1=Label(root, text="Futures Margin: ")
label_1.grid(row=0, sticky=W)
label_1.pack()
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
t = Text(root,wrap=WORD, yscrollcommand=scrollbar.set)
for i in range(0,days):
    t.insert(END, 'Day ' + day[i] +': ' + lst[i] + '\n' + '\n')
    t.pack()
    t.configure(font=("Times New Roman", 14, "bold"))
    t.configure(spacing2=10)

frame = Frame(root)
frame.pack()
b=Button(frame, text="Exit", command=close_window)
b.pack()

root.mainloop()


##############################################################################################
#Plotting
import matplotlib.pyplot as plt
x=range(1,days+1)
plt.plot(x, var_ewma1,label='VaR',marker='o',color='g')
plt.bar(x, abs(actual1),label='Actual Loss',width=1,color='r')
if model==1:
    plt.title('Historical Simulation with EWMA (SBV2016)')
else:
    plt.title('Parametric VaR with EWMA (SBV2016)')

plt.xlabel('Day')
plt.ylabel("VaR vs. Actual Loss")
plt.legend()
plt.show()
plt.close('all')













