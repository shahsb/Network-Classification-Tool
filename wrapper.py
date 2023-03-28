from subprocess import Popen, PIPE, TimeoutExpired
from queue import Queue, Empty
from threading import Thread
from time import sleep , time
import csv


def write_csv(dict , filename , field_names):
	f = open(filename,'a')
	writer = csv.DictWriter(f, fieldnames = field_names)
	writer.writerow(dict)
	f.close()



def add_conversation(source_ip, dest_ip, ts_Sec , ts_uSec,source_port,dest_port , size):
	# print("In add conservation")
	# print(source_ip)
	# print(dest_ip)
	#print(ts_Sec)
	#print(ts_uSec)

	flag = 0

	# print("===")
	# print(len(conversations))
	# print("===")
		

	#for i in range(len(conversations)):
	for c in conversations:
		c = conversations[i]
		if ((c['ip_1'] == source_ip and c['ip_2'] == dest_ip) or (c['ip_1'] == dest_ip and c['ip_2'] == source_ip)):
			# print("Inside if")
			c['total_packets'] += 1
			time = int(ts_Sec) + int(ts_uSec)/1000000
			c['duration'] += time - c['last_timestamp']
			c['last_timestamp'] = time
			c['netsize'] += size
			if(c['ip_1'] == dest_ip): 
				# print(conversations[i]['packets_to_ip_1'])
				conversations[i]['packets_to_ip_1'] += 1
				# print(conversations[i]['packets_to_ip_1'])
				#c['packets_to_ip_1'] += 1
				flag = 1
				# print("=====================================================================")
				break
			else:
				# print(conversations[i]['packets_to_ip_2'])
				conversations[i]['packets_to_ip_2'] += 1
				# print(conversations[i]['packets_to_ip_2'])
				#c['packets_to_ip_2'] += 1
				flag = 1
				print("=====================================================================")
				break			
			

			
		
	if flag == 0:
		# print("NEW PACKET")
		single_conversation = {}
		single_conversation['ip_1'] = source_ip
		single_conversation['ip_2'] = dest_ip
		single_conversation['total_packets'] = 1
		single_conversation['packets_to_ip_1'] = 0
		single_conversation['packets_to_ip_2'] = 1
		single_conversation['last_timestamp'] = int(ts_Sec) + int(ts_uSec)/1000000
		single_conversation['duration'] = 0
		single_conversation['netSize'] = size
		conversations.append(single_conversation)
		

def write_conversations(conversations):
	print(conversations)
	for c in conversations:
		write_csv(c,'summary.csv', field_names_conversation)


# FIELDNAMES FOR CSV FILES
header_names_packet = ['TimeStamp_Sec', 'TimeStamp_uSec', 'SourceIp','DestIp','TTL','Protocol','SourcePort','DestPort','SequenceNo','NLHeaderSize','PacketSize']
header_names_conversation = ['A' , 'B' , 'A -> B' , 'B -> A' , 'Total Packets', 'TimeStamp' , 'Duration']
field_names_conversation = ['ip_1' , 'ip_2' , 'packets_to_ip_2' , 'packets_to_ip_1' ,'total_packets', 'last_timestamp' , 'duration' , 'netSize' , 'avg_flowSize' , 'bytes_per_flow']

# INITIALIZING PACKET HEADER FILE
f = open('data.csv','w')
writer = csv.DictWriter(f, fieldnames = header_names_packet) 
writer.writeheader()
f.close()

# INITIALIZING CONVERSATIONS HEADER FILE
f = open('summary.csv','w')
writer = csv.DictWriter(f, fieldnames = header_names_conversation)
writer.writeheader()
f.close()


"""
FUNCTION TO BE EXECUTED AS A SEPERATE THREAD THAT READS CONTINUOUSLY WITHOUT 
BLOCKING FROM THE STDOUT OF THE SNIFFER SUBPROCESS AND PLACES THE READ DATA
IN A QUEUE. QUEUE CAN LATER USED FROM THE MAIN THREAD TO GET STDOUT DATA.
"""
def read_continuous(buf, queue):
	for line in buf:
		queue.put(line.decode('utf-8'))
	buf.close()


# VARAIBLES TO GET THE PACKET PARAMETERS
packet = {}
packets = []
packet_attributes = []
conversations = []

count = 0

# STARTING THE EXECUTION OF SNIFFER EXECUTABLE
p = Popen(['./sniffer' , 'wlan0'], stdout = PIPE, stderr = PIPE)

# CREATING QUEUE FOR STROING CONTINUOUS READ DATA FROM STDOUT OF SUBPROCESS
q = Queue()

# CREATING AND STARTING A NEW THREAD
t = Thread(target = read_continuous, args = (p.stdout, q))
t.start()

# LOOPINF INDEFINITLY TILL USER INTERRUPTION AND CAPTURING PACKETS
while 1:
	try:
		# WAIT FOR SOME DATA TO BE GENERATED
		sleep(0.005)
		
		# EXTRACT NON BLOCKINGLY FROM QUEUE
		line = q.get_nowait()
		line = line[:-1]
		# print(line)
		
		# START OF NEW PACKET
		if line == "New Packet":
			count = 1
			continue

		if count > 0:
			if count == 1:
				packet['TimeStamp_Sec'] = line
			elif count == 2:
				packet['TimeStamp_uSec'] = line
			elif count == 3:
				packet['SourceIp'] = line
			elif count == 4:
				packet['DestIp'] = line
			elif count == 5:
				packet['TTL'] = line
			elif count == 6:
				packet['Protocol'] = line
			elif count == 7:
				packet['SourcePort'] = line
			elif count == 8:
				packet['DestPort'] = line
			elif count == 9:
				packet['SequenceNo'] = line
			elif count == 10:
				packet['NLHeaderSize'] = line
			elif count == 11:
				packet['PacketSize'] = line

			count += 1

		# END OF A PACKET
		if line == "End Packet":
			write_csv(packet, 'data.csv', header_names_packet)
			#print(packet['SourceIp'])
			
			add_conversation(packet['SourceIp'], packet['DestIp'], packet['TimeStamp_Sec'], packet['TimeStamp_uSec'] , packet['SourcePort'] , packet['DestPort'] , packet['PacketSize'])
			
			
			#conversations['avg_flowSize'] = conversations['total_packets']/10
			#conversations['bytes_per_flow'] = conversations['netSize']/conversations['total_packets']


			#sessionHandler(packet['SourceIp'] , packet['DestIp'] , packet['TimeStamp_Sec'], packet['TimeStamp_uSec'] , packet['SourcePort'] , packet['DestPort'], packet['PacketSize'])
			count = 0


	
	# EXCEPTION RAISED IF QUEUE IS EMPTY	
	except Empty:
		pass
		# print("No Output")

	except KeyboardInterrupt:
		print("Keyboard Interrupt User")
		write_conversations(conversations)
		break



