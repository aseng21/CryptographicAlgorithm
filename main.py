"""
A Feistel cipher implementation using prime numbers for the round function.
Includes visualization tools to help understand the mathematical properties.
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from sympy import primerange
import hashlib


def plot_decimal_pattern(prime):
    # Visualize how 1/prime creates repeating patterns
    seq = get_decimal_sequence(prime)
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(seq)), seq, label=f"1/{prime}")
    plt.xlabel("Position")
    plt.ylabel("Value")
    plt.title(f"Pattern for 1/{prime}")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_mixing_function(prime, input_range):
    # Shows how well our cipher scrambles different inputs
    results = [mix_value(x, prime) for x in input_range]
    plt.figure(figsize=(10, 6))
    plt.plot(input_range, results, label=f"p={prime}")
    plt.xlabel("Input")
    plt.ylabel("Output")
    plt.title("Value Mixing")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_3d_pattern(prime, sequence):
    # Adds a third dimension to better spot patterns or weaknesses
    x = np.arange(len(sequence))
    y = np.array(sequence)
    z = np.sin(np.linspace(0, 2 * np.pi, len(sequence)))

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, label=f"p={prime}")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    ax.set_zlabel("Layer")
    ax.set_title("3D Pattern")
    ax.legend()
    plt.show()


def find_reptend_primes(start, end):
    # These primes give the best mixing properties
    primes = list(primerange(start, end))
    return [p for p in primes if pow(10, p - 1, p) == 1]


def get_decimal_sequence(p):
    # Long division of 1/p reveals useful patterns
    seq = []
    r = 1
    for _ in range(p - 1):
        r = (r * 10) % p
        seq.append((r * 10) // p)
    return seq


def generate_round_keys(key, rounds, prime):
    # Uses SHA-256 for better avalanche effect
    keys = []
    for i in range(rounds):
        data = f"{key}{prime}{i}".encode()
        h = int(hashlib.sha256(data).hexdigest(), 16)
        round_key = h % prime
        keys.append(round_key)
        key = round_key
    return keys


def substitute_value(value, prime, box_size=256):
    # Maps input to a different value using prime patterns
    box = get_decimal_sequence(prime)[:box_size]
    return box[value % len(box)]


def mix_value(x, prime, box_size=256):
    # Three-stage mixing: cubic -> substitute -> cubic
    x = (x ** 3 + 7 * x + 11) % prime
    x = substitute_value(x, prime, box_size)
    return (x ** 3 + 5 * x + 13) % prime


def feistel_round(right, round_key, prime, box_size=256):
    # Core of the Feistel network
    return mix_value((right + round_key) % prime, prime, box_size)


def encrypt_block(block, key, rounds, prime, box_size=256):
    # Process a 16-bit block through the Feistel network
    keys = generate_round_keys(key, rounds, prime)
    left, right = block >> 8, block & 0xFF
    
    for i in range(rounds):
        # XOR and swap
        new_right = (left ^ feistel_round(right, keys[i], prime, box_size)) % 256
        left = right
        right = new_right
    
    return (left << 8) | right


def decrypt_block(block, key, rounds, prime, box_size=256):
    # Reverse the encryption process
    keys = generate_round_keys(key, rounds, prime)
    left, right = block >> 8, block & 0xFF
    
    for i in reversed(range(rounds)):
        new_left = (right ^ feistel_round(left, keys[i], prime, box_size)) % 256
        right = left
        left = new_left
    
    return (left << 8) | right


def encrypt_text(text, prime, key, rounds, box_size=256):
    # Split text into blocks and encrypt each
    blocks = []
    for i in range(0, len(text), 2):
        # Combine pairs of characters
        block = (ord(text[i]) << 8)
        if i + 1 < len(text):
            block |= ord(text[i + 1])
        blocks.append(encrypt_block(block, key, rounds, prime, box_size))
    return blocks


def decrypt_text(blocks, prime, key, rounds, box_size=256):
    # Rebuild text from decrypted blocks
    text = []
    for block in blocks:
        dec = decrypt_block(block, key, rounds, prime, box_size)
        # Only append characters if they're not null bytes
        high = chr(dec >> 8)
        low = chr(dec & 0xFF)
        text.append(high)
        if low != '\x00':  # Only append if not null
            text.append(low)
    return ''.join(text)


class CipherTest:
    def __init__(self, prime, key, rounds, box_size=256):
        self.prime = prime  # For mixing operations
        self.key = key     # Starting key value
        self.rounds = rounds  # Security level
        self.box_size = box_size  # Substitution space

    def test_encryption(self, text):
        print(f"\nEncrypting: {text}")
        start = time.time()
        encrypted = encrypt_text(text, self.prime, self.key, self.rounds, self.box_size)
        elapsed = time.time() - start
        print(f"Got: {encrypted}")
        print(f"Took {elapsed:.3f}s")
        return encrypted, elapsed

    def test_decryption(self, blocks):
        print("\nDecrypting...")
        start = time.time()
        text = decrypt_text(blocks, self.prime, self.key, self.rounds, self.box_size)
        elapsed = time.time() - start
        print(f"Got: {text}")
        print(f"Took {elapsed:.3f}s")
        return text, elapsed

    def run_tests(self, text):
        encrypted, _ = self.test_encryption(text)
        decrypted, _ = self.test_decryption(encrypted)
        print(f"\nOriginal text: '{text}'")
        print(f"Decrypted text: '{decrypted}'")
        assert text.strip() == decrypted.strip(), "Decryption failed!"
        print("\nEverything works!")


if __name__ == "__main__":
    # Quick test
    message = "Hello, World!"
    prime = 61  # Using a reptend prime
    key = 17
    rounds = 10
    box_size = 256

    cipher = CipherTest(prime, key, rounds, box_size)
    cipher.run_tests(message)

    # Show some cool visualizations
    plot_decimal_pattern(prime)
    plot_mixing_function(prime, range(1, 100))
    plot_3d_pattern(prime, get_decimal_sequence(prime))
