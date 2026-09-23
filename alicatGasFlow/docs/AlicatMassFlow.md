# Alicat Mass Flow

The Alicat Mass Flow meters can read many different gases.

In order to provide full functionality along with customisation, the builder xml allows you to provide unique gas codes and names for up to 36 different gases.
This allows you to choose *any* of the 206 or so gases available at time of writing, and just the ones you need. **NUMGASES** allows you to specify how many gases you want to be freely available through the GUI.

For example, SiH4 has a gas code of 86 and O2 has a gas code of 11. If only these gases are required, the builder xml would look something like this:


| NUMGASES | GASNUM00 | GASNAME00 | GASNUM00 | GASNAME00 |
| :-------:|:--------:| :--------:|:--------:| :--------:|
| 2        | 86       | SiH4      |12        | O2        |

On the Gas Select GUI, only gases 0 and 2 would be available to select. Although other default values would appear as text monitors, the message buttons which trigger the value to be written would not appear.

## Pure Corrosive Gases

A number of gases, categorised as Pure Corrosive Gases, are only available with the *S-series models. This is approximately gas codes 30-36 and some others. Trying to write these values to the meter will just set it to reading air.