# Python plugin for controlling energenie OOK devices
#
# Author: DerekGn
#
"""
<plugin key="RfmEnergOok" name="RfmUsb Energenie OOK" author="DerekGn" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://github.com/DerekGn/rfmusb-mihome-ook-plugin">
    <description>
        <h2>RfmUsb Energenie Ook Devices Plugin</h2>
        <br/>
        The RfmUsb Energenie Ook Devices Plugin allows controlling various Energenie OOK devices.
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Supports MIHO07, MIHO021, MIHO022, MIHO023 double sockets</li>
            <li>Supports MIHO008, MIHO024, MIHO025, MIHO026, MIHO071, MIHO072, MIHO073 light switches</li>
            <li>Can pair switch when switch or socket placed in pairing mode</li>
        </ul>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Switch - On off control</li>
        </ul>
        <h3>Configuration</h3>
        Serial port is the name of the 
    </description>
    <params>
        <param field="SerialPort" label="Serial Port" width="150px" required="true" default="/dev/serial1"/>
        <param field="Mode1" label="Home Addresses" width="300px" required="true" default="6C6C6"/>
        <param field="Mode4" label="Tx Power Level" width="100px" required="true" default="0">
            <options>
                <option label="-2 dbm" value="-2"/>
                <option label="-1 dbm" value="-1"/>
                <option label="0 dbm" value="0"/>
                <option label="1 dbm" value="1"/>
                <option label="2 dbm" value="2"/>
                <option label="3 dbm" value="3"/>
                <option label="4 dbm" value="4"/>
                <option label="5 dbm" value="5"/>
                <option label="6 dbm" value="6"/>
                <option label="7 dbm" value="7"/>
                <option label="8 dbm" value="8"/>
                <option label="9 dbm" value="9"/>
                <option label="10 dbm" value="10"/>
                <option label="11 dbm" value="11"/>
                <option label="12 dbm" value="12"/>
                <option label="13 dbm" value="13"/>
                <option label="14 dbm" value="14"/>
                <option label="15 dbm" value="15"/>
                <option label="16 dbm" value="16"/>
                <option label="17 dbm" value="17"/>
                <option label="18 dbm" value="18"/>
                <option label="19 dbm" value="19"/>
                <option label="20 dbm" value="20"/>
            </options>
        </param>
        <param field="Mode5" label="Tx Count" width="100px" default="5">
            <options>
                <option label="Five" value="5"/>
                <option label="Eight" value="8"/>
                <option label="Thirteen" value="13"/>
            </options>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

class BasePlugin:

    GET_FIRMWARE_VERSION = "g-fv\n"

    SerialConn = None
    enabled = False
    lastCommand = ""

    def __init__(self):
        #self.var = 123
        return
    
    def onStart(self):
        homeAddresses = Parameters["Mode1"].Split(";")

        # Can have up too 5 switches per home address, Switch ALL, 1, 2, 3, 4
        if(len(Devices) < len(homeAddresses) * 5):
            Domoticz.Log("Creating Devices")
            for x in range(0, len(homeAddresses) * 5):
                Domoticz.Device(Name="Home Switch"+str(x), Unit=x, Type=244, SubType=62).Create()

            Domoticz.Log("Created "+str(len(Devices))+" Devices")

        SerialConn = Domoticz.Connection(Name="Serial Connection", Transport="Serial", Protocol="None", Address=Parameters["SerialPort"], Baud=115200)
        SerialConn.Connect()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        global SerialConn
        if (Status == 0):
            Domoticz.Log("Connected successfully to: "+Parameters["SerialPort"])
            SerialConn = Connection
            sendCommand("g-fv\n")
        else:
            Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"])
            Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"]+" with error: "+Description)
        return True

    def onMessage(self, Connection, Data):
        strData = Data.decode("ascii")
        Domoticz.Debug("Received data from RfmUsb ["+strData+"]")

        if(lastCommand == BasePlugin.GET_FIRMWARE_VERSION):
            return True

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("Connection '"+Connection.Name+"' disconnected.")
        return

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

# Support functions
def sendCommand(Command):
    global SerialConn, lastCommand
    lastCommand = Command
    SerialConn.Send(Command)
def AddSwitches(Prefix, BaseIndex):
    for x in range(BaseIndex, BaseIndex + 5):
        if((x % 5) == 0):
            Domoticz.Log("Creating Device [Home "+str(Prefix)+" Switch All]")
        else:
            Domoticz.Log("Creating Device [Home "+str(Prefix)+" Switch"+str(x)+"]")
        #Domoticz.Device(Name="Home "+str(Prefix)+" Switch"+str(x), Unit=x, TypeName="Switch").Create()

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return