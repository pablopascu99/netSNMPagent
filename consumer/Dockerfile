FROM python

WORKDIR /consumer

COPY ./consumer/requirements.txt .
COPY ./consumer/mibs /usr/share/snmp/mibs
COPY ./consumer/mibs /usr/share/mibs

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /usr/share/snmp/mibs
RUN chmod +x /usr/share/mibs
EXPOSE 162

CMD [ "python", "-u", "./consumer/consumer.py"]