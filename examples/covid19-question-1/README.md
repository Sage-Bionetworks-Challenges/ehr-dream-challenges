# Example model for COVID-19 DREAM Challenge: Question 1

## Overview

Here we describe how to build and run locally an example model provided for Challenge Question 1 of the [COVID-19 DREAM Challenge](https://www.synapse.org/#!Synapse:syn18404605). The goal of this continuous benchmarking project is to develop models that take as input the electronic health records (EHRs) of a patient and outputs the probability of this patient to be tested positive for COVID-19.

## Description of the model

This example model takes 13 features including clinical symptoms and vital signs, and refers to research conducted by [Feng et al.](https://www.medrxiv.org/content/10.1101/2020.03.19.20039099v1)
Each patient is given a risk score of being COVID-19 positive based on the presence of the 13 features. A threshold of risk score is chosen basing on 10% test positive rate in Washington state. Patients whose risk scores are above threshold are assigned test-positive probability as 1, otherwise 0. Note that this model has not been trained on any real COVID patient data.

| Feature|OMOP Code|Domain|Threshold|
|-|-|-|-|
|age|-|person|>60|
|temperature|3020891|measurement|>37.5'|
|heart rate|3027018|measurement|>100n/min|
|diastolic blood pressure|3012888|measurement|>80mmHg|
|systolic blood pressure|3004249|measurement|>120mmHg|
|hematocrit|3023314|measurement|>52|
|neutrophils|3013650|measurement|>8|
|lymphocytes|3004327|measurement|>4.8|
|oxygen saturation in artery blood|3016502|measurement|<95|
|cough|254761|condition|-|
|pain in throat|259153|condition|-|
|headache|378253|condition|-|
|fever|437663|condition|-|

When developing your own model, generate a continuous score between 0 and 1 for more fine-grained predictions.

## Dockerize the model

1. Start by cloning this repository.

2. Move to this example folder

3. Build the Docker image that will contain the move with the following command:

    ```bash
    docker build -t awesome-covid19-q1-model:v1 .
    ```

## Run the model locally on synthetic EHR data

1. Go to the page of the [synthetic dataset](https://www.synapse.org/#!Synapse:syn21978034) provided by the COVID-19 DREAM Challenge. This page provides useful information about the format and content of the synthetic data.

2. Download the file [synthetic_data.tar.gz](https://www.synapse.org/#!Synapse:syn22043931) to the location of this example folder (only available to registered participants).

3. Extract the content of the archive

    ```bash
    $ tar xvf synthetic_data.tar.gz
    x synthetic_data/
    x synthetic_data/procedure_occurrence.csv
    x synthetic_data/location.csv
    x synthetic_data/visit_occurrence.csv
    x synthetic_data/condition_era.csv
    x synthetic_data/device_exposure.csv
    x synthetic_data/drug_era.csv
    x synthetic_data/observation.csv
    x synthetic_data/goldstandard.csv
    x synthetic_data/drug_exposure.csv
    x synthetic_data/condition_occurrence.csv
    x synthetic_data/person.csv
    x synthetic_data/measurement.csv
    x synthetic_data/observation_period.csv
    ```

4. Create an `output` and `scratch` (optional) folders.

    ```bash
    mkdir output scratch
    ```

5. Run the dockerized model to generate predictions for the patients included in the synthetic dataset.

    ```bash
    docker run \
        -v $(pwd)/synthetic_data:/data:ro \
        -v $(pwd)/output:/output:rw \
        -v $(pwd)/scratch:/scratch:rw \
        awesome-covid19-q1-model:v1 bash /app/infer.sh
    ```

6. The predictions generated are saved to `output/predictions.csv`. The column `person_id` includes the ID of the patient and the column `test-positive` the probabily for the patient to be COVID-19 positive.

## Submit this model to the COVID-19 DREAM Challenge

This model meets the requirements for models to be submitted to Question 1 of the COVID-19 DREAM Challenge. Please see [this page](https://www.synapse.org/#!Synapse:syn21849256/wiki/601875) for instructions on how to submit this model.
