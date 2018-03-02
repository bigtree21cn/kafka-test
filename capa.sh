	fileN=$1
	awk -F, 'BEGIN {tmpFile=""}
	{
		if (match($1, "Consumer")) { 
			consumer[0]+=$2;
			consumer[1]+=$3;
		}
		if (match($1, "Producer")) {
			producer[0]+=$2;
			producer[1]+=$3;
		}
	}
	END{ 
		consumer[1] = consumer[1]/1000.0;
		producer[1] = producer[1]/1000.0;
		printf("Producer: Event Sent:     %d, Duration:%fs, Throughput:%d/s\n", producer[0], producer[1], producer[0]/producer[1]);
		printf("Consumer: Event Received: %d, Duration:%fs, Throughput:%d/s\n", consumer[0], consumer[1], consumer[0]/consumer[1]);
	}' ${fileN}  #2>/dev/null
	
	grep "Summary" ${fileN}	
