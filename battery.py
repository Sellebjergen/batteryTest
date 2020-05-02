import psutil
import time
import sys
import matplotlib.pyplot as plt


#TODO maybe try to process the data? make a project out of it!
#TODO run the program while you work on it (in a separate window)
#TODO create a "-a" which shows a box plot of all the different times from one percent to another. 


def getBatteryPercentage():
    battery = psutil.sensors_battery()
    percent = str(battery.percent)

    with open("battery_data.txt", "w") as file:
        start = time.time()
        while True:
            battery = psutil.sensors_battery()
            if percent == battery.percent:
                time.sleep(10)
                print("... ... ...")
            else:
                print(str(battery.percent) + "% at time " + str(time.time() - start))
                file.write(str(battery.percent) + "%," + str(time.time() - start) + "\n")
                percent = battery.percent


def getGraph():
    percentages = []
    times = []

    with open("battery_data.txt", "r") as file:
        lines = file.readlines()
        for x in lines:
            x = x.split(",")

            percentage = x[0].rstrip("%")
            time = x[1].rstrip("\n")
           
            percentages.append(int(percentage))
            times.append(float(time) / 60)

    plt.plot(times, percentages)
    plt.xlabel("time in min")
    plt.ylabel("percentage of computer")
    plt.show()


if __name__ == "__main__":
	if len(sys.argv) <= 0: print("you need to provide an argument")
	if "-g" in sys.argv or "--graph" in sys.argv:
		print("creating graph") 
		getGraph()
	elif "-r" in sys.argv or "--record" in sys.argv:
		print("recording")
		getBatteryPercentage()		


