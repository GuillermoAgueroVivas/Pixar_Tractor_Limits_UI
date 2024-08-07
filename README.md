# Pixar_Tractor_Limits_UI

This complete UI has been created using PyQT and it serves as a way to manipulate a specific '.config' file which affects the limits for different 'Limit Tags' of a specific Show within Tractor Engine or the limits of a specific Application or License (Arnold, Katana, Maya, etc). This UI automatically adjusts its size and the amount of optons displayed according to how many shows there is.

- **main_limits_selection_window.py:** allows for the selection of what the user wishes to adjust. This could be the "Show Defined Limits" or the "License/Application Limits".

**Show Defined Limits:**
- **show_selection_window.py:** depending on the selection of the first window, this window may not run. It displays a list of all available Shows as a dropdown (the list is auto-generated from the '.config' file) and allows the user to select one and therefore show the limits of that Show on the next window.
- **show_limits_window.py:** This window shows all 'Limit Tags' available within the show selected on the previous window together with a set of combo-boxes showing their current value.

**OR**

**License/Application Limits:**
- **application_limits_window.py:** depending on the selection of the first window, this window may not run. It displays all 'Limit Tags' related to different 'Applications' and 'Licenses' within the '.config' file, together with a set of combo-boxes showing their current value.

**Confirmation Window / Changes Applied Window:**
- **changes_confirmation_window.py:** This window will allow the user to stage and push the changes to the '.config' file, choose to go back to the first window and make more changes (this will create a temporary '.config' file) or simply exit and discard all changes.
changes_applied_window.py

After the changes have been submitted, the terminal running the script will display a multiple messages related to the success of the tool changing the '.config' file and reloading Tractor while comparing the values to the ones that are currently live.

**Please note **
- For this UI to work in a different environment, a '.config' file is necessary as well as changing the paths required in the first window
- The images have the name of Shows covered due to NDA agreements

