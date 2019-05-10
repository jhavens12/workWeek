import datetime, pprint
import ui, os


w,h = ui.get_screen_size()
view = ui.View(bg_color = 'red', frame = (0,0,w,h)) #main view



view.present(style='sheet', hide_title_bar=True)
