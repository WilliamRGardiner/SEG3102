from queue import Queue, LifoQueue

''' Processes Tasks and rolls them back upon error'''
class TaskProcessor():
    def __init__(self):
        self.taskQueue = Queue()
        self.taskCalledStack = LifoQueue()

    def add(self, task):
        self.taskQueue.put(task)

    def clear(self):
        self.taskQueue = Queue()
        self.taskCalledStack = LifoQueue()

    def process(self):
        # try:
        while not self.taskQueue.empty():
            task = self.taskQueue.get()
            self.taskCalledStack.put(task)
            task.do()
        # except:
        #     errTasklet = self.taskCalledStack.get()
        #     try:
        #         while not self.taskCalledStack.empty():
        #             task = self.taskCalledStack.get()
        #             task.undo()
        #         raise Exception("Task Failed: \n" + errTasklet.getErrorMessage())
        #     except:
        #         raise Exception("Task Undo Failed: Possible Data Curruption")
