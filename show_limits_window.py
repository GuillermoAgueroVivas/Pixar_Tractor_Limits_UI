#!/usr/bin/python3

""" 
This window opens up when selected through the 'Farm_Selection_Window' of the Farm UI.
Represents the Linux Farm as a whole.
Created using PyQt5.
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD
"""

import json
import os
from collections import OrderedDict
from qtpy import QtCore, QtGui, QtWidgets

from changes_confirmation_window import UiConfirmFarmChangesMainWindow


class UiShowLimitsMainWindow(QtWidgets.QMainWindow):
    """
    This class represents the main window for the Show Limits application within
    the Farm UI. It provides a user interface to display and manage the license
    limits for a specific show.

    The window allows users to view current license limits, adjust them using
    spin boxes, and submit or cancel their changes.

    Methods:
        setup_ui(): Sets up the user interface components.
        create_show_limit_sections(): Creates a list of show limit sections based
        on the provided show name.
        show_limits_window_setup(): Sets up the main window for the Show Limits
        application.
        groupbox_creation(): Creates and sets up the group box for the Show Limits window.
        groupbox_info_creation(): Creates and configures the labels and spin boxes
        within the show limits group box.
        update_current_values(limit, spinbox, capital_limit): Applies the current values
        from the configuration to the spin boxes and updates the dictionary of current values.
        info_label_creation(): Creates informational labels within the show limits group box.
        button_creation(): Creates and configures the Submit and Cancel buttons within
        the show limits group box.
        cancel_button_clicked(): Handles the click event of the Cancel button.
    """

    def __init__(self, show, config_file_path_name, temp_folder, backup_folder):
        """Initializes the instance of the UiShowLimitsMainWindow class.

        This constructor sets up the initial state and user interface components for
        managing show limits in the Farm UI. It initializes the necessary attributes
        and prepares the UI elements for displaying and modifying show limits.

        Parameters:
            show (str): The name of the show.
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.

        UI Components:
            centralwidget (QWidget): Central widget for the main window.
            show_limit_sections (list): List to hold sections related to show limits.
            show_limits_groupbox (QGroupBox): Group box containing UI elements
            related to show limits.
            spinboxes_list (list): List to hold QSpinBox widgets for adjusting
            show limits.
            current_values_full_dict (dict): Dictionary to store the current
            full values for the show limits.

        Fonts:
            l_font (QFont): Large, bold, italic font with underline for headings.
            m_font (QFont): Medium, bold font with underline for sub-headings.
            s_font (QFont): Smaller font for most text elements.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # Variables
        self.show_name = show
        self.config_file_path_name = config_file_path_name
        self.temp_folder = temp_folder
        self.backup_folder = backup_folder

        # Sections of the window
        self.centralwidget = ""
        self.show_limit_sections = []
        self.show_limits_groupbox = None
        self.spinboxes_list = []
        self.current_values_full_dict = dict()

        # Fonts
        self.l_font = QtGui.QFont(
            "Cantarell", 14, QtGui.QFont.Bold, QtGui.QFont.StyleItalic
        )
        self.l_font.setUnderline(True)
        self.m_font = QtGui.QFont(
            "Cantarell",
            12,
            QtGui.QFont.Bold,
        )
        self.m_font.setUnderline(True)
        self.s_font = QtGui.QFont("Cantarell", 11)  # Smaller Font for most text

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the Show Limits application.

        This method initializes the UI components, loads configuration data, and
        prepares the main window for displaying and adjusting show limits.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        if os.path.exists(self.temp_folder + "temp.config"):
            # Opening config file
            with open(self.temp_folder + "temp.config", "r") as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)
        else:
            # Opening config file
            with open(self.config_file_path_name, "r") as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        self.create_show_limit_sections()
        self.show_limits_window_setup()
        self.groupbox_creation()
        self.groupbox_info_creation()
        self.info_label_creation()
        self.button_creation()

    def create_show_limit_sections(self):
        """Creates a list of show limit sections based on the provided show name.

        This method populates the `show_limit_sections` attribute with sections
        that match the given show name.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """
        low_cap_show = self.show_name.lower()
        show_search = f"{low_cap_show}_"
        extras_pwp = "yeti_"

        # This generates a list of all shows with limits available for change
        for key in self.contents_dict["Limits"].keys():
            if show_search in key:
                self.show_limit_sections.append(key)

        # Adds any extra settings PWP has regarding Yeti
        if "pwp" in show_search:
            for key in self.contents_dict["Limits"].keys():
                if extras_pwp in key:
                    self.show_limit_sections.append(key)

    def show_limits_window_setup(self):
        """Sets up the main window for the Show Limits application.

        This method configures the window title, size, style sheet, and central widget
        for the Show Limits application. It also centers the window on the screen.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """
        # Title
        self.setWindowTitle("Show Limits Window")
        self.setFixedSize(730, 430)  # Window Size can be adjusted
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )
        # Using this style sheet the theme can be changed
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        def center_window(window):

            frame = window.frameGeometry()
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())

            if screen is None:
                screen = QtGui.QGuiApplication.primaryScreen()

            frame.moveCenter(screen.geometry().center())
            window.move(frame.topLeft())

        center_window(self)

    def groupbox_creation(self):
        """Creates and sets up the group box for the Show Limits window.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Group Box
        self.show_limits_groupbox = QtWidgets.QGroupBox(
            "Show Limits", self.centralwidget
        )
        self.show_limits_groupbox.setGeometry(10, 10, 710, 410)
        self.show_limits_groupbox.setFont(self.l_font)

    def groupbox_info_creation(self):
        """Creates and configures the labels and spin boxes within the show limits
        group box.

        This method dynamically generates labels and spin boxes for each show limit
        section, setting their properties and positioning them within the group box.
        It ensures the elements are properly arranged in multiple columns as needed.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Y-axis values for both Labels and Boxes individually
        label_y_axis_value = 45  # Initial values for the first column
        label_y_axis_original = label_y_axis_value
        box_y_axis_value = 72
        box_y_axis_original = box_y_axis_value
        # X-axis value for both Labels and Boxes together
        x_axis_value = 270

        labels_list = []

        def label_creation(
            capital_limit,
            label_y_axis_value,
            x_axis_value,
        ):
            """Creates a label within the show limits group box.

            Parameters:
                capital_limit (str): The text for the label.
                label_y_axis_value (int): The Y-axis position of the label.
                x_axis_value (int): The X-axis position of the label.

            Returns:
                QLabel: The created label widget.
            """

            # Tests
            label = QtWidgets.QLabel(capital_limit, self.show_limits_groupbox)
            label.setGeometry(x_axis_value, label_y_axis_value, 100, 20)
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)

            return label

        def spin_box_creation(limit, box_y_axis_value, x_axis_value):
            """Creates a spin box within the show limits group box.

            Parameters:
                limit (str): The name of the limit associated with the spin box.
                box_y_axis_value (int): The Y-axis position of the spin box.
                x_axis_value (int): The X-axis position of the spin box.

            Returns:
                QSpinBox: The created spin box widget.
            """

            # Minimum and Maximum for all spin boxes
            minimum = 0
            maximum = 10000

            spinbox = QtWidgets.QSpinBox(self.show_limits_groupbox)
            spinbox.setGeometry(x_axis_value, box_y_axis_value, 68, 22)
            spinbox.setFont(self.s_font)
            spinbox.setObjectName(f"{limit}_spinBox")
            spinbox.setMinimum(minimum)
            spinbox.setMaximum(maximum)

            return spinbox

        for limit in self.show_limit_sections:

            capital_limit = limit.capitalize()
            label = label_creation(
                capital_limit,
                label_y_axis_value,
                x_axis_value,
            )
            labels_list.append(label)
            spin_box = spin_box_creation(limit, box_y_axis_value, x_axis_value)
            self.spinboxes_list.append(spin_box)
            self.update_current_values(limit, spin_box, capital_limit)

            label_y_axis_value += 65
            box_y_axis_value += 65

            if len(labels_list) == 5:  # After this many labels, creates a new column
                label_y_axis_value = label_y_axis_original
                box_y_axis_value = box_y_axis_original
                x_axis_value = 435
            elif len(labels_list) == 10:
                label_y_axis_value = label_y_axis_original
                box_y_axis_value = box_y_axis_original
                x_axis_value = 600
            elif len(labels_list) == 15:
                label_y_axis_value = label_y_axis_original
                box_y_axis_value = box_y_axis_original
                x_axis_value = 765

    def update_current_values(self, limit, spinbox, capital_limit):
        """
        Applies the current values from the configuration to the spin boxes and updates
        the dictionary of current values.

        This method retrieves the current site maximum value for a given limit from the
        configuration dictionary, sets this value to the corresponding spin box, and
        updates the internal dictionary with the capitalized limit name and its value.

        Parameters:
            self (object): The object instance.
            limit (str): The key representing the limit in the configuration dictionary.
            spinbox (QSpinBox): The spin box widget to set the value for.
            capital_limit (str): The capitalized limit name used as a key in
            the internal dictionary.

        Returns:
            None
        """

        current_value = self.contents_dict["Limits"][limit]["SiteMax"]
        spinbox.setValue(current_value)
        self.current_values_full_dict.update({capital_limit: current_value})

    def info_label_creation(self):
        """Creates informational labels within the show limits group box.

        This method creates and configures two QLabel objects that provide
        instructions and information to the user regarding the current license
        limits and the use of spin boxes for adjusting these limits.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Main Definition label
        def_label = QtWidgets.QLabel(
            f"To the right side you will see a list of all current available "
            f"keys with license limits for {self.show_name} with its "
            f"current values.",
            self.show_limits_groupbox,
        )
        def_label.setGeometry(10, 50, 200, 71)
        def_label.setFont(self.s_font)
        def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        def_label.setScaledContents(False)
        def_label.setWordWrap(True)

        # Second Definition Label
        def_label_boxes = QtWidgets.QLabel(
            "Utilizing the available spin boxes, please change the "
            "limits per section accordingly: ",
            self.show_limits_groupbox,
        )
        def_label_boxes.setGeometry(10, 140, 201, 81)
        def_label_boxes.setFont(self.s_font)
        def_label_boxes.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        def_label_boxes.setScaledContents(False)
        def_label_boxes.setWordWrap(True)

    def button_creation(self):
        """Creates and configures the Submit and Cancel buttons within the show
        limits group box.

        The Submit button collects the new values from the spin boxes and
        passes them to the confirmation window for further action. The Cancel
        button discards the changes and closes the window.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Name can be changed here
        submit_pushbutton = QtWidgets.QPushButton("Submit", self.show_limits_groupbox)
        submit_pushbutton.setGeometry(495, 375, 91, 22)
        submit_pushbutton.setFont(self.s_font)

        # Runs when submit button is clicked
        # config_file_path_name, temp_folder, backup_folder
        def submit_button_clicked():
            """Handles the click event of the Submit button.

            This method collects the new values from the spin boxes and
            creates a dictionary with the updated values. It then opens the
            confirmation window to review the changes.

            Parameters:
                None

            Returns:
                None
            """

            new_values_list = []
            capital_key_list = []
            for limit in self.show_limit_sections:
                capital_key_list.append(limit.capitalize())
            for box in self.spinboxes_list:
                new_value = box.value()
                new_values_list.append(new_value)

            new_values_full_dict = dict(zip(capital_key_list, new_values_list))
            changes_confirmation_window = UiConfirmFarmChangesMainWindow(
                self.current_values_full_dict,
                new_values_full_dict,
                self.contents_dict,
                self.config_file_path_name,
                self.temp_folder,
                self.backup_folder,
            )

            changes_confirmation_window.show()

        submit_pushbutton.clicked.connect(submit_button_clicked)
        submit_pushbutton.clicked.connect(self.close)

        # Name can be changed here
        cancel_pushbutton = QtWidgets.QPushButton("Cancel", self.show_limits_groupbox)
        cancel_pushbutton.setGeometry(605, 375, 91, 22)
        cancel_pushbutton.setFont(self.s_font)

        cancel_pushbutton.clicked.connect(self.cancel_button_clicked)
        cancel_pushbutton.clicked.connect(self.close)

    def cancel_button_clicked(self):
        """Handles the click event of the Cancel button.

        This method opens the main limits selection window, allowing the user
        to go back and select different options or cancel the current operation.
        It also closes the current window.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        from main_limits_selection_window import UiLimitsMainWindow

        farm_selection_windows = UiLimitsMainWindow()
        farm_selection_windows.show()
        self.close()
