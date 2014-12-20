from ModernEnigma import ModernEnigma
from CharIndexMap import CharIndexMap
from Wiring import Wiring
from Rotor import Rotor
from MapperSwitch import MapperSwitch
from Reflector import Reflector
from PlugBoard import PlugBoard
from Util import Util
from RandomGenerator import RandomGenerator
from EnigmaConfigGenerator import EnigmaConfigGenerator
class EnigmaDynamicFactory(object):
    def __init__(self,random=None):
        if not random:
            self.random=RandomGenerator()

    def createEnigmaMachineFromModel(self,modelNo):
        generator=EnigmaConfigGenerator(self.random)
        cfg=generator.createMachineConfig(modelNo)
        mc=self.createEnigmaMachineFromConfig(cfg)
        mc.adjustMachineSettings()
        return mc


    def createCipherModuleFromConfig(self,config):
        cipherModule={}
        cipherModuleCfg=config["CIPHER_MODULE"]
        rotorCfgList=cipherModuleCfg["ROTOR_STOCK"]
        rotorStockList=[]
        for r in rotorCfgList:
            rotorStockList.append(Rotor(r["ID"],Wiring(r["wiring"]),r["notch"]))
        plugboard=PlugBoard(Wiring(cipherModuleCfg["PLUGBOARD"]["wiring"]))
        reflector=Reflector(Wiring(cipherModuleCfg["REFLECTOR"]["wiring"]))
        cipherModule["ROTOR_STOCK"]=rotorStockList
        cipherModule["PLUGBOARD"]=plugboard
        cipherModule["REFLECTOR"]=reflector

        return cipherModule

    def createSwappingModuleFromConfig(self,config):
        swapModule={}
        swappingModuleCfg=config["SWAPPING_MODULE"]
        l1rotorCfgList=swappingModuleCfg["L1_ROTOR_STOCK"]
        l2rotorCfgList=swappingModuleCfg["L2_ROTOR_STOCK"]
        l1l2MapperCfg=swappingModuleCfg["L1_L2_MAPPER"]

        l1SwappingRotorStockList=[]
        for l1r in l1rotorCfgList:
            l1SwappingRotorStockList.append(Rotor(l1r["ID"],Wiring(l1r["wiring"]),l1r["notch"]))


        l2SwappingRotorStockList=[]
        for l2r in l2rotorCfgList:
            l2SwappingRotorStockList.append(Rotor(l2r["ID"],Wiring(l2r["wiring"]),l2r["notch"],len(l2r["wiring"])))


        l1l2Mapper=self.createMapper(l1l2MapperCfg)

        swapModule["L1_ROTOR_STOCK"]=l1SwappingRotorStockList
        swapModule["L2_ROTOR_STOCK"]=l1SwappingRotorStockList
        swapModule["L1_L2_MAPPER"]=l1l2Mapper

        return swapModule
    def createEnigmaMachineFromConfig(self,config):
        cipherModule=self.createCipherModuleFromConfig(config)
        swappingModule=self.createSwappingModuleFromConfig(config)

        rotorStockList=cipherModule["ROTOR_STOCK"]
        reflector=cipherModule["REFLECTOR"]
        plugboard=cipherModule["PLUGBOARD"]

        l1SwappingRotorStockList=swappingModule["L1_ROTOR_STOCK"]
        l2SwappingRotorStockList=swappingModule["L2_ROTOR_STOCK"]
        l1l2SeparatorSwitch=swappingModule["L1_L2_MAPPER"]
        l2CipherMapper=None



        mc=ModernEnigma(rotorStockList,reflector,plugboard,l1SwappingRotorStockList,l2SwappingRotorStockList,l1l2SeparatorSwitch)
        return mc

    def createMapper(self,config):

        w=Wiring(config["wiring"])

        return MapperSwitch(w)


