
create_env : 
	pyenv virtualenv penguins 
	pyenv local penguins

install_deps : 
	pip install -e . 

mlflow : 
	@echo "Starting MLflow UI..."
	mlflow ui

fastapi :
	uvicorn api.fast:my_api --host 0.0.0.0 --port 8000 --reload

allow_direnv : 
	direnv allow .

#############################################################################################################################################

#								Deployment

#############################################################################################################################################

run_api_docker : 
	docker build -t ${API_IMAGE_NAME} -f Dockerfile-api .
	docker run  -p 8000:8000  ${API_IMAGE_NAME}

push_api : 
	docker build --platform=linux/amd64 -t ${REPO_REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPOSITORY}/${API_IMAGE_NAME} -f Dockerfile-api .
	docker push ${REPO_REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPOSITORY}/${API_IMAGE_NAME}

#############################################################################################################################################

#								Docker

#############################################################################################################################################

launch:
	docker-compose up -d

# mlflow_docker: 
# 	docker run --platform linux/amd64 -d --name mlflow-container -e TZ=UTC -p 5000:5000 ubuntu/mlflow:2.1.1_1.0-22.04

# mlflow_docker_build: 
# 	docker build -t mlflow-local -f Dockerfile-mlflow .

# mlflow_docker_run : mlflow_docker_build	
# 	echo "🔥 MLflow container is running... 🔥"
# 	docker run -d --name mlflow-container --env-file .env -p ${MLFLOW_PORT}:${MLFLOW_PORT} mlflow-local

# prefect_docker_build :
# 	docker build -t prefect-local -f Dockerfile-prefect .

# prefect_docker_run : prefect_docker_build
# 	docker run -d --name prefect-container  -p 4200:4200 prefect-local

# run_all : mlflow_docker_run prefect_docker_run
# 	@echo "🔥 All System ready... 🔥"

# clean:
# 	docker stop mlflow-container prefect-container
# 	docker rm mlflow-container prefect-container
# 	docker rmi mlflow-local prefect-local