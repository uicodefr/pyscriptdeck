VERSION=$(shell sed "s/^    version=\"\(.*\)\",/\1/;t;d" setup.py)
NEXUS_USER=deployment
DOCKER_URL=docker.uicode.dev
PYPI_URL=https://nexus.uicode.dev/repository/pypi-hosted/

DOCKER_IMG_NAME=pyscriptdemo

all:
	@echo "do nothing (version: $(VERSION))"

test:
	pip install -r requirements.txt -U
	pip install -r requirements-test.txt -U
	pytest

build:
	pip install -r requirements.txt -U
	pip install twine -U
	python setup.py clean sdist
	twine upload dist/* --repository-url $(PYPI_URL) -u $(NEXUS_USER) -p $$NEXUS_PASSWORD

containerize_demo:
	echo $$NEXUS_PASSWORD | docker login --username $(NEXUS_USER) --password-stdin $(DOCKER_URL)
	docker build --tag $(DOCKER_IMG_NAME):$(VERSION) --tag $(DOCKER_IMG_NAME):latest ./
	docker tag $(DOCKER_IMG_NAME) $(DOCKER_URL)/$(DOCKER_IMG_NAME):$(VERSION)
	docker push $(DOCKER_URL)/$(DOCKER_IMG_NAME):$(VERSION)
