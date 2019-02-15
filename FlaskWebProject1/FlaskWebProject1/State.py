class DoubleRatchetState(object):
    """description of class"""
    def __init__(self, *args, **kwargs):
        
        self.DHs=bytearray(32) #DH Ratchet key pair (the “sending” or “self” ratchet key)
        self.DHr=bytearray(32) #DH Ratchet public key (the “received” or “remote” key)
        self.RK=bytearray(32)  #32-byte Root Key
        self.CKs=bytearray(32) #32-byte Chain Keys for sending and receiving
        self.CKr=bytearray(32) #32-byte Chain Keys for sending and receiving
        self.Ns=0              #Message numbers for sending and receiving 
        self.Nr=0              #Message numbers for sending and receiving
        self.PN=0              #Number of messages in previous sending chain
        self.MKSKIPPED={}      #Dictionary of skipped-over message keys, indexed by ratchet public key and message number. Raises an exception if too manyelements are stored.

        return super(State, self).__init__(*args, **kwargs)
    
