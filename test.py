import master_socketer
master_socketer.connect()
data=[0]*16
while True:
    i=int(input("enter Motor number:"))
    if i>=0 and i<16:
        j=int(input("enter Motor Angle:"))
        data[i]=j
        master_socketer.slow(data)
    elif i<0:
        master_socketer.end_wireless()
    elif i==100:
        data=eval(input("enter all motor angles"))
        master_socketer.slow(data)