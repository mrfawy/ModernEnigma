from ModernEnigma import ModernEnigma
from EnigmaDynamicFactory import EnigmaDynamicFactory
from CharIndexMap import CharIndexMap
from Encryptor import Encryptor
from Decryptor import Decryptor


stg="232221201918171615141312111009080706050403020100|AAAAAAAAAAAAAAAAAAAAACDO||3"
mc1=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCx")
mc1.adjustMachineSettings(stg)
print(mc1.getWindowDisplay())
msg="AAAAAAAA"
print("MSG"+msg)
encMsg=Encryptor(mc1).encryptMsg(msg)

print ("Encrpyted:"+encMsg)

mc2=EnigmaDynamicFactory().createEnigmaMachineFromModel("MCx")
mc2.adjustMachineSettings(stg)
decMsg=Decryptor(mc2).decryptMsg(encMsg)
print("Decrypted:"+decMsg)
print("settings:"+mc1.getMachineSettings())




# import pdb; pdb.set_trace()
