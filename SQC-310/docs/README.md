INTRODUCTION
------------

This is the EPICS support module for the
quartz crystal microbalance (QCM) SQC-310

USAGE
-----

One template is provided here:
1) SQC-310.template
this instantiate all the records associated with the controller's
functionality


The user inteface is presently available via EDM screen.
Starting with the root screen:
SQC-310.edl

Serial communications is managed via EPICS streamDevice , using the protocol file:
SQC-310.proto

MAINTENANCE
------------

Current maintainers:
* Laura Arcidiacono (Diamond Light Source) laura.arcidiacono@diamond.ac.uk

First created June 2021.
