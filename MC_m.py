# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 16:33:15 2019

@author: zeguang
"""

import smart_charing_model_m
import pandas as pd
import matplotlib.pyplot as plt

all_stat =pd.DataFrame(columns=['elec_norm','revenue_norm','acc_norm','rej_norm','elec_SC','revenue_SC','flex_SC','payback_SC','simutaneity','acc_SC','rej_SC'])

#monte carlo simulation
for i in range(100):
    
    all_stat.loc[i] = (smart_charing_model_m.run_EV_simulation())     
    #'elec_norm','revenue_norm','acc_norm','rej_norm','elec_SC','revenue_SC','flex_SC','payback_SC','simutaneity','acc_SC','rej_SC']    

key_stat = pd.DataFrame()
key_stat['elec_net'] = all_stat['elec_SC']-all_stat['elec_norm']
key_stat['flex_net'] = all_stat['flex_SC']
key_stat['flex_PB'] = all_stat['payback_SC']
key_stat['profit_net'] = all_stat['revenue_SC']-all_stat['revenue_norm'] - all_stat['payback_SC']

ax = plt.gca()

#key_stat.plot(kind='line', y='elec_net',ax=ax)
#key_stat.plot(kind='line', y='flex_net',color ='red',ax=ax)
#key_stat.plot(kind='line', y='flex_PB',color = 'green',ax=ax)
#key_stat.plot(kind='line', y='profit_net',color = 'black',ax=ax)
#plt.show()
all_stat['total_request']=(all_stat['rej_norm'] + all_stat['acc_norm'])
all_stat['accept_ratio_n']=all_stat['acc_norm']/(all_stat['rej_norm'] + all_stat['acc_norm'])
all_stat['accept_ratio_SC']=all_stat['acc_SC']/(all_stat['rej_SC'] + all_stat['acc_SC'])


print("mean value of monte carlo simulation: \n extra electricity sold (in kWh): " ,key_stat['elec_net'].mean(), "\n total flexibility (in kWh): ", key_stat['flex_net'].mean(),"\n flexibility payback (in Euro): ",key_stat['flex_PB'].mean(),"\n extra net profit (in Euro): ",key_stat['profit_net'].mean() )
print("\n electricity sold normal charging: ",all_stat['elec_norm'].mean(),"\n electricity sold smart charging: ",all_stat['elec_SC'].mean(),"simutaneity: ",all_stat['simutaneity'].mean() )

acc_rej_ratio_n = all_stat['acc_norm'].mean()/(all_stat['rej_norm'].mean()+all_stat['acc_norm'].mean())
acc_rej_ratio = all_stat['acc_SC'].mean()/(all_stat['rej_SC'].mean()+all_stat['acc_SC'].mean()) 


all_stat.plot(kind='line', y='accept_ratio_n',color = 'green',ax=ax)
all_stat.plot(kind='line', y='accept_ratio_SC',color = 'red',ax=ax)
#acc_rej_ratio_n.plot(label='Mean', linestyle='--',ax=ax)
plt.show()
print("avg accepted rate (nor)",acc_rej_ratio_n,"\n avg accepted rate (sc)",acc_rej_ratio )

