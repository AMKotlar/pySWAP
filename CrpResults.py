def Crpresults(file,scenario,cropnum,plotcon,saveres):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.dates import DateFormatter
    indx="Date"
    linnum=7

    indx="Date"
    with open(file, "r") as f:
        lines=f.readlines()
        header=[i.strip() for i in lines[linnum][:-1].split(",")] # extracts the labels for DF
        lines=lines[linnum+1:] # Headers should be removed
        for line in lines: # Run the cell to create dic datasei
                #if line!="*\n" and line!="\n" and 'cm' not in line and indx not in line:
                if line!="*\n" and "grC" not in line and indx not in line:
                    values=[i.strip() for i in line[:-1].split(",")]

    header
    dataframe={} # Create a Dic for creating DF later
    for i in header:
        dataframe[i]=[]
    aa=[i.strip() for i in lines[0][:-1].split(",")]#this takes every row
    for line in lines: # Run the cell to create dic datasei
            #if line!="*\n" and line!="\n" and 'cm' not in line and indx not in line:
            if line!="*\n" and "grC" not in line and indx not in line:
                values=[i.strip() for i in line[:-1].split(",")]
                #print('here1')
                for att,value in zip(header,values):
                    #print('here2')
                    #print(att,value)
                    if value=='':
                        dataframe[att].append('0.0')
                    elif att!=indx:
                        dataframe[att].append(np.float64(value))
                    else:
                        dataframe[att].append(value)
                    #print(np.shape(value))
    df=pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dataframe.items()])) # of dic dataset, create a pandas data framer
    df["cumday"]=df['Daynr'].cumsum()
    finaldays=np.where(df["Daycrp"].diff()!=1)
    idxs=pd.DataFrame(list(zip(*finaldays)))-1
    #idxs[1:]
    s1=(idxs[1:][0])
    s2=pd.Series(np.shape(df)[0]-1)
    s3 = s1.append(s2, ignore_index=True)
    finaldf=df.iloc[s3.tolist(),:]
    years= pd.to_datetime(finaldf['Date'],format='%Y-%m-%d')
    years=years.dt.year
    if plotcon=="TRUE":
        fig, ax = plt.subplots(figsize=(20, 5))
        bars=ax.bar(finaldf.Date,finaldf["CWSO"],tick_label=years,color=['gold'],edgecolor='black')
        #bars.set_xticks(finaldf['Date'].dt.year,finaldf['Date'].dt.month)
        #ax.xticks(np.arange(6, len(finaldf), 12))
        if cropnum=="2":
            for item in bars[::2]:
                item.set_color('tan')
                item.set_edgecolor('black')
            ax.set_title(label=scenario,fontsize=14,color="black")
            legend_elements = [Patch(facecolor='tan', edgecolor='tan',
                                 label='Winter Wheat'),Patch(facecolor='gold', edgecolor='gold',
                                 label='Maize')]
            ax.legend(handles=legend_elements,loc="upper left")
    ax.figure.savefig(scenario+'Yield'+'.png',format='png',dpi=200)
      #finaldf
  
    if saveres=="TRUE":
        finaldf.to_csv(scenario+'_yield.csv',index=False)
    
    return finaldf 
