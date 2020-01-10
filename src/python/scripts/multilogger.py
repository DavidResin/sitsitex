import logging, threading, time

def ticker(parent, period, arg):
	while arg["stop"]:
		parent.tick()
		time.sleep(period)

class MultiLogger:
	def __init__(self, steps, verbose=1):
		self.mainLogger = logging.getLogger(name="sitsitex.mainLog")
		self.fileLogger = logging.getLogger(name="sitsitex.fileLog")

		self.verbose = verbose
		self.period = period

		# MAKE STEPS DEPEND ON NUMBER OF SONG FILES AND PDFLATEX RUNS!!!
		# TRY WITH INSTANT BAR PROGRESSION

		self.properties = {
			"period" :	.2,
			"length" :	15,
			"steps" : 	steps
			"prefix" : 	"[ ",
			"suffix" : 	" ]",
			"full" :	u"\u2588",
			"void" : 	" ",
			"loop" : 	["o", "O", "°", "'", "°", "O", "o", "."],
		}

		self.progress = 0
		self.ticks_tgt = 0
		self.ticks = 0
		self.anim_pos = 0
		self.anim_step = 0
		self.anim_status = 1

		self.bar = ""
		self.message = ""
		self.words = {
			"pre" : 	"Step"
			"mid" : 	"of"
			"post" : 	""
		}

		self.info = { stop : False }
		self.clock = threading.Thread(target=ticker, args=(self, self.properties["period"], self.info))
		
	def status(self):
		return not self.info["stop"]

	def start(self):
		self.clock.start()

	def stop(self):
		self.info["stop"] = True
		self.clock.join()

	def tick(self):
		if self.ticks < self.ticks_tgt:
			self.ticks += 1

		full_ticks = [self.properties["full"]] * self.ticks
		void_ticks = [self.properties["void"]] * (self.properties["length"] - self.ticks)

		if not void_ticks:
			return

		self.anim_pos += self.anim_status

		if self.anim_pos < self.ticks or self.anim_pos >= self.properties["length"]:
			self.anim_pos = max(self.ticks, min(self.anim_pos, self.properties["length"]))
			self.anim_status *= -1
			self.anim_pos += self.anim_status
		
		self.anim_step += 1

		bar = full_ticks + void_ticks
		bar[self.anim_pos] = self.properties["loop"][self.anim_step]
		bar = self.properties["prefix"] + "".join(bar) + self.properties["suffix"]
		self.loading_bar = bar

		update()

	def message(self, payload):
		if not status() and payload["start"]:
			start()

		if status() and payload["end"]:
			stop()

		if status() and payload["progress"]:
			if payload["progress"] < self.progress:
				raise Exception("Progress should not decrease. This should never happen!")

			if payload["progress"] > self.properties["steps"]:
				raise Exception("Progress is going over the maximum. This should never happen!")

			self.progress = payload["progress"]
			self.ticks_tgt = self.properties["steps"] * self.progress // self.properties["length"]

	def update():
		temp = [self.words["pre"], "{:{}d}".format(self.progress, len(str(self.properties["steps"]))), self.words["mid"], self.properties["steps"], self.words["post"]]
		stepcount = " ".join([str(t) for t in temp]).strip()

		print(f"\r{ stepcount } - { self.loading_bar } - { self.message }", end="")