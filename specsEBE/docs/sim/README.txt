The ebe python module contains a simulator and client for the Specs EBE-4.

The client can communicate with and control the real device.
The simulator can be used to test an EPICS IOC or the python client.

Run Simulator:

  $ python ebe/simapp.py -i 127.0.0.1 -p 8080

Run Client App:

  $ python ebe/app.py -h                                         # View Help
  $ python ebe/app.py -i 127.0.0.1 -p 8080                       # Read Device Name
  $ python ebe/app.py -i 127.0.0.1 -p 8080 --param 10            # Get param 10
  $ python ebe/app.py -i 127.0.0.1 -p 8080 --param 10 --value 2  # Set param 10 to 2
