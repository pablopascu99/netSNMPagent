FROM python

WORKDIR /consumer

COPY ./consumer/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-u", "./consumer/consumer.py"]