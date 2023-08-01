import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import time
import fit
import models
import pickle
import matplotlib.font_manager
import scipy.stats



data_df_full=pd.read_csv("/home/meghna/rincewind/meghna1/DrCiampaglia/data_tweets_noncum.csv")
data_df_full.head()
scipy.stats.uniform.random_state = 10

story_ids = data_df_full['story_id'].to_list()
storyids = set(story_ids)
new_storyids = [3,10,13,14,18,24,25,26,27,28,29,30,31,32,36,37,44,45,46,47]
#new_storyids = [3,10,13]
for storyid in new_storyids:
    sub_df = pd.DataFrame()
    #sub_df = data_df_full
    sub_df['story_id'] = data_df_full[data_df_full['story_id'] == storyid]['story_id']
    sub_df['timestamp'] = data_df_full[data_df_full['story_id'] == storyid]['timestamp']
    sub_df['fact'] = data_df_full[data_df_full['story_id'] == storyid]['fact'].rolling(window=25, min_periods = 1,center=True).mean()
    sub_df['fake'] = data_df_full[data_df_full['story_id'] == storyid]['fake'].rolling(window=25, min_periods = 1,center=True).mean()
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
            
    
    new_m = fit.fit(sub_df,'HoaxModel','all',nrep = 100)
    new_m2 = fit.fit(sub_df,'SegHoaxModel','all',nrep = 100)
    new_m3 = fit.fit(sub_df,'SEIZ','all',nrep = 100)
    new_m4 = fit.fit(sub_df,'DoubleSIR','all', nrep = 100)
    
    data_BA_list2 = []
    data_FA_list2 = []
    sub_df = sub_df.set_index(["story_id"])
    
    data_BA2 = sub_df.loc[storyid]['fake']
    data_FA2 = sub_df.loc[storyid]['fact']
    data_BA_list2 = data_BA2.tolist()
    data_FA_list2 = data_FA2.tolist()
    range_times2 = len(data_BA_list2)    
    times2 = list([*range(range_times2)])

    model_values_all2 = new_m.simulate(times=times2)
    model_values_all_list2 = list(model_values_all2)

    model_values_all_sg2 = new_m2.simulate(times=times2)
    model_values_all_list_sg2 = list(model_values_all_sg2)

    model_values_seiz2 = new_m3.simulate(times=times2)
    model_values_seiz_list2 = list(model_values_seiz2)

    model_values_dsir2 = new_m4.simulate(times=times2)
    model_values_dsir_list2 = list(model_values_dsir2)

    model_values_all_ba2 = [item[0] for item in model_values_all_list2]
    model_values_all_fa2 = [item[1] for item in model_values_all_list2]
    model_values_all_sg_ba2 = [item[0] for item in model_values_all_list_sg2]
    model_values_all_sg_fa2 = [item[1] for item in model_values_all_list_sg2]
    model_values_seiz_ba2 = [item[0] for item in model_values_seiz_list2]
    model_values_seiz_fa2 = [item[1] for item in model_values_seiz_list2]
    model_values_dsir_ba2 = [item[0] for item in model_values_dsir_list2]
    model_values_dsir_fa2 = [item[1] for item in model_values_dsir_list2]

    plt.rc('font', family='serif', serif='Times')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    width  = 3.487
    height = width / 1.618
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(width,height),sharey=True)
    fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
    ax1.tick_params(axis='both', labelsize=5)
    ax2.tick_params(axis='both', labelsize=5)
    axes = [ax1,ax2]
    line1, = ax1.plot(times2,data_BA_list2,label = 'Data',color = 'black',linestyle = '',marker = 'o',markersize = 4)
    line2, = ax1.plot(times2,model_values_all_ba2,linestyle = "-",label = 'Standard',color = '0.70',linewidth = 2.64)
    line3, = ax1.plot(times2,model_values_all_sg_ba2,linestyle = "--",label = 'Ext. w/ seg.',color = '0.40',linewidth = 2.64)
    line4, = ax1.plot(times2,model_values_seiz_ba2,linestyle = "-.",label = 'SEIZ',color = '#762a83',linewidth = 2.64)
    line5, = ax1.plot(times2,model_values_dsir_ba2,linestyle = "-.",label = 'Double SIR',color = '#bf812d',linewidth = 2.64)
    ax1.set_title(str(storyid)+': Active Believers', fontsize = 8)
    #first_legend = ax1.legend(handles = [line1,line2,line3,line4,line5], loc = 'best', prop = {'size':5})
    ax1.set_xlabel('Hours',fontsize = 8)
    ax1.set_ylabel('Active Users', fontsize = 8)
    ax1.set_yscale('symlog')

    line6, = ax2.plot(times2,data_FA_list2,label = 'Data',color = 'black',linestyle = '',marker = 'o',markersize = 4)
    line7, = ax2.plot(times2,model_values_all_fa2,linestyle = "-",label = 'Standard',color='0.70',linewidth = 2.64)
    line8, = ax2.plot(times2,model_values_all_sg_fa2,linestyle = "--",label = 'Ext. w/ seg.',color = '0.40',linewidth = 2.64)
    line9, = ax2.plot(times2,model_values_seiz_fa2,linestyle = "-.",label = 'SEIZ',color = '#762a83',linewidth = 2.64)
    line10, = ax2.plot(times2,model_values_dsir_fa2,linestyle = "-.",label = 'Double SIR',color = '#bf812d',linewidth = 2.64)
    first_legend = ax2.legend(handles = [line6,line7,line8,line9,line10], loc = 'best', prop = {'size':5})
    ax2.set_title(str(storyid)+': Active Fact-checkers', fontsize = 8)
    ax2.set_xlabel('Hours',fontsize = 8)
    ax1.set_yscale('symlog')
    #fig.tight_layout()
    #fig.suptitle('Story '+ str(storyid), fontsize=8,va = 'center',x = 1,y = 1.5,ha = 'center')
    pickle.dump(new_m, open('/home/meghna/Hoax_PickleFiles2/'+str(storyid)+'.pkl', 'wb'))
    pickle.dump(new_m2, open('/home/meghna/SegHoax_PickleFiles2/'+str(storyid)+'.pkl', 'wb'))
    pickle.dump(new_m3, open('/home/meghna/SEIZ_PickleFiles2/'+str(storyid)+'.pkl', 'wb'))
    pickle.dump(new_m4, open('/home/meghna/DoubleSIR_PickleFiles2/'+str(storyid)+'.pkl', 'wb'))
    fig.savefig('/home/meghna/forked_repo_figures3/story  ' + str(storyid)+ '.pdf', dpi=300, facecolor='w', edgecolor='w', orientation='portrait', format=None, transparent=False, bbox_inches='tight')




