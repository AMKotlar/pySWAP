#this funtion needs both inc and swb files
def Swbresults(file,fileInc,warmupyrs,nameScen,firstdate,secdate,controldrain,ylim1, arbitvar):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from IncResults import Incresults
    #import inc_result 
    linnum=21
    indx="Date"
    with open(file, "r") as f:
        lines=f.readlines()
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
    df[indx]= pd.to_datetime(df[indx],format='%Y-%m-%d') #  change the data type
    df['day'] = df[indx].dt.day
    df['month'] = df[indx].dt.month
    df['year'] = df[indx].dt.year
    yearly_Gwl=df.groupby(df.year,as_index=False)[['GWL']].apply(sum)#/np.size(years)
 
    yearly_inc=df.groupby(df.year,as_index=False)[['GWL','WLST','WLS','swst','DRORR','QSUPP','QOUT']].apply(sum)#/np.size(years)
    fsize=18
    yearly_inc,yearmonth_Gwl,dff,dfInc,ppp,qqq=Incresults(fileInc,warmupyrs, nameScen,"FALSE","FALSE")
    
    #dfInc,yearly_incb=Incresults(file=fileInc,nameSc="sc",saveres="FALSE",plotcon="FALSE")
    years_list=df.year.unique()
    yearly_inc.to_csv(nameScen+'_SWB.csv',index=False) 
    depth_list=df.year.unique()
    print(depth_list)
    all_depthdata={}
    df[df["year"]==depth_list[2]]
    len(depth_list)
    for i in range(len(depth_list)):
        #print(i)
        depth_data=df[df["year"]==depth_list[i]]
    dfSW=df
    dfplot=df[df['Date'].between(pd.to_datetime(firstdate), pd.to_datetime(secdate))]
    dfIncplot=dfInc[dfInc['Date'].between(pd.to_datetime(firstdate), pd.to_datetime(secdate))]
    
    
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1,figsize=(10, 6))

    #fig, ax1 = plt.subplots()
 

    ax1.plot(dfplot.Date, dfplot.GWL, label ="GWL")
    if controldrain=="TRUE":
        ax1.plot(dfplot.Date, dfplot.WLS, label ="Drain Level")
        ax1.plot(dfplot.Date, dfplot.WLST, label ="Drain Level Adjusted")
        #ax1.plot(dfplot.Date, dfplot.WLST,'--',label ="Controlled Levels", color="black")
    
    #ax1.set(ylim=(min(dfplot.GWL),30)) 
    ax1.set(ylim=(ylim1,30)) 

    
    ax1.set_ylabel('Level(cm)') 
    #ax2.tick_params(axis ='y', labelcolor = 'gray') 
    ax1.legend(loc="lower left")
    ax1.set_title(label=nameScen,fontsize=18,color="black")
    # 
    ax2.set_ylabel('P-ET', color = 'blue') 
    ax2.bar(dfIncplot.Date, dfIncplot.Rain-(dfIncplot.Tact+dfIncplot.Eact), label ="P-ET",color = 'gray') 
    
    #ax2.set(ylim=(1.2*min(dfIncplot.Rain-(dfIncplot.Tact+dfIncplot.Eact)),2*max(dfIncplot.Rain-(dfIncplot.Tact+dfIncplot.Eact))))
    ax2.set(ylim=(0,10))    
    ax2.invert_yaxis()
    ax2.set_ylabel('P-ET (cm)', color = 'gray') 
    ax2.tick_params(axis ='y', labelcolor = 'gray') 
    #ax1.plot(dfb.Date, dfb.Drainage,'--',label ="Draiange", color="red")
    ax2a = ax2.twinx()
    #ax0.plot(x, y, color='blue') 
    #ax01.scatter(x, z, color='red') 
    #ax01 = ax0.twinx() 
    dfInc.index=[dfInc.Date.dt.year, dfInc.Date.dt.month]
    MonthlyDr=dfIncplot.groupby(['year','month'])['Drainage'].sum()
    ax2a.bar(dfIncplot.Date, dfIncplot.Drainage, color = 'blue')
    ax2a.set_ylabel('Drainage (cm)', color = 'blue') 
    # Add legend
    ax2a.tick_params(axis ='y', labelcolor = 'blue') 
    #ax1.tick_params(labelsize=20)
    
    ax2a.set(ylim=(-.1,1))

    # Show plot
    ax3.plot(dfplot.Date, dfplot[arbitvar], label =arbitvar)
    ax3.hlines(y=0, xmin=dfplot.Date[0], xmax=dfplot.Date[-1:], linewidth=1, color='r')
    
    # 
    ax3.set_ylabel(arbitvar, color = 'blue') 
    plt.show()
    fig.savefig(nameScen+'Levels_PEDr'+'.png',format='png',dpi=200)

    return dfSW, dfInc
    