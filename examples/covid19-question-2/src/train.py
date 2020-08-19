import datetime
import pandas as pd
import numpy as np
from datetime import datetime
'''for implementing simple logisticregression'''
import sklearn
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
'''for saving models'''
from joblib import dump

def add_COVID_measurement_date():
    measurement = pd.read_csv("/data/measurement.csv",usecols =['person_id','measurement_date','measurement_concept_id','value_as_concept_id'])
    measurement = measurement.loc[measurement['measurement_concept_id']==706163]
    measurement = measurement.loc[(measurement['value_as_concept_id']==45877985) &(measurement['value_as_concept_id']==45884084)]
    measurement = measurement.sort_values(['measurement_date'],ascending=False).groupby('person_id').head(1)
    covid_measurement = measurement[['person_id','measurement_date']]
    return covid_measurement

def add_demographic_data(covid_measurement):
    '''add demographic data including age, gender and race'''
    person = pd.read_csv('/data/person.csv',usecols = ['person_id','gender_concept_id','year_of_birth','race_concept_id'])
    demo = pd.merge(covid_measurement,person,on=['person_id'], how='inner')
    demo['measurement_date'] = pd.to_datetime(demo['measurement_date'], format='%Y-%m-%d')
    demo['year_of_birth'] = pd.to_datetime(demo['year_of_birth'], format='%Y')
    demo['age'] = demo['measurement_date'] - demo['year_of_birth']
    demo['age'] = demo['age'].apply(lambda x: x.days/365.25)
    print("****",flush = True)
    print(demo,flush = True)
    print("patients' ages are calculated", flush = True)
    person["count"] = 1
    gender = person.pivot(index = "person_id", columns="gender_concept_id", values="count")
    gender.reset_index(inplace = True)
    gender.fillna(0,inplace = True)
    race = person.pivot(index ="person_id", columns="race_concept_id", values="count")
    race.reset_index(inplace = True)
    race.fillna(0,inplace = True)
    race = race[['person_id', 8516, 8515, 8527, 8552]]
    gender = gender[['person_id',8532]]
    print("patients' gender and race information are added", flush = True)
    scaler = MinMaxScaler(feature_range = (0, 1), copy = True)
    scaled_column = scaler.fit_transform(demo[['age']])
    demo = pd.concat([demo, pd.DataFrame(scaled_column,columns = ['scaled_age'])],axis=1)
    predictors = demo[['person_id','scaled_age']]
    predictors = predictors.merge(gender, on = ['person_id'], how = 'left')
    predictors = predictors.merge(race, on = ['person_id'], how = 'left')
    predictors.fillna(0,inplace = True)
    return predictors

def logit_model(predictors):
    '''
    apply logistic regression models for selected demographics features and use GridSearchCV to optimize parameters
    '''
    X = predictors.drop(['person_id'], axis = 1)
    #features = X.columns.values
    gs = pd.read_csv('/data/goldstandard.csv')
    result = predictors.merge(gs,on = ['person_id'], how ='left')
    result.fillna(0,inplace = True)
    X = np.array(X)
    Y = np.array(result[['status']]).ravel()
    clf = LogisticRegressionCV(cv = 20, penalty = 'l2', tol = 0.0001, fit_intercept = True, intercept_scaling = 1, class_weight = None, random_state = None,
    max_iter = 100, verbose = 0, n_jobs = None).fit(X,Y)
    dump(clf, '/model/baseline.joblib')
    print("Training stage finished", flush = True)

if __name__ == '__main__':
    covid_measurement = add_COVID_measurement_date()
    predictors = add_demographic_data(covid_measurement)
    logit_model(predictors)
