import base64

class FileReader(object):
    def writeSeqTofile(self,seq,f,asHex=True):
        output=bytes(seq)
        if asHex:
            output=base64.b64encode(output)
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

