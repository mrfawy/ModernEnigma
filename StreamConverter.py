class StreamConverter(object):
    def convertInput(self,inputStream):
        print("no stream converion !!")
        return inputStream

    def convertOutput(self,outputStream):
        print("no stream converion !!")
        return outputStream

class CharacterStreamConverter(StreamConverter):
    def convertInput(self,inputStream):
        result=[]
        if not isinstance(inputStream,str):
            raise Exception("invalid stream , expecting a string !!")
        for c in inputStream:
            result.append(ord(c))
        return result

    def convertOutput(self,outputStream):
        result=""
        for o in outputStream:
            result+=chr(o)
        return result
