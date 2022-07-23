# Building CircuitPython for Sapling

```
MICROPY_PY_COLLECTIONS_DEQUE 1
```

per https://learn.adafruit.com/building-circuitpython/linux you need the arm-none-eabi toolchain 10 q4 major. Older/newer versions do not work.

Flynn's notes/research into frozen module
- seems like it makes the import faster
- which could be good for pycubed (mainly a performance advantage during development since PyCubed module will not be imported often on orbit)
https://forum.micropython.org/viewtopic.php?t=4510
