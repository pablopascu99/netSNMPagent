FROM python

WORKDIR /producer

COPY ./producer/requirements.txt .
COPY ./producer/mibs /usr/share/snmp/mibs
COPY ./producer/mibs /usr/share/mibs

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /usr/share/snmp/mibs
RUN chmod +x /usr/share/mibs
EXPOSE 162

CMD [ "python", "-u", "./producer/producer.py"]