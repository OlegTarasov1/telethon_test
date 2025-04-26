FROM python

WORKDIR /tg_app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY /app .

CMD ["python3", "run.py"]