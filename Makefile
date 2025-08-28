
create_env : 
	pyenv virtualenv penguins 
	pyenv local penguins

install_deps : 
	pip install -e . 

mlflow : 
	@echo "Starting MLflow UI..."
	mlflow ui

allow_direnv : 
	direnv allow .

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