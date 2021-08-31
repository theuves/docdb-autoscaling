all: validate fmt

validate:
	terraform validate

fmt:
	terraform fmt -recursive