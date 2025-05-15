import numpy as np
import matplotlib.pyplot as plt

def double_exponential(x, A1, k1, b1, A2, k2, b2, alpha):
    return alpha*(A1*np.exp(-x/k1)+b1)+(1-alpha)*(A2*np.exp(-x/k2)+b2)

# data taken from M7.5_X6.5_T1_L0.1\EtOH
conversion = 80*480/1000 # 80 ms, 480 mW -> mW*s
pb_data = {
    '0%':[961.14660881, 160.16256778, 220.00524541, 744.06208013,  29.49435168,   2.42547841, 0.4137356255550854],
    '5%':[1003.49140481,  131.73299355,  195.81958854, 987.75555348,  22.86608871,   7.89924147, 0.5910350508221933],
    '20%':[1.09945507e+03, 2.44058102e+01, 9.41696769e-01, 825.88235247, 136.60413061, 148.12858876, 0.42253216095823504],
    '50%':[466.99175554,  41.43741687,  32.16803072, 366.25279345, 285.55738868,  17.20224369, 0.6282289615532989],
    '100%':[1.65504888e+02, 1.67504975e+02, 5.63107935e-05, 230.61709374,  31.26775909,  31.00376685, 0.4694505574798288],
}

xs = np.linspace(0,500,100)
for key in pb_data:
    plt.plot(xs*conversion, double_exponential(xs, *pb_data[key]), label=key)

    val = double_exponential(187.5, *pb_data[key])
    print(f"Value at 7200 mW*s: {val}")

plt.legend()
plt.show()