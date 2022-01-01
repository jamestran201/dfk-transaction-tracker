# Build and deployment instructions

The current build and deployment process is currently manual and can be improved.

## Steps

### Build Docker images

Build new Docker images for the Django app and Celery worker by running:
```bash
scripts/build-docker-images.sh <account> <image-tag>
```

For example, to build new images for version `0.2.0`, you would run `scripts/build-docker-images.sh <docker-hub-account> v0.2.0`. The image tag should follow semver.

The `<account>` argument should be your account name in the Docker registry you're using.

### Pushing the Docker images

1. Log in to the Docker registry that you are using

2. Run `scripts/push-docker-images.sh <account-name> <image-tag>`. Use the same account name and image tag as in the build step.

### Deploy the Django app and Celery worker

TBD
