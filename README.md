Modern WWII Engima
========
[Enigma](http://l2.yimg.com/bt/api/res/1.2/3xLnpXMlOtk3jVr7Xx7iug--/YXBwaWQ9eW5ld3M7cT04NQ--/http://media.zenfs.com/en-US/blogs/en-us-visit-britain-travel/Enigma.jpg "Engima")

What's Engima ?
----
http://ucsb.curby.net/broadcast/thesis/thesis.pdf

-suggessted protocol
---
http://hireme.geek.nz/modern-enigma-system.html
http://digital.library.louisville.edu/utils/getfile/collection/etd/id/449/filename/450.pdf

SIGABA 
http://www.cs.sjsu.edu/faculty/stamp/students/Sigaba298report.pdf

M4 Project 
what went wrong with Enigma that led to it's fall ?
----------------------------
http://cromwell-intl.com/security/history/enigma.html
http://ucsb.curby.net/broadcast/thesis/thesis.pdf

WhyModern ?
-----
Alan Turing is considered to be the father of modern computing , at his time electro-mechanical machines were used to perform computations.This is a software implementation with enhanced features to prevent some  weakness points in original Enigma that allowed Turing to crack it .

Features:
---
* Dynamic configuration of the machine based on Model Token , thus no single machine with fixed wiring that can be reverse engineered 
* A new random per msg setting is setup for the operator , eliminating the lazy habits for not changing machine offset per message 
* More Rotors and more special characters used , to increase the key space   
* After all , it's just a software you can curry easily , it's just some lines of code ;)

Mathematics of Modern Enigma :
----------------------------
Number of availalbe rotor wiring=64! ~~ 1.3×10^9 × the number of atoms in the visible universe (~~ 10^80)
Number of availalbe rotors per machine = N , we recommend larger n >100
Number of bits to store the rotor offset [0-64] = 6 bits
Number of bits ( Key) to store machine setting of N rotors =m(no of bit to represent N)xN +6xN
e.g. for a 100 rotors machine =7x100+6x100=1200 bits


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


INTERNAL MODERN Enigma Protocol WORKING:
====================
* Multi level , each one needs 2 machines , the first one needs a base machine , and a chosen one 
* each level is as following:
..Generate Per Msg B ->Bp
..Encrypt as enigma Msg : -> EMsg
....Encrypt Per Msg Bp using Bs,o times->EBp
....Merge with Encrypted Msg with Bp ->EMsg
..Encrypt EMsg with Bs , i times ->x
..Encypt x with Ms ,j time ->y
..Generate per msg setting in machime Mp ->MP ( as M per message )
..Encrypt MP with M ,k times ->EMp
..Encrypt y with Mp , l times -> M0
..Merge ( join ) EMp + M0 -> W
..Shuffle W ->S
..Encrypt S with M ,m tims ->R
..Encrypt R with B, n times->E ( encrypted)
* Each level input :
.. B , Base Machine settings
.. M , Chosen level machine Settings
* Each level output:
.. i , int 
.. j , int 
.. k , int 
.. l , int 
.. m , int 
.. n , int 
.. s , int shuffle seed number ,to be able to deshuffle back
* For extra level of scrambling , you can take the output of one level , feed it into other level as many times you need,
each level will need a different machine though



* for shuffling , and reverse shuffling , there is a key 
http://stackoverflow.com/questions/3541378/reversible-shuffle-algorithm-using-a-key

USer our implementation of PRNG 
http://www0.cs.ucl.ac.uk/staff/d.jones/GoodPracticeRNG.pdf
