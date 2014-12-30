import unittest
from EnigmaDynamicFactory import EnigmaDynamicFactory
from Util import Util


class TestEnigmaDynamicFactory(unittest.TestCase):
    def setUp(self):
        self.factory=EnigmaDynamicFactory()

        self.machineConfig={
        "CIPHER_MODULE": {
            "PLUGBOARD": {
                "ID": "PLGBRD",
                "wiring": {
                    "0": [
                        "0"
                    ],
                    "1": [
                        "2"
                    ],
                    "2": [
                        "1"
                    ]
                }
            },
            "REFLECTOR": {
                "ID": "RFLCTR",
                "wiring": {
                    "0": [
                        "0"
                    ],
                    "1": [
                        "2"
                    ],
                    "2": [
                        "1"
                    ]
                }
            },
            "ROTOR_STOCK": [
                {
                    "ID": "0",
                    "notch": [
                        1
                    ],
                    "wiring": {
                        "0": [
                            0
                        ],
                        "1": [
                            2
                        ],
                        "2": [
                            1
                        ]
                    }
                }
            ]
        },
        "SWAPPING_MODULE": {
            "L1_L2_MAPPER": {
                "ID": "L1L2MPPR",
                "wiring": {
                    "0": [
                        0
                    ],
                    "1": [
                        2
                    ],
                    "2": [
                        1
                    ]
                }
            },
            "L1_ROTOR_STOCK": [
                {
                    "ID": "0",
                    "notch": [
                        2
                    ],
                    "wiring": {
                        "0": [
                            0
                        ],
                        "1": [
                            2
                        ],
                        "2": [
                            1
                        ]
                    }
                }
            ],
            "L2_ROTOR_STOCK": [
                {
                    "ID": "0",
                    "notch": [
                        0
                    ],
                    "wiring": {
                        "0": [
                            0
                        ],
                        "1": [
                            2
                        ],
                        "2": [
                            1
                        ]
                    }
                }
            ]
        }
    }

    def testCreateCipherModuleFromConfig(self):
        module=self.factory.createCipherModuleFromConfig(self.machineConfig)
        self.assertIsNotNone(module)
        self.assertIsNotNone(module["ROTOR_STOCK"])
        self.assertIsNotNone(module["PLUGBOARD"])
        self.assertIsNotNone(module["REFLECTOR"])
    def testCreateSwappingModuleFromConfig(self):
        module=self.factory.createSwappingModuleFromConfig(self.machineConfig)
        self.assertIsNotNone(module)
        self.assertIsNotNone(module["L1_ROTOR_STOCK"])
        self.assertIsNotNone(module["L2_ROTOR_STOCK"])
        self.assertIsNotNone(module["L1_L2_MAPPER"])


    def testCreateEnigmaMachineFromConfig(self):
        mc=self.factory.createEnigmaMachineFromConfig(self.machineConfig)
