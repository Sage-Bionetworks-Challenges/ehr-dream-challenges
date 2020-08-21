# Example model for COVID-19 DREAM Challenge: Question 2

## Overview

Here we describe how to build and run locally an example model provided for Challenge Question 2 of the [COVID-19 DREAM Challenge](https://www.synapse.org/#!Synapse:syn18404605). The goal of this continuous benchmarking project is to develop models that take as input the electronic health records (EHRs) of a patient and outputs the probability of a COVID-19-positive patient to be hospitalized within 21 day after his/her recent COVID-measurement.

## Description of the model

This example model takes three basic demographics features include age, gender and race. First, we generate a feature set for each patient in the `/data` folder using the demographics feature and then we apply a 10-fold cross-validation logistic regression model on the feature set. Once the model is trained, we save the model file in the `/model`folder.

During the inference stage, we create a feature matrix using the same set of demographics features. Then we load the trained model and apply the model on the feature matrix to generate a prediction file as `/output/predictions.csv`



## Dockerize the model

1. Start by cloning this repository.

2. Move to this example folder

3. Build the Docker image that will contain the move with the following command:

    ```bash
    docker build -t awesome-covid19-q2-model:v1 .
    ```

## Run the model locally on synthetic EHR data

1. Go to the page of the [synthetic dataset](https://www.synapse.org/#!Synapse:syn21978034) provided by the COVID-19 DREAM Challenge. This page provides useful information about the format and content of the synthetic data.

2. Download the file [synthetic_data.tar.gz](https://www.synapse.org/#!Synapse:syn22043931) to the location of this example folder (only available to registered participants).

3. Extract the content of the archive

    ```bash
    $ tar xvf synthetic_data.tar.gz
    x synthetic_data/
    x synthetic_data/training
    x synthetic_data/evaluation
    ```

4. Create an `output` , `model` and `scratch` (optional) folders.

    ```bash
    mkdir output scratch model
    ```

5. Run the dockerized model to train on the patients in the training dataset.

    ```bash
    docker run \
        -v $(pwd)/synthetic_data/training:/data:ro \
        -v $(pwd)/output:/output:rw \
        -v $(pwd)/scratch:/scratch:rw \
        -v $(pwd)/model:/model:rw \
        awesome-covid19-q2-model:v1 bash /app/train.sh
    ```

6. Run the trained model on evaluation dataset and generate the prediction file.

    ```bash
    docker run \
        -v $(pwd)/synthetic_data/evaluation:/data:ro \
        -v $(pwd)/output:/output:rw \
        -v $(pwd)/scratch:/scratch:rw \
        -v $(pwd)/model:/model:rw \
        awesome-covid19-q2-model:v1 bash /app/infer.sh
    ```

7. The predictions generated are saved to `/output/predictions.csv`. The column `person_id` includes the ID of the patient and the column `score` the probability for the COVID-19-positive patient to be hospitalized within 21 days after the latest COVID test.

    ```text
    $ cat output/predictions.csv
    person_id,score
    0,0.6153846153846154
    1,0.5384615384615384
    2,0.5384615384615384
    3,0.3076923076923077
    ...
    ```

## Submit this model to the COVID-19 DREAM Challenge

This model meets the requirements for models to be submitted to Question 2 of the COVID-19 DREAM Challenge. Please see [this page](https://www.synapse.org/#!Synapse:syn21849255/wiki/602419) for instructions on how to submit this model.
