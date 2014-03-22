from src.sim import Sim
from src.connection import Connection
from src.tcppacket import TCPPacket

import math

class My_RTP(Connection):
	def __init__(self,transport,source_address,source_port,
				 destination_address,destination_port,app=None):
		Connection.__init__(self,transport,source_address,source_port,
							destination_address,destination_port,app)
		self.send_buffer = ''
		self.receive_buffer = []
		self.bytes_outstanding = 0
		self.mss = 1000
		self.sequence = 0
		self.ack = 0
		self.timer = None
		self.timeout = 1
		self.max_sequence = math.pow(2,64)
		self.window_size = 1
		self.window_start = 0
		self.timer_set = False
		self.queueing_delay = 0
		self.pkt_q_delay_threshold = 0.0000000001
		self.pkts_rcvd = 0
		self.ssthresh = 100000

	def handle_packet(self,packet):
		# handle ACK
		if packet.ack_number > self.window_start and packet.ack_number <= len(self.send_buffer):
			# this acks new data, so advance the window with slide_window()
			Sim.trace("%d received My_RTP ACK from %d for %d" % (packet.destination_address,packet.source_address,packet.ack_number))
			self.slide_window(packet.ack_number)

		# handle data
		if packet.length > 0:
			self.pkts_rcvd += 1

			Sim.trace("%d received My_RTP segment from %d for %d" % (packet.destination_address,packet.source_address,packet.sequence))
			# if the packet is the one we're expecting increment our
			# ack number and add the data to the receive buffer

			if packet.sequence >= self.ack:
				self.receive_buffer.append(packet)

				if packet.sequence == self.ack:
					self.receive_buffer = sorted(self.receive_buffer, key=lambda TCPPacket: TCPPacket.sequence)
					while self.receive_buffer and (self.ack == self.receive_buffer[0].sequence):
						pkt = self.receive_buffer.pop(0)
						self.increment_ack(pkt.sequence + pkt.length)
						# deliver data that is in order
						self.app.handle_packet(pkt)

			# always send an ACK
			self.send_ack()

			if packet.queueing_delay > self.pkt_q_delay_threshold:
				self.queueing_delay += packet.queueing_delay

			print "\n[Average Queuing Delay so far:", str(self.queueing_delay / self.pkts_rcvd) + "]"
			print "\n[Total Queueing Delay so far:", str(self.queueing_delay) + "]\n"

	def load_buffer(self, data):
		self.send_buffer += data

	def window_init(self):
		for i in range(math.ceil(self.window_size / self.mss)):
			self.send_if_possible()

	def slide_window(self, ack_number):
		bytes_acked = ack_number - self.window_start
		self.bytes_outstanding -= bytes_acked
		self.window_start = ack_number
		if self.windows_size < self.ssthresh:
			self.window_size += bytes_acked
		else:
			self.window_size += math.ceil(self.mss * bytes_acked / self.window_size) # check this when running program

		for i in range(math.ceil(self.window_size - self.bytes_outstanding) / self.mss):
			self.send_if_possible()
		self.cancel_timer()
		if ack_number < len(self.send_buffer):
			self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)
		else:
			self.timer_set = False

	def send_if_possible(self):
		if self.bytes_outstanding >= self.window_size:
			return
		packet = self.send_one_packet(self.sequence)
		if packet:
			self.increment_sequence(packet.length)

	def send_one_packet(self, sequence):
		num_bytes = 0
		if sequence >= len(self.send_buffer):
			return
		if sequence + self.mss > len(self.send_buffer):
			num_bytes = len(self.send_buffer) - sequence
			body = self.send_buffer[sequence : ]
		elif sequence + self.mss > self.window_start + self.window_size: 
			num_bytes = self.window_start + self.window_size - sequence
			body = self.send_buffer[sequence : sequence + bytes_to_send]
		else:
			body = self.send_buffer[sequence : sequence + self.mss]
			num_bytes = self.mss

		self.bytes_outstanding += num_bytes

		# get one packet worth of data
		packet = TCPPacket(source_address=self.source_address,
						   source_port=self.source_port,
						   destination_address=self.destination_address,
						   destination_port=self.destination_port,
						   body=body,
						   sequence=sequence,ack_number=self.ack)

		# send the packet
		Sim.trace("%d sending My_RTP segment to %d for %d" % (self.source_address,self.destination_address,packet.sequence))
		self.transport.send_packet(packet)

		# set a timer
		if not self.timer_set:
			self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)
			self.timer_set = True
		return packet

	def send_ack(self):
		packet = TCPPacket(source_address=self.source_address,
						   source_port=self.source_port,
						   destination_address=self.destination_address,
						   destination_port=self.destination_port,
						   sequence=self.sequence,ack_number=self.ack)
		# send the packet
		Sim.trace("%d sending My_RTP ACK to %d for %d" % (self.source_address,self.destination_address,packet.ack_number))
		self.transport.send_packet(packet)

	def increment_sequence(self,length):
		self.sequence += length
		if self.sequence >= self.max_sequence:
			self.sequence = self.sequence - self.max_sequence

	def increment_ack(self,sequence):
		self.ack = sequence
		if self.ack >= self.max_sequence:
			self.ack = 0
		return True

	def retransmit(self,event):
		self.timer_set = False
		if self.bytes_outstanding <= 0:
			return

		self.ssthresh = max(math.ceil(self.window_size / 2), self.mss)
		self.window_size = self.mss

		Sim.trace("%d retransmission timer fired" % (self.source_address))
		packet = self.send_one_packet(self.window_start)

	def cancel_timer(self):
		if not self.timer:
			return
		Sim.scheduler.cancel(self.timer)
		self.timer = None
