from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def calculate_stats(data, place):
    data2 = []
    total = sum(data)
    mean = round(total / len(data), place)

    sorted_data = sorted(data)
    n = len(data)
    if n % 2 == 0:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median = sorted_data[n // 2]

    mode = max(set(data), key=data.count)
    data_range = max(data) - min(data)
    IQR = np.percentile(data, 75) - np.percentile(data, 25)

    for item in data:
        data2.append(abs(item - mean))
    MAD = round(sum(data2) / len(data2), place)

    data2.clear()
    for i in data:
        data2.append((i - mean)**2)

    Standard_Deviation = (sum(data2) / len(data2))**0.5
    Standard_Deviation = round(Standard_Deviation, place)

    return {
        'mean': mean,
        'median': median,
        'mode': mode,
        'range': data_range,
        'IQR': IQR,
        'MAD': MAD,
        'Standard Deviation': Standard_Deviation
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        place = int(request.form['place'])
        data = list(map(int, data.split(',')))

        stats = calculate_stats(data, place)
        return render_template('result.html', stats=stats)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
