import base64

class FileReader(object):
    def writeSeqTofile(self,seq,f):
        output=bytes(seq)
        with open(f,"wb") as f:
            f.write(output)
    def readSeqFromFile(self,f):
        result=[]
        with open(f, "rb") as f:
            byte = f.read(1)
            while byte:
                result.append(int.from_bytes(byte, byteorder='big', signed=False))
                byte = f.read(1)
        return result

