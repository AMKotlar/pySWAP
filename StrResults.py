def Strresults(file,scenario,saveres):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt 
    indx="Date"
    linnum=6
    with open(file, "r") as f:
        lines=f.readlines()
        #if str(file)[-3:]=='vap':
            #header=[i.strip() for i in lines[11][:-1].split(",")] # extracts the labels for DF
            #lines=lines[12:] # Headers should be removed
            #indxname="date"
        #elif str(file)[-3:]=='inc':
        header=[i.strip() for i in lines[linnum][:-1].split(",")] # extracts the labels for DF
        lines=lines[linnum+1:] # Headers should be removed
    dataframe={} # Create a Dic for creating DF later
    for i in header:
        dataframe[i]=[]
    aa=[i.strip() for i in lines[0][:-1].split(",")]#this takes every row       
    #for head,value in zip(header,aa): # use zip for pairing columns(Attribute) and values
    for line in lines: # Run the cell to create dic datasei
                #if line!="*\n" and line!="\n" and 'cm' not in line and indx not in line:
                if line!="*\n" and indx not in line:
                    values=[i.strip() for i in line[:-1].split(",")]
                     #print('here1')
                for att,value in zip(header,values):
                    #print('here2')
                    if value=='':
                        dataframe[att].append('0.0')
                    elif att!=indx:
                        dataframe[att].append(np.float64(value))
                    else:
                        dataframe[att].append(value)

    df=pd.DataFrame(dataframe) # of dic dataset, create a pandas data frame
    df
    df[indx]= pd.to_datetime(df[indx],format='%Y-%m-%d') #  change the data type
    df['day'] = df[indx].dt.day
    df['month'] = df[indx].dt.month
    df['year'] = df[indx].dt.year
    yearly_Str=df.groupby(df.year,as_index=False)[['Tredwet','Treddry','Tredsol','Tredfrs']].apply(sum)#/np.si
    monthly_Str=df.groupby(['year','month'],as_index=False)[['Tredwet','Treddry','Tredsol','Tredfrs']].apply(sum)#/np.si
    
    if saveres=="TRUE":
        yearly_Str.to_csv(scenario+'_strYear.csv',index=False)
        monthly_Str.to_csv(scenario+'_strMonth.csv',index=False)
    
    return yearly_Str,monthly_Str 
