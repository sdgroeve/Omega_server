import time
import sys
from multiprocessing import Process, Value, Lock

mfac = 100./500.

def func(val, lock, pid):
	cfac = 10
	for i in range(50):
		time.sleep(0.1)
		if pid == 0:
			tmp = val.value * mfac
			if tmp >= cfac:
				sys.stderr.write("processed %s %i%%\n"%(sys.argv[1],cfac))
				cfac += 10
  		with lock:
			val.value += 1
	return True
	
if __name__ == '__main__':
	v = Value('i', 0)
	lock = Lock()
	procs = [Process(target=func, args=(v, lock, i)) for i in range(10)]

	for p in procs: p.start()
	for p in procs: p.join()

	sys.stderr.write("Done\n")
	print v.value
	
	with open("/home/pitro11a/flask-base/app/static/files/test.test","w") as f:
		f.write("hello")

	for p in procs:
		print p.get()
