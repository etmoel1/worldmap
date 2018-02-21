# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:06:17 2018

@author: Eric Moeller
"""


import pandas as pd

from bokeh.io import output_file, show
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import CategoricalColorMapper, HoverTool
from bokeh.layouts import column, row
from bokeh.io import curdoc
curdoc().clear()

output_file('pop-life.html')

file = 'country-pops.csv'

countries = pd.read_csv(file, nrows=1000)

country_data = ColumnDataSource(countries)

color_mapper = CategoricalColorMapper(factors=['Asia', 'Africa', 'Anarctica', 
                                               'Australia', 'Central America',
                                               'Europe', 'North America', 
                                               'Oceania', 'South America'], 
                                      palette=['#00FF00', '#FFd343', 
                                               'darkgray', 'brown', 'cyan', 
                                               'crimson', 'red', '#0000FF', 
                                               'purple']) 
                                      

TOOLTIPS = 'pan, wheel_zoom, box_zoom, reset, hover, save'

plot_life_expect = figure(x_axis_label = 'Population', y_axis_label='Life Expectancy',
              tools=TOOLTIPS, title="Population vs Life Expectancy")


plot_birth_rate = figure(x_axis_label='Population', y_axis_label = 'Birth Rate', title = 'Population vs Birth Rate', tools=TOOLTIPS)

plot_death_rate = figure(x_axis_label = "Population", y_axis_label= "Date Rate", title="Population vs Death Rate", tools=TOOLTIPS)

plot_birth_rate.circle (x="Population", y="Birthrate", source=country_data, size =10, color=dict(field="Continent", transform=color_mapper), legend="Continent")

plot_death_rate.triangle(x="Population", y="Deathrate", source=country_data, size=10, color=dict(field="Continent", transform=color_mapper), legend="Continent")

plot_life_expect.diamond(x= 'Population', y='Life_expectancy', source=country_data, size=10, color=dict(field='Continent', transform=color_mapper), legend='Continent')


hover= plot_life_expect.select_one(HoverTool)
hover.tooltips = [('Country Name English', '@Country_English'),
                  ('Population', '@Population'),
                  ('Life Expectancy (years)', '@Life_expectancy')]

hover= plot_death_rate.select_one(HoverTool)
hover.tooltips = [('Country Name English', '@Country_English'),
                  ('Population', '@Population'),
                  ('Death Rate', '@Deathrate')]

hover= plot_birth_rate.select_one(HoverTool)
hover.tooltips = [('Country Name English', '@Country_English'),
                  ('Population', '@Population'),
                  ('Birthrate', '@Birthrate')]

plot_life_expect.legend.location = 'bottom_right'
plot_life_expect.legend.background_fill_color = 'lightgrey'

plot_birth_rate.x_range= plot_life_expect.x_range
plot_death_rate.x_range= plot_life_expect.x_range

show(row(column(plot_life_expect, plot_birth_rate), column(plot_death_rate)))