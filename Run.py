import pandas as pd
import numpy as np
import datetime
import pyodbc as db
import os
import glob
from dateutil.relativedelta import relativedelta
from Parameter import B as B
from Parameter import Employee_Profile as EP
from CrossJoin import CJ as CJ
from Email import send_mail as email
from Email import send_mail2 as email2

start_datetime = datetime.datetime.now()
print (start_datetime,'execute')
today = datetime.datetime.now().strftime('%Y-%m-%d')

#### 1. Input Location and Transfrom (Cross Join)#####

Input_Path = r'C:/Users/70032204/OneDrive - Thai Beverage Public Company Limited/COVID_Alert/Timeline COVID-19 (Responses).xlsx'

DF_CJ = CJ(Input_Path)
#print(DF_CJ)

#### 2. Traceability#####
dfoutB = pd.DataFrame(columns=['Location_Name','TRACE_DATE','Location_Lat','Location_Long','EMPID','EMPID_LAT','EMPID_LONG','EMPID_CheckIn_Date'])
df_outB = B(dfoutB,DF_CJ)

#### 3 Lookup value Employee Detail #####
# Employee 
df_EP = EP() 
df_join = df_outB.merge(df_EP, how='left', left_on='EMPID', right_on='EmployeeId')
df_drop = df_join.drop(['EmployeeId'], axis=1)

#### 4 Save File #####
Output_PathB = r'./Output/Ouput'+str(today)+'.xlsx'
df_drop.to_excel(Output_PathB,index=False)

#### employee_id ####
df_uniqe = pd.DataFrame(df_drop['EMPID'].unique(), columns=['employee_id'])
####เพิ่มรหัสพี่ขจรและตัวเองเข้าไปก่อนส่ง#####
df_uniqe = df_uniqe.append({'employee_id': '11027745'}, ignore_index=True)
df_uniqe = df_uniqe.append({'employee_id': '70032204'}, ignore_index=True)
df_uniqe = df_uniqe.append({'employee_id': '70047231'}, ignore_index=True)
df_uniqe = df_uniqe.append({'employee_id': '70018928'}, ignore_index=True)
df_uniqe = df_uniqe.append({'employee_id': '11028263'}, ignore_index=True)
Output_Unqiue = r'./Output/CovidAlert_'+str(today)+'.xlsx'
df_uniqe.to_excel(Output_Unqiue,index=False)

#SEND EMAIL
#email(Output_Unqiue,today)
email2(Output_PathB,today)
print("Finish send Mail")

####UPDATE#####
data_In= pd.read_excel(Input_Path)
data_In.loc[(data_In['Trace_Flag']==0),'Trace_Flag']=1
data_In.to_excel(Input_Path,index=False)

end_datetime = datetime.datetime.now()
print ('---Start---',start_datetime)
print('---complete---',end_datetime)
DIFFTIME = end_datetime - start_datetime 
DIFFTIMEMIN = DIFFTIME.total_seconds()
print('Time_use : ',round(DIFFTIMEMIN,2), ' Seconds')
