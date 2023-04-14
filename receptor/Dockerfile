FROM python

WORKDIR /receptor

COPY ./receptor/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-u", "./receptor/snmpGet.py"]