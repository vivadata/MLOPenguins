
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