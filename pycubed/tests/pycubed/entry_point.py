"""if code.py is present, main.py doesn't run. So we run any setup necessary before
the entrypoint
"""
try:
    import setup
except ImportError: # no setup no problem
    pass
import main