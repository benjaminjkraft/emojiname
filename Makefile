deps:
	pip install -r requirements.txt

deploy: deps
	pip install -t lib -r requirements.txt
	gcloud app deploy --promote --stop-previous-version --project emojihunt-names
