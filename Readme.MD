
### Running with python
Use the following commands to run the application using python

> 1. Setup virtual environment - `python3 -m venv env`
> 2. Activate virtual environment in env folder - `source env/bin/activate`
> 3. Check python version and folder where dependencies will be run from - `which python`
> 4. Install dependencies - `pip install -r requirements.txt`
> 5. Set environment variables
    > `export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"`
    >  run `gcloud auth application-default login` to set ADC (application default credentials) if you wish to no use a key 
    > `export TABLE="useful-circle-358120.log_sink.cloudaudit_googleapis_com_activity_20231122"` 
    > `export BUCKET="bigquery-test-chainomi-2023"`

> 6. Run application - `python3 app.py`
## Docker run

From root folder
>1. Build container - `docker build -t bigq-gcp-sb .`
>2. Login to google to get ADC (application default credentials) into ~/.gcloud/config - `gcloud auth application-default login` 
>3. Docker run - 

    `docker run  \
    -v ~/.config/gcloud:/home/app-user/.config/gcloud \
    -e TABLE="useful-circle-358120.log_sink.cloudaudit_googleapis_com_activity_20231122" \
    -e GOOGLE_PROJECT="useful-circle-358120" \
    -e GCP_PROJECT=useful-circle-358120
    -e SLACK_BOT_TOKEN=xxxx \
    bigq-gcp-sb`

docker run  \
-v ~/.config/gcloud:/home/app-user/.config/gcloud \
-e TABLE="useful-circle-358120.log_sink.cloudaudit_googleapis_com_activity_20231122" \
-e GOOGLE_CLOUD_PROJECT=useful-circle-358120 \
-e SLACK_BOT_TOKEN=xxxx \
bigq-gcp-sb

docker run  \
-e TABLE="useful-circle-358120.log_sink.cloudaudit_googleapis_com_activity_20231122" \
-e GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token --impersonate-service-account=big-query-sql-sa@useful-circle-358120.iam.gserviceaccount.com) \
-e SLACK_BOT_TOKEN=xxxx \
bigq-gcp-sb


## Deploy to cluster

### docker tag & push
1. gcloud login - `gcloud auth login`
2. set project - `gcloud config set project <project id>`
3. add docker credentials to $HOME/.docker/config.json - `gcloud auth configure-docker`
https://cloud.google.com/container-registry/docs/advanced-authentication

1. Tag image - `docker tag bigq-gcp-sb gcr.io/useful-circle-358120/bigq-gcp-sb:v1`
2. Push image - `docker push gcr.io/useful-circle-358120/bigq-gcp-sb:v1`

### setup workload identity
---
## Apply kubernetes resources
From root folder
1. Connect to cluser - `gcloud container clusters get-credentials <cluster-name> --region us-central1 --project <project_id>`
2. Apply resources - `kube`
connect to cluster
install gke-gcloud-auth-plugin - https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke







ubuntu - sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
windows - 

gcloud container clusters get-credentials big-query-sql-cluster --region us-central1 --project useful-circle-358120

gcloud container clusters get-credentials <cluster-name> --region <region> --project <project-id>

windows install - https://cloud.google.com/sdk/docs/downloads-interactive

Slack push

pdf dependency - sudo apt install wkhtmltopdf

slack instructions - https://api.slack.com/tutorials/uploading-files-with-python
invite bot to channel
/invite @BOTNAME
export SLACK_BOT_TOKEN=xxxxxxx
https://api.slack.com/apps/A06837LUGJD/oauth



From root folder
docker build -t bigq-gcp-sb .


The not so proper way - had to add key to dockerfile because i could not do a volume mount on WSL ubuntu
docker run  \
-e GOOGLE_APPLICATION_CREDENTIALS="useful-circle-358120-5ebbc15b4e95.json" \
-e TABLE="useful-circle-358120.log_sink.cloudaudit_googleapis_com_activity_20231122" \
-e BUCKET="bigquery-test-chainomi-2023" \
bigq-gcp-sb


docker run  \
-e GOOGLE_APPLICATION_CREDENTIALS=$(cat useful-circle-358120-5ebbc15b4e95.json) \
-e TABLE="useful-circle-358120.log_sink.cloudaudit_googleapis_com_activity_20231122" \
-e BUCKET="bigquery-test-chainomi-2023" \
bigq-gcp-sb



Proper way

docker run  \
-v $(pwd)/key:/tmp/keys/useful-circle-358120-5ebbc15b4e95.json:ro \
-e GOOGLE_APPLICATION_CREDENTIALS="/tmp/keys/useful-circle-358120-5ebbc15b4e95.json" \
-e TABLE="useful-circle-358120.log_sink.cloudaudit_googleapis_com_activity_20231122" \
-e BUCKET="bigquery-test-chainomi-2023" \
bigq-gcp-sb




