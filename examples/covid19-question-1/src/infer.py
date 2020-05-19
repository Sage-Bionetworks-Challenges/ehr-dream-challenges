import datetime as dt
import numpy as np
from datetime import date
import pandas as pd

measurement = pd.read_csv('/data/measurement.csv')
measurement_feature = {'3020891':37.5,'3027018':100,'3012888':80,'3004249':120,
'3023314':52,'3013650':8,'3004327':4.8,'3016502':95}
measurement = measurement.dropna(subset=['measurement_concept_id'])
measurement =measurement.astype({"measurement_concept_id": int})
measurement =measurement.astype({"measurement_concept_id": str})
feature = dict()
'''
 measurement
| Feature|OMOP Code|Domain|Notes|
|-|-|-|-|
|age|-|person|>60|
|temperature|3020891|measurement|>37.5'|
|heart rate|3027018|measurement|>100n/min|
|diastolic blood pressure|3012888|measurement|>80mmHg|
|systolic blood pressure|3004249|measurement|>120mmHg|
|hematocrit|3023314|measurement|>52|
|neutrophils|3013650|measurement|>8|
|lymphocytes|3004327|measurement|>4.8|
|oxygen saturation in artery blood|3016502|measurement|<95%|
'''
for i in measurement_feature.keys():
    subm = measurement[measurement['measurement_concept_id']==i]
    if i != '3016502':
        subm_pos = subm[subm['value_as_number'] > measurement_feature[i]]
        feature[i] = set(subm_pos.person_id)
    else:
        subm_pos = subm[subm['value_as_number'] < measurement_feature[i]]
        feature[i] = set(subm_pos.person_id)

'''
condition
| Feature|OMOP Code|Domain|Notes|
|-|-|-|-|
|cough|254761|condition|-|
|pain in throat|259153|condition|-|
|headache|378253|condition|-|
|fever|437663|condition|-|
'''
condition_feature = ['254761','437663','378253','259153']
condition = pd.read_csv("./condition_occurrence.csv")
condition = condition.dropna(subset=['condition_concept_id'])
condition = condition.astype({"condition_concept_id": int})
condition = condition.astype({"condition_concept_id": str})
for i in condition_feature:
    subm = condition[condition['condition_concept_id']==i]
    feature[i] = set(subm.person_id)
person = pd.read_csv('./person.csv')
today = date.today().year
person['age']= person['year_of_birth'].apply(lambda x: today - x )
sub = person[person['age']>60]
feature['age'] = set(sub.person_id)

'''generate the feature set'''
person = person.drop_duplicates(subset = ['person_id'])
person_index = dict(zip(person.person_id, range(len(person.person_id))))
feature_index = dict(zip(feature.keys(), range(len(feature.keys()))))
index_feat_matrix = np.zeros((len(person_index), len(feature_index)))
for i in feature.keys():
    index_f = feature_index[i]
    for person_id in feature[i]:
        index_p = person_index[person_id]
        index_feat_matrix[index_p,index_f]=1
score = index_feat_matrix.sum(axis = 1)
top_ratio = 0.07
top_index = (-score).argsort()[:int(score.shape[0]*top_ratio)]
top_index_list = list(top_index)
top_person = []
person_index_inv = {v:k for k,v in person_index.items()}
for i in top_index_list:
    top_person.append(person_index_inv[i])

predictions = pd.DataFrame(list(person_index.keys()), columns = ['person_id'])
predictions['score'] = np.zeros(predictions.shape[0])
for i in top_person:
    predictions.loc[predictions['person_id']==i , 'score']=1
predictions.to_csv('/output/predictions.csv', index = False)
