# Prime-Based Encryption Algorithm

A Feistel cipher that uses reptend primes (primes with repeating decimal expansions) 
for data transformation. Built with Python, it includes tools to visualize and 
analyze the cipher's behavior. Uses SHA-256 for key generation and a 3-stage 
nonlinear function.

## Features

1. **Reptend Prime-Based Feistel Network**:
   - Uses cyclic patterns from reptend primes for data transformation
   - SHA-256 based key generation
   - Three-stage nonlinear function: cubic → reptend pattern → cubic
   - Substitution box built from prime's decimal expansion
   
2. **Visualization Tools**:
   - See the repeating patterns in 1/prime expansions
   - Watch how the nonlinear function transforms data
   - 3D view of the prime's cyclic behavior

## Getting Started

### Prerequisites

You'll need these Python libraries:
- `matplotlib`
- `numpy`
- `sympy`
- `hashlib`

### Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the environment:
```bash
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install matplotlib numpy sympy
```

### Usage

1. **Basic Encryption and Decryption**:

```python
from main import CipherTest

message = "Hello, World!"
prime = 61    # A prime with good properties
key = 17      # Any number works
rounds = 10   # More rounds = more security
box_size = 256  # Size of substitution space

# Create cipher and run test
cipher = CipherTest(prime, key, rounds, box_size)
cipher.run_tests(message)
```

2. **Visualizations**:

```python
from main import plot_decimal_pattern, plot_nonlinear_function, plot_3d_pattern

# View the patterns in 1/prime
plot_decimal_pattern(61)

# See how well inputs get scrambled
plot_nonlinear_function(61, range(1, 100))

# Look for patterns in 3D
plot_3d_pattern(61, get_decimal_sequence(61))
```

## Core Functions

### Encryption/Decryption
- `encrypt_text(text, prime, key, rounds)`: Converts text to encrypted blocks
- `decrypt_text(blocks, prime, key, rounds)`: Recovers original text from blocks

### Key Generation
- `generate_round_keys(key, rounds, prime)`: Creates round keys using SHA-256

### Nonlinear Operations
- `transform_value(x, prime)`: Three-stage nonlinear function
- `substitute_value(value, prime)`: Maps inputs using prime patterns
- `feistel_round(right, round_key, prime)`: Core Feistel network operation

### Visualization
- `plot_decimal_pattern(prime)`: Shows patterns in 1/prime
- `plot_nonlinear_function(prime, range)`: Displays scrambling effectiveness
- `plot_3d_pattern(prime, sequence)`: 3D view of patterns

### Prime Number Tools
- `find_reptend_primes(start, end)`: Finds primes with good properties
- `get_decimal_sequence(prime)`: Gets patterns from 1/prime division

## Testing

Run the test suite with:

```bash
python -m unittest test_encryption.py
```

The tests verify that:
1. Encryption followed by decryption recovers the original message
2. The process works with different message lengths
3. The cipher handles various prime numbers and key values
