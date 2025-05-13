# 0.5.0

* fix LSS baudrate configuration handling
* provide LSS store configuration functionality (bitrate and node id)

# 0.4.12

* update object dictionary on type change in PDOs

# 0.4.11

* check limits for numeric datatypes when using `object_dictionary.write`
* check if object is existing when using `object_dictionary.write`

# 0.4.10

* fix upload of objects with size 0 (use segmented transfer instead of expetited)

# 0.4.9

* harding stack by checking message length

# 0.4.8

* adding .stop method to CANBusNetwork
* remove .shutdown method from scheduler base class and add .stop to SyncScheduler

# 0.4.7

* adding .shutdown method to schedulers

# 0.4.6

* fix object_dictionary.read in LSS service

# 0.4.5

* fix unit tests for LSS

# 0.4.4

* fix SDO server startup when entering OPERATIONAL directly

## 0.4.3

* fix eds generation

## 0.4.2

* fix size in PDO mapping (it's bits not bytes)

## 0.4.1

* fix eds format datatype

## 0.4.0

* rename "adapter" to "network"

## 0.3.x

* completed missing services

## 0.2.0

* SDO server: segmented, expetited and block transfer working for upload and download
* default of 127 SDO servers per node

## 0.1.1

* adding long description in setup.py

## 0.1.0

* initial version
