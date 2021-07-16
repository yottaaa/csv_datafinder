from os import sep
from django.shortcuts import render, redirect
import pandas as pd
import os
import secrets
import json
from .models import CSVData

# Create your views here.
def index(request):
    context = {}
    # if request method post
    if request.method == 'POST':
        # if there is a file uploaded
        if len(request.FILES) != 0:
            # if the filename is more than 293 char
            if len(request.FILES.get('csv_file').name) >= 293:
                context['remarks'] = "maxname"
            else:
                df = pd.read_csv(request.FILES.get('csv_file'))

                dataname = secrets.token_hex(4) + "_" + request.FILES.get('csv_file').name 
                datajson = df.to_json()
                dataitems = df.shape[0] # row count

                data = CSVData(
                    data_name=dataname,
                    data_json=datajson,
                    data_items=dataitems
                )
                data.save()

                context['remarks'] = "success"
        else:
            context['remarks'] = "error"

    csv_files = CSVData.objects.all()
    if len(csv_files) != 0:
        context['files'] = csv_files
    return render(request, 'cdf_app/index.html', context)

def dataView(request, pk):
    context = {}
    data = CSVData.objects.get(pk=pk)
    df = pd.read_json(data.data_json)

    df = df.applymap(str)
    # if searching data
    search_key = ''
    if request.method == 'POST':
        search_col = request.POST.get('data_column')
        search_key = request.POST.get('data_search')
        if search_col != '' and search_key != '':
            df = df.loc[df[search_col].str.contains(search_key)] 
        
    tb_rows = []

    for rows in df.iterrows():
        values = rows[1]
        items = []
        for value in values:
            items.append(value)
        tb_rows.append(items)

    context = {
        'tb_header': df.columns, 
        'tb_rows': tb_rows, 
        'tb_shape': df.shape,
        'search_key': search_key
    }
    return render(request, 'cdf_app/detail.html', context) 

def dataDelete(request, pk):
    data = CSVData.objects.get(pk=pk)
    data.delete()
    return redirect('index')