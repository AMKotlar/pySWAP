def Drfresults(file,fileInc,warmupyrs,nameScen,firstdate,secdate,ylim1):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from IncResults import Incresults
    #import inc_result 
    linnum=18
    cols=[ "Date","Daynr","CQDinc1","CQDinc2","CQDinc3","CQDinc4","CQDinc5",
      "CQDRDinc","CRUNOFFinc","CQDRARinc","CQDcum1","CQDcum2","CQDcum3",
      "CQDcum4","CQDcum5","CQDRDcum","CRUNOFFcum","CQDRARcum"]
    df = pd.DataFrame(columns=cols)

    with open(file, "r") as f:
        lines=f.readlines()
        header=[i.strip() for i in lines[linnum][:-1].split(",")] # extracts the labels for DF
        lines=lines[linnum+1:] # Headers should be removed
        lines=[x for x in lines if "*" not in x]
        lines=[x for x in lines if "Date" not in x]
        lines=[x for x in lines if len(x) > 1]
        lines = [item.strip() for item in lines]
        #print(lines)
        dataframe={} # Create a Dic for creating DF later
        list1 = []
        for line in lines:
            list1.append(line.replace(' ', '').split(','))
    df = pd.DataFrame(list1, columns=cols)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df.set_index('Date')
    df['day'] = df["Date"].dt.day
    df['month'] = df["Date"].dt.month
    df['year'] = df["Date"].dt.year
    df
    df[cols[1:]] = df[cols[1:]].apply(pd.to_numeric, errors='coerce')

    #"CQDinc1","CQDinc2","CQDinc3","CQDinc4","CQDinc5","CQDRDinc","CRUNOFFinc","CQDRARinc","CQDcum1","CQDcum2","CQDcum3","CQDcum4","CQDcum5","CQDRDcum","CRUNOFFcum","CQDRARcum"
    #yearly_inc=df.groupby(df.year,as_index=False)[["CQDinc1","CQDinc2"]].apply(sum)#/np.size(years)
    fsize=18
    yearly_inc,yearmonth_Gwl,dff,dfInc,ppp,qqq=Incresults(fileInc,warmupyrs, nameScen,"FALSE","FALSE")
    
    #dfInc,yearly_incb=Incresults(file=fileInc,nameSc="sc",saveres="FALSE",plotcon="FALSE")
    years_list=df.year.unique()
    yearly_inc.to_csv(nameScen+'_DRF.csv',index=False) 
    depth_list=df.year.unique()
    depth_list
    all_depthdata={}
    df[df["year"]==depth_list[2]]
    len(depth_list)
    for i in range(len(depth_list)):
        #print(i)
        depth_data=df[df["year"]==depth_list[i]]
    dfDrf=df
    dfplot=df[df['Date'].between(pd.to_datetime(firstdate), pd.to_datetime(secdate))]
    dfIncplot=dfInc[dfInc['Date'].between(pd.to_datetime(firstdate), pd.to_datetime(secdate))]
    
    
    
    fig, (ax1) = plt.subplots(nrows=1, ncols=1,figsize=(10, 5))

    #fig, ax1 = plt.subplots()
 

    ax1.plot(dfplot.Date, dfplot.CQDinc1, label ="CQDinc1")
    #if controldrain=="TRUE":
     #   ax1.plot(dfplot.Date, dfplot.WLS, label ="Drain Level")
        #ax1.plot(dfplot.Date, dfplot.WLST,'--',label ="Controlled Levels", color="black")
    
    #ax1.set(ylim=(min(dfplot.GWL),30)) 
    #ax1.set(ylim=(ylim1,30)) 

    
    ax1.set_ylabel('drainage flux(cm)') 
    #ax2.tick_params(axis ='y', labelcolor = 'gray') 
    ax1.set_title(label=nameScen,fontsize=18,color="black")
    
    ax1.plot(dfplot.Date, dfplot.CQDinc2, label ="CQDinc2")
    ax1.plot(dfplot.Date, dfplot.CQDinc2+dfplot.CQDinc2, label ="sum")
    
    ax1.axhline(y=0, xmin=0, xmax=100000, c="black", linewidth=1)

    ax1.legend(loc="upper right")

    # 
    #ax2.plot(dfplot.Date, dfplot["CQDinc2"]), color = 'gray') 
    #ax2.set_ylabel('P-ET', color = 'blue') 

    #ax2.set(ylim=(1.2*min(dfIncplot.Rain-(dfIncplot.Tact+dfIncplot.Eact)),2*max(dfIncplot.Rain-(dfIncplot.Tact+dfIncplot.Eact))))
    #ax2.set(ylim=(0,10))    
    #ax2.invert_yaxis()
    #ax2.set_ylabel('P-ET (cm)', color = 'gray') 
    #ax2.tick_params(axis ='y', labelcolor = 'gray') 
    #ax1.plot(dfb.Date, dfb.Drainage,'--',label ="Draiange", color="red")
    #ax2a = ax2.twinx()
    #ax0.plot(x, y, color='blue') 
    #ax01.scatter(x, z, color='red') 
    #ax01 = ax0.twinx() 
    dfInc.index=[dfInc.Date.dt.year, dfInc.Date.dt.month]
    MonthlyDr=dfIncplot.groupby(['year','month'])['Drainage'].sum()
    #ax2a.bar(dfIncplot.Date, dfIncplot.Drainage, color = 'blue')
    #ax2a.set_ylabel('Drainage (cm)', color = 'blue') 
    # Add legend
    #ax2a.tick_params(axis ='y', labelcolor = 'blue') 
    #ax1.tick_params(labelsize=20)
    #ax1.xaxis.set_major_locator(ticker.MultipleLocator(.1))

    #ax1.set(ylim=(-.5,1.5))

    # Show plot
    #ax3.plot(dfplot.Date, dfplot[arbitvar], label =arbitvar)
    #ax3.hlines(y=0, xmin=dfplot.Date[0], xmax=dfplot.Date[-1:], linewidth=1, color='r')
    
    # 
    #ax3.set_ylabel(arbitvar, color = 'blue') 
    plt.show()
    fig.savefig(nameScen+'Levels_PEDr'+'.png',format='png',dpi=200)

    return dfDrf, dfInc
    