#Modern WWII Enigma
>"If a trick is overused, it's less likely that anyone will expect us to use it again” 

##Introduction

The above motto is a qoute from a comic movie, and hence this fun project came into existance , it aims to revive the famous (ehm, for being cracked) Enigma machine .But why bother ? 

Protecting your privacy today? Well, good luck. you are using tools that you don't know how it's working (you shouldn’t trust), and when they are cracked you'll barely know after it's too late .So if you can add an extra level or encryption of your data even if it's a homegrown technique, it'll make the problem for your attacker just a little bit harder .Modern Enigma tries to provide a step in this direction.

Alan Turing is considered to be the father of modern computing, at his time electro-mechanical machines were used to perform computations. This is a software implementation with enhanced features to prevent some weakness points in original Enigma.

#####Modern Enigma is not patented and will never be

#Enigma Background

###What's Enigma?
![Enigma](http://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/EnigmaMachineLabeled.jpg/640px-EnigmaMachineLabeled.jpg)

Generally speaking it's an encryption machine used by Germans during WWWII to encrypt the communication between forces , the allied were able to crack it ( Alan Turing is the most famous team member), and that led to their defeat .Deciphering Enigma  messages is still in progress ,look for the M4 project if your interested !

###What went wrong with Enigma that led to its fall?
Many Design and operating problems allowed the allied to crack it, just to name a few

* Design
    * No letter is mapped to itself
    * Constraints on Rotor usage in certain days of month
    * Fixed number plug board cables
    * Rotor stepping in a predictable clockwise motion, US implemented SIGABA to fix this problem

* Operation
    * Message indicator settings were chosen by operators none randomly (CIL)
    * Predictable clear text (Cribs)
    * Using less secured means to send the same message 

* For more info:
    * Weakness points in enigma, [more info](http://cromwell-intl.com/security/history/enigma.html "for more info")
    * SIGABA working, [more info](http://ucsb.curby.net/broadcast/thesis/thesis.pdf)

##Modern Engima

###Modern Enigma Features:
* It's a protocol that can be implemented by many environments; currently we provide Python code as the reference implementation 
* Dynamic configuration of the machine based on Model Token, thus no single machine with fixed wiring that can be reverse engineered 
* A new random per msg setting is setup for the operator, eliminating the lazy habits for not changing machine offset per message 
* More Rotors and larger rotor size to increase the key space   
* Non clockwise rotor stepping
* Non linear Rotor swapping during encryption process
* Multilevel Encryption each consists of various rounds
* Multiple different machines (2 for now), are used to encrypt a message within single level
* After all, it's just software, just some lines of code ;)

##Sample Usage:
Here We will explain the minimum code to use the machine , a lot of defaults will be selected for you , The tool is very flexibe and many intesting scenarios could be applied

* First things first , let's create a machine 
    * Here we let the tool create a random model for us , use it to create a machine of this model , a model is a string that we could use to create the exact same machine on sender and reciever  

```Python
    #Create a random model name 
    baseMachineModelName=EnigmaConfigGenerator().createRandomModelName()
    #Create a Machine 
    baseMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel(baseMachineModelName)
    #For now just set default settings 
    baseMachine.adjustMachineSettings()
```

* We need to a minimum of  2 machines for each Level, let's create another one
```Python
    levelMachineModelName=EnigmaConfigGenerator().createRandomModelName()
    levelMachine=EnigmaDynamicFactory().createEnigmaMachineFromModel(levelMachineModelName)
    levelMachine.adjustMachineSettings()
```

* Create a level settings , you can think of a level as a unit of encryption , it uses two machines to encrypt some text/stream , levels can be cascaded for further security. For now let's use the current machine settings , we could generate any settings we want , but let's be simple for now 
```Python
    level=Level(baseMachine.getMachineSettings(),levelMachine.getMachineSettings())
```

* Cool,Now lets create a sample message "Hello Enigma !" , convert it to byte stream and set it as the level input 

```Python
    msg="Hello Enigma !"
    #Util Class provides many useful methods , we will see later , for now lets convert this string into bytes suitable to be processed
    msgSeq=Util.encodeStringIntoByteList(msg)
    level.inputMsg=msgSeq
```

* OK , let's Encrypt some text !, use a LevelEncryptor, it needs the level and the actual machines to do the work

```Python
    levelEncryptor=LevelEncryptor(baseMachine,levelMachine,level)
    level=levelEncryptor.encryptLevel()
```
* let's see the output , use Util to convert the byte stream into hex string
```Python
    encryptedMsg=Util.convertByteListIntoHexString(level.outputMsg)
```
    * Sample output ( it'll be different each time )
    05F5112B6A010B4FC3632217DB2919617D21C514FEC150A86776359E5A7A2DE59B66A6807889C3D6EAFDB6316360230AAC4F2D446BE938D0D692B06D97522634D272AED7546CD04FBEAE52689A5E5336DB6C7DB2712FEB3B3529FEADB93679067218DC021E649AB91AED39447998830ACFC9F8AB9151A6D80EA45F2EF972EC9499CB1EE91958C8BA940377A92A2DD55D5692A6CD261B12E94483F20EAB53F835E01DB6F4D18C6759EEB01917519F2BC93EF63974FAEA13CDCBFC0AAE84E2C63F4F9B033F95BC1F877C9D7DB43E2C4A39460408518EE30ADB293CF64318DB3A6199B4717AEE74647FDBA5B4DC02CCC270CB17D7EA10AC591BA1CA3B4486FFE7EAD4F24B98A2769E2DDC669C640D77D12EF6398551BBBF0FBBD082DFFAC2BA55C3CA0445A9E3CAE9FD

* OK let's try to decrypt this back into the original msg,use a LevelDecryptor
```Python
    levelDecryptor=LevelDecryptor(baseMachine,levelMachine,level)
    resultLevel=levelDecryptor.decryptLevel()
```
* Let's print the result(decrypted) level msg
```Python
    print(Util.decodeByteListIntoString(resultLevel.inputMsg))
```
    * Output
        Hello Enigma !
##### Congratulations !!, that was your first Modern Enigma encrypted communication!, Please read further into documentation to understand what's going on and customize the tool to best suit your needs

### Main Concepts 
You need to understand the idea of Rotors, Reflectors, Swapping and stepping
####Rotor
####Reflector
####Inside a machine 
for the image belows follow the number to get an idea about how signal is transfered into different machine modules
![Main signal path](https://github.com/mrfawy/ModernEnigma/blob/master/documentation/diagrams/signalPath.jpg)
####Level overview
####Inside a Level
### How secure Is Modern Enigma?
According to Schneider’s Law "Any person can invent a security system so clever that he or she can't imagine a way of breaking it.", which means that people create a cipher that they themselves can't break, and then use that as evidence they've created an unbreakable cipher. Also According to Kerckhoffs's principle "A cryptosystem should be secure even if everything about the system, except the key, is public knowledge”.

Based on these 2 principles we provided an open source machine and tried to make it's security based on the key that will have many parameters to alter the machine working.
We tried to fix the original Machine problems , provided a new protocol with different machines needed for multiple level , minimized any component dependcy in the machine ,we simplified a machine creation operation so you can use a new set of machines for each message ,you can use it even as a one time pad if it's works for you.

So the right question should be is it secure enough for your needs ? You descide,we are still investigating the weaknesses points  of this tool.

##### Any help from an expert on the security assessment or cryptoanalysis of this Modern Enigma is highly appreciated; it’s still in early development phase.

###Mathematics of Modern Enigma:
Security can be largely affected by a key size  and available states the machine can take (key space ) , here we show how you can calculate key space for sample machine:

* Counting Equations:
    * Number of available rotor wirings for a rotor of size N=N!, e.g. a rotor of size 64 =>64! ~ 1.3 x 10^9 the number of atoms in the visible universe (~ 10^80)
    * Number of ways to pick n rotors each of size of N in order =P(N,n) , e.g Wolfram couldn't calculate P(64!,3)"Result cannot be determined using current methods" 
    * Number of ways to set rotors offsets for n rotors each of size N  = N ^ n
    * Number of ways to select M pair for plug board of size N=N! / ( (N-2M)! x M! x 2^M ) 
    * number of ways to select an integer (32 bit)=2 ^ 32
* Cipher Module:
    * Number of available Cipher rotors per machine = n , we recommend larger n >100

* Swapping Module:
    * Level 1 : pick l1 rotors each of size 64 (see above)
    * Level 2 :pick l2 rotors each of size K (see above)
    * l1 l2 mapper As a rotor like above
    * l2 Cipher mapper as a rotor like above
    * Number of ways to select active signals of size s= C(64,s)

* You can calculate the total key space and the different possible machine configurations , but don't let the number deceive you , it only works if you are trying a brute force attack .

* Deriving A key size :
    * To encrypt/decrypt a single level 2 machines are needed
    * for each machine we need :
        * n bits to represent n cipher rotors orders, and offsets
        * l1 bits to represent l2 cipher rotors orders, and offsets
        * l2 bits to represent l2 cipher rotors orders, and offsets
        * m bits to represent wiring mapping of l2 Cipher mapper
    * around 10-12 * integer(32 bit),of various flags that alter the working of the algorithm


* An example for a Cipher module of 100 rotors each of size of 64 :
    * Number of bits to store the rotor offset [0-64] = 6 bits
    * Number of bits ( Key) to store machine setting of N rotors =m(no of bit to represent N)xN +6xN
    * Result # of bits =7x100+6x100=1200 bits ( Only for this module, while a typical machine will have 2 more modules)

* it's worth mentioning here that the key is part of the operating instructions, it's like the manual for the algorithm , Thus it'll be a large number of bits.

####Please don't let the large key size fool you. Any help from an expert is appreciated


Modern Enigma Protocol:
====================
* General Guideline:
    * In this protocol we define a certain steps that has to be performed , for each step a certain algorithm will be choosed. As each step has it's own attack vectors and it's algorithm has it's volunerablities , each major version of this protocol will try to cope with that .Backward compatibility is not currently one of our main design goals.
    * Main design Goals :
        * Confidentiality 
        * Message integrity 
        * Close to the original enigma rotor based design (as its main substitution box technique)
        * Operating instructions should be part of the key; no fixed decision should be made by the machine 
        * Generation of a new machine should be an easy and a low cost operation
        * Extreme flexibility in designing your own machine down to  the wiring level 
        * Platform independence, ability to de/encrypt using any platform/environment, extremely low resources (e.g. card) are not considered
        * Generation of human readable machine description, allowing the reconstruction of a machine 
        * No use of patented or platform specific algorithms 
        * It's a fun project, not the next Symmetric key polyalphabetic encryption technology, please keep this in mind 
    * Out of scope:
        * Not to be used for mission critical and/or large files 
        * Key management/sharing process is not handled , use any key management technique you desire.
            Because the keys and machine descriptions are human readable, old tricks can still work(remember our Motto) .Be creative and use overused techniques like calling your friend by phone and telling him part of the key ,SMS another part , Facebook another part, and if you are not in a hurry you can send a postal mail ;).of course all of theses platform might be tracked (well ,you know it's ).If the attacker was able to track all of these communications ,well, I think this guy            deserves to read your messages any ways and you are totally screwed , nothing can help you my friend ;)



* Message Integrity:
    * Perform a secure hashing of the original message, and encrypt it using a machine X 
    * All hashing functions will use a non patented algorithm: Whirlpool is selected
    * When exchanging the keys for the message, include this hashed value 
    * As only Sender and receiver knows how to decrypt this value (the encrypted checksum), origin integrity is satisfied
    * As checksum will be different for any changed/corrupted message , message integrity is satisfied
    * if Sender and receiver agree to use only certain pair of keys for each different correspondent , Ripudation of origin can be satisfied, The problem as with all symmetric key tools , a lot of keys will be needed which might not be practical for large parties communication

* Un/padding a message:
    * User will have a choice to select Block size for each level
    * For each En/Decryption step a padding procedure should follow to match the block size
    * Padding procedure:
        * add a one byte in the beginning of the sequence 
        * calculate the total size of the new sequence 
        * add any extra bytes as needed, select bytes at random from sequence 
        * set the value of the first byte to the number of added padding, 00 if no padding performed
    * Unpadding Procedure:
        * ignore the last number of bytes equal to the value of the first byte in the sequence 


* Multi level , each level needs 2 machines , the first one needs a base machine , and a chosen one 
* we will refer to base machine as B , and level machine as M
* we will refer to  machine settings as s , and it's per message settings as p
* like in original Enigma you need only to know ( exchange) s between sender and receiver
* each level is as following:
* Encrypt as enigma Msg : 
    * Generate Per Msg setting by machine B ->Bp
    * Encrypt Per Msg Bp using Ms,o times->EBp
    * Encrypted Msg with Bp,p times ->msg_Bp
    * Merge EBp with msg_Bp ->EMsg
* Shuffle EMsg,s1 times->SEmsg
* Encrypt SEMsg with Bs , i times ->x
* Encypt x with Ms ,j time ->y
* Encrypt as enigma Msg : 
    * Generate per msg setting in machime Mp ->MP 
    * Encrypt MP with Bs ,k times ->EMp
    * Encrypt y with Mp , l times -> Y_Mp
    * Merge ( join ) EMp + M0 -> W
* Shuffle W ,s2 times->S
* Encrypt S with Ms ,m tims ->R
* Encrypt R with Bs, n times->E ( encrypted)

* Each level input :
    * B , Base Machine settings
    * M , Chosen level machine Settings
* Each level output:
    * i , int 
    * j , int 
    * k , int 
    * l , int 
    * m , int 
    * n , int 
    * s , int shuffle seed number ,to be able to deshuffle back

* Block mechanism
    * Cipher rotor size can take range of 1 byte to 4 bytes ( int 32 bit range)
    * for selected Rotor size , determine how many bytes needed (e.g 2 bytes)
    * now for each input byte , output will use 2 bytes
    * according to setting , determines number of bytes to be batch procesed from range 1 to rotorsize/256
    * each byte will be maaped to corresponing place 1>0,255 , 2 ->256,512,..
    

* TODO : generate  random machine name of size n, hashit , machine model is the first m numbers from the hashed value , use this number as seed to build machine

* For extra level of scrambling , you can take the output of one level , feed it into other level as many times you need,
each level will need a different machine though

License Terms disclaimer:
-------------------------
Modern Enigma is licensed under MIT terms .Modern Engima is not patented and will never be . Like any tool it can be used for good or the bad 
The main goal was to enhance user privacy for good means ,Project Team holds no responsiblitiy for any illegal use or damage .

References:
----------------
what it is ?
https://www.youtube.com/watch?v=G2_Q9FoD-oQ
http://enigma.louisedade.co.uk/howitworks.html
https://www.youtube.com/watch?v=mcX7iO_XCFA
http://www.cryptomuseum.com/crypto/enigma/working.htm
https://www.youtube.com/watch?v=ncL2Fl6prH8
http://en.wikipedia.org/wiki/Enigma_machine


* Suggessted protocol
http://hireme.geek.nz/modern-enigma-system.html
http://digital.library.louisville.edu/utils/getfile/collection/etd/id/449/filename/450.pdf
http://www.cs.sjsu.edu/faculty/stamp/students/Sigaba298report.pdf

what's wrong with it ?
https://www.youtube.com/watch?v=V4V2bpZlqx8
http://www.mlb.co.jp/linux/science/genigma/enigma-referat/node6.html
http://cromwell-intl.com/security/history/enigma.html
http://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma


Modern Encryption techniques:
https://www.gnupg.org/gph/en/manual.html

history : http://www.eng.utah.edu/~nmcdonal/Tutorials/EncryptionResearchReview.pdf



