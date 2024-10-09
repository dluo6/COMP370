import preprocess
import pandas as pd
import numpy as np
import os.path
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import Dropdown

zipcode_average = 'nyc_311_limit.2020.preprocessedbyzip.csv'
total_average = 'nyc_311_limit.2020.preprocessedtotal.csv'
# preprocess.main(output_file)

df = pd.read_csv(os.path.join(os.path.dirname(__file__), zipcode_average))
zipcode_options = [str(x) for x in df['zipcode'].unique().tolist()]
y1, y2 = zipcode_options[0:2]
total_df = pd.read_csv(os.path.join(os.path.dirname(__file__), total_average))

def get_y_data(zipcode):
    res = [0]*12
    temp = df[df['zipcode'] == int(zipcode)]
    for i in range(len(temp)):
        entry = temp.iloc[i]
        res[int(entry['month'])-1] = entry['hour difference'].item()
    return res

l1 = get_y_data(y1)
l2 = get_y_data(y2)
l3 = total_df['hour difference'].tolist() + [0,0,0]

x = [x for x in range(1, 13)]

plot = figure(title='Average Response Time Per Month',
              x_axis_label='Months',
              y_axis_label='Response Time in Hours')

renderer1 = plot.line(x=x, y=l1, line_width=2, color='blue', legend_label='Zipcode 1')
renderer2 = plot.line(x=x, y=l2, line_width=2, color='green', legend_label='Zipcode 2')
renderer3 = plot.line(x=x, y=l3, line_width=2, color='red', legend_label='Total')

ds1 = renderer1.data_source
ds2 = renderer2.data_source

# Dropdown to create a responsive chart
def z1_selection_callback(event):
    print('Zipcode1:', event.item)
    ds1.data = {'x': x, 'y': get_y_data(event.item)}

def z2_selection_callback(event):
    print('Zipcode 2:', event.item)
    ds2.data = {'x': x, 'y': get_y_data(event.item)}

z1_selector = Dropdown(
    label='Select a zip code',
    menu=zipcode_options
)
z2_selector = Dropdown(
    label='Select a zip code',
    menu=zipcode_options
)
z1_selector.on_event('menu_item_click', z1_selection_callback)
z2_selector.on_event('menu_item_click', z2_selection_callback)

curdoc().add_root(column(z1_selector, z2_selector, plot))