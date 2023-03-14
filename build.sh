set -o errexit

pip install -r requirements.txt
python -m spacy download es_core_news_md

python manage.py collectstatic --no-input
python manage.py migrate