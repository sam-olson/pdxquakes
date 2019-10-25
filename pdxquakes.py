import json
import urllib
import os
from datetime import datetime
import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource

def saveQueryJSON(fname, start_date, end_date = False):
    
    '''
    Updates or creates JSON file with given start names containing data
    within specified start/end dates. JSON file is saved in current directory

    Parameters
    ----------
    fname: name of .json file to be created
    start_date: date of earliest earthquakes (in format YY-MM-DD)
    end_date (optional: date of most recent earthquakes (in format YY-MM-DD)
    '''

    if end_date:
        qry = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=42.001&minlongitude=-131&maxlatitude=45.994&maxlongitude=-116.920&starttime={0}&endtime={1}".format(start_date,end_date)
    else:
        qry = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=42.001&minlongitude=-131&maxlatitude=45.994&maxlongitude=-116.920&starttime={0}".format(start_date)
    with urllib.request.urlopen(qry) as f:
        dta = json.loads(f.read().decode())

    if fname[-5:] != '.json':
        fname += '.json'
    
    with open(fname, 'w', encoding = 'utf-8') as j:
        json.dump(dta, j, indent = 4)

    print("Saved data in '{}'".format(fname))
    
    return fname

def plotData(fname, minmag = 0):
    
    '''
    Creates an embeddable HTML file containing a plot with data contained within
    a JSON file created using the function saveQueryJSON

    Parameters
    ----------
    fname: name of .json file to plot
    minmag (optional): minimum magnitude of earthquake to plot
    
    '''
    if fname[-5:] != '.json':
        fname += '.json'
        
    with open(fname) as f:
        dta = json.load(f)
    
    realData = dta['features']
    dates = []
    mags = []

    for i in realData:
        dt = str(i['properties']['time'])
        dt = float(dt[:10] + '.' + dt[10:])
        dates.append(datetime.fromtimestamp(dt))
        mags.append(i['properties']['mag'])

    all_data = pd.DataFrame({'dates': dates, 'mags': mags}, index = None)
    all_data = all_data[all_data.mags > minmag]

    if fname[-5:] != '.json':
        html_fname = fname + '.html'
    else:
        html_fname = fname[:-5] + '.html'
    
    # output plot to HTML file and show
    output_file(html_fname)
    dts = all_data['dates']
    dt_label = [i.strftime('%Y-%m-%d %H:%M:%S') for i in dts]
    mgs = all_data['mags']
    srce = ColumnDataSource(data=dict( x = dts,
                                       y = mgs,
                                       date = dt_label,
                                       magnitude = mgs
                                       ))
    TOOLTIPS = [
        ("date", "@date"),
        ("magnitude", "@magnitude"),
        ]
    p = figure(plot_width=1000, plot_height=400, x_axis_type="datetime", y_range = (0,10), tooltips = TOOLTIPS)
    p.circle('x', 'y', size = 5, color = "blue", alpha = 0.5, source=srce)
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Magnitude'
    show(p)
    


