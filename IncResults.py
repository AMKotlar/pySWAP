
def Incresults(file,warmupyrs,nameSc,plotcon,saveres):
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    linnum=6
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
    df['Gwl']=pd.to_numeric(df.Gwl, errors='coerce').fillna(0, downcast='infer')
    df = df[df.year != warmupyrs]

    yearly_Gwl=df.groupby(df.year,as_index=False)[['Gwl']].apply(sum)#/np.size(years)
    #climdata.set_index('dateInt', inplace=True)
    yearmonth_Gwl=df.groupby(['year','month'])['Gwl'].mean().reset_index()#/np.size(years)
    yearmonth_Rain=df.groupby(['year','month'])['Rain'].sum().reset_index()
    yearmonth_EvP=df.groupby(['year','month'])['Epot'].sum().reset_index()
    yearmonth_TrP=df.groupby(['year','month'])['Tpot'].sum().reset_index()
    yearmonth_TrP["EvP"]=yearmonth_EvP.Epot
    yearmonth_TrP["Rain"]=yearmonth_Rain.Rain
    yearmonth_TrP["def"]=-yearmonth_TrP.Tpot-yearmonth_TrP.EvP+yearmonth_TrP.Rain

    
    yearly_inc=df.groupby(df.year,as_index=False)[['Drainage','QBottom','Tact','Eact','dstorage','Rain','Interc','Runon','Runoff','Tpot','Epot']].apply(sum)#/np.size(years)
    fsize=14
    years_list=df.year.unique()
    yearly_inc['WatBal']=yearly_inc.Rain-yearly_inc.Drainage+yearly_inc.QBottom-yearly_inc.Tact-yearly_inc.Eact-yearly_inc.dstorage-yearly_inc.Interc
    mean_GWlevel=df.groupby(df.year,as_index=False)[['Gwl']].apply(np.mean)
    yearly_inc['GWlevel']=mean_GWlevel.Gwl
    if saveres=="TRUE":
        yearmonth_Gwl.to_csv(nameSc+'_GWLmoyr'+'_Inc.csv',index=False)
        yearly_inc.round(3).to_csv(nameSc+'_Inc.csv',index=False) 
        df.to_csv(nameSc+'_daily'+'_Inc.csv',index=False)
    if plotcon=="TRUE":
        sns.boxplot(data=yearmonth_TrP, x="month", y="def")
        sns.boxplot(data=yearmonth_Gwl, x="month", y="Gwl")

        #ax=yearly_inc.plot(x="year", y=["DrainagePerc","QbotPerc", "TactPerc", "EactPerc"], kind="bar")
        #ax.set_ylabel("[mm]",color="black",fontsize=fsize)
        #ax.legend(["Drainage/Rain","Qbot/Rain","Tact/Rain", "Eact/Rain"])
        plt.title(label=nameSc+"(a)",
                  fontsize=14,
                  color="black")
        #ax.set_xticks(np.arange(0, len(x)+1, 5))
        #ax.figure.savefig(nameSc+'.png',format='png',dpi=200)
        WaterLoss=np.mean(yearly_inc.QBottom)
        np.std(yearly_inc.QBottom)
        #plt.subplot(1, 2, 2)
        mean_GWlevel.plot(x='year',y='Gwl')
        plt.savefig(nameSc+'GWL'+'.png',format='png',dpi=200)
        plt.title(label=nameSc+"(b)",
                  fontsize=14,
                  color="black")
        fig, ax1 = plt.subplots() 
        ax1.set_xlabel('Time') 
        ax1.set_ylabel('GWL(m)', color = 'red') 
        ax1.plot(df.Date, df.Gwl, color = 'red') 
        ax1.tick_params(axis ='y', labelcolor = 'red') 
        plt.ylim((-300, 0))   
        ax2 = ax1.twinx() 
        ax2.set_ylabel('P-ET', color = 'blue') 
        ax2.plot(df.Date, df.Rain-(df.Tact+df.Eact), color = 'blue') 
        ax2.tick_params(axis ='y', labelcolor = 'blue') 
        plt.ylim((-1, 5)) 
        # Show plot
        plt.title(label=nameSc,
                  fontsize=14,
                  color="black")
        #ax1.set_ylabel('depth')
        plt.savefig(nameSc+'GWL_PET'+'.png',format='png',dpi=200)
        plt.show()
        fig, ax3 = plt.subplots() 
        ax = yearmonth_Gwl.set_index(pd.to_datetime(yearmonth_Gwl[['year', 'month']].assign(day=15)))['Gwl']\
        .plot(color='b', title='Monthly Data')#,marker='.', linestyle='none')
        _ = ax.set_xlabel('Data')
        _ = ax.set_ylabel('Data')
    return yearly_inc,yearmonth_Gwl,yearmonth_Rain,df,yearmonth_EvP,yearmonth_TrP