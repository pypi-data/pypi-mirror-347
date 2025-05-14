



### import renardo_reapy.runtime just hang

-> the import python command is probably not ran with the same python that is configured in REAPER

### error with python 3.13 ?



### overall reapy chicken and eggs problems

- reapy needs to be available inside reaper, i.e. installed in the python environment that is configured
- when accessing any reapy function even thoses that configure the connection all the module is imported : its not possible to run configure_reaper or other methods from tools if reapy/REAPER are not in sync ie using the same python installation