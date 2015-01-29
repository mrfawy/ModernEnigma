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
    def __init__(self,seed=None):
        self.seed=seed
        self.random=RandomGenerator(seed)

    def createEnigmaMachineFromModel(self,modelNo):
        generator=EnigmaConfigGenerator(self.seed)
        cfg=generator.createMachineConfig(modelNo)
        mc=self.createEnigmaMachineFromConfig(cfg)
        return mc


    def createCipherModuleFromConfig(self,config):
        cipherModule={}
        cipherModuleCfg=config["CIPHER_MODULE"]
        cipherRotorStockCfg=cipherModuleCfg["ROTOR_STOCK"]
        cipherRotorMap={}
        for key,val in cipherRotorStockCfg.items():
            cipherRotorMap[key]=Rotor(val["ID"],Wiring(val["wiring"]),val["notch"])
        plugboard=PlugBoard(Wiring())
        reflector=Reflector(Wiring(cipherModuleCfg["REFLECTOR"]["wiring"]))
        cipherModule["ROTOR_STOCK"]=cipherRotorMap
        cipherModule["PLUGBOARD"]=plugboard
        cipherModule["REFLECTOR"]=reflector

        return cipherModule

    def createSwappingModuleFromConfig(self,config):
        swapModule={}
        swappingModuleCfg=config["SWAPPING_MODULE"]
        swapRotorStockCfg=swappingModuleCfg["SWAP_ROTOR_STOCK"]
        swapRotorMap={}
        for key,val in swapRotorStockCfg.items():
            swapRotorMap[key]=Rotor(val["ID"],Wiring(val["wiring"]),val["notch"])

        swapModule["SWAP_ROTOR_STOCK"]=swapRotorMap

        return swapModule
    def createEnigmaMachineFromConfig(self,config):
        cipherModule=self.createCipherModuleFromConfig(config)
        swappingModule=self.createSwappingModuleFromConfig(config)

        cipherRotorStockMap=cipherModule["ROTOR_STOCK"]
        reflector=cipherModule["REFLECTOR"]
        plugboard=cipherModule["PLUGBOARD"]

        swapRotorStockMap=swappingModule["SWAP_ROTOR_STOCK"]

        mc=ModernEnigma(cipherRotorStockMap,reflector,plugboard,swapRotorStockMap)
        return mc
