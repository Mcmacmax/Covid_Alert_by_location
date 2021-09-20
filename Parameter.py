import pandas as pd
import numpy as np
import datetime
import pyodbc as db
import os
import glob
from dateutil.relativedelta import relativedelta

def B(dfoutB,DF_CJ):
    count = 0
    dfout=[]
    count=count+1
    data_In= DF_CJ
    dfobj = pd.DataFrame(data_In)
    df_write=dfobj.replace(np.nan,"''")
    for v in df_write.values:
        #ConfirmID1 = v[0]
        Location_Name = str(v[0]).replace("'", "")
        #Location_Name =v[0]
        #FROM_EMPID1 = v[2]
        #FROM_LOCATION_DATE1 = v[3].strftime('%Y-%m-%d %H:%M:%S')
        datefrom1 = v[4].date()
        dateto1 = v[4].date()
        FROM_LAT1 = v[2]
        FROM_LONG1 = v[3]
        #TRACE_DATE1 =v[7]
        print(Location_Name)

        dfout = pd.DataFrame(columns=['Location_Name','TRACE_DATE','Location_Lat','Location_Long','EMPID','EMPID_LAT','EMPID_LONG','EMPID_CheckIn_Date'])
        ##################################################### 1. Del Data and write from data frame
        """ database connection ={SQL Server Native Client 11.0};"""
        conn = db.connect('Driver={SQL Server Native Client 11.0};'
                            'Server=SBNDCTSREMP;'
                            'Database=SR_APP;'
                            'Trusted_Connection=yes;')
        cursor = conn.cursor()
        SQL =  """
        /* Declare Tracking Date Preriod */

        --------------INPUT FILED---------------
        declare @Location_Name nvarchar(255) =N'"""+str(Location_Name)+"""'
        declare @dateFrom date = '"""+str(datefrom1)+"""'
        declare @dateTo date = '"""+str(dateto1)+"""' 
        declare @LatIn float  = '"""+str(FROM_LAT1)+"""'
        declare @longIn float = '"""+str(FROM_LONG1)+"""'


        --------------AUTO CALCUCATE-------------------
        ------------------100m-----------------
        declare @Lat float =   cast(cast(@LatIn as nvarchar) as float)-0.00085
        declare @Lat1 float =  cast(cast(@LatIn as nvarchar) as float)+0.00085
        declare @long float  = cast(cast(@LongIn as nvarchar)as float)-0.00085
        declare @long1 float = cast(cast(@LongIn as nvarchar)as float)+0.00085
        ------------------200m-----------------
        ---declare @Lat float =   cast(cast(@LatIn as nvarchar) as float)-0.0017
        ---declare @Lat1 float =  cast(cast(@LatIn as nvarchar) as float)+0.0017
        ---declare @long float  = cast(cast(@LongIn as nvarchar)as float)-0.0017
        ---declare @long1 float = cast(cast(@LongIn as nvarchar)as float)+0.0017
        ----------------------------------------------

        /* List All Check-In Transection in Risk Area */

        select @Location_Name Location_Name
        ,cast(getdate() as smalldatetime) Trace_datetime
        ---,@EMP FROM_EMPID
        ---,@status FROM_STATUS
        ,@Lat Location_Lat
        ,@long Location_Long
        ---,@FROMDATETIME FROM_LOCATIONDATETIME
        ,MN.EmployeeId TO_EMP
        ---,'B' FROM_STATUS
        ,MN.latitude TO_LAT
        ,MN.longitude TO_LONG
        ,MN.CheckinDatetime TO_LOCATIONDATETIME
        from ( /* QR check in*/
        SELECT TS.[EmployeeId] 
        ,cast(TS.CreatedDateTime as date) [CheckinDate]
        ,TS.CreatedDateTime [CheckinDatetime]
        ,Loc.LocationNameTH 
        ,TS.ShopName
        ,coalesce(Loc.LocationNameTH, case when TS.ShopName = '' then NULL else TS.ShopName end ) LocationName
        ,[UserLat] as [latitude] 
        ,[UserLong] as [longitude] 
        FROM [SR_APP].[dbo].[TB_QR_TimeStamp] TS
        left join [SR_APP].[dbo].[TB_QR_Location] Loc on Loc.LocationId = TS.LocationId
        where cast(TS.CreatedDateTime as date) between @dateFrom and @dateTo
        and cast([UserLat] as float) between @lat and @lat1
        and cast([UserLong] as float) between @long and @long1
        
        union /* PG check in*/
        select  A.[EmployeeId]
        ,cast(A.[CreatedDateTime] as date) as [CheckinDate]
        ,A.[CreatedDateTime] as [CheckinDatetime] 
        ,A.[ShopName] [LocationNameTH]
        ,cast(A.[ShopId] as nvarchar(20)) ShopName
        ,A.[ShopName] [LocationName]
        ,[UserLat] as [latitude] 
        ,[UserLong] as [longitude] 
        from [SR_APP].[dbo].[TB_Checkin_PG] A
        where cast(A.[CreatedDateTime] as date) between @dateFrom and @dateTo
        and cast(A.[UserLat] as float) between @lat and @lat1
        and cast(A.[UserLong] as float) between @long and @long1
        
        ) MN
        """
        print(SQL)
        cursor.execute(SQL)
        data_Out = cursor.fetchall()
        for row in data_Out:
            newrow= {'Location_Name':row[0],'TRACE_DATE':row[1],'Location_Lat':row[2],'Location_Long':row[3],'EMPID':row[4],'EMPID_LAT':row[5],'EMPID_LONG':row[6],'EMPID_CheckIn_Date':row[7]}
            dfout = dfout.append(newrow, ignore_index=True)
        print('B Complete ===>> ',count,' : ')
        #Output_Path = r'./'+str(Location_Name)+'.xlsx'
        dfoutB = dfoutB.append(dfout,ignore_index=True)
        #dfoutB.to_excel(Output_Path,index=False)
        print(dfoutB)
    dfoutB.sort_values(by=['Location_Name'])

    cursor.commit()
    return(dfoutB)
    
def Employee_Profile():
    """database connection ={SQL Server Native Client 11.0};"""
    conn = db.connect('Driver={SQL Server Native Client 11.0};'
                        'Server=SBNDCTSREMP;'	
                        'Database=SR_APP;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    #dfout = pd.DataFrame(columns=['EmployeeId','FullName', 'CompanyName','GroupBU','ContactPhone'])
    SQL = """ 
    SELECT [EmployeeId]
	  ,CONCAT(LocalFirstName,' ',LocalLastName) FullName
      ,[CompanyName]
      ,[GroupBU]
      ,[ContactPhone]
    FROM [SR_APP].[dbo].[TB_Employee]
    """ 
    #print(SQL)
    dfout = pd.DataFrame(data=pd.read_sql_query(SQL,conn),columns=['EmployeeId','FullName', 'CompanyName','GroupBU','ContactPhone'])
    cursor.commit()
    return(dfout)