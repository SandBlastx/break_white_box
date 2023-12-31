
---

# White Box Breaker

## Overview

This project aims to break a white-box implementation developed in Rust. In the `breaker` folder, you'll find Python scripts that implement various attack methods inspired by research in the field, particularly the techniques described in the paper [On the ineffectiveness of internal
encodings - revisiting the dca attack on white-box cryptography](https://eprint.iacr.org/2018/301.pdf) .

## Project Structure

- `player_db`: Contains all the logs and the database generated by the Tracer tool.
- `tmp`: Includes different players with various versions of keys.
- `breaker`: Contains Python scripts to analyze and attack the white-box implementation.
  - `analyse.py`: Contains different functions implementing the attack methods.
  - `breaker.py`: The main script that generates log files, parses them, and converts them into traces stored in the `Traces` folder.

## Main Usage

To break the white-box implementation, the main script in `breaker.py` can be executed as follows:

```python
python breaker.py -g 1
```

- `-g 1`: Generate traces and perform the attack.

## Other Parameters

- `nb_trace`: Number of traces to generate.
- `path_pe`, `path_se`, `path_player`: Paths to relevant directories.
- `path_tracer`: Path to the Tracer tool.
- `path_log`: Path to the player database.
- `address_read`: Addresses of interest to perform the attack.

## Attack Workflow

0. Anaylse the flow of player using Tracer tool.
1. Generate traces using the Tracer tool.
2. Parse log files and convert them into traces.
3. Perform the attack to recover the key.
4. The recovered key is displayed.

