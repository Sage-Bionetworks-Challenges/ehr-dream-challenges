# EHR DREAM Challenge: Baseline Model
## Overview
This repository describes how to build and run locally the
baseline model of the [EHR DREAM Challenge: Patient Mortality Prediction](https://www.synapse.org/#!Synapse:syn18404605). The goal of this [DREAM Challenge](http://dreamchallenges.org/) is to develop models that take as input the electronic health records (EHRs) of a patient and outputs the probability that this patient will die within 6 months after a given Prediction Date (PD).

## Description of the model
This baseline model uses a logistic regression approach to predict whether the patient will die in the next DeltaT days after the Prediction Date (PD). The model only uses three features from the demographic data: the age (on the PD), gender and ethnicity of the patient.

## Dockerize the model

1. Clone this GitHub repository
2. `docker build -t docker.synapse.org/syn12345/my_model:v0.1 example/app`

## Run the baseline model locally on synthetic data
This section describes how to train and evaluate the performance of the model locally, that is, without using the IT infrastructure of the [EHR DREAM Challenge: Patient Mortality Prediction](https://www.synapse.org/#!Synapse:syn18404605).

### Description of the data
[Learn more about OMOP Synpuf data](https://www.synapse.org/#!Synapse:syn18405992/wiki/594233)

### Download the data
[The Synpuf data are available here](https://www.synapse.org/#!Synapse:syn20685954). After downloading them, uncompress the archive and place the data folder where it can later be accessed by the dockerized model (see below).

### Train the model locally on Synpuf data
Once the baseline model has been dockerized (see above), run the following command to train the model on Synpuf data:

```
docker run -v <path to train folder>:/train:ro
-v <path to scratch folder>:/scratch:rw
-v <path to model folder>:/model:rw  docker.synapse.org/syn12345/my_model:v0.1 bash /app/train.sh
```

where

- `<path to train folder>` is the absolute path to the training data (e.g. `/home/charlie/ehr_experiment/synpuf_data/train`).
- `<path to scratch folder>` is the absolute path to the scratch folder (e.g. `/home/charlie/ehr_experiment/scratch`).
- `<path to model folder>` is the absolute path to where the trained model will be exported (e.g. `/home/charlie/ehr_experiment/model`))

### Predict the mortality status of patients

Run the following command to generate mortality status predictions for a group of XXX patients whose data are stored in the folder `synpuf/infer`.


```
docker run -v <path to infer folder>:/infer:ro
-v <path to scratch folder>:/scratch:rw
-v <path to output folder>:/output:rw
-v <path to model folder>:/model:rw
docker.synapse.org/syn12345/my_model:v0.1 bash /app/infer.sh
```

where

- `<path to infer folder>` is the absolute path to the inference data (e.g. `/home/charlie/ehr_experiment/synpuf_data/infer`).
- `<path to output folder>` is the absolute path to where the prediction file will be saved.

If the docker model runs successfully, the prediction file `predictions.csv` file will be created in the output folder. This file has two columns: 1) person_id and 2) 6-month mortality probability. Note: make sure the column 2) contains no NA and the values are between 0 and 1.


## Build your own docker model  


## Preparation
We suggest EHR DREAM challenge participants to prepare two scripts: train.py and infer.py.
train.py is for building a prediction model and infer.py is for generating predictions using the model; two bashfiles: train.sh and infer.sh for running train.py and infer.py.

*An example of script is:*
```
import pandas as pd
from joblib import load

input_df = pd.read_csv('/train/person.csv')
model = load('/model/baseline.joblib')
scores = model.predict_proba(input_df)[:,1]
output_df.to_csv( '/output/predictions.csv')

```


*An example of bashfile is:*
```
#!/usr/bin/env bash

python /app/train.py

```
*notice:* participants can also name their scripts differently as train.py and infer.py, and can have multiple scripts for the training and predicting purposes, but they will need to specify in the train.sh which scripts to run for training models and in the infer.sh which scripts to run for generating predictions.

## Docker container structure

A docker container is built basing on the docker images submitted by participants. The illustration below shows the structure of a docker container.

![docker container structure](./pics/docker_container_structure.png)


"app" directory is created by participants in which scripts for building prediction models (train.py), generating predictions (infer.py) and bashfiles to run those scripts (train.sh and infer.sh) live. Information to build "app" directory is in the dockerfile.

Other directories ("train","infer","scratch","model","output") will be mounted to the docker container by Synapse later. Participants don't need to create those directories but need to know the location of different directories in the container to access and store data.

Omop data inside "train" directory are provided to participants for building the models. Predictions are generated by applying models to omop data in the "infer" directory.  Omop data inside "train" and "infer" directories have the same tables and formats as synpuf data except there is no death.csv file  in "infer" directory."scratch" directory is used to store intermediate files(e.g. selected features)
"model" directory is used to store the model."output" directory is used to store the prediction generated from the "infer" omop data.


## Create a docker image
Put dockerfile, train.sh, train.py, infer.sh, infer.py in the same direcotory and run the command below:
```
docker build -t docker.synapse.org/syn12345/my_model:v0.1 <path to the dockerfile>
```
[Learn more about building docker images](https://docs.docker.com/get-started/)
## Submission to synapse platform
Log in Synapse
```
docker login -u <synapse username> -p <synapse password> docker.synapse.org
```
After logging in, view docker images and decide which ones to push into the registry.
```
docker images
#REPOSITORY                                 TAG                 IMAGE ID            CREATED             SIZE
#docker.synapse.org/syn12345/mytestrepo   version1            f8d79ba03c00        6 days ago          126.4 MB
#ubuntu                                     latest              f8d79ba03c00        6 days ago          126.4 MB
#docker.synapse.org/syn12345/my-repo	latest	df323sdf123d	2 days ago	200.3 MB
```
Push the docker image to Synapse platform.
```
docker push docker.synapse.org/syn12345/my_model:v0.1
```
[Learn more about submitting images to Synapse platform](https://docs.synapse.org/articles/docker.html)
