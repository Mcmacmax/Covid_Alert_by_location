import pandas as pd
import numpy as np

def CJ(Input_Path):
    #dict_Datetime = {'วันที่เริ่มต้นของสถานที่ใน Timeline':pd.to_datetime,'วันที่สิ้นสุดของสถานที่ใน Timeline':pd.to_datetime}
    data_In= pd.read_excel(Input_Path)
    print(data_In['วันที่เริ่มต้นของสถานที่ในTimeline'])
    dfobj = pd.DataFrame(data_In)
    df_write=dfobj.replace(np.nan,"''")
    DF_Crossjoin = pd.DataFrame(columns=['ชื่อสถานที่',
    'จังหวัด',
    'พิกัด Latitude',
    'พิกัด Longitude',
    'Date'])
    #Filter
    df_write2 = df_write.loc[df_write['Trace_Flag'] == 0]
    print(df_write2)
    for v in df_write2.values:
        #Prep_DATA
        #Replace DATA 
        data1 = {'ชื่อสถานที่':[v[9]],
                'จังหวัด':[v[10]],
                'พิกัด Latitude':[v[11]],
                'พิกัด Longitude':[v[12]]
                }  
        try:
            if v[8] == "''":
                data2 = {'Date':[v[7].strftime('%Y-%m-%d')]}
                #print(data2)
            else: 
                data2 = pd.date_range(start=v[7],end=v[8])
        except:
            data2 = {'Date':[v[7].strftime('%Y-%m-%d')]}
            #data2 = data2.to_frame()
            #print("else__",data2)
        #print(data2)
        # Convert the dictionary into DataFrame   
        df = pd.DataFrame(data1) 
        #print(df)
        # Convert the dictionary into DataFrame   
        df1 = pd.DataFrame(data2,columns=['Date'])
        df1['Date']=pd.to_datetime(df1['Date'],format="%Y-%m-%d")
        #print(df1)
        # Now to perform cross join, we will create 
        # a key column in both the DataFrames to  
        # merge on that key. 
        df['key'] = 1
        df1['key'] = 1
        # to obtain the cross join we will merge  
        # on the key and drop it. 
        result = pd.merge(df, df1, on ='key').drop("key", 1)
        #print(result)
        DF_Crossjoin = DF_Crossjoin.append(result,ignore_index=True)
    #Save to excel
    Output = r'./Output/Timeline_Crossjoin.xlsx'
    DF_Crossjoin.to_excel(Output,index=False)
    return(DF_Crossjoin)