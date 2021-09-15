import redis
from time import sleep

try:
    conn = redis.StrictRedis(
        host='redis-19196.c273.us-east-1-2.ec2.cloud.redislabs.com',
        port=19196,
        password='Hjc*H^kDzZuxV6@HiZYY#m6KefVCkz&kb%h5gtpT')
    print(conn)
    conn.ping()
    print('Connected!')
except Exception as ex:
    print('Error:'), ex
    exit('Failed to connect, terminating.')

sub1 = conn.pubsub()

sub1.subscribe('topic-analytics')

def messageReceptor():
    while(1):
        message = sub1.get_message()
        if(message == None):
            sleep(5)
            print("Nadinha")
        else:
            sleep(3)
            print(message)