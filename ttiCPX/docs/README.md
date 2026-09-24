INTRODUCTION
------------
This is the EPICS support module for the
Thurlby Thandar Instruments (TTi) CPX200DP Programmable Bench Power Supply

USAGE
-----


One template is provided here:

1) ttiCPX.template
This instatiates all the records associated with the controller's 
functionality


The user interface is presently available via EDM screens. 
Starting with the root screen: 
ttiCPX.edl

Serial communications is managed via EPICS streamDevice, usin the protocol file:
ttiCPX.protocol

MAINTAINERS
-----------

Current maintainers:
* Ian Gillingham (Diamond Light Source) - ian.gillingham@diamond.ac.uk

First created December 2014.


