# TextMimic

A tool to hide text using custom templates !

## Installation
```sh
git clone https://github.com/mathysEthical/TextMimic.git
```

## Usage

```sh
python3 mimic.py -h
usage: mimic.py [-h] encodedFile template mode

TextMimic is a tool to hide text using custom templates

positional arguments:
  encodedFile  Encoded file path exemple encoded/cipher.txt
  template     Template to use, for exemple templates/event.txt
  mode         Mode: encode or decode

options:
  -h, --help   show this help message and exit
```

## To encode
```sh
python3 mimic.py encoded/cipher.txt templates/event.txt encode
```

## To decode

```sh
python3 mimic.py encoded/cipher.txt templates/event.txt decode
```