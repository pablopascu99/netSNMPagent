FROM elcolio/net-snmp

WORKDIR /agent

COPY . .

CMD [ "python", "-u", "./agent/trapAgent.py"]