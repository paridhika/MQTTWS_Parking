#!/usr/bin/python
import paho.mqtt.client as mqtt
import time
import datetime
import random
import threading
import csv
import subprocess
from Queue import Queue
from collections import OrderedDict
from sets import Set

def createPutClient(sumarray,location):
	start = time.time()
	# The callback for when the client receives a CONNACK response from the server.
	def on_connect(client, userdata, rc):
		print("Connected with result code "+str(rc))

	def on_publish(client, userdata, msg):
		client.disconnect()
		end = time.time()
		sumarray.append(end - start);

	client = mqtt.Client(client_id="", clean_session=True, userdata=None, transport="websockets")
	client.on_connect = on_connect
	client.on_publish = on_publish
	client.connect("localhost", 8000, 60)
	client.publish(topic="loc/put",payload=location)
	
	
class PutClientThread(threading.Thread):
	def __init__(self,put_mean,mean_hold,count):
		threading.Thread.__init__(self)
		self.put_mean = put_mean
		self.mean_hold = mean_hold
		self.count = count
	def store_time(self,location):
		print "put at: " + location
		wait = random.expovariate(self.mean_hold)
		filled_slotsdict[location] = time.time() + wait
		
	def run(self):
		f1 = open('put_simulation_service_time.csv', 'wt')
		f = open('put_simulation_result.csv', 'wt')
		writer = csv.writer(f)
		service = csv.writer(f1)
		writer.writerow( ('Arrival Rate', 'Service Time','Throughput') )
		service.writerow( ('Mean', 'Count', 'Service Time') )
		sumarray = []
		sum = 0.0;
		for index in range(0,self.count):
			wait = random.expovariate(self.put_mean)
			lockobj.acquire()
			location = empty_slotsset.pop()
			self.store_time(location)
			lockobj.release()
			createPutClient(sumarray,location);
			time.sleep(wait);
		i = 1
		for val in sumarray:
			service.writerow((self.put_mean , i, val))
			i += 1
			sum += val
		writer.writerow((self.put_mean , sum/self.count, (int)(self.count*3600/sum)))
		f.close()

def createDeleteClient(sumarray,location):
	start = time.time()
	# The callback for when the client receives a CONNACK response from the server.
	def on_connect(client, userdata, rc):
		print("Connected with result code "+str(rc))
	def on_publish(client, userdata, msg):
		client.disconnect()
		end = time.time()
		sumarray.append(end - start);

	client = mqtt.Client(client_id="", clean_session=True, userdata=None, transport="websockets")
	client.on_connect = on_connect
	client.on_publish = on_publish
	client.connect("localhost", 8000, 60)
	client.publish(topic="loc/delete",payload=location)
	
class DeleteClientThread(threading.Thread):
	def __init__(self,mean_hold,count):
		threading.Thread.__init__(self)
		self.mean_hold = mean_hold
		self.count = count
	def run(self):
		f1 = open('delete_simulation_service_time.csv', 'wt')
		f = open('delete_simulation_result.csv', 'wt')
		writer = csv.writer(f)
		service = csv.writer(f1)
		writer.writerow( ('Arrival Rate', 'Service Time','Throughput') )
		service.writerow( ('Mean', 'Count', 'Service Time') )
		sumarray = []
		arrival_interval = []	#array to store interarrival times of delete processes
		arrival_start = time.time()
		sum = 0.0
		delete_mean = 0.0		#variable to calculate mean interarrival time of delete
		temp_count = self.count
		while(temp_count !=0):
			if any(filled_slotsdict):
				sorted_dict = OrderedDict(sorted(filled_slotsdict.items(), key=lambda t: t[1]))
				location,kill_time = sorted_dict.items()[0]
				if kill_time <= time.time():
					arrival_interval.append(kill_time - arrival_start)
					delete_mean += kill_time - arrival_start
					arrival_start = kill_time
					lockobj.acquire()
					filled_slotsdict.pop(location)
					empty_slotsset.add(location)
					lockobj.release()
					temp_count -= 1
					print "delete at: " + location
					createDeleteClient(sumarray,location)
		i = 1
		delete_mean /= self.count
		for val in sumarray:
			service.writerow((delete_mean , i, val))
			i += 1
			sum += val
		writer.writerow((delete_mean , sum/self.count, (int)(self.count*3600/sum)))
		f.close()

def createGetClient(sumarray,mean_hold):
	start = time.time()
	# The callback for when the client receives a CONNACK response from the server.
	def on_connect(client, userdata, rc):
		print("Connected with result code "+str(rc))

	def store_time(location,mean_hold):
		print "Get at: " + location
		wait = random.expovariate(mean_hold)
		filled_slotsdict[location] = time.time() + wait

	# The callback for when a PUBLISH message is received from the server.
	def on_message(client, userdata, msg):
		location = str(msg.payload)
		store_time(location,mean_hold)
		end = time.time()
		sumarray.append(end - start);
		client.disconnect()

	client = mqtt.Client(client_id="", clean_session=True, userdata=None, transport="websockets")
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 8000, 60)
	client.subscribe("loc/get")
	client.loop_forever()

class GetClientThread(threading.Thread):
	def __init__(self,get_mean,mean_hold,count):
		threading.Thread.__init__(self)
		self.get_mean = get_mean
		self.mean_hold = mean_hold
		self.count = count
	def run(self):
		f1 = open('get_simulation_service_time.csv', 'wt')
		f = open('get_simulation_result.csv', 'wt')
		writer = csv.writer(f)
		service = csv.writer(f1)
		writer.writerow( ('Arrival Rate', 'Service Time','Throughput') )
		service.writerow( ('Mean', 'Count', 'Service Time') )
		sumarray = []
		sum = 0.0;
		for index in range(0,self.count):
			wait = random.expovariate(self.get_mean)
			createGetClient(sumarray,self.mean_hold)
			time.sleep(wait);
		i = 1
		for val in sumarray:
			service.writerow((self.get_mean , i, val))
			i += 1
			sum += val
		writer.writerow((self.get_mean , sum/self.count, (int)(self.count*3600/sum)))
		f.close()

def initEmptySet(empty_slotsset):
	size=10
	for i in range(10):
		for j in range(10):
			empty_slotsset.add(str(i)+","+str(j))

empty_slotsset = set()
filled_slotsdict = OrderedDict()
initEmptySet(empty_slotsset)
lockobj = threading.Lock()
put_mean = 1
get_mean = 1
mean_hold = 0.8
count = 10
put_thread = PutClientThread(put_mean,mean_hold,count)
put_thread.start()
delete_thread = DeleteClientThread(mean_hold,2*count)
delete_thread.start()
get_thread = GetClientThread(get_mean,mean_hold,count)
get_thread.start()
put_thread.join()
delete_thread.join()
get_thread.join()

