from matplotlib import pyplot as plt

def scan_inspector(scan):
    for i in range(len(scan)):
        if i % 20 == 0:
            plt.gray()
            plt.imshow(scan[i], vmax=4000)
            plt.show()