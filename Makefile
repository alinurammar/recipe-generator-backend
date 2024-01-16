backend-run:
	python app.py
requirements:
	pip install -r requirements.txt
deploy:
	git push heroku main
