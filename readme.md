Group Members: <br>
1. SHUBHANG ARORA [1410110399] <br>
2. SAHIL SHARMA [1410110345]

NAME: <br>
two phase locking

How To Run <br>
python Assignment.py

DESCRIPTION <br>
Simulation of two-phase locking (2PL) protocol for concurrency control, with the wound-wait method for dealing with deadlock.
Input to the program is given via a text file (Input1.txt). Each line has a single transaction operation. The possible operations are: b (begin transaction), r (read item), w (write item), and e (end transaction). Each operation will be followed by a transaction id that is an integer between 1 and 99. For r and w operations, an item name follows between parentheses (item names are single letters from A to Z). An example is given below. <br>
Example Input File: <br>
Input 1: <br>
b1; <br>
r1 (Y); <br>
w1 (Y);<br>
r1 (Z); <br>
b2; <br>
r2 (X); <br>
w2 (X); <br>
w1 (Z); <br>
e1; <br>
r2 (Y); <br>
b3; <br>
r3 (Z); <br>
w3 (Z); <br>
w2 (Y); <br>
e2; <br>
r3 (X); <br>
w3 (X); <br>
e3; <br>

Program first identifies what is the operation in method assignFunction and then it assigns different functions to begin transaction, readLock, writeLock, end transaction. <br>

Output is printed to the console <br>


BUGS: <br>
 If      you     find     a     bug,     please     report     it     at
       https:/github.com/shubhang-arora/two-phase-locking


