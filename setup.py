from distutils.core import setup
import py2exe

setup(console=['multi-agent.py'],
        options={"py2exe":{"includes":["numpy","numpy.core","numpy.core.multiarray"]}})