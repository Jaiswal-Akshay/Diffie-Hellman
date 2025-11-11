import streamlit as st
import random
from Crypto.Util import number

letters = r"""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|-=[]\:"<>?;',./` """

key_bits  = 16
prime_bits = 8

SEED = 123456789
rng_params = random.Random(SEED)
def randfunc(n: int) -> bytes:
    return rng_params.getrandbits(8 * n).to_bytes(n, "big")
rng_private = random.SystemRandom()

if "p_" not in st.session_state:
    # same on both ports
    p_ = number.getPrime(prime_bits, randfunc=randfunc)
    g_ = 2 + (rng_params.getrandbits(key_bits) % max(1, p_ - 3))

    # different per session / per port
    a_ = 2 + rng_private.randrange(max(1, p_ - 3))

    A_ = pow(g_, a_, p_)
    st.session_state.update({"p_": p_, "g_": g_, "a_": a_, "A_": A_})
else:
    p_ = st.session_state["p_"]
    g_ = st.session_state["g_"]
    a_ = st.session_state["a_"]
    A_ = st.session_state["A_"]

st.title("Diffie Hellman Demo")
st.subheader("Parameters")

st.write("p (prime modulus)"); st.code(p_)
st.write("g (generator)");     st.code(g_)

st.write("Your public key (A)"); st.code(A_)
their_key = st.number_input("Their public key (B)", step=1, min_value=0, value=None, placeholder=0)

def derive_shared(B):
    if B < 2 or B > p_ - 2:
        return None
    return pow(int(B), a_, p_)

def encrypt(msg, key):
    offset = key % len(letters)
    out = []
    for ch in msg:
        if ch in letters:
            i = (letters.index(ch) + offset) % len(letters)
            out.append(letters[i])
        else:
            out.append(ch)  # pass-through unknown characters
    return "".join(out)

def decrypt(msg, key):
    back = key % len(letters)
    out = []
    for ch in msg:
        if ch in letters:
            i = (letters.index(ch) - back) % len(letters)
            out.append(letters[i])
        else:
            out.append(ch)
    return "".join(out)

col1, col2 = st.columns(2)
send_ms = col1.text_area("Enter original message here...")
recv_ms = col2.text_area("Enter encoded message here...")

send_btn = col1.button("Send")
recv_btn = col2.button("Receive")


if send_btn:
    shared = derive_shared(their_key)
    if shared is None:
        st.warning("Please enter a valid peer public key (2 ≤ B ≤ p-2).")
    else:
        enc = encrypt(send_ms, shared)
        st.write("Encrypted message:")
        st.code(enc)

if recv_btn:
    shared = derive_shared(their_key)
    if shared is None:
        st.warning("Please enter a valid peer public key (2 ≤ B ≤ p-2).")
    else:
        dec = decrypt(recv_ms, shared)
        st.write("Decrypted message:")
        st.code(dec)
