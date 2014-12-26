Modern WWII Engima
========
>"If a trick is overused , it's less likely that anyone will expect us to use it again " 

The above motto is a qoute from a comic movie, and hence this fun project came into existance , it aims to revive the famouse (ehm, for being cracked) Enigma machine .But why bother ? 

Protecting your privacy in todays world ? well, goodluck . you are using tools that you don't know it's working (you shuoldn't trust), and when they are cracked you'll know after it's too late .So if you can add an extra level or encryption of your data even if it's a homegrown technique, it'll make the problem for your attacker just a little bit harder .Modern Enigma tries to provide a step in this direction .

Alan Turing is considered to be the father of modern computing , at his time electro-mechanical machines were used to perform computations.This is a software implementation with enhanced features to prevent some  weakness points in original Enigma .

###Modern Enigma is not patented and will never be

What's Engima ?
----
![Enigma](http://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/EnigmaMachineLabeled.jpg/640px-EnigmaMachineLabeled.jpg)

Generally speaking it's an encryption machine used by germans during WWWII to encrypt the communication between forces , the allied were able to crack it ( Alan Turing is the most famouse team member), and that led to their defeat .Deciphering Enigma  messages is still in progress ,look for the M4 project if your intersteed !

what went wrong with Enigma that led to it's fall ?
---------------------------------------------------

Many Design and operating problems allowed the allied to creack it , just to name a few

* Design
    * No letter is mapped to itself
    * Constraints on Rotor usage in certain days of month
    * Fixed number plugboard cables
    * Rotor Stepping in a predictable clockwise motion, US implemented SIGABA to fix this problem

* Operation
    * Message indicator settings were choosed by operators non randomly (CIL)
    * Predictable clear text ( Cribs)
    * Using less secured means to send the same message 

* For more info:
    * Weakness points in enigma ,[more info](http://cromwell-intl.com/security/history/enigma.html "for more info")
    * SIGABA working ,[more info](http://ucsb.curby.net/broadcast/thesis/thesis.pdf)

Modern Enigma Features:
-------------------------
* It's a protocol that can be implemented by many environments, currently we provide Python code  as the reference implementation 
* Dynamic configuration of the machine based on Model Token , thus no single machine with fixed wiring that can be reverse engineered 
* A new random per msg setting is setup for the operator , eliminating the lazy habits for not changing machine offset per message 
* More Rotors and more larger rotor size to increase the key space   
* Non clockwise rotor stepping
* Non linear Rotor swapping during encryption process
* MultiLevel Encryption each conists of various rounds
* Multiple different machines( 2 for now) , are used to encrypt a message within single level
* After all , it's just a software ,just some lines of code ;)

Example Usage :
-------------------

Mathematics of Modern Enigma :
----------------------------
* Counting Equations:
* Number of availalbe rotor wirings for a rotor of size N=N!, e.g. a rotor of size 64 =>64! ~ 1.3 x 10^9 the number of atoms in the visible universe (~ 10^80)
* Number of ways to pick n rotors each of size of N in order =P(N,n) , e.g Wolfram couldn't calculate P(64!,3)"Result cannot be determined using current methods" 
* Number of ways to set rotors offsets for n rotors each of size N  = N ^ n
* Number of ways to select M pair for plugboard of size N=N! / ( (N-2M)! x M! x 2^M ) 
* number of ways to select an integer (32 bit)=2 ^ 32
* Cipher Module:
    * Number of availalbe Cipher rotors per machine = n , we recommend larger n >100

* Swapping Module:
    * Level 1 : pick l1 rotors each of size 64 (see above)
    * Level 2 :pick l2 rotors each of size K (see above)
    * l1 l2 mapper As a rotor like above
    * l2 Cipher mapper as a rotor like above
    * Number of ways to select active signals of size s= C(64,s)

* You can calculate the total key space and the different possible machine configurations , but don't let the number deceive you , it only works if you are trying a brute force attack .Accrdoing to Schneier's Law "Any person can invent a security system so clever that he or she can't imagine a way of breaking it.", which means that people create a cipher that they themselves can't break, and then use that as evidence they've created an unbreakable cipher.Also According to Kerckhoffs's principle "A cryptosystem should be secure even if everything about the system, except the key, is public knowledge".That's why we are still Investigating the weaknesses of this tool.
* Deriving A key size :
    *To encrypt/decrypt a signle level 2 machines are needed
    *for each machine we need :
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
* Again don't let the large key size fool you .
* Any help from an expert on the security assestement or a peer review of this Modern Enigma is highly appreciated ,it's still in early development phase.

-suggessted protocol
---
http://hireme.geek.nz/modern-enigma-system.html
http://digital.library.louisville.edu/utils/getfile/collection/etd/id/449/filename/450.pdf
http://www.cs.sjsu.edu/faculty/stamp/students/Sigaba298report.pdf


Modern Enigma Protocol:
====================
* General GuidLine :
    * In this protocol we define a certain steps that has to be performed , for each step a certain algorithm will be choosed. As each step has it's own attack vectors and it's algorithm has it's volunerablities , each major version of this protocol will try to cope with that .Backward compatiblity is not currently one of our main design goals.
    * Main desing Gaols :
        * Confideintiality 
        * Message integrity 
        * Close to the original enigma rotor based design ( as it's main subistition box technique)
        * Operating instructions should be part of the key , no fixed decision should be made by the machine 
        * Generation of a new machine should be an easy and a low cost operation
        * Extreme felixibility in desgining your own mahcine down to  the wiring level 
        * Platform independece , ability to de/encrypt using any platform/environment , extremly low resources(e.g. card) are not considered
        * Generation of human readable machine description , allowing the reconstruction of a machine 
        * No use of patented or platform specific algorthims 
        * It's a fun project , not the next Symmetric key polyalphabetic encryption technology , please keep this in mind 
    * Out of scope :
        * Not to be used for mission critical and/or large files 
        * Key management/sharing process is not handled , use any key mangement technique you desire.
            Because the keys and machine descriptions are human readable, old tricks can still work(remember our Motto) .Be creative and use overused techniques like calling your firend by phone and telling him part of the key ,SMS another part , Facebook another part,and if you are not in a hurry you can send a postal mail ;).ofcourse all of theses platform might be tracked (well ,you know it's ).If the attacker was able to track all of these communications ,well, I think this guy
            deserves to read your messages any ways and you are tottaly screwed , nothing can help you my firend ;)



* Message Integrity:
    * Perfrom a secure hashing of the original message,encrypt it using a machine X 
    * All hashing function's will use a non patented algorithm: Whirlpool is selected
    * when exchanging the keys for the message , include this hashed value 
    * As only Sender  and reciever knows how to decrypt this value ( the encrypted checksum), origin integrity is satisfied
    * As checksum will be different for any changed/corrpted message , message intigrity is satisfied
    * if Sender and reciever agree to use only certian pair of keys for each different correspondent , Ripudation of orogin can be satisfied,The probelm as with all symmetric key tools , a lot of keys will be needed which might not be practical for large parties communication

* Un/padding a message :
    * User will have a choice to select Block size for each level
    * for each En/Decryption step a padding procedure shuold follow to match the block size
    * Padding procedure:
        * add a one byte in the begining of the sequence 
        * calculate the total size of the new sequence 
        * add any extra bytes as needed , select bytes at random from sequence 
        * set the value of the first byte to the number of added padding , 00 if no padding performed
    * Unpadding Proedure:
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

* For extra level of scrambling , you can take the output of one level , feed it into other level as many times you need,
each level will need a different machine though


* http://www.larc.usp.br/~pbarreto/WhirlpoolPage.html
* for shuffling , and reverse shuffling , there is a key 
http://stackoverflow.com/questions/3541378/reversible-shuffle-algorithm-using-a-key

USer our implementation of PRNG 
http://www0.cs.ucl.ac.uk/staff/d.jones/GoodPracticeRNG.pdf


References:
----------------
what it is ?
https://www.youtube.com/watch?v=G2_Q9FoD-oQ
http://enigma.louisedade.co.uk/howitworks.html
https://www.youtube.com/watch?v=mcX7iO_XCFA
http://www.cryptomuseum.com/crypto/enigma/working.htm
https://www.youtube.com/watch?v=ncL2Fl6prH8
http://en.wikipedia.org/wiki/Enigma_machine


what's wrong with it ?
https://www.youtube.com/watch?v=V4V2bpZlqx8
http://www.mlb.co.jp/linux/science/genigma/enigma-referat/node6.html
http://cromwell-intl.com/security/history/enigma.html
http://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma


Modern Encryption techniques:
https://www.gnupg.org/gph/en/manual.html

history : http://www.eng.utah.edu/~nmcdonal/Tutorials/EncryptionResearchReview.pdf


