#!/usr/bin/env python
import threading, logging, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer

NO_OF_EVENT = 50000
NO_OF_EACHROUND = 2000
MY_MSG = b'message!'*128  #1KB
MY_MSG_SIZE = len(MY_MSG)/1024  #KB
INSTANCE_OF_PRODUCER=2
INSTANCE_OF_CONSUMER=2

class Producer(threading.Thread):
    def __init__(self, evtRange):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
	self.event_range = evtRange
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092', \
				 acks=1, \
				 linger_ms=100, \
                                 compression_type="gzip", \
				 buffer_memory=64*1024*1024 \
                   )

        totalNum = 0
#        while not self.stop_event.is_set():
        start = time.time()
        for i in range(self.event_range[0], self.event_range[1]):
            #producer.send('my-topic', b"event id="+str(i))
            producer.send('my-topic', MY_MSG)
            totalNum+=1
            if totalNum%NO_OF_EACHROUND==0:
                end = time.time()
                print("Producer,%d,%d" % (NO_OF_EACHROUND, (end-start)*1000))
                start = time.time()
                #time.sleep(1)
        print "producer metrics######,", producer.metrics()
        producer.close()

class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        
    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
				 enable_auto_commit = False,
                                 consumer_timeout_ms=200)
        consumer.subscribe(['my-topic'])

        totalNum = 0
        start = time.time()
        # while not self.stop_event.is_set():
        for message in consumer:
            #print(message)
            totalNum+=1
            if totalNum%NO_OF_EACHROUND==0:
                end = time.time()
                print("Consumer,%d,%d" % (NO_OF_EACHROUND, (end-start)*1000))
                start = time.time()
            if self.stop_event.is_set():
                break
        print "consumer metrics#####,", consumer.metrics()
        consumer.close()
        
        
def main():
    event_per_producer = NO_OF_EVENT/INSTANCE_OF_PRODUCER
    #tasks = [
    #    Producer([1,NO_OF_EVENT+1]),
    #    Consumer()
    #]
    producers = [Producer([event_per_producer*i+1,event_per_producer*(i+1)+1]) for i in range(INSTANCE_OF_PRODUCER)]
    consumers = [Consumer() for i in range(INSTANCE_OF_CONSUMER)]
    tasks = producers + consumers

    for t in tasks:
        t.start()

    start = time.time()
    #time.sleep(10)
    
    #for task in tasks:
    #    task.stop()

    for task in tasks:
        task.join()
    
    duration = time.time() - start
    print ("Summary: Events:%d, Duration:%fs, Throughput:%d/s,%fMB/s" %  \
			(NO_OF_EVENT, duration, NO_OF_EVENT/duration, \
                         NO_OF_EVENT*MY_MSG_SIZE/1024/duration)) 
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()

