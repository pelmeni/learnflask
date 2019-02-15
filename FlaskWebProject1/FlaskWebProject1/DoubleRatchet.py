class DoubleRatchet(object):
    """The following state variables are tracked by each party:
    • DHs: DH Ratchet key pair (the “sending” or “self” ratchet key)
    • DHr: DH Ratchet public key (the “received” or “remote” key)
    • RK: 32-byte Root Key
    • CKs, CKr: 32-byte Chain Keys for sending and receiving
    • Ns, Nr: Message numbers for sending and receiving
    • PN: Number of messages in previous sending chain
    • MKSKIPPED: Dictionary of skipped-over message keys, indexed by ratchet public key and message number. Raises an exception if too many elements are stored.
    """
    """
    The following choices are recommended for instantiating the cryptographic functions from Section 3.1:
    • GENERATE_DH(): This function is recommended to generate a key pair based on the Curve25519 or Curve448 elliptic curves [7].
    • DH(dh_pair, dh_pub): This function is recommended to return the output from the X25519 or X448 function as defined in [7]. There is no need to check for invalid public keys.
    • KDF_RK(rk, dh_out): This function is recommended to be implemented using HKDF [3] with SHA-256 or SHA-512 [8], using rk as HKDF salt, dh_out as HKDF input key material, and an application-specific byte sequence as HKDF info. 
      The info value should be chosen to be distinct from other uses of HKDF in the application.
    • KDF_CK(ck): HMAC [2] with SHA-256 or SHA-512 [8] is recommended, using ck as the HMAC key and using separate constants as input (e.g. a single byte 0x01 as input to produce the message key, and a single byte 0x02 as input to produce the next chain key).
    • ENCRYPT(mk, plaintext, associated_data): This function is recommended to be implemented with an AEAD encryption scheme based on either SIV or a composition of CBC with HMAC [5], [9]. 
      These schemes provide some misuse-resistance in case a key is mistakenly used multiple times. A concrete recommendation based on CBC and HMAC is as follows:
        – HKDF is used with SHA-256 or SHA-512 to generate 80 bytes of output. The HKDF salt is set to a zero-filled byte sequence equal to the hash’s output length. HKDF input key material is set to mk.
      HKDF info is set to an application-specific byte sequence distinct from other uses of HKDF in the application.
        – The HKDF output is divided into a 32-byte encryption key, a 32-byte authentication key, and a 16-byte IV.
        – The plaintext is encrypted using AES-256 in CBC mode with PKCS#7 padding, using the encryption key and IV from the previous step [10],[11].
        – HMAC is calculated using the authentication key and the same hash function as above [2]. The HMAC input is the associated_data prepended to the ciphertext. The HMAC output is appended to the ciphertext.
    """

    def RatchetInitAlice(state, SK, bob_dh_public_key):
        state.DHs = GENERATE_DH()
        state.DHr = bob_dh_public_key
        state.RK, state.CKs = KDF_RK(SK, DH(state.DHs, state.DHr))
        state.CKr = None
        state.Ns = 0
        state.Nr = 0
        state.PN = 0
        state.MKSKIPPED = {}

    def RatchetInitBob(state, SK, bob_dh_key_pair):
        state.DHs = bob_dh_key_pair
        state.DHr = None
        state.RK = SK
        state.CKs = None
        state.CKr = None
        state.Ns = 0
        state.Nr = 0
        state.PN = 0
        state.MKSKIPPED = {}

    """ RatchetEncrypt() is called to encrypt messages. This function performs a
    symmetric-key ratchet step, then encrypts the message with the resulting message
    key. In addition to the message’s plaintext it takes an AD byte sequence
    which is prepended to the header to form the associated data for the underlying
    AEAD encryption:"""

    def RatchetEncrypt(state, plaintext, AD):
        state.CKs, mk = KDF_CK(state.CKs)
        header = HEADER(state.DHs, state.PN, state.Ns)
        state.Ns += 1
        return header, ENCRYPT(mk, plaintext, CONCAT(AD, header))
    
    """RatchetDecrypt() is called to decrypt messages. This function does the following:
    • If the message corresponds to a skipped message key this function decrypts
    the message, deletes the message key, and returns.
    • Otherwise, if a new ratchet key has been received this function stores any
    skipped message keys from the receiving chain and performs a DH ratchet
    step to replace the sending and receiving chains.
    • This function then stores any skipped message keys from the current
    receiving chain, performs a symmetric-key ratchet step to derive the relevant
    message key and next chain key, and decrypts the message.
    If an exception is raised (e.g. message authentication failure) then the message
    is discarded and changes to the state object are discarded. Otherwise, the
    decrypted plaintext is accepted and changes to the state object are stored:"""
    
    def RatchetDecrypt(state, header, ciphertext, AD):
        
        plaintext = TrySkippedMessageKeys(state, header, ciphertext, AD)
        
        if plaintext != None:
            return plaintext
        
        if header.dh != state.DHr:
            SkipMessageKeys(state, header.pn)
            DHRatchet(state, header)

        SkipMessageKeys(state, header.n)
        state.CKr, mk = KDF_CK(state.CKr)
        state.Nr += 1
        return DECRYPT(mk, ciphertext, CONCAT(AD, header))

    def TrySkippedMessageKeys(state, header, ciphertext, AD):
        
        if (header.dh, header.n) in state.MKSKIPPED:
            mk = state.MKSKIPPED[header.dh, header.n]
            del state.MKSKIPPED[header.dh, header.n]
            return DECRYPT(mk, ciphertext, CONCAT(AD, header))
        else:
            return None

    def SkipMessageKeys(state, until):
        if state.Nr + MAX_SKIP < until:
            raise Error()
        if state.CKr != None:
            while state.Nr < until:
                state.CKr, mk = KDF_CK(state.CKr)
                state.MKSKIPPED[state.DHr, state.Nr] = mk
                state.Nr += 1

    def DHRatchet(state, header):
        state.PN = state.Ns
        state.Ns = 0
        state.Nr = 0
        state.DHr = header.dh
        state.RK, state.CKr = KDF_RK(state.RK, DH(state.DHs, state.DHr))
        state.DHs = GENERATE_DH()
        state.RK, state.CKs = KDF_RK(state.RK, DH(state.DHs, state.DHr))