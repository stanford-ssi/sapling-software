"""Entry point to the program, which allows user to specify setup that will run
before main.py
"""
try:
    import setup
except ImportError: # no setup no problem
    pass
import main