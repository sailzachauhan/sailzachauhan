
## Steps to deploy service in cloud run:
1. Update Dockerfile
2. Update cloudbuild.yml file
3. Create a repository in GAR i.e. artifact registry
4. Hit below cmd to create docker image through cloud build and push to GAR repo,

gcloud builds submit --config cloudbuild.yaml . \
--service-account="projects/hack-team-bank-the-unbanked/serviceAccounts/workload@hack-team-bank-the-unbanked.iam.gserviceaccount.com" \
--default-buckets-behavior=regional-user-owned-bucketcd ..

5. Then, create a service in Cloud run, make sure to create evrything in the same region and port number in cloud run app.py,dockerfile and service should match