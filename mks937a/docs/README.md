# mks937a
MKS 937A pressure gauge controller EPICS support module

INTRODUCTION
------------
This is the EPICS support module for the
MKS 937A Gauge Controller.

The specification is based on MKS document:
HPS937-232-485MAN


USAGE
-----

Several EPICS templates are provided here:

mks937a.template
mks937aPirg.template
mks937aPirgGroup.template
mks937aPirgDummy.template
mks937aImg.template
mks937aImgGroup.template
mks937aImgMean.template
mks937aImgDummy.template
mks937aGauge.template
mks937aGaugeGroup.template
mks937aInterlock.template

example:
# Initialise templates for an MKS937A Multi-Sensor System
# Ian Gillingham - 23/9/04
#
# substitutions:
# device  - device name
# port    - serial port (steam device code ie /ty/0/1 => ty_0_1)
# channel - MKS 937A channel number (1-5)
# dom     - domain
# id      - ID
# c       - ADC card number
# s       - ADC signal number
# Controller
#
file mks937a.template
{
pattern {    device        ,  port   }
        { FE03I-VA-GCTLR-01,  ty_70_1}
		    { FE03I-VA-GCTLR-02,  ty_70_2}
		    { FE03I-VA-GCTLR-03,  ty_70_3}
		}




# Gauges
#
# substitutions:
# device  - device name
# port    - serial port (steam device code ie /ty/0/1 => ty_0_1)
# channel - MKS 937A channel number (1-4)
#
# IMGs
# Inverted Magnetron guages on channels CC & A (1 & 2)
file mks937aImg.template
{
pattern {     device     ,  port  ,  channel }
        { FE03I-VA-IMG-01, ty_70_1, 1}
		    { FE03I-VA-IMG-02, ty_70_1, 2}
		    { FE03I-VA-IMG-03, ty_70_2, 1}
		    { FE03I-VA-IMG-04, ty_70_2, 2}
		    { FE03I-VA-IMG-05, ty_70_3, 1}
		    { FE03I-VA-IMG-06, ty_70_3, 2}
		}

# Gauges
#
# substitutions:
# device  - device name
# port    - serial port (steam device code ie /ty/0/1 => ty_0_1)
# channel - MKS 937A channel number (1-4)
#
# PIRGs
# pirani guages on channels B1 & B2 (4 & 5)
file mks937aPirg.template
{
pattern {     device      ,  port  ,  channel }
        { FE03I-VA-PIRG-01, ty_70_1, 4}
		    { FE03I-VA-PIRG-02, ty_70_1, 5}
		    { FE03I-VA-PIRG-03, ty_70_2, 4}
		    { FE03I-VA-PIRG-04, ty_70_2, 5}
		    { FE03I-VA-PIRG-05, ty_70_3, 4}
		    { FE03I-VA-PIRG-06, ty_70_3, 5}
		}


# Combination Gauges
#
# substitutions:
# domain - Front End domain
# ID    	- gauge id value
# card 	- Card number of ADC carrier
# signal	- ADC channel number
#
file mks937aGauge.template
{
pattern { dom, id,  c, s }
        { FE03I, 01, 60, 0}
		    { FE03I, 02, 60, 1}
		    { FE03I, 03, 60, 2}
		    { FE03I, 04, 60, 3}
		    { FE03I, 05, 60, 4}
		    { FE03I, 06, 60, 5}
		}


The user interface is presently available via EDM screens. 
Starting with the root screen: 

mks937a.edl
mks937aGauge.edl
mks937aImg.edl
mks937aImgIlks.edl
mks937aImgWarning.edl
mks937aPirg.edl
mks937aPirgIlks.edl

Serial communications protocol is described by the EPICS streamDevice protocol file:
mks937a.protocol

MAINTAINERS
-----------

Current maintainers:
* Ian Gillingham (Diamond Light Source) - ian.gillingham@diamond.ac.uk

First created December 2014.
