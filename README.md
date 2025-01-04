# hivebox

## Purpose
This API aggregates and provides an average temparature from the [OpenSenseMap API](https://api.opensensemap.org/) and is limited to a bounding box which roughly encompasses Washington state.

## Usage
### Routes
- `/version`: returns the current application version
- `/temperature`: returns the average temperature over the last hour

## Running locally
### FastAPI
To run this API locally, navigate to `src` and run `fastapi dev` from a command-line. By default this will launch a FastAPI instance at <http://127.0.0.1:8000>.

### Docker Build
#### Build and run the image locally
1 - Go to the root directory and run `docker build . -f .Dockerfile -t hivebox:local` (replace the `local` tag with something else if desired)

2 - Run `docker run -p 8000:8000 hivebox:local`

3 - Navigate to <http://127.0.0.1:8000> to view the running container's API.


#### Docker run from Docker Hub
1 - Go to the root directory and run `docker run --name hivebox -p 8000:8000 darianhuotari/hivebox-integration-api:latest`

2 - Navigate to <http://127.0.0.1:8000> to view the running container's API.

## Testing:
[Hadolint](https://github.com/hadolint/hadolint) is used to lint the Dockerfile.

[Pytest](https://docs.pytest.org/en/stable/) and [Codecov](https://docs.codecov.com/docs/code-coverage-with-python) are used for testing. 

To run only `pytest` locally, navigate to the root directory and run `pytest`.

To run both `codecov` and `pytest` locally, navigate to the root directory and run `pytest --cov`.

Hadolint automatically runs in the CI pipeline when changes to the dockerfile are detected. Pytest / Codecov are automatically run on PRs.