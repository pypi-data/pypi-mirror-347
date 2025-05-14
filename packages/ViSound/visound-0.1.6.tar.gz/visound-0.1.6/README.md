# ViSound

Library to convert images to sounds.

Refer to the wiki [here](https://github.com/dheerajshenoy/ViSound/blob/main/WIKI.md)

## Introduction

This is just a standalone library for use in other programs that can make use of `ViSound` capabilities. On it's own `ViSound` doesn't do anything. You have to use it in some way to get the output and play the audio yourself.

## Installation

ViSound can be installed using pip:

```
pip install visound
```

## Features

* Sonify images in a number of different ways
* Output the audio to a file or stdout
* Apply effects

## Traversal Modes

You can traverse the given input images in different ways to get different audio output. The following modes are currently supported.

* Left To Right
* Right to Left
* Top to Bottom
* Bottom to Top
* Circle Inward
* Circle Outward

## Usage

`visound <path to an image> --play --verbose`

## Dependencies

* numpy
* opencv-python
* sounddevice
* soundfile

# TODO

- [X] Traversal
    - [X] Left to Right
    - [X] Right to left
    - [X] Top to bottom
    - [X] Bottom to top
    - [X] Circular inward
    - [X] Circular outward
- [X] Apply effects to the output audio
- [ ] Allow for custom pixel to frequency mapping
- [X] CLI client
- [ ] Machine learning to apply effects and custom image traversal
