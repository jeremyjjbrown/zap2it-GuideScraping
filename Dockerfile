FROM python

COPY app.py app.py
COPY zap2it.py zap2it.py
COPY madison.ini madison.ini
COPY milwaukee.ini milwaukee.ini
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
