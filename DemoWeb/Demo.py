import matplotlib.pyplot as plt

if __name__ == "__main__":
    caida = [1] * 10
    cernet = [2] * 10
    tsinghua = [3] * 10
    hgc = [4] * 10
    plt.figure()
    plt.grid()
    plt.ylim([0, 1])
    plt.xticks(range(2, 11, 2), ("0.2", "0.4", "0.6", "0.8", "1.0"))
    plt.plot(range(1, 11), caida, label="CAIDA", marker="x", color='blue')
    plt.plot(range(1, 11), cernet, label="CERNET", marker="^", color='red')
    plt.plot(range(1, 11), tsinghua, label="Tsinghua", marker="<", color='green')
    plt.plot(range(1, 11), hgc, label="HGC", marker="o", color='purple')
    plt.legend(frameon=False)
    plt.xlabel("Memory Consumption/MB")
    plt.ylabel("HH ARE")
    plt.savefig("hh_are.pdf", bbox_inches="tight")
    plt.close()