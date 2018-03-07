#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 16:14:45 2018

@author: laisy
"""

import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import matplotlib.pyplot as plt

feb_23 = pd.read_csv(, index_col = 0)
feb_10To22 = pd.read_csv(, index_col = 0)
jan30_to_feb10 = pd.read_csv(, index_col = 0)
historic_data_concat = pd.concat([jan30_to_feb10, feb_10To22], ignore_index=True)
print(feb_10To22.head())
print(feb_23.head())

ltc_dtr = DecisionTreeRegressor(random_state=0)
print(cross_val_score(ltc_dtr, feb_10To22[:], feb_23[:], cv=10))

print('')
x_train = historic_data_concat[['Time', 'Low', 'High', 'Open', 'Volume']].values
y_train = historic_data_concat['Close'].values
print(x_train[0:10])
    
ltc_dtr.fit(x_train, y_train)

x_test = feb_23[['Time', 'Low', 'High', 'Open', 'Volume']].values
y_actual = feb_23['Close'].values
#print(ltc_dtr.predict(x_test))

ltc23_predictions = ltc_dtr.predict(x_test)
ltc23_diff = []
for index, value in enumerate(ltc23_predictions):
    ltc23_diff.append(feb_23['Close'][index] - value)

#print(ltc23_diff)
#print('')
print(np.average(ltc23_diff), np.max(ltc23_diff), np.min(ltc23_diff))
print(np.average(y_actual), np.max(y_actual), np.min(y_actual))

line_colors = ['b', 'g', 'c', 'm', 'y','b', 'g', 'c', 'm', 'y']
fig = plt.figure(figsize=(10,10))
#list_axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
fig_position = [331, 332, 333, 334, 335, 336, 337, 338, 339]

for depth in range(1,10):
    loop_tree = DecisionTreeRegressor(max_depth = depth, random_state=0)
    if loop_tree.fit(x_train, y_train).tree_.max_depth < depth:
        break
    score = np.mean(cross_val_score(loop_tree, x_train, y_train, cv=10))
#    current_ax = list_axes[-1 + depth]
    current_ax = fig.add_subplot(fig_position[-1 + depth])
    
    current_ax.plot(feb_23.index.values, loop_tree.predict(x_test), 
                    c=line_colors[-1 + depth])

    print('Depth: ', depth, ' Accuracy: ', score)
plt.show()
    
#print(feb_23.index.values)
    
plt.plot(feb_23.index.values,y_actual, c='r')
plt.plot(feb_23.index.values, ltc23_predictions, c='b')
plt.show()

plt.plot(historic_data_concat.index.values, historic_data_concat['Close'].values)
plt.show()

#print(historic_data_concat.index.values)