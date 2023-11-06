# Pixar_Tractor_Limits_UI

This complete UI has been created using PyQT and it serves as a way to manipulate a specific '.config' file which affects the limits for different 'Limit Tags' of a specific Show within Tractor Engine or the limits of a specific Application or License (Arnold, Katana, Maya, etc). This UI automatically adjusts its size and the amount of optons displayed according to how many shows there is.



show_limits_window.py
application_limits_window.py
changes_confirmation_window.py
changes_applied_window.py

- First window - (main_limits_selection_window.py) allows for the selection of what the user wishes to adjust. This could be the "Show Defined Limits" or the "License/Application Limits".
show_selection_window.py - (depending on the selection, either  or  will run) displays a list of all available Shows as a dropdown (the list is auto-generated from the '.config' file) and allows the user to select one.
Last Window (changes_applied_window.py) will allow the user to stage and push the changes to the '.config' file, choose to go back to the first window and make more changes (this will create a temporary '.config' file) or simply exit and discard all changes.
After the changes have been submitted, the terminal running the script will display a multiple messages related to the success of the tool changing the '.config' file and reloading Tractor while comparing the values to the ones that are currently live.
