import numpy as np
from bokeh.palettes import Magma256
from bokeh.plotting import figure, show
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.models import LinearColorMapper
from bokeh.plotting import figure, show
from flask import Flask, url_for, render_template, request
from markupsafe import Markup
from bokeh.models import ColorBar, BasicTicker
import os
import json
app = Flask(__name__)
    



@app.route('/')
def home():
    
    with open('opiodDeath.json') as deathData:
        data = json.load(deathData)
    M = 0
    for num in data:
        if int( num["deaths"]) > M:
            M = int(num["deaths"])
    print(M)
   
    
    return render_template('about.html')
    
    


@app.route('/map')
def map():
  


    

    
    
    with open('opiodDeath.json') as deathData:
        data = json.load(deathData)
        states1 = states.copy()

    del states1["HI"]
    del states1["AK"]

   

    state_xs = [states1[code]["lons"] for code in states1]
    state_ys = [states1[code]["lats"] for code in states1]
    '''county_xs = [counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
    county_ys = [counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]'''
    stateA = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
    }
    deaths = {}
    for deaths1 in data:
        if deaths1['year'] == "2016" and deaths1['state'] in stateA:
            deaths[stateA[deaths1['state']]] = int(deaths1['deaths'])
    state_colors = []
    county_colors = []
    print(deaths)
    for state in states1:
        print(state)
        try:
            rate = deaths[state]
            print(rate)
            idx = int(rate/5000*256)
            
            state_colors.append(Magma256[idx])
            print(idx)
        except KeyError:
            state_colors.append("black")
    

    p = figure(title="Opiod Death Counts 2016",
               x_axis_location=None, y_axis_location=None,
               width=1000, height=600)
    p.grid.grid_line_color = None

    '''p.patches(county_xs, county_ys,
              fill_color=county_colors, fill_alpha=0.7,
              line_color="white", line_width=0.5)'''

    p.patches(state_xs, state_ys,
        line_alpha=0.3,
        fill_color=state_colors, fill_alpha=0.7,
        line_color="white", line_width=0.5)
   
    color_mapper = LinearColorMapper(palette="Magma256", low=0, high=5000)

    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')

    show(p)  # Change to save(p) to save but not show the HTML file

    
    return render_template('map.html')

@app.route('/states')
def States():
    return render_template('states.html')
    

def Get_state():
    state = request.args.get("state")
    with open('opiodDeath.json') as deathData:
        stateS = json.load(deathData)
    state=[]
    
    for s in stateS:
        if s["state"] not in state:
            state.append(s["state"])
    return state

def getData(state):
    counts = {"deaths":0}
    with open('opiodDeath.json') as deathData:
        states = json.load(deathData)
        stateArray = []
        deathCounts = 0
        for s in states:
            if state == s["state"]:
                deathCounts += int(s["deaths"])
    return deathCounts
            
        
@app.route('/selection')  
def ShowData():
    deaths = getData(request.args["state"])
    fact1= "there have been " + str(deaths) + " deaths from 1999 to 2016 in " + str(request.args["state"])
    return render_template('states.html', Fact1=fact1)
if __name__=="__main__":
    app.run(debug=True)