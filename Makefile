ROOT_DIR = $(CURDIR)
SOURCE_DIR = $(CURDIR)

MANAGER = python3 $(SOURCE_DIR)/manage.py
#VENV = . $(ROOT_DIR)/.env/bin/activate;
SUPERVISOR = sudo supervisorctl

# Clean project
.PHONY : clean
clean:
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete

.PHONY : static
static:
	$(MANAGER) collectstatic --noinput

.PHONY : pip
pip:
	pip3 install -r $(ROOT_DIR)/requirements.txt

.PHONY : migrate
migrate:
	$(MANAGER) migrate --noinput

.PHONY : makemigrations
makemigrations:
	$(MANAGER) makemigrations --noinput

.PHONY : runserver
runserver:
	$(MANAGER) runserver 127.0.0.1:8170

.PHONY : reload
reload:
	cd $(ROOT_DIR) ; sudo supervisorctl restart smm_dj; sudo supervisorctl restart smm_worker
	#cd $(ROOT_DIR) ; touch reload

# Update instance
.PHONY : update
update: pip migrate static reload
