# pdxquakes

As an Oregonian, the ever present threat of [the big one](https://en.wikipedia.org/wiki/Cascadia_subduction_zone) happening tends to have one thinking about earthquakes quite a bit. Luckily, the USGS has a [free API](https://earthquake.usgs.gov/fdsnws/event/1/) that allows programmers to track earthquakes from around the globe.  

This Python code sends queries to the USGS API and saves/plots the resultant data. The data is saved in a JSON file, which can then be used to create an embeddable HTML file with a plot containing the data. 

## Using the code

The code in its current version finds all earthquakes within the rectangle with corners at the following longitude/latitude pairs:
* NW: 45.994, -131.000
* NE: 45.994, -116.920
* SW: 42.001, -131.000
* SE: 42.001, -116.920

This rectangle encompasses the state of Oregon, as well as roughly 350 miles off of the coast (around where the [Blanco Fracture Zone](https://en.wikipedia.org/wiki/Blanco_Fracture_Zone) lies). 

To use this code, you must have the external packages [pandas](https://pandas.pydata.org/) and [bokeh](https://docs.bokeh.org/en/latest/index.html). Queries can be plotted in the following manner:

```python
f = 'quakes.json'			# name of .json file
start = '2019-01-01'			# all quakes Jan 1, 2019 to date
plotData(saveQueryJSON(f, start))	# saving/plotting the data - creates an html file 'quakes.html'
```
This is the resulting plot, showing the ability to display information via hovering the mouse over a datapoint:

![Example plot](https://github.com/sam-olson/pdxquakes/blob/master/assets/example.png)

FYI, here's how the JSON object is structured (this is located within the attribute `features`):

```json
"type": "Feature",
            "properties": {
                "mag": 6.3,
                "place": "285km W of Bandon, Oregon",
                "time": 1567091278646,
                "updated": 1569957053771,
                "tz": -540,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us700059qh",
                "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us700059qh&format=geojson",
                "felt": 793,
                "cdi": 5,
                "mmi": 0,
                "alert": "green",
                "status": "reviewed",
                "tsunami": 1,
                "sig": 1007,
                "net": "us",
                "code": "700059qh",
                "ids": ",at00px07dc,us700059qh,",
                "sources": ",at,us,",
                "types": ",dyfi,general-text,geoserve,impact-link,losspager,moment-tensor,oaf,origin,phase-data,shakemap,",
                "nst": null,
                "dmin": 2.678,
                "rms": 1.17,
                "gap": 31,
                "magType": "mww",
                "type": "earthquake",
                "title": "M 6.3 - 285km W of Bandon, Oregon"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -127.8817,
                    43.5425,
                    10
                ]
            },
            "id": "us700059qh"
        }
```
