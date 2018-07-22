from __future__ import print_function, division
import os
import ot_helpers as ot
import query_graphs
from pprint import pprint
from IPython import display
from matplotlib import cm
from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

dir_script = os.path.dirname(os.path.realpath(__file__))
dir_queries = os.path.join(dir_script, './results/queries')
if not os.path.exists(dir_queries):
    os.makedirs(dir_queries)
#%%    
client = ot.get_client()
query_str = 'colorectal AND cancer'
print('query_str:'+ query_str)
results = ot.query(client, q=query_str, endpoint='trials')
print('{} {}'.format(results['total_count'], len(results['items'])))
#pprint(results['items'][:1])
f_pkl = os.path.join(dir_queries, '{}.pkl'.format(query_str))
ot.save_results(filename=f_pkl, results=results)
#%%
f_pkl = os.path.join(dir_queries, '{}.pkl'.format(query_str))
results = ot.load_results(filename=f_pkl)
locations=[]
years=[]
for item in results['items']:
    #print(item['locations'])
    if item['locations'] and item['registration_date']:
       #locations.append([this['name'] for this in item['locations']])
       locations.append(item['locations'][0]['name'])
       years.append(item['registration_date'].year)
#%%
locations=pd.Series(locations)
years=pd.Series(years)

trials=pd.DataFrame({'Registration year':years, 'Countries':locations})   
trials.hist('Registration year')
dummy=pd.get_dummies(trials['Countries'])
trials=pd.concat([trials['Registration year'],dummy],axis=1)
trials['count']=1
by_country=trials.groupby('Registration year').sum()
desc=by_country.describe()
mean=-desc.ix[1]
mean=mean.sort_values()
#%%
countries_toPlot=mean.index[1:7]
plt.figure(figsize=(13, 8))
  # Output a graph of loss metrics over periods.
plt.subplot(2, 1, 2)
plt.ylabel("Fraction")
plt.xlabel("Year")
plt.title("Fraction of total trials by country")
plt.tight_layout()
for country in countries_toPlot:
    plt.plot(by_country[country]/by_country['count'], label=country)
plt.xticks(np.arange(1999, 2018, 1.0))
plt.legend()
plt.subplot(2, 1, 1)
plt.ylabel("Trials")
plt.xlabel("Year")
plt.title("Colorectal cancer trials per year")
plt.tight_layout()
plt.plot(by_country['count'])
plt.xticks(np.arange(1999, 2018, 1.0))