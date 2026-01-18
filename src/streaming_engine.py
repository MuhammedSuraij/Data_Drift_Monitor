import pandas as pd

class StreamBuffer:

    def __init__(self,batch_size=50):
        self.batch_size=batch_size
        self.buffer=[]

    def add(self,record):
        self.buffer.append(record)
        return len(self.buffer) >=self.batch_size

    def get_dataframe(self):
        df=pd.DataFrame(self.buffer)
        self.buffer = []
        return df