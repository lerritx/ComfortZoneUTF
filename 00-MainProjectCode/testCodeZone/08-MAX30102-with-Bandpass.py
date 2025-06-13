import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt


pathfile = input("Enter the path of file: ").strip('"')
df = pd.read_csv(rf"{pathfile}")

ppg_raw = df['IR']

# ppg_raw = nk.ppg_simulate(duration=60, sampling_rate=100, heart_rate=70)
sampling_rate = 100

ppg_filtered = nk.signal_filter(ppg_raw,
                                            sampling_rate=sampling_rate,
                                            lowcut=0.5, highcut=5,
                                            method="bessel", order=5)


ppg_clean = nk.ppg_clean(ppg_filtered, sampling_rate=sampling_rate)

ppg_normalized = nk.rescale(ppg_clean, to=[-1, 1])      # เพิ่มการ Normalized


peaks, info = nk.ppg_peaks(ppg_normalized, sampling_rate=100, method="bishop", show=True)
plt.show()
