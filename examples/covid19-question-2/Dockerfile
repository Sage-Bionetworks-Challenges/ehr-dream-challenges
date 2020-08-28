FROM python:3.5

# Do not change
LABEL challenge="covid19"

# Enable training
LABEL enable_training=true

# Description of the model (max 500 characters)
LABEL description="hospitalization  baseline prediction"

# Comma-separated list of arbitrary feature names used by the model in desc
# order of importance.
LABEL ranked_features="age,gender,race"

# Comma-separated list of references (URL)
LABEL references=""

# Install dependencies
RUN pip install pandas \
  numpy \
  sklearn \
  datetime \
  joblib

# Move to the app folder
RUN mkdir /app
WORKDIR /app

# Copy our python program for training and inference
COPY src/train.py .
COPY src/infer.py .

# Copy Bash scripts expected by the IT infrastructure of the EHR DREAM Challenge
COPY train.sh .
COPY infer.sh .


# Add executable permission to Bash scripts
RUN chmod +x train.sh
RUN chmod +x infer.sh
