import scheduler

class Sim(object):
	scheduler = scheduler.Scheduler()
	debug = False
	rate_file = open("rate_data.txt", "w")

	@staticmethod
	def set_debug(value):
		Sim.debug = value

	@staticmethod
	def trace(message):
		if Sim.debug:
			print Sim.scheduler.current_time(),message

	@staticmethod
	def print_rate_info(packet):
		if packet.length == 0:
			Sim.rate_file.write(str(packet.flow_id) + " " + str(Sim.scheduler.current_time()) + " " + str(packet.ack_number - 1000) + " " + str(packet.length) + "\n")
		else:
			Sim.rate_file.write(str(packet.flow_id) + " " + str(Sim.scheduler.current_time()) + " " + str(packet.sequence) + " " + str(packet.length) + "\n")

	@staticmethod
	def print_packet_loss(packet):
		Sim.rate_file.write(str(packet.flow_id) + " " + str(Sim.scheduler.current_time()) + " " + str(packet.sequence) + " x\n")

	@staticmethod
	def close_rate_file():
		Sim.rate_file.close()
