FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 162

CMD [ "python", "-u", "snmpGet.py"]