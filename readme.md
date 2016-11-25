Group Members:
1. SHUBHANG ARORA [1410110399]
2. SAHIL SHARMA [1410110345]

NAME:
two phase locking

How To Run
python Assignment.py

DESCRIPTION
Simulation of two-phase locking (2PL) protocol for concurrency control, with the wound-wait method for dealing with deadlock.
Input to the program is given via a text file (Input1.txt). Each line has a single transaction operation. The possible operations are: b (begin transaction), r (read item), w (write item), and e (end transaction). Each operation will be followed by a transaction id that is an integer between 1 and 99. For r and w operations, an item name follows between parentheses (item names are single letters from A to Z). An example is given below.
Example Input File:
Input 1:
b1;
r1 (Y);
w1 (Y);
r1 (Z);
b2;
r2 (X);
w2 (X);
w1 (Z);
e1;
r2 (Y);
b3;
r3 (Z);
w3 (Z);
w2 (Y);
e2;
r3 (X);
w3 (X);
e3;

Program first identifies what is the operation in method assignFunction and then it assigns different functions to begin transaction, readLock, writeLock, end transaction.

Output is printed to the console
