tf-sample-model
=================================


please add some text to describe me!


How to run locally:
-------------------

Create a gcp auth key:

```terminal
project_id=$(gcloud config list project --format='value(core.project)')
project_number=$(gcloud projects list --filter="name:${project_id}"  --format='value(project_number)')

gcloud iam service-accounts keys create ~/.ssh/$project_number-compute-sa-key.json --iam-account $project_number-compute@developer.gserviceaccount.com

mkdir -p secrets && cp ~/.ssh/$project_number-compute-sa-key.json secrets/creds.json

make airflow-run
```

__Note__: It is Highly advised to create a dedicated dev Service Account and not use this one. This was just a simple way to start.

launch the docker compose with: airflow, jupyter and mlflow services:

```terminal

make local-plateform-up
```

services UIs are accessible:

 - airflow: http://localhost:8080
 - mlflow: http://localhost:5000
 - jupyter: http://localhost:8081

you can launch and open tensorboard after a pipeline train run with:

```terminal

make open-tensorboard
```

