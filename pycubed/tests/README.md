# PyCubed Test Harness

## Why?

This test harnes facilitates automated testing in a controlled environment on PyCubed, and can address a variety of issues. It works for both integration tests and unit tests of specific functionality. 

This is especially useful because it is far easier to log data on a host computer, and easier to control the environment on PyCubed from the host computer, and make modifications at runtime to achieve desirable conditions on PyCubed.

## Resources

https://tinkering.xyz/async-serial/

## How?

The `board` fixture creates a connection to PyCubed, and validates that the board is mounted correctly. There is a hardcoded list of tests parametrizing the `name_of_test` fixture. This fixture is requested by the `test`. Because the fixture is parametrized, `test()` runs for each `name_of_test`. Each test folder has `src/` directory with files that will be copied onto PyCubed, and a optionally a `runner.py` which exports a `TestRunner` class. The `board.json` file specifies a number of configuration options, such as the name of the CIRCUITPY drive, name of the source directory (the code that normally runs, _not_ the test code), a list of patterns to ignore (as specified by `shutil`), an incude list of specific files that are copied in exception to the ignore patterns, an entry point folder which holds code that will run before `main.py` on PyCubed, a list of errors to ignore (such as missing peripherals).

## Guide

Install test dependencies on your host machine

```sh
pip install -r tests/requirements.txt
```

Plug in an assembled CubeSat.

Test the integrity of subsystems of an assembled satellite

```sh
pytest -k sat_integrity --version Sapling.3
```
