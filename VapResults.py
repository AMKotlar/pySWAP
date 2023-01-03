#this funtion needs both inc and swb files
def Vapresults(file,desvar,nameScen,dat1,dat2,dmax):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from IncResults import Incresults
    ftsz=14
    #import inc_result 
    linnum=21
    
    indx="date"
    with open(file, "r") as f:
        lines=f.readlines()
        header=[i.strip() for i in lines[11][:-1].split(",")] # extracts the labels for DF
        lines=lines[12:] # Headers should be remove

    dataframe={} # Create a Dic for creating DF later
    for i in header:
        dataframe[i]=[]
    aa=[i.strip() for i in lines[0][:-1].split(",")]#this takes every row       
    #for head,value in zip(header,aa): # use zip for pairing columns(Attribute) and values
    for line in lines: # Run the cell to create dic datasei
                #if line!="*\n" and line!="\n" and 'cm' not in line and indx not in line:
                if line!="*\n" and line!="\n" and 'cm' not in line and indx not in line:
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
    df[indx]= pd.to_datetime(df[indx],format='%Y-%m-%d') #  change the data type
    df['day'] = df[indx].dt.day
    df['month'] = df[indx].dt.month
    df['year'] = df[indx].dt.year
    depth_list=df.depth.unique()
    depth_list
    all_depthdata={}
    df[df["depth"]==depth_list[2]]
    len(depth_list)
    for i in range(len(depth_list)):
        #print(i)
        depth_data=df[df["depth"]==depth_list[i]]
    
    df['year'] = df['date'].dt.year
    df2=df[df['date'].between(pd.to_datetime(dat1), pd.to_datetime(dat2))]
    df2=df2[df2.bottom != '0.0']
    
    fig, ax1 = plt.subplots(1,1, sharex=True, sharey=True, figsize=(15,8))
    df2['depth']=-df2.depth
    if desvar=="wcontent":
        sc1 = ax1.scatter(df2.date, df2.depth, c=df2.wcontent, cmap='RdYlBu', vmin = .1, vmax =.38,marker = 's', s=2.5)
        ie = df2['depth'].between(0, 90) & df2['date'].dt.month.between(5, 6) 
        x = df2.loc[ie,['date','wcontent']]
        xx[k]=x
    #print((x.wcontent))
    if desvar=="solute1":
        sc1 = ax1.scatter(df2.date, df2.depth, c=df2.solute1/max(df2.solute1), cmap='coolwarm',marker = 's', s=40)
    if desvar=="phead":
        df2["phead"]=df2["phead"].mask(df2["phead"]>=0).fillna(1)
        sc1 = ax1.scatter(df2.date, df2.depth,c=np.log10(np.asarray((abs(df2.phead))).astype(np.float64)), 
                          cmap='coolwarm',vmin =-2, vmax =4.5,marker = 's', s=50)
    plt.ylim([0,dmax])
    # Because the X and Y axes are shared, we only have to set limits once
    ax1.invert_yaxis() # Invert y axis
    #ax1.set_xlim(df.date[0],df.date[-1]) # Set the time limits to match the dataset
    cbar = fig.colorbar(sc1, ax=ax1, orientation='vertical')
    cbar.ax.set_ylabel(desvar,fontsize=ftsz)
    #cbar.clim(.25, .42)
    #cbar = fig.colorbar(sc2, ax=ax2, orientation='vertical')
    #cbar.ax.set_ylabel('Salinity')
    plt.xticks(fontsize=ftsz, rotation=60)#, rotation=90
    plt.yticks(fontsize=ftsz)#, rotation=90
    ax1.set_ylabel('depth [cm]', fontsize=16)

    return 
    