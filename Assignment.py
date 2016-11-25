__author__ = 'Sahil Sharma   [1410110345]' \
             'Shubhang Arora [1410110399]'
import copy
import os

#filename=raw_input("Please enter the file name: ")
#print(filename)
class lockTable:
    def __init__(self, lockedDataItem, transactionID, lockState):
        self.lockedDateItem=lockedDataItem
        self.lockState=lockState
        self.waitingTransactions=[]
        self.lockHeldBy=[]
        self.lockHeldBy.append(transactionID)

    def addWaitingTransaction(self, transactionID):
        self.waitingTransactions.append(transactionID)

    def addLockHeld(self, transactionID):
        self.lockHeldBy.append(transactionID)

    def changeLockState(self, LS):
        self.lockState = LS

class transactionTable():
    def __init__(self, transactionID, timestamp, transactionState):
        self.transactionID=transactionID
        self.timestamp=timestamp
        self.transactionState=transactionState
        self.lockedResoures=[]
        self.blockedOperation=[]
        #self.blockedOperation=blockedOperations

    def changeTransactionState(self, state):
        self.transactionState = state

    def addBlockedOperation(self, operation):
        self.blockedOperation.append(operation)

    def addLockedResource(self, resourceName):
        self.lockedResoures.append(resourceName)

lockTableObjects=[]
transactionTableObjects=[]
waitingTransactions=[]
RL = "readlock"
WL = "writeLock"
inputList = []
A = "Abort "
W = "Waiting"
C = "Committed"
AC = "Active"
returnflag=1


#specify the input file.
with open(os.listdir(os.getcwd())[12], 'r') as text:
    for line in text:
        inputList.append(line)

#this method takes a string and returns the digit in that string.
#This wa used in the program to get the transaction number form the input string
def get_digit(str1):
    c = ""
    for i in str1:
        if i.isdigit():
            c += i
    return int(c)

#this method adds a new object to the transactionTableObject every time a new transaction is started
def beginTransaction(str):
    tranNumber = get_digit(str)
    print "Begin Transaction %d" % (tranNumber)
    temp = int(len(transactionTableObjects))+1
    transactionTableObjects.append(transactionTable(tranNumber, temp, AC))

#for a string input, this method returns the resource name(1 of X,Y or Z) and the transactionID
def resourcenID(inputLine):
    if inputLine.find("X")!=-1:
        resourceName = "X"
    elif inputLine.find("Y") != -1:
        resourceName = "Y"
    elif inputLine.find("Z") != -1:
        resourceName = "Z"
    transactionID = get_digit(inputLine)
    return resourceName, transactionID


#this method take the transaction ID and input and searched for the transaction in the transactionTable
def searchTransactionID(transactionID):
    for transaction in transactionTableObjects:
        if transaction.transactionID == transactionID:
            return transaction

#this method is used to put a resource under read lock by a specific transaction.
#it checks for conflicting locks and calls the wound-wait routine to get take care of deadlock situations.
def readLock(inputLine):
    resourceName = resourcenID(inputLine)[0]
    transactionID= resourcenID(inputLine)[1]
    flag=0
    length = len(lockTableObjects)
    if length != 0:
        for i in range(0,length):
            if lockTableObjects[i].lockedDateItem == resourceName:
                flag = 1
                if lockTableObjects[i].lockState == WL:         #This checks if the resource taht's been requested in under a writeLock by any other transaction anfd if thats the case, wound wait is called
                    print "Conflicting Write lock: data item " + resourceName + " is under ReadLock by Transaction %d" %(lockTableObjects[i].lockHeldBy[0])
                    print "calling wound-wait mechanism"
                    woundWait(searchTransactionID(transactionID), searchTransactionID(lockTableObjects[i].lockHeldBy[0]), lockTableObjects[i], inputLine)
                elif lockTableObjects[i].lockState == RL:  #if resources is just under readLock, the new transaction is added to the list of transactions that hold a readLock on the resource
                    lockTableObjects[i].addLockHeld(transactionID);
                    searchTransactionID(transactionID).addLockedResource(resourceName)
                    print "Putting the data item " + resourceName + " under ReadLock by Transaction %d" %(lockTableObjects[i].lockHeldBy[0])
        if flag == 0:
            lockTableObjects.append(lockTable(resourceName, transactionID, RL))         #adding a new resource to the locktable if its not already in the lockTable
            searchTransactionID(transactionID).addLockedResource(resourceName)
            print "Putting the data item " + resourceName + " under ReadLock by Transaction %d" %transactionID
    else:
        lockTableObjects.append(lockTable(resourceName, transactionID, RL))
        searchTransactionID(transactionID).addLockedResource(resourceName)
        print "Putting the data item " + resourceName + " under ReadLock by Transaction %d" %(lockTableObjects[0].lockHeldBy[0])


#this method is used to put a resource under read lock by a specific transaction.
#it checks for conflicting locks and calls the wound-wait routine to get take care of deadlock situations.
def writeLock(inputLine):
    resourceName = resourcenID(inputLine)[0]
    transactionID= resourcenID(inputLine)[1]
    flag = 0
    length = len(lockTableObjects)
    if length != 0:
        for i in range(0, length):
            if lockTableObjects[i].lockedDateItem == resourceName:
                flag = 1
                if lockTableObjects[i].lockState == RL:
                    if len(lockTableObjects[i].lockHeldBy) == 1:
                        if lockTableObjects[i].lockHeldBy[0] == transactionID:  #checks to see if the resources is under readLock by the same transaction
                            lockTableObjects[i].lockState = WL
                            print "Upgrading Readlock to WriteLock on data item "+resourceName+" for transaction %d" %transactionID
                        else:
                            print "data item " + resourceName + "is under ReadLock by multiple transaction. "
                            print "call Wound Wait" #call wound wait if its under readlock by another transaction
                            woundWait(searchTransactionID(transactionID), searchTransactionID(lockTableObjects[i].lockHeldBy[0]), lockTableObjects[i], inputLine)
                    else:
                        count = 0
                        for lockedresource in lockTableObjects:
                            if lockedresource.lockedDateItem == resourceName:
                                for tempheldby in lockedresource.lockHeldBy:
                                    if tempheldby == transactionID:
                                        count += 1
                        #calling wound wait if its under readLock by multiple transactions
                        woundWait(searchTransactionID(transactionID), searchTransactionID(lockTableObjects[i].lockHeldBy[count]), lockTableObjects[i], inputLine)
                elif lockTableObjects[i].lockState == WL:
                    print "Conflicting WriteLock: data item " + resourceName + " is under WriteLock by Transaction %d" %(lockTableObjects[i].lockHeldBy[0])
                    print "call wound wait"
                    woundWait(searchTransactionID(transactionID), searchTransactionID(lockTableObjects[i].lockHeldBy[0]), lockTableObjects[i], inputLine)
        if flag == 0:
            lockTableObjects.append(lockTable(resourceName, transactionID, WL)) #appending a new resource to the lockTable
            searchTransactionID(transactionID).addLockedResource(resourceName)
            print "data item " + resourceName + " is under WriteLock by Transaction %d" %(lockTableObjects[0].lockHeldBy[0])
    else:
        lockTableObjects.append(lockTable(resourceName, transactionID, WL))
        searchTransactionID(transactionID).addLockedResource(resourceName)


#the wound wait deadlock prevention mechanism
def  woundWait(requestingTransaction, holdingTransaction, lockedResource, operation):
    if requestingTransaction.timestamp < holdingTransaction.timestamp:
        holdingTransaction.changeTransactionState(A)
        print "Aborting Transaction %d" %holdingTransaction.transactionID
        requestingTransaction.changeTransactionState(W)
        requestingTransaction.addBlockedOperation(operation)
        waitingTransactions.append(requestingTransaction)
        unlock(holdingTransaction.transactionID)        #unlocking all the resources of the transaction that was aborted by wound wait
    else:
        requestingTransaction.changeTransactionState(W) #adds the transaction to the waitingTransactions list
        print "changing transaction state for transaction %d to blocked" %requestingTransaction.transactionID
        if checkDuplicateOperation(operation, requestingTransaction):
            requestingTransaction.addBlockedOperation(operation)
        if checkDuplicateTransaction(requestingTransaction):
            waitingTransactions.append(requestingTransaction)

#this method checks to see if the transaction is already in the waitingTransactions list
def checkDuplicateTransaction(transaction):
    for t in waitingTransactions:
        if t.transactionID == transaction.transactionID:
            return 0
    return 1


def checkDuplicateOperation(operation, transaction):
    for blockedOperation in transaction.blockedOperation:
        if blockedOperation == operation:
            return 0
    return 1

#this method checks the state of the transaction the method is for so that if the transaction is aborted, the operation  can be ignored
def checkState(operation):
    resourceName = resourcenID(operation)[0]
    transactionID= resourcenID(operation)[1]

    length = len(transactionTableObjects)
    if length != 0:
        for i in range(0,length):
            if transactionTableObjects[i].transactionID == transactionID and transactionTableObjects[i].transactionState == W:
                transactionTableObjects[i].addBlockedOperation(operation)
            elif transactionTableObjects[i].transactionState == A:
                operation = ""
                print("Operation Ignored")
    return operation

#This method deletes unlocks all the resourced held by the transactionID passed to it
def unlock(transactionID):
    print "Unlocking all resources held by transaction %d" %transactionID
    for transaction in transactionTableObjects:
        if transaction.transactionID == transactionID:
            for lock in transaction.lockedResoures:
                for resource in lockTableObjects:
                    if resource.lockedDateItem == lock:
                        if len(resource.lockHeldBy) == 1:
                            lockTableObjects.remove(resource)  #if the same sources is held by multiple transactions, remove this transaction from a that list of transactions holding the lock
                        else:
                            resource.lockHeldBy.remove(transactionID) #if only this transaction has any kind of lock on the resource, remove the resource from the lockTable completely.
    startWaitingTrans()

#see if any transactions that were waiting for resources can now be resumed
def startWaitingTrans():
    print "checking if there are any transactions waiting on the freed resources"
    for transaction in waitingTransactions:
        if transaction.transactionState == A:
            waitingTransactions.remove(transaction)
        else:
            blockOpCopy = copy.deepcopy(transaction.blockedOperation)
            for blockedOperation in transaction.blockedOperation:
                transaction.transactionState = AC         #we activate the transaction in the waitingTransactions list and pull the operations that are in the waitlist
                print "attempting operation " + blockedOperation
                assignFunction(blockedOperation)  #call the assignFunction method on the waiting operation and see if the transaction can now continue
                if transaction.transactionState != W:
                    blockOpCopy.remove(blockedOperation)
            transaction.blockedOperation = blockOpCopy
            if len(transaction.blockedOperation) == 0:
                waitingTransactions.remove(transaction)


# called when the function reaches its end. This method commits the transaction and frees all its resources.
def functionEnd(operation):
    tranNumber = get_digit(operation)
    for transactoin in transactionTableObjects:
        try:
            if transactoin.transactionID == tranNumber and transactoin.trasnsactionState != A:
                print "Committing transaction %d" % tranNumber
                transactoin.transactionState = C
        except AttributeError:
            print "Committing transaction %d" % tranNumber
            transactoin.transactionState = C
    unlock(tranNumber)

#this method procesees the input operation string and calls the required function accordingly.
def assignFunction(operation):
    if operation.find('b') == 1:
        operation = checkState(operation)

    if operation.find('b')!=-1:
        beginTransaction(operation)
    elif operation.find('r') !=-1:
        print "Read operation"
        readLock(operation)
    elif operation.find('w') != -1:
        print "write operation"
        writeLock(operation)
    elif operation.find("e") != -1:
        print "end"
        functionEnd(operation)

for operation in inputList:
    assignFunction(operation)




