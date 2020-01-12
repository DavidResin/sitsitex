from multilogger import MultiLogger as ML
import atexit

ml = ML(4)
atexit.register(ml.stop)
ml.start()

