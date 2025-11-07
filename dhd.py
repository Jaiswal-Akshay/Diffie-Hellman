import streamlit as st
import random
from Crypto.Util import number

letters = r"""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|-=[]\:"<>?;',./` """
key_bits = 16
prime_bits = 8
seed = random.Random(123456789)

st.title("Diffie Hellman")

if st.session_state.get("my_key"):
    my_key = st.session_state["my_key"]
    parameter = st.session_state["parameter"]
    generator = st.session_state["generator"]
    prime = st.session_state["prime"]
else:
    parameter = seed.getrandbits(key_bits)
    generator = seed.getrandbits(key_bits)
    prime = number.getPrime(prime_bits)
    my_key = (generator ** prime) % parameter

    st.session_state["my_key"] = my_key
    st.session_state["prime"] = prime
    st.session_state["parameter"] = parameter
    st.session_state["generator"] = generator

st.write("Your key")
st.code(my_key)
their_key = st.number_input(label= "Their Key",step=1, placeholder="123456", value=None)


def decryption(m, key):
    backset = key % len(letters)
    decrypted = ""

    for i in range(len(m)):
        new = letters.index(m[i]) - backset
        decrypted += letters[new]

    return decrypted

def encryption(n, key):
    offset = key % len(letters)
    encrypted = ""
    
    for i in range(len(n)):
        asi = (letters.index(n[i]) + offset) % len(letters)
        encrypted += letters[asi]
    return encrypted


col1,col2 = st.columns(2)

send_ms = col1.text_area("Enter original message here...")
recv_ms = col2.text_area("Enter encoded message here...")

send_btn = col1.button("Send", width="stretch")
recv_btn = col2.button("Recieve", width="stretch")


if send_btn:
    if their_key:
        key = (their_key**prime) % parameter
        enc = encryption(send_ms, key)
        st.write("Encrypted message:")
        st.code(enc)
    else:
        st.warning("The Other person's key is required")

if recv_btn:
    if their_key:
        key = (their_key**prime) % parameter
        dec = decryption(recv_ms, key)
        st.write("Decrypted message:")
        st.write(dec)
    else:
        st.warning("The Other person's key is required")
