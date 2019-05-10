import datetime, pprint
import ui, os
import credentials
import requests

def format_text(x):
    x = float(x)
    return str("{0:.2f}".format(x))

def nt(time):
    hours = int(time)
    minutes = (time*60) % 60
    seconds = (time*3600) % 60
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def vis(w,h):
    vis = {}
    vis['side_margin'] = 3
    vis['w_adjusted'] = w-vis['side_margin']
    vis['top_margin'] = 35
    vis['other_label_height'] = 32
    vis['spacing_margin'] = 0

    #Subview
    vis['subview_w'] = w/2
    vis['subview_h'] = h/2.25
    vis['subview_y'] = (h/2) + vis['top_margin'] - (vis['subview_h']/2)
    vis['subview_x'] = w/2 - (vis['subview_w']/2)

    #Header
    vis['header_x'] = 0
    vis['header_y'] = 0
    vis['header_width'] = vis['subview_w']
    vis['header_height'] = vis['other_label_height']


    #Title Labels
    vis['title_label_x'] = vis['side_margin']
    vis['title_label_y'] = 20
    vis['title_label_width'] = vis['subview_w']-(vis['side_margin']*4)
    vis['title_label_height'] = 20
    vis['title_label_margins'] = -1

    #Buttons
    vis['button_height'] = 32 #above button_y
    vis['button_y'] = h - vis['button_height'] - 15 #view height minus button height plus some
    vis['button_width'] = vis['header_width']

    #Text Size?
    vis['title_label_size'] = 14
    vis['value_label_size'] = 16
    vis['header_label_size'] = 16

    return vis


def get_weekly_hours():

    input_var = '/api/states'
    url = credentials.api_url+input_var
    headers = {'x-ha-access': credentials.api_password,
               'content-type': 'application/json'}

    response = requests.get(url, headers=headers).json()
    response_dict = {}

    for x in response:
        if x['entity_id'] == 'sensor.work_this_week':
            response_dict['6'] = {}
            week_total = x['state']
            response_dict['6']['Total:'] = nt(float(x['state']))
        if x['entity_id'] == 'sensor.work_mhs_this_week':
            response_dict['3'] = {}
            response_dict['3']['Week MHS:'] = nt(float(x['state']))
        if x['entity_id'] == 'sensor.work_mems_this_week':
            response_dict['4'] = {}
            response_dict['4']['Week MEMS:'] = nt(float(x['state']))

        # if x['entity_id'] == 'sensor.work_mhs_today':
        #     response_dict['today mhs'] = format_text(x['state'])
        # if x['entity_id'] == 'sensor.work_mems_today':
        #     response_dict['today mems'] = format_text(x['state'])
        if x['entity_id'] == 'sensor.work_today':
            response_dict['1'] = {}
            response_dict['1']['Today:'] = nt(float(x['state']))

    response_dict['2'] = {}
    response_dict['2'][''] = ''

    response_dict['5'] = {}
    response_dict['5'][''] = ''

    diff = float(40)-float(week_total)
    response_dict['7'] = {}
    response_dict['7']['Difference:'] = nt(diff)

    timestamp = datetime.datetime.now()
    cur_weekday = timestamp.weekday()

    if cur_weekday == 4: #Friday
        leave_time = timestamp + datetime.timedelta(hours=diff)
        leave_time_n = str(leave_time.time()).split(".",1)[0]

        response_dict['8'] = {}
        response_dict['8'][''] = ''

        response_dict['9'] = {}
        response_dict['9']['Leave At:'] = str(leave_time_n)

    return response_dict


def gen_header(data):
    label = ui.Label(name = 'data', bg_color = 'transparent', frame = (vis['header_x'],vis['header_y'],vis['header_width'],vis['header_height']))
    label.border_color = 'black'
    label.text_color = 'black'#data['text_color']
    label.border_width = 0
    label.alignment = 1 #1 is center, #0 is left justified
    label.font = ('<system-bold>',vis['header_label_size'])
    label.number_of_lines = 1
    label.text = data
    return label

def gen_title_label(c,data_label):

    adjusted_label_y = vis['title_label_y'] + vis['title_label_height'] + ( c*( vis['title_label_height'] + vis['title_label_margins'] ) )
    c = c+1
    label_name = "tlabel"+str(c)
    label = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['title_label_x'], adjusted_label_y, vis['title_label_width'], vis['title_label_height']))
    label.border_color = 'black'
    label.text_color = 'black'#data['text_color']
    label.border_width = 0
    label.alignment = 0 #1 is center, #0 is left justified
    label.font = ('<system-bold>',vis['title_label_size'])
    label.number_of_lines = 1
    label.text = data_label
    return label

def gen_value_label(c,data):

    adjusted_label_y = vis['title_label_y'] + vis['title_label_height'] + ( c*( vis['title_label_height'] + vis['title_label_margins'] ) )
    c = c+1
    label_name = "tlabel"+str(c)
    label = ui.Label(name = label_name, bg_color ='transparent', frame = (vis['title_label_x'], adjusted_label_y, vis['title_label_width'], vis['title_label_height']))
    label.border_color = 'black'
    label.text_color = 'black'#data['text_color']
    label.border_width = 0
    label.alignment = 2 #1 is center, #0 is left justified, 2 is right justified
    label.font = ('<system-bold>',vis['title_label_size'])
    label.number_of_lines = 1
    label.text = data
    return label

w,h = ui.get_screen_size()
vis = vis(w,h)
view = ui.View(bg_color = 'red', frame = (0,0,w,h)) #main view
frame_1 = (vis['subview_x'], vis['subview_y'], vis['subview_w'], vis['subview_h'])
sview1 = ui.View(title='sview1', frame=frame_1, background_color = 'white', corner_radius = 10)

view.add_subview(sview1)

header = gen_header('Timesheet')
sview1.add_subview(header)
week_dict = get_weekly_hours()
pprint.pprint(week_dict)

for item in week_dict:
    c = int(item) #item is the number in the dictionary
    my_title = next(iter(week_dict[item].keys())) #pulls first (and only) key from the inside dictionary aka title
    my_value = next(iter(week_dict[item].values())) #pulls first (and only) value from the inside dictionary aka value

    set_title = gen_title_label(c,my_title)
    set_value = gen_value_label(c,my_value)

    sview1.add_subview(set_title)
    sview1.add_subview(set_value)


view.present(style='sheet', hide_title_bar=True)
