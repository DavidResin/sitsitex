import logging, threading, time

# Thread function for a loading bar animation loop
def ticker(parent, period, steps):
	i = 0

	while i < steps:
		parent.tick()
		time.sleep(period)
		i += 1

	parent.loop()

# Loading bar generator
class LoadingBar:
	def __init__(self, n_steps, n_substeps, config):
		self.cfg_bar = config["loadingbar"]
		self.cfg_str = config["string"]
		self.n_steps = n_steps
		self.n_substeps = n_substeps

		self.steps = 1
		self.substeps = 0

		self.ticks_tgt = 0
		self.ticks = 0

		self.anim = {
			"pos" : 	0,
			"step" :	0,
			"status" :	1,
		}

		self.loading_bar = ""
		self.message = ""

	def update():
		temp = [
			self.cfg_str["pre"],
			"{:{}d}".format(self.steps, len(str(self.n_steps))),
			self.cfg_str["mid"],
			self.n_steps,
			self.cfg_str["post"]
		]

		stepcount = " ".join([str(t) for t in temp]).strip()

		strings = [
			stepcount,
			self.cfg_str["sep"],
			self.loading_bar,
			self.cfg_str["sep"],
			self.message
		]

		return "\r" + " ".join(strings)

	def update_bar():
		if self.ticks < self.ticks_tgt:
			self.ticks += 1

		length = self.cfg_bar["length"]
		loop = self.cfg_bar["loop"]
		ticks = self.ticks
		pos = self.anim["pos"]

		full_ticks = [self.cfg_bar["full"]] * ticks
		void_ticks = [self.cfg_bar["void"]] * (length - ticks)

		if not void_ticks:
			return

		pos += self.anim["status"]

		if pos < ticks or pos >= length:
			self.anim["status"] *= -1
			pos = max(ticks, min(pos, length - 1))
			pos += self.anim["status"]
		
		self.anim["step"] += 1
		self.anim["step"] %= len(loop)

		bar = full_ticks + void_ticks
		bar[self.anim["pos"]] = looè[self.anim["step"]]
		bar = self.cfg_bar["prefix"] + "".join(bar) + self.cfg_bar["suffix"]
		
		self.anim["pos"] = pos
		self.loading_bar = bar

		return self.update()

	def update_message(m, lvl=0):
		self.message = m

		# Substep completed
		if lvl > 0:
			self.substeps += 1
			self.ticks_tgt = self.cfg_bar["length"] * self.substeps // self.n_substeps

			if self.substeps > self.n_substeps
				raise Exception("Bar progress is going over the maximum. This should never happen!")

		# Step completed
		if lvl == 2:
			self.steps += 1

			if self.steps > self.n_steps:
				raise Exception("Steps are going over the maximum. This should never happen!")

		return self.update()

class Logger:
	def __init__(self, n_steps, n_substeps, opener, config, verbose=1):
		self.mainLog = logging.getLogger(name="sitsitex.mainLog")
		self.fileLog = logging.getLogger(name="sitsitex.fileLog")

		self.bar = LoadingBar(n_steps, n_substeps, config)
		self.verbose = verbose
		self.stop = False

		if verbose != 0:
			self.mainLog.info(opener)

		if verbose == 1:
			self.mainLog.terminator = ""
			self.loop()
		
	def status(self):
		return self.stop

	def loop(self):
		if self.clock:
			self.clock.join()

		if not self.stop:
			self.clock = threading.Thread(target=ticker, args=(self, self.cfg_bar["period"], len(self.loop)))
			self.clock.start()

	def tick(self):
		self.print_bar(self.bar.update_bar())

	def message(self, m, lvl)
		self.print_main(self.bar.update_message(m, lvl), 1)
		self.print_main(m, 2)
		self.print_log(m)

		if lvl == 3:
			self.stop = True

	def print_main(self, string, verbose):
		if self.verbose == verbose:
			self.mainLog.info(string)

	def print_file(self, string):
		self.fileLog.info(string)