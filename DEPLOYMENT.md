# Build and deployment instructions

The project is hosted on GCP in the region us-central1:
- Docker images are stored using Artifact Registry
- The PostgreSQL database is hosted using Cloud SQL
- The Redis instance is hosted using Memory Store

The current build and deployment process is currently manual and can be improved.

## Steps

### Set up gcloud CLI locally

Download the `gcloud` CLI tool and run `gcloud init` to set up the credentials locally.

### Build Docker images

Build new Docker images for the Django app and Celery worker by running:
```bash
scripts/build-docker-images.sh <image-tag>
```
For example, to build new images for version `0.2.0`, you would run `scripts/build-docker-images.sh v0.2.0`. The image tag should follow semver.

This scripts will generate a `requirements.txt` file using Poetry, this file will not be checked into git.
It will then be used to install the dependencies in the Docker images.

### Pushing the Docker images

Run `scripts/push-docker-images.sh <image-tag>`. Use the same image tag as in the build step.

### Deploy the Django app and Celery worker

TBD
