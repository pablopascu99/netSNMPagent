from confluent_kafka import Consumer
import json
import psycopg2

c = Consumer({'bootstrap.servers':'kafka1:19091','group.id':'counting-group','auto.offset.reset':'earliest'})
print('Kafka Consumer has been initiated...')

#print('Available topics to consume: ', c.list_topics().topics)
c.subscribe(['snmptrap-tracker'])

#establishing the connection
conn = psycopg2.connect(database="postgres", user='postgres', password='postgres', host='postgres', port= '5432')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

sql= '''CREATE TABLE IF NOT EXISTS snmpTraps (
    ID SERIAL PRIMARY KEY,
    IPSource VARCHAR (255),
    Version VARCHAR (255),
    MIB VARCHAR (255),
    Type VARCHAR (255),
    AdditionalInfo JSON,
    Datetime VARCHAR (255)
)'''

cursor.execute(sql)
conn.commit()
def main():

    while True:
        msg=c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        #Setting auto commit false
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        data = json.loads(msg.value().decode('utf-8'))
        print(data)
        additionalInfoJson=json.dumps(data['AdditionalInfo'])
        print(type(additionalInfoJson))
        cursor.execute(""" INSERT INTO snmpTraps (IPSource, Version, MIB, Type, AdditionalInfo, Datetime) VALUES (%s,%s,%s,%s,%s,%s)""",
            (data['IPSource'],
             data['Version'],
             data['MIB'],
             data['Type'],
             additionalInfoJson,
             data['Datetime']))

main()