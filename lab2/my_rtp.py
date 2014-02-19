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
		self.packets_outstanding = 0
		self.mss = 1000
		self.sequence = 0
		self.ack = 0
		self.timer = None
		self.timeout = 1
		self.max_sequence = math.pow(2,64)
		self.window_size = 3
		self.window_start = 0
		self.timer_set = False

	def handle_packet(self,packet):
		# handle ACK
		if packet.ack_number > self.window_start and packet.ack_number <= self.sequence:
			# this acks new data, so advance the window with slide_window()
			Sim.trace("%d received My_RTP ACK from %d for %d" % (packet.destination_address,packet.source_address,packet.ack_number))
			self.slide_window(packet.ack_number)

		# handle data
		if packet.length > 0:
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

	def load_buffer(self, data):
		self.send_buffer += data

	def window_init(self):
		for i in range(self.window_size):
			self.send_if_possible()

	def slide_window(self, ack_number):
		packets_acked = int(math.ceil((ack_number - self.window_start)/self.mss))
		self.packets_outstanding -= packets_acked
		self.window_start = ack_number
		for i in range(self.window_size - self.packets_outstanding):
			self.send_if_possible()
		self.cancel_timer()
		if ack_number < len(self.send_buffer):
			self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)
		else:
			self.timer_set = False

	def send_if_possible(self):
		if self.packets_outstanding >= self.window_size:
			return
		self.packets_outstanding += 1
		packet = self.send_one_packet(self.sequence)
		if packet:
			self.increment_sequence(packet.length)

	def send_one_packet(self, sequence):
		if sequence >= len(self.send_buffer):
			return
		if sequence + self.mss > len(self.send_buffer):
			body = self.send_buffer[sequence : ]
		else:
			body = self.send_buffer[sequence : sequence + self.mss]

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
		if self.packets_outstanding <= 0:
			return
		Sim.trace("%d retransmission timer fired" % (self.source_address))
		packet = self.send_one_packet(self.window_start)

	def cancel_timer(self):
		if not self.timer:
			return
		Sim.scheduler.cancel(self.timer)
		self.timer = None
