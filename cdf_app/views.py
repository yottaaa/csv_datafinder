from django.http import HttpResponse
from django.shortcuts import render, redirect
import pandas as pd
import os
import secrets
import json
from .models import CSVData

# landing page
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

# detail view
def dataView(request, pk):
    context = {}
    data = CSVData.objects.get(pk=pk)
    df = pd.read_json(data.data_json)

    df = df.applymap(str)
    # if searching data
    search_key = ''
    search_col = ''
    searchparam = {}
    if request.method == 'POST':
        search_col = request.POST.get('data_column')
        search_key = request.POST.get('data_search')
        if search_col != '' and search_key != '':
            df = df.loc[df[search_col].str.contains(search_key)] 
        searchparam = {
            'pk':pk,
            'search_col':search_col,
            'search_key':search_key,
        }
        
    tb_rows = []

    for rows in df.iterrows():
        values = rows[1]
        items = []
        for value in values:
            items.append(value)
        tb_rows.append(items)

    print(searchparam)

    context = {
        'tb_header': df.columns, 
        'tb_rows': tb_rows, 
        'tb_shape': df.shape,
        'searchparam': searchparam,
        'search_key': search_key,
    }
    return render(request, 'cdf_app/detail.html', context) 

# for deleting data
def dataDelete(request, pk):
    data = CSVData.objects.get(pk=pk)
    data.delete()
    return redirect('index')

# for exporting data
def exportData(request):
    # load data
    if request.GET:
        data = CSVData.objects.get(pk=request.GET['pk'])
        df = pd.read_json(data.data_json)

        # convert to all types to strings
        df = df.applymap(str)

        # searching data
        search_col = request.GET['search_col']
        search_key = request.GET['search_key']
        if search_col != '' and search_key != '':
            df = df.loc[df[search_col].str.contains(search_key)]

        response = HttpResponse(content_type='text/csv')

        filename = ''
        dataname = data.data_name
        if search_key != '':
            filename = dataname.replace('.csv', '_sortBy{}.csv'.format(search_key))
        else:
            filename = dataname

        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        df.to_csv(response,index=False)

        return response
    else:
        return HttpResponse(status=400)