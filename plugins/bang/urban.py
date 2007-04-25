#!/usr/bin/python
"""Look up a word in the Urban Dictionary.
!urban word"""

def bang(pipein, arguments, event):
    import SOAPpy

    server = SOAPpy.SOAPProxy("http://api.urbandictionary.com/soap")
    urban = server.lookup("7df8eccad5391dbbb45e81fa77f4c1a8", arguments)

    if len(urban) > 1:
        return (arguments + ": " + urban[0].definition + "\n", None)

    return ("Could not find a definition for " + arguments + "\n", None)
    
