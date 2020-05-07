import psutil
import time
import sys
import matplotlib.pyplot as plt


# TODO create a "-a" which shows a box plot of all the different times from one percent to another.
# TODO make it possible to see 2 graphs from 2 files side by side.


def getBatteryPercentage(file):
    battery = psutil.sensors_battery()
    percent = str(battery.percent)

    with open(file, "w") as file:
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


def getGraph(files):
    for file in files:
        percentages = []
        times = []

        with open(file, "r") as file:
            lines = file.readlines()
            for x in lines:
                x = x.split(",")

                percentage = x[0].rstrip("%")
                time = x[1].rstrip("\n")

                percentages.append(int(percentage))
                times.append(float(time) / 60)

        plt.plot(times, percentages, label=file.name)

    plt.xlabel("time in min")
    plt.ylabel("percentage of computer")
    plt.legend()
    plt.show()


def getBarGraph(files):
    highest_percent = 100
    lowest_percent = 0

    for file in files:
        percentages = []
        times = []
        differenceTimes = []

        with open(file, "r") as file:
            lines = file.readlines()
            for x in lines:
                x = x.split(",")

                percentage = x[0].rstrip("%")
                time = x[1].rstrip("\n")

                percentages.append(int(percentage))
                times.append(float(time))

        for x in range(len(times) - 1):
            differenceTimes.append(times[x + 1] - times[x])

        percentages = percentages[0: len(differenceTimes)]

        plt.bar(percentages, differenceTimes, align='edge', width=-0.8, label=file.name)

    plt.xlim(highest_percent, lowest_percent)
    plt.xlabel("percentage")
    plt.ylabel("time in seconds")
    plt.legend()
    plt.show()


def dashedline(amount):
    print("- " * amount)


def getHelp():
    print(" - - - - - ")
    print("\n Welcome to the battery tester. Here is a list of all functions to be used.")
    dashedline(45)
    print("-h               --help                  a list of functions of which to perform")
    print("-r <file.txt>    --record <file>         start a new recording of battery")
    print("-g <files>       --graph <files>         shows a graph of battery percentages over time")
    print("-b <files>       --bargraph <files>      shows a bargraph of how much time between each percentage")
    dashedline(45)
    print("")


if __name__ == "__main__":
    if len(sys.argv) <= 0:
        print("you need to provide an argument")
        exit()
    if len(sys.argv) <= 2 and (not ("-h" in sys.argv or "--help" in sys.argv)):
        print("please provide at least one fil after the argument.")
        exit()

    files = sys.argv[2:]

    if "-g" in sys.argv or "--graph" in sys.argv:
        print("creating graph")
        getGraph(files)
    elif "-r" in sys.argv or "--record" in sys.argv:
        print("began recording battery")
        getBatteryPercentage(files[0])
    elif "-b" in sys.argv or "--bargraph" in sys.argv:
        print("Creating bar graph")
        getBarGraph(files)
    elif "-h" in sys.argv or "--help" in sys.argv:
        getHelp()
    else:
        getHelp()
