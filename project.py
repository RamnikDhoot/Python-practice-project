from platform import platform # just import platform does not work
from platform import machine
from platform import processor
from platform import system
from platform import version
from platform import python_implementation, python_version_tuple







dir(os)
#show you a list of the entities contained inside an imported module

print("test")
# platform(aliased = False, terse = False)
# aliased → when set to True (or any non-zero value) it may cause the function to present the alternative underlying layer names instead of the common ones;
# terse → when set to True (or any non-zero value) it may convince the function to present a briefer form of the result (if possible)

print(machine())
#AMD64

print(platform())
#Windows-10-10.0.22621-SP0

print(platform(1))
#Windows-10-10.0.22621-SP0

print(platform(0, 1))
#Windows-10

print(processor())
#AMD64 Family 23 Model 104 Stepping 1, AuthenticAMD

print(system())
#Windows

print(version())
#10.0.22621

print(python_implementation())
for atr in python_version_tuple():
    print(atr)


