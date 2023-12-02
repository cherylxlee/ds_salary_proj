# -*- coding: utf-8 -*-
"""
@author: cherylee
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

# Load data from a CSV file
df = pd.read_csv('eda_data.csv')

# Display available columns in the dataframe
df.columns

# Select relevant columns for the model
df_model = df[['avg_salary','Rating','Size','Type of ownership','Industry','Sector','Revenue',
             'Job_State','age_of_company','python_yn','spark_yn','aws_yn', 
             'excel_yn','job_simp','seniority','desc_len']]

# Create dummy variables for the entire dataset
df_dum = pd.get_dummies(df_model, dummy_na=True)

for col in df_dum.columns:
    if df_dum[col].dtype == bool:
        df_dum[col] = df_dum[col].astype(int)

# Splitting data into training and testing sets
from sklearn.model_selection import train_test_split
X = df_dum.drop('avg_salary', axis =1).values
y = df_dum.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ensure both X_train and X_test have the same dummy variables
# This step is crucial to prevent column mismatch
X_train.shape, X_test.shape

# Multiple linear regression with statsmodels
import statsmodels.api as sm
X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

# Linear regression using scikit-learn
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

# Cross-validation for linear regression model
np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))

# Lasso regression
lm_l = Lasso(alpha=.13)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))

# Tuning the Lasso model by testing different alpha values
alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3)))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]

# Random forest regression
from sklearn.ensemble import RandomForestRegressor

# Initialize the Random Forest Regressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error', cv= 3))

from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('squared_error','absolute_error'), 'max_features':('sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3, error_score='raise')
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

# Testing ensemble predictions
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, tpred_rf)

# Combining predictions and calculating mean absolute error
mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)

# Saving the model using pickle
import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

# Load the saved model
file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

# Make a prediction with the loaded model
model.predict(np.array(list(X_test[1,:])).reshape(1,-1))[0]

# Extracting the features for a specific test instance
list(X_test[1,:])
