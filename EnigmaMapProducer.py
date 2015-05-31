from queue import Queue
from threading import Thread
from ModernEnigma import ModernEnigma


class EnigmaMapProducer(Thread):
    def __init__(self,queue,machine):
        self.queue=queue
        self.machine=machine
        self.inputVector=List(range(0,255))
        self.stopped=False

    def run(self):
        while not self.stopped:
            item=machine.processKeyListPress(self.inputVector)
            self.queue.put(item,True)
    def stop(self):
        self.stop=True


