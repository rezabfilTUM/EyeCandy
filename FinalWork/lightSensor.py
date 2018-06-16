import serial, time
ser = serial.Serial ('/dev/ttyUSB0',9600, timeout=.5)
while True:
      ser.write("L")
      readText = ser.read(10)
      line = ser.readline()
      print readText, "Line: ",line
      time.sleep(3)


