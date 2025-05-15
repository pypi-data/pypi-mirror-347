import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])  # Allow frontend origin

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Serve static files (plots and text files)
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def hourly_events(data_file, heading, water_table, water_temp, winterr, springg, summerr, falll, season_deli):
    df = pd.read_csv(data_file)
    print('\nThis is the first 50 lines\n')
    print(df.head(51))
    print('\n')
    
    Date = []
    Discharge = []
    concentration = []
    with open(data_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == '':
                break
            else:
                Date.append(row[0])
                Discharge.append(float(row[1]) if row[1] else 0.0)
                concentration.append(float(row[2]) if row[2] else 0.0)
    
    if water_table == 'y':
        water_level = []
        with open(data_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == '':
                    break
                else:
                    water_level.append(float(row[3]) if row[3] else 0.0)
    
    if water_temp == 'y':
        water_chill = []
        with open(data_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == '':
                    break
                else:
                    water_chill.append(float(row[4]) if row[4] else 0.0)
    
    if heading == 'y':
        Date.pop(0)
        Discharge.pop(0)
        concentration.pop(0)
        if water_table == 'y':
            water_level.pop(0)
        if water_temp == 'y':
            water_chill.pop(0)
    
    for i in range(len(Discharge)):
        Discharge[i] = float(Discharge[i])
        concentration[i] = float(concentration[i])
        if water_table == 'y':
            water_level[i] = float(water_level[i])
        if water_temp == 'y':
            water_chill[i] = float(water_chill[i])
    
    Dates = [[date] for date in Date]
    
    percentage_discharge_change = ['event']
    for i in range(1, len(Discharge)):
        change = Discharge[i] - Discharge[i - 1]
        if Discharge[i - 1] == 0:
            percentage_discharge_change.append('no flow')
        else:
            percent_change = (change / Discharge[i - 1]) * 100
            percentage_discharge_change.append(percent_change)
    
    high_compound_flow = []
    low_compound_flow = []
    combine_compound_flow = []
    events = []
    event_dates = []
    baseflow = []
    baseflow_dates = []
    event_bunch = []
    catch_no = 0
    packer = 0
    caught_events = {}
    event_occuring = False
    switch = False
    all_varient = [float(winterr), float(springg), float(summerr), float(falll)]
    mean_jump = sum(all_varient) / len(all_varient)
    season_delineation = season_deli
    
    winter = float(winterr)
    spring = float(springg)
    summer = float(summerr)
    fall = float(falll)
    
    searching = True
    month = ''
    if season_delineation == 'B':
        step = 0
        while searching:
            day = list(Dates[0][0])
            member = day[step]
            try:
                member = int(member)
                month += str(member)
                step += 1
            except:
                searching = False
                if float(month) == 12 or float(month) < 3:
                    event_point = winter
                    print('Analysis starting in Winter')
                elif 2 < float(month) < 6:
                    event_point = spring
                    print('Analysis starting in spring')
                elif 5 < float(month) < 9:
                    event_point = summer
                    print('Analysis starting in summer')
                elif 8 < float(month) < 12:
                    event_point = fall
                    print('Analysis starting in fall')
    elif season_delineation == 'A':
        step = 0
        while searching:
            day = list(Dates[0][0])
            member = day[step]
            try:
                member = int(member)
                month += str(member)
                step += 1
            except:
                searching = False
                if float(month) < 4:
                    event_point = winter
                    print('Analysis starting in Winter')
                elif 3 < float(month) < 7:
                    event_point = spring
                    print('Analysis starting in spring')
                elif 6 < float(month) < 10:
                    event_point = summer
                    print('Analysis starting in summer')
                elif float(month) > 9:
                    event_point = fall
                    print('Analysis starting in fall')
    print('\n')
    
    if Discharge[0] > event_point:
        event_occuring = True
    
    event_ends = 0
    base_compound = 0
    high_compound = 0
    for elements in range(len(Discharge)):
        searching = True
        month = ''
        if season_delineation == 'B':
            step = 0
            while searching:
                day = list(Dates[elements][0])
                member = day[step]
                try:
                    member = int(member)
                    month += str(member)
                    step += 1
                except:
                    searching = False
                    if float(month) == 12 or float(month) < 3:
                        event_point = winter
                    elif 2 < float(month) < 6:
                        event_point = spring
                    elif 5 < float(month) < 9:
                        event_point = summer
                    elif 8 < float(month) < 12:
                        event_point = fall
        elif season_delineation == 'A':
            step = 0
            while searching:
                day = list(Dates[elements][0])
                member = day[step]
                try:
                    member = int(member)
                    month += str(member)
                    step += 1
                except:
                    searching = False
                    if float(month) < 4:
                        event_point = winter
                    elif 3 < float(month) < 7:
                        event_point = spring
                    elif 6 < float(month) < 10:
                        event_point = summer
                    elif float(month) > 9:
                        event_point = fall
        
        last_slope = -1
        if event_occuring and elements >= len(events):
            truncated_list = Discharge[elements:]
            section_dates = Dates[elements:]
            changing_flow = percentage_discharge_change[elements:]
            for elements1 in range(len(truncated_list)):
                if event_occuring:
                    if truncated_list[elements1] > event_point:
                        event_ends = 0
                        if elements1 > 0:
                            if changing_flow[elements1] == 'no flow':
                                changing_flow[elements1] = 0.0000000001
                            if changing_flow[elements1] < 0:
                                events.append(truncated_list[elements1])
                                event_dates.append(section_dates[elements1])
                                last_slope = changing_flow[elements1]
                                baseflow.append('')
                            else:
                                if last_slope < 0:
                                    high_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                                else:
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                        else:
                            event_ends = 0
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            baseflow.append('')
                    else:
                        event_ends += 1
                        if event_ends < 2:
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            drop_1 = truncated_list[elements1]
                            baseflow.append('')
                        else:
                            if truncated_list[elements1] <= drop_1:
                                baseflow.append(truncated_list[elements1])
                                baseflow_dates.append(section_dates[elements1])
                                event_occuring = False
                                switch = True
                                events.append('')
                            else:
                                if truncated_list[elements1] <= event_point:
                                    baseflow.append(truncated_list[elements1])
                                    baseflow_dates.append(section_dates[elements1])
                                    events.append('')
                                    event_occuring = False
                                    switch = True
                                else:
                                    base_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    baseflow.append('')
        else:
            if len(events) > 0 and len(events) >= packer and switch:
                catch_no += 1
                event_bunch.append(events)
                packer = len(events)
                caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                switch = False
                if high_compound > 1:
                    if base_compound > 1:
                        combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    else:
                        high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                elif base_compound > 1:
                    low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
            
            if elements >= len(events):
                if Discharge[elements] >= event_point:
                    event_ends = 0
                    event_dates = []
                    event_occuring = True
                    if event_occuring and elements >= len(events):
                        truncated_list = Discharge[elements:]
                        section_dates = Dates[elements:]
                        changing_flow = percentage_discharge_change[elements:]
                        for elements1 in range(len(truncated_list)):
                            if event_occuring:
                                if truncated_list[elements1] > event_point:
                                    event_ends = 0
                                    if elements1 > 0:
                                        if changing_flow[elements1] == 'no flow':
                                            changing_flow[elements1] = 0.0000000001
                                        if changing_flow[elements1] < 0:
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            last_slope = changing_flow[elements1]
                                            baseflow.append('')
                                        else:
                                            if last_slope < 0:
                                                high_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                            else:
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                    else:
                                        event_ends = 0
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        baseflow.append('')
                                else:
                                    event_ends += 1
                                    if event_ends < 2:
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        drop_1 = truncated_list[elements1]
                                        baseflow.append('')
                                    else:
                                        if truncated_list[elements1] <= drop_1:
                                            baseflow.append(truncated_list[elements1])
                                            baseflow_dates.append(section_dates[elements1])
                                            event_occuring = False
                                            switch = True
                                            events.append('')
                                        else:
                                            if truncated_list[elements1] <= event_point:
                                                baseflow.append(truncated_list[elements1])
                                                baseflow_dates.append(section_dates[elements1])
                                                events.append('')
                                                event_occuring = False
                                                switch = True
                                            else:
                                                base_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                baseflow.append('')
                else:
                    baseflow.append(Discharge[elements])
                    baseflow_dates.append(Dates[elements])
                    events.append('')
    
    print(f'Caught_event -\n{caught_events}\n')
    print(f'Number of events - {len(caught_events)}\n')
    
    valid_drop = mean_jump * 1.25
    for i in range(len(events)):
        if isinstance(events[i], float) and i > 0 and events[i] > valid_drop:
            events[i - 1] = Discharge[i - 1]
    
    file_name = "hourly_flow_event_data.txt"
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), "w") as file:
        for number in events:
            file.write(f"{number}\n")
    print(f"Numbers successfully written to {file_name}")
    
    if len(Discharge) < 5000:
        y2 = events
        y1 = Discharge
        x = list(range(len(y1)))
        y2_clean = [float(val) if val != '' else np.nan for val in y2]
        
        fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
        axs[0].plot(x, y1, marker='', color='green')
        axs[0].set_title('Plot of Discharge Data')
        axs[0].set_ylabel('Drainage (cm3/day)')
        axs[0].grid(False)
        
        axs[1].plot(x, y2_clean, marker='', linestyle='-', color='blue')
        axs[1].set_title('Plot of Events')
        axs[1].set_xlabel('Dates')
        axs[1].set_ylabel('Drainage (cm3/day)')
        axs[1].grid(False)
        points = min(30, len(x))
        axs[1].xaxis.set_major_locator(plt.MaxNLocator(nbins=points))
        fig.autofmt_xdate(rotation=45)
        
        y_min = min(min(y1, default=np.nan), min(y2_clean, default=np.nan))
        y_max = max(max(y1, default=np.nan), max(y2_clean, default=np.nan))
        if not np.isnan(y_min) and not np.isnan(y_max):
            axs[0].set_ylim(y_min, y_max)
            axs[1].set_ylim(y_min, y_max)
        
        plot_file = "hourly_events_plot.png"
        plt.tight_layout()
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], plot_file))
        plt.close()
    
    file_name = "hourly_flow_base_data.txt"
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), "w") as file:
        for number in baseflow:
            file.write(f"{number}\n")
    print(f"Numbers successfully written to {file_name}")
    
    refine_caught_event = {}
    label = 0
    for key in caught_events:
        label += 1
        pick = list(str(caught_events[key]))
        pick = [x for x in pick if x not in ['[', ']', ',', "'"]]
        tt = ''.join(pick)
        refine_caught_event[f'{label}-event'] = tt
    
    caught_events = refine_caught_event
    flow_weighted_concentration = []
    average_water_table_depth = []
    average_water_table_temp = []
    
    for key in caught_events:
        label = int(key.split('-')[0])
        matcher = list(caught_events[key])
        start_date = False
        good_break_point = False
        for elementss in range(len(Dates)):
            if good_break_point:
                break
            if not start_date:
                mini_conc = []
                mini_flow = []
                mini_table = []
                mini_temp = []
                plucks = 0
                plucks1 = 0
                starter = list(Dates[elementss][0])
                hit = 0
                for i in range(min(len(starter), len(matcher))):
                    if starter[i] == matcher[i]:
                        hit += 1
                    if hit == len(starter):
                        start_date = True
                        half_band = starter + [' ', '-', ' ']
                        mini_conc.append(concentration[elementss])
                        mini_flow.append(events[elementss])
                        if water_table == 'y':
                            mini_table.append(water_level[elementss])
                            plucks += 1
                        if water_temp == 'y':
                            mini_temp.append(water_chill[elementss])
                            plucks1 += 1
            else:
                full_band_unsure = half_band.copy()
                ender = list(Dates[elementss][0])
                full_band_unsure.extend(ender)
                hit = 0
                for i in range(min(len(full_band_unsure), len(matcher))):
                    if full_band_unsure[i] == matcher[i]:
                        hit += 1
                    if hit == len(full_band_unsure):
                        start_date = False
                        good_break_point = True
                mini_conc.append(concentration[elementss])
                mini_flow.append(events[elementss])
                if water_table == 'y':
                    mini_table.append(water_level[elementss])
                    plucks += 1
                if water_temp == 'y':
                    mini_temp.append(water_chill[elementss])
                    plucks1 += 1
                
                if not start_date:
                    conc_flow_sum = 0
                    flow_sum = 0
                    level_sum = 0
                    temp_sum = 0
                    for i in range(len(mini_conc)):
                        try:
                            y = float(mini_conc[i])
                            b = float(mini_flow[i])
                            if water_table == 'y':
                                level = float(mini_table[i])
                            if water_temp == 'y':
                                temp = float(mini_temp[i])
                            if y > 0:
                                conc_flow_sum += y * b
                                flow_sum += b
                            if water_table == 'y' and level > 0:
                                level_sum += level
                            if water_temp == 'y' and temp > 0:
                                temp_sum += temp
                        except:
                            pass
                    if flow_sum > 0:
                        F_W_C = conc_flow_sum / flow_sum
                        flow_weighted_concentration.append(f'{label}_event - {F_W_C}')
                    if water_table == 'y' and plucks > 0:
                        A_W_T_D = level_sum / plucks
                        average_water_table_depth.append(f'{label}_event - {A_W_T_D}')
                    if water_temp == 'y' and plucks1 > 0:
                        A_W_T_T = temp_sum / plucks1
                        average_water_table_temp.append(f'{label}_event - {A_W_T_T}')
    
    print(f'\nThe flow weighted concentration for the events are:\n{flow_weighted_concentration}\n')
    if water_table == 'y':
        print(f'These are the average water table depths for the events:\n{average_water_table_depth}\n')
    if water_temp == 'y':
        print(f'These are the average water temperatures for the events:\n{average_water_table_temp}\n')
    
    return {
        'events': caught_events,
        'flow_weighted_concentration': flow_weighted_concentration,
        'avg_water_table': average_water_table_depth,
        'avg_water_temp': average_water_table_temp,
        'plot_file': 'hourly_events_plot.png' if len(Discharge) < 5000 else None,
        'event_data_file': 'hourly_flow_event_data.txt',
        'base_data_file': 'hourly_flow_base_data.txt'
    }

def daily_events(data_file, heading, water_table, water_temp, winterr, springg, summerr, falll, season_deli):
    df = pd.read_csv(data_file)
    print('\nThis is the first 50 lines\n')
    print(df.head(51))
    print('\n')
    
    Date = []
    Discharge = []
    concentration = []
    with open(data_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == '':
                break
            else:
                Date.append(row[0])
                Discharge.append(float(row[1]) if row[1] else 0.0)
                concentration.append(float(row[2]) if row[2] else 0.0)
    
    if water_table == 'y':
        water_level = []
        with open(data_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == '':
                    break
                else:
                    water_level.append(float(row[3]) if row[3] else 0.0)
    
    if water_temp == 'y':
        water_chill = []
        with open(data_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == '':
                    break
                else:
                    water_chill.append(float(row[4]) if row[4] else 0.0)
    
    if heading == 'y':
        Date.pop(0)
        Discharge.pop(0)
        concentration.pop(0)
        if water_table == 'y':
            water_level.pop(0)
        if water_temp == 'y':
            water_chill.pop(0)
    
    for i in range(len(Discharge)):
        Discharge[i] = float(Discharge[i])
        concentration[i] = float(concentration[i])
        if water_table == 'y':
            water_level[i] = float(water_level[i])
        if water_temp == 'y':
            water_chill[i] = float(water_chill[i])
    
    Dates = [[date] for date in Date]
    
    percentage_discharge_change = ['event']
    for i in range(1, len(Discharge)):
        change = Discharge[i] - Discharge[i - 1]
        if Discharge[i - 1] == 0:
            percentage_discharge_change.append('no flow')
        else:
            percent_change = (change / Discharge[i - 1]) * 100
            percentage_discharge_change.append(percent_change)
    
    high_compound_flow = []
    low_compound_flow = []
    combine_compound_flow = []
    events = []
    event_dates = []
    baseflow = []
    baseflow_dates = []
    event_bunch = []
    catch_no = 0
    packer = 0
    caught_events = {}
    event_occuring = False
    switch = False
    all_varient = [float(winterr), float(springg), float(summerr), float(falll)]
    mean_jump = sum(all_varient) / len(all_varient)
    season_delineation = season_deli
    
    winter = float(winterr)
    spring = float(springg)
    summer = float(summerr)
    fall = float(falll)
    
    searching = True
    month = ''
    if season_delineation == 'B':
        step = 0
        while searching:
            day = list(Dates[0][0])
            member = day[step]
            try:
                member = int(member)
                month += str(member)
                step += 1
            except:
                searching = False
                if float(month) == 12 or float(month) < 3:
                    event_point = winter
                    print('Analysis starting in Winter')
                elif 2 < float(month) < 6:
                    event_point = spring
                    print('Analysis starting in spring')
                elif 5 < float(month) < 9:
                    event_point = summer
                    print('Analysis starting in summer')
                elif 8 < float(month) < 12:
                    event_point = fall
                    print('Analysis starting in fall')
    elif season_delineation == 'A':
        step = 0
        while searching:
            day = list(Dates[0][0])
            member = day[step]
            try:
                member = int(member)
                month += str(member)
                step += 1
            except:
                searching = False
                if float(month) < 4:
                    event_point = winter
                    print('Analysis starting in Winter')
                elif 3 < float(month) < 7:
                    event_point = spring
                    print('Analysis starting in spring')
                elif 6 < float(month) < 10:
                    event_point = summer
                    print('Analysis starting in summer')
                elif float(month) > 9:
                    event_point = fall
                    print('Analysis starting in fall')
    print('\n')
    
    if Discharge[0] > event_point:
        event_occuring = True
    
    event_ends = 0
    base_compound = 0
    high_compound = 0
    for elements in range(len(Discharge)):
        searching = True
        month = ''
        if season_delineation == 'B':
            step = 0
            while searching:
                day = list(Dates[elements][0])
                member = day[step]
                try:
                    member = int(member)
                    month += str(member)
                    step += 1
                except:
                    searching = False
                    if float(month) == 12 or float(month) < 3:
                        event_point = winter
                    elif 2 < float(month) < 6:
                        event_point = spring
                    elif 5 < float(month) < 9:
                        event_point = summer
                    elif 8 < float(month) < 12:
                        event_point = fall
        elif season_delineation == 'A':
            step = 0
            while searching:
                day = list(Dates[elements][0])
                member = day[step]
                try:
                    member = int(member)
                    month += str(member)
                    step += 1
                except:
                    searching = False
                    if float(month) < 4:
                        event_point = winter
                    elif 3 < float(month) < 7:
                        event_point = spring
                    elif 6 < float(month) < 10:
                        event_point = summer
                    elif float(month) > 9:
                        event_point = fall
        
        last_slope = -1
        if event_occuring and elements >= len(events):
            truncated_list = Discharge[elements:]
            section_dates = Dates[elements:]
            changing_flow = percentage_discharge_change[elements:]
            for elements1 in range(len(truncated_list)):
                if event_occuring:
                    if truncated_list[elements1] > event_point:
                        event_ends = 0
                        if elements1 > 0:
                            if changing_flow[elements1] == 'no flow':
                                changing_flow[elements1] = 0.0000000001
                            if changing_flow[elements1] < 0:
                                events.append(truncated_list[events])
                                event_dates.append(section_dates[elements1])
                                last_slope = changing_flow[elements1]
                                baseflow.append('')
                            else:
                                if last_slope < 0:
                                    high_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                                else:
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                        else:
                            event_ends = 0
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            baseflow.append('')
                    else:
                        event_ends += 1
                        if event_ends < 2:
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            drop_1 = truncated_list[elements1]
                            baseflow.append('')
                        else:
                            if truncated_list[elements1] <= drop_1:
                                baseflow.append(truncated_list[elements1])
                                baseflow_dates.append(section_dates[elements1])
                                event_occuring = False
                                switch = True
                                events.append('')
                            else:
                                if truncated_list[elements1] <= event_point:
                                    baseflow.append(truncated_list[elements1])
                                    baseflow_dates.append(section_dates[elements1])
                                    events.append('')
                                    event_occuring = False
                                    switch = True
                                else:
                                    base_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    baseflow.append('')
        else:
            if len(events) > 0 and len(events) >= packer and switch:
                catch_no += 1
                event_bunch.append(events)
                packer = len(events)
                caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                switch = False
                if high_compound > 1:
                    if base_compound > 1:
                        combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    else:
                        high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                elif base_compound > 1:
                    low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
            
            if elements >= len(events):
                if Discharge[elements] >= event_point:
                    event_ends = 0
                    event_dates = []
                    event_occuring = True
                    if event_occuring and elements >= len(events):
                        truncated_list = Discharge[elements:]
                        section_dates = Dates[elements:]
                        changing_flow = percentage_discharge_change[elements:]
                        for elements1 in range(len(truncated_list)):
                            if event_occuring:
                                if truncated_list[elements1] > event_point:
                                    event_ends = 0
                                    if elements1 > 0:
                                        if changing_flow[elements1] == 'no flow':
                                            changing_flow[elements1] = 0.0000000001
                                        if changing_flow[elements1] < 0:
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            last_slope = changing_flow[elements1]
                                            baseflow.append('')
                                        else:
                                            if last_slope < 0:
                                                high_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                            else:
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                    else:
                                        event_ends = 0
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        baseflow.append('')
                                else:
                                    event_ends += 1
                                    if event_ends < 2:
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        drop_1 = truncated_list[elements1]
                                        baseflow.append('')
                                    else:
                                        if truncated_list[elements1] <= drop_1:
                                            baseflow.append(truncated_list[elements1])
                                            baseflow_dates.append(section_dates[elements1])
                                            event_occuring = False
                                            switch = True
                                            events.append('')
                                        else:
                                            if truncated_list[elements1] <= event_point:
                                                baseflow.append(truncated_list[elements1])
                                                baseflow_dates.append(section_dates[elements1])
                                                events.append('')
                                                event_occuring = False
                                                switch = True
                                            else:
                                                base_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                baseflow.append('')
                else:
                    baseflow.append(Discharge[elements])
                    baseflow_dates.append(Dates[elements])
                    events.append('')
    
    print(f'Caught_event -\n{caught_events}\n')
    print(f'There are {len(caught_events)} events\n')
    
    valid_drop = mean_jump
    pack = 0
    blocks = 0
    event_kickout = []
    for i in range(len(events)):
        if isinstance(events[i], float):
            pack += 1
        elif i > pack - 1 and pack > 0 and pack < 3:
            look_max = []
            blocks += 1
            for j in range(pack):
                look_max.append(events[i - pack])
            max_look = max(look_max)
            if max_look < 1.25 * event_point:
                event_kickout.append(f'{blocks} event ')
                for k in range(pack):
                    events[i - pack + k] = ''
            pack = 0
        else:
            if pack > 0:
                blocks += 1
            pack = 0
    
    print(f'blocks (representing the amount of events left) = {blocks}')
    for kickout in event_kickout:
        caught_events.pop(kickout, None)
    
    print(f'\nThese are the modified events\n{caught_events}\n')
    print(f'There are {len(caught_events)} events\n')
    
    for i in range(len(events)):
        if isinstance(events[i], float) and i > 0 and events[i] > valid_drop:
            events[i - 1] = Discharge[i - 1]
    
    file_name = "daily_flow_event_data.txt"
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), "w") as file:
        for number in events:
            file.write(f"{number}\n")
    print(f"Numbers successfully written to {file_name}")
    
    y2 = events
    y1 = Discharge
    x = [date[0] for date in Dates]
    y2_clean = [float(val) if val != '' else np.nan for val in y2]
    
    fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
    axs[0].plot(x, y1, marker='', color='green')
    axs[0].set_title('Plot of Discharge Data')
    axs[0].set_ylabel('Drainage (cm3/day)')
    axs[0].grid(False)
    
    axs[1].plot(x, y2_clean, marker='', linestyle='-', color='blue')
    axs[1].set_title('Plot of Events')
    axs[1].set_xlabel('Dates')
    axs[1].set_ylabel('Drainage (cm3/day)')
    axs[1].grid(False)
    points = min(30, len(x))
    axs[1].xaxis.set_major_locator(plt.MaxNLocator(nbins=points))
    fig.autofmt_xdate(rotation=45)
    
    y_min = min(min(y1, default=np.nan), min(y2_clean, default=np.nan))
    y_max = max(max(y1, default=np.nan), max(y2_clean, default=np.nan))
    if not np.isnan(y_min) and not np.isnan(y_max):
        axs[0].set_ylim(y_min, y_max)
        axs[1].set_ylim(y_min, y_max)
    
    plot_file = "daily_events_plot.png"
    plt.tight_layout()
    plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], plot_file))
    plt.close()
    
    for i in range(len(Discharge)):
        if isinstance(events[i], float) and isinstance(baseflow[i], float):
            baseflow[i] = ''
        elif isinstance(events[i], str) and isinstance(baseflow[i], str) and Discharge[i] > 0:
            baseflow[i] = Discharge[i]
    
    file_name = "daily_flow_base_data.txt"
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), "w") as file:
        for number in baseflow:
            file.write(f"{number}\n")
    print(f"Numbers successfully written to {file_name}")
    
    flow_weighted_concentration = []
    average_water_table_depth = []
    average_water_table_temp = []
    
    for key in caught_events:
        label = int(key.split('-')[0])
        matcher = [item for item in list(caught_events[key]) if item not in ['[', ']', "'"]]
        start_date = False
        good_break_point = False
        for elementss in range(len(Dates)):
            if good_break_point:
                break
            if not start_date:
                mini_conc = []
                mini_flow = []
                mini_table = []
                mini_temp = []
                plucks = 0
                plucks1 = 0
                starter = list(Dates[elementss][0])
                hit = 0
                for i in range(min(len(starter), len(matcher))):
                    if starter[i] == matcher[i]:
                        hit += 1
                    if hit == len(starter):
                        start_date = True
                        half_band = starter + [' ', '-', ' ']
                        mini_conc.append(concentration[elementss])
                        mini_flow.append(events[elementss])
                        if water_table == 'y':
                            mini_table.append(water_level[elementss])
                            plucks += 1
                        if water_temp == 'y':
                            mini_temp.append(water_chill[elementss])
                            plucks1 += 1
            else:
                full_band_unsure = half_band.copy()
                ender = list(Dates[elementss][0])
                full_band_unsure.extend(ender)
                hit = 0
                for i in range(min(len(full_band_unsure), len(matcher))):
                    if full_band_unsure[i] == matcher[i]:
                        hit += 1
                    if hit == len(full_band_unsure):
                        start_date = False
                        good_break_point = True
                mini_conc.append(concentration[elementss])
                mini_flow.append(events[elementss])
                if water_table == 'y':
                    mini_table.append(water_level[elementss])
                    plucks += 1
                if water_temp == 'y':
                    mini_temp.append(water_chill[elementss])
                    plucks1 += 1
                
                if not start_date:
                    conc_flow_sum = 0
                    flow_sum = 0
                    level_sum = 0
                    temp_sum = 0
                    for i in range(len(mini_conc)):
                        try:
                            y = float(mini_conc[i])
                            b = float(mini_flow[i])
                            if water_table == 'y':
                                level = float(mini_table[i])
                            if water_temp == 'y':
                                temp = float(mini_temp[i])
                            if y > 0:
                                conc_flow_sum += y * b
                                flow_sum += b
                            if water_table == 'y' and level > 0:
                                level_sum += level
                            if water_temp == 'y' and temp > 0:
                                temp_sum += temp
                        except:
                            pass
                    if flow_sum > 0:
                        F_W_C = conc_flow_sum / flow_sum
                        flow_weighted_concentration.append(f'{label}_event - {F_W_C}')
                    if water_table == 'y' and plucks > 0:
                        A_W_T_D = level_sum / plucks
                        average_water_table_depth.append(f'{label}_event - {A_W_T_D}')
                    if water_temp == 'y' and plucks1 > 0:
                        A_W_T_T = temp_sum / plucks1
                        average_water_table_temp.append(f'{label}_event - {A_W_T_T}')
    
    print(f'\nThe flow weighted concentration for the events are:\n{flow_weighted_concentration}\n')
    if water_table == 'y':
        print(f'These are the average water table depths for the events:\n{average_water_table_depth}\n')
    if water_temp == 'y':
        print(f'These are the average water temperatures for the events:\n{average_water_table_temp}\n')
    
    return {
        'events': caught_events,
        'flow_weighted_concentration': flow_weighted_concentration,
        'avg_water_table': average_water_table_depth,
        'avg_water_temp': average_water_table_temp,
        'plot_file': 'daily_events_plot.png',
        'event_data_file': 'daily_flow_event_data.txt',
        'base_data_file': 'daily_flow_base_data.txt'
    }

@app.route('/analyze-events', methods=['POST'])
def analyze_events():
    try:
        # Validate file upload
        if 'file' not in request.files:
            return jsonify({'message': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        if not file.filename.endswith('.csv'):
            return jsonify({'message': 'File must be a CSV'}), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract form data
        heading = 'y' if request.form.get('includeTableHeading') == 'true' else 'n'
        water_table = 'y' if request.form.get('avgWaterTable') == 'true' else 'n'
        water_temp = 'y' if request.form.get('eventAvgTemp') == 'true' else 'n'
        seasonal_method = request.form.get('seasonalMethod')  # 'A' or 'B'
        analysis_type = request.form.get('analysisType')  # 'Daily' or 'Hourly'
        thresholds = json.loads(request.form.get('thresholds'))
        winterr = float(thresholds['winter'])
        springg = float(thresholds['spring'])
        summerr = float(thresholds['summer'])
        falll = float(thresholds['fall'])
        
        # Run analysis
        if analysis_type == 'Daily':
            result = daily_events(file_path, heading, water_table, water_temp, winterr, springg, summerr, falll, seasonal_method)
        else:
            result = hourly_events(file_path, heading, water_table, water_table, winterr, springg, summerr, falll, seasonal_method)
        
        # Extract results
        events = result['events']
        flow_weighted_concentration = result['flow_weighted_concentration']
        avg_water_table = result['avg_water_table']
        avg_water_temp = result['avg_water_temp']
        plot_file = result['plot_file']
        event_data_file = result['event_data_file']
        base_data_file = result['base_data_file']
        
        # Prepare response
        response = {
            'ticker': 'EVENT_ANALYSIS',
            'event_date': list(events.values())[0] if events else 'N/A',
            'car': len(events),  # Number of events as a proxy for "car"
            'p_value': 0.05,  # Placeholder (replace with actual p-value if available)
            'avg_water_table': float(avg_water_table[0].split('-')[1]) if avg_water_table else None,
            'avg_water_temp': float(avg_water_temp[0].split('-')[1]) if avg_water_temp else None,
            'plotUrl': f'/uploads/{plot_file}' if plot_file else None,
            'textFileUrl': f'/Uploads/{event_data_file}'
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        print(f'Error in /analyze-events: {str(e)}')
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/log-usage', methods=['POST'])
def log_usage():
    try:
        data = request.get_json()
        print(f'Usage logged: {data}')
        return jsonify({'message': 'Usage logged'}), 200
    except Exception as e:
        print(f'Error in /log-usage: {str(e)}')
        return jsonify({'message': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)