from os import sep
from django.shortcuts import render
import pandas as pd

# Create your views here.
def index(request, keyword=None):
    context = {}
    if request.method == 'POST':
        if len(request.FILES) != 0:
            csv_data = pd.read_csv(request.FILES.get('csv_file'))
            if isinstance(csv_data, pd.DataFrame):
                cols = csv_data.columns
                data = []
                csv_data = csv_data.applymap(str)
                # condition for search
                for rows in csv_data.iterrows():
                    values = rows[1]
                    item = list()
                    for value in values:
                        item.append(value)
                    data.append(item)

                context = {'remarks': 'done', 'tb_header': cols, 'tb_rows': data}
            else:
                context = {'remarks': 'error'}
        else:
            context = {'remarks': 'no file uploaded'}
    if keyword:
        context = {'remarks': keyword}
        return render(request, 'cdf_app/index.html', context)
    else:
        return render(request, 'cdf_app/index.html', context)