import PID

pid = PID.PID()
moisture = 1
for i in range(1000):
    moisture += -0.01
    pid.setPoint(5)
    delta = pid.update(moisture)
    moisture += delta*0.35 if delta > 0 else 0
    print("moisture = %f, delta = %f " %(moisture,delta))
