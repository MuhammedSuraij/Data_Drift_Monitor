import pandas as pd

class StreamBuffer:

    def __init__(self,batch_size=30):
        self.batch_size=batch_size
        self.buffer=[]

    def add(self,record):
        self.buffer.append(record)

        if len(self.buffer)>= self.batch_size:
            batch=pd.DataFrame(self.buffer)
            self.buffer.clear()
            return batch
        
        return None