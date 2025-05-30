import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Tarih aralıkları
dates = {
    "Proje Konusu & Teklif": ("2025-05-31", "2025-06-03"),
    "Literatür Taraması & Veri Toplama": ("2025-06-04", "2025-06-17"),
    "Veri Ön İşleme & Görselleştirme": ("2025-06-18", "2025-06-30"),
    "Ara Rapor Teslimi": ("2025-07-03", "2025-07-03"),
    "Modelleme & Değerlendirme": ("2025-07-01", "2025-07-14"),
    "Sunum & Demo Hazırlığı": ("2025-07-15", "2025-07-20"),
    "Sözlü Sunum": ("2025-07-21", "2025-07-24"),
    "Final Rapor Yazımı": ("2025-07-22", "2025-07-29"),
    "Final Rapor Teslimi": ("2025-07-31", "2025-07-31"),
}

fig, ax = plt.subplots(figsize=(12,6))

y_pos = range(len(dates))
labels = list(dates.keys())

for i, (phase, (start_str, end_str)) in enumerate(dates.items()):
    start = datetime.datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_str, "%Y-%m-%d")
    ax.barh(i, (end-start).days+1, left=start, height=0.5, align='center', color='skyblue')

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

plt.title("BİL476/573 Veri Madenciliği Proje Takvimi (31 Mayıs - 31 Temmuz 2025)")
plt.xlabel("Tarih")
plt.tight_layout()

# Kaydet
plt.savefig("BIL476_573_Proje_Takvimi_Gantt.png")
plt.show()