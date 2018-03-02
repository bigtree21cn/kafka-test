# Kafka-test


## ACKS=0 did not improve the throughput of producer in such environments:
jefli@jefli-1:~/vol3$ sh capa.sh 50k_11_default.txt
Producer: Event Sent:     50000, Duration:6.025000s, Throughput:8298/s
Consumer: Event Received: 50000, Duration:6.032000s, Throughput:8289/s
## Summary: Eventsl50000, Duration:7.279738s, Throughput:6868/s
jefli@jefli-1:~/vol3$ sh capa.sh 50k_11_noacks.txt
Producer: Event Sent:     50000, Duration:6.273000s, Throughput:7970/s
Consumer: Event Received: 50000, Duration:6.280000s, Throughput:7961/s
Summary: Eventsl50000, Duration:7.526140s, Throughput:6643/s

## linger_ms setup properly will improve the throughput very much. In case of the load is high, the will utilize the batch send to improve the throughput, but in case of the load is low, this would increase the latency.
jefli@jefli-1:~/vol3$ sh capa.sh 50k_11_linger50_r2.txt
Producer: Event Sent:     50000, Duration:3.210000s, Throughput:15576/s
Consumer: Event Received: 50000, Duration:3.254000s, Throughput:15365/s
Summary: Events:50000, Duration:4.497590s, Throughput:11117/s
jefli@jefli-1:~/vol3$ sh capa.sh 50k_11_linger100.txt
Producer: Event Sent:     50000, Duration:3.019000s, Throughput:16561/s
Consumer: Event Received: 50000, Duration:3.122000s, Throughput:16015/s
Summary: Events:50000, Duration:4.474004s, Throughput:11175/s

Message size is very critical to the throughput,  1KB for each message, only 1/8 throughput comparing to   10bytes.
jefli@jefli-1:~/vol3$ sh capa.sh 50K_11_linger100.txt
Producer: Event Sent:     50000, Duration:25.604000s, Throughput:1952/s
Consumer: Event Received: 50000, Duration:25.614000s, Throughput:1952/s
Summary: Events:50000, Duration:26.951665s, Throughput:1855/s

## Message compression is improved the throughput very much
jefli@jefli-1:~/vol3$ sh capa.sh 50K_11_gzip.txt
Producer: Event Sent:     50000, Duration:9.411000s, Throughput:5312/s
Consumer: Event Received: 50000, Duration:9.416000s, Throughput:5310/s
Summary: Events:50000, Duration:10.754869s, Throughput:4649/s

## Partition NO(1->7) will increase the throughput even in 1 consumer  1 producer environment:
jefli@jefli-1:~/vol3$ sh capa.sh 1.txt
Producer: Event Sent:     50000, Duration:8.975000s, Throughput:5571/s
Consumer: Event Received: 50000, Duration:8.976000s, Throughput:5570/s
Summary: Events:50000, Duration:10.319693s, Throughput:4845/s, 4.651301MB/s
jefli@jefli-1:~/vol3$ ./bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic my-topic --partitions 
jefli@jefli-1:~/vol3$ sh capa.sh 3.txt
Producer: Event Sent:     50000, Duration:7.598000s, Throughput:6580/s
Consumer: Event Received: 50000, Duration:7.614000s, Throughput:6566/s
Summary: Events:50000, Duration:8.961139s, Throughput:5579/s,5.356462MB/s
jefli@jefli-1:~/vol3$ /home/jefli/kafka_2.11-1.0.0/bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic my-topic --partitions 4
jefli@jefli-1:~/vol3$ sh capa.sh 7.txt
Producer: Event Sent:     50000, Duration:7.254000s, Throughput:6892/s
Consumer: Event Received: 50000, Duration:7.270000s, Throughput:6877/s
Summary: Events:50000, Duration:8.615246s, Throughput:5803/s,5.571518MB/s
jefli@jefli-1:~/vol3$ /home/jefli/kafka_2.11-1.0.0/bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic my-topic --partitions 7
jefli@jefli-1:~/vol3$ sh capa.sh 7.txt
Producer: Event Sent:     50000, Duration:6.961000s, Throughput:7182/s
Consumer: Event Received: 50000, Duration:6.970000s, Throughput:7173/s
Summary: Events:50000, Duration:8.310289s, Throughput:6016/s,5.775972MB/s
jefli@jefli-1:~/vol3$ /home/jefli/kafka_2.11-1.0.0/bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic my-topic --partitions 11
jefli@jefli-1:~/vol3$ sh capa.sh 11.txt
Producer: Event Sent:     50000, Duration:6.948000s, Throughput:7196/s
Consumer: Event Received: 50000, Duration:6.965000s, Throughput:7178/s
Summary: Events:50000, Duration:8.309806s, Throughput:6016/s,5.776308MB/s
