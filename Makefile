
create_env : 
	pyenv virtualenv penguins 
	pyenv local penguins

install_deps : 
	pip install -r requirements.in