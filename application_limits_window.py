#!/sw/pipeline/rendering/python3/venv/bin/python

""" 
This window opens up when selected through the 'Application_Limits_Selection_Window'
of the Atomic Limits UI. Created using PyQt5.
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

import json
import os
from collections import OrderedDict
from qtpy import QtCore, QtGui, QtWidgets

# Main Window
from changes_confirmation_window import UiConfirmFarmChangesMainWindow


class UiApplicationLimitsMainWindow(QtWidgets.QMainWindow):
    """
    The main window class for managing application limits.

    This class sets up the initial state and user interface components for the application.
    It defines paths for the configuration, temporary, and backup folders, initializes
    necessary UI components and fonts, and loads configuration data.

    Args:
        config_file_path_name (str): Path to the main configuration file.
        temp_folder (str): Path to the temporary folder.
        backup_folder (str): Path to the backup folder.

    Methods:
        setup_ui(): Sets up the user interface components.
        create_applications_list(): Creates a list of applications based on the config file.
        application_limits_window_setup(): Sets up the application limits window.
        groupbox_creation(): Creates a group box widget for limit selection.
        groupbox_info_creation(): Adjusts the size and position of the group
        box and creates sliders and spin boxes for each show.
        info_label_creation(): Creates information labels within the application
        limits group box.
        button_creation(): Creates 'submit' and 'cancel' buttons within the
        application limits group box.
        submit_button_clicked(): Calls upon the Confirmation Window to check
        the values changed and continue the process.
        cancel_button_clicked(): Calls upon the main window of the UI if the
        user decides to cancel the process.
    """

    def __init__(self, config_file_path_name, temp_folder, backup_folder):
        """
        Initializes an instance of the class.

        This constructor sets up the initial state and user interface components
        for the application. It defines the paths for the configuration, temporary,
        and backup folders, initializes the necessary UI components and fonts, and
        loads the configuration data.

        Args:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.

        Attributes:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.
            applications (list): List to store application names.
            current_values_full_dict (dict): Dictionary to store current values.
            spin_boxes_list (list): List to store spin box widgets.

        UI Components:
            centralwidget (QWidget): Central widget for the main window.
            app_limits_groupbox (QGroupBox): Group box for application limits UI components.
            show_select_window_ui (object): UI object for the show selection window.
            app_selection_limits_ui (object): UI object for the application selection limits.


        Config File:
            contents_dict (dict): Dictionary to store the contents of the configuration file.

        Fonts:
            l_font (QFont): Large, bold, italic font with underline for headings.
            m_font (QFont): Medium, bold font with underline for subheadings.
            s_font (QFont): Smaller font for other text elements.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # All Folders
        self.config_file_path_name = config_file_path_name
        self.temp_folder = temp_folder
        self.backup_folder = backup_folder

        # Variables
        self.applications = []
        self.current_values_full_dict = dict()
        self.spin_boxes_list = []

        # Sections of the window
        self.centralwidget = ""
        self.app_limits_groupbox = None

        # Opening config file
        temp_file_name = f"{self.temp_folder}temp.config"

        if os.path.exists(temp_file_name):
            # Opening temp. config file
            with open(temp_file_name, "r") as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)
        else:
            # Opening config file
            with open(config_file_path_name, "r") as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        # Fonts
        self.l_font = QtGui.QFont(
            "Cantarell", 14, QtGui.QFont.Bold, QtGui.QFont.StyleItalic
        )
        self.l_font.setUnderline(True)

        self.m_font = QtGui.QFont(
            "Cantarell",
            11,
            QtGui.QFont.Bold,
        )
        self.m_font.setUnderline(True)
        self.s_font = QtGui.QFont("Cantarell", 12)

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the App Limits application.

        This method initializes and configures the main window of the App Limits UI.
        It sets up various UI components such as the applications list, group boxes,
        information labels, and buttons to provide a functional and interactive
        interface for the application limits management.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.create_applications_list()
        self.application_limits_window_setup()
        self.groupbox_creation()
        self.groupbox_info_creation()
        self.info_label_creation()
        self.button_creation()

    def create_applications_list(self):
        """Creates a list of applications based on the contents of the config file.

        This method generates a list of application names by filtering out unwanted
        shows and specific keywords from the configuration file. It first gathers
        all shows from the Linux farm that are considered unwanted and adds them
        to a list of terms to avoid. It then iterates over the configuration keys,
        adding only those that do not match any of the unwanted terms to the
        applications list.

        Attributes:
            self (object): The object instance

        Returns:
            None
        """

        # This generates a list of all shows in the linux farm
        unwanted_shows = []
        for key in self.contents_dict["Limits"]["linuxfarm"]["Shares"].keys():
            lower_key = str(key.lower())
            unwanted_shows.append(lower_key)

        # List for all applications in the config file (avoiding all unwanted
        # shows and others)
        avoid = ["linux", "windows", "yeti"]
        for show in unwanted_shows:
            avoid.append(show)

        for key in self.contents_dict["Limits"].keys():
            if all(word not in key for word in avoid):
                self.applications.append(key)

    def application_limits_window_setup(self):
        """Sets up the application limits window, including the window's size,
        style, and title, and centers it on the screen.

        This method configures the main window for the application limits
        interface by setting its title, fixed size, and style sheet. It also
        initializes the central widget and centers the window on the screen
        using a method that replaces the deprecated centering technique.

        Parameters:
            self (object): The object instance

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Application Limits Window")
        # Window Size can be adjusted here
        self.setFixedSize(955, 430)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        def center_window(window):

            # New method to replace the deprecated centering method

            frame = window.frameGeometry()
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())

            if screen is None:
                screen = QtGui.QGuiApplication.primaryScreen()

            frame.moveCenter(screen.geometry().center())
            window.move(frame.topLeft())

        center_window(self)

    def groupbox_creation(self):
        """Creates a group box widget for limit selection.

        Parameters:
            self (QtWidgets.QWidget): The class object.

        Returns:
            None
        """

        # Title of the Group Box
        self.app_limits_groupbox = QtWidgets.QGroupBox(
            "Application Limits", self.centralwidget
        )
        self.app_limits_groupbox.setFont(self.l_font)
        self.app_limits_groupbox.setGeometry(10, 10, 935, 410)

    def groupbox_info_creation(self):
        """Adjusts the size and position of the group box and creates sliders
        and spin boxes for each show.

        Parameters:
            self (object): The class object containing the group box and
            applications list.

        Returns:
            None
        """

        label_y_axis_value = 45  # Initial values for the first column
        label_y_axis_original = label_y_axis_value
        box_y_axis_value = 72
        box_y_axis_original = box_y_axis_value
        x_axis_value = 270

        labels_list = []

        def label_creation(
            capital_app,
            label_y_axis_value,
            x_axis_value,
        ):
            """Creates a label for a given application and sets its properties.

            Parameters:
                capital_app (str): The capitalized name of the application for the label.
                label_y_axis_value (int): The y-axis coordinate for the label's position.
                x_axis_value (int): The x-axis coordinate for the label's position.

            Returns:
                label (QtWidgets.QLabel): The created label widget.
            """
            # Tests
            label = QtWidgets.QLabel(capital_app, self.app_limits_groupbox)
            label.setGeometry(x_axis_value, label_y_axis_value, 100, 20)
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)

            return label

        def spin_box_creation(application, box_y_axis_value, x_axis_value):
            """Creates a spin box for a given application and sets its properties.

            Parameters:
                application (str): The name of the application associated with the spin box.
                box_y_axis_value (int): The y-axis coordinate for the spin box's position.
                x_axis_value (int): The x-axis coordinate for the spin box's position.

            Returns:
                spinbox (QtWidgets.QSpinBox): The created spin box widget.
            """
            minimum = 0
            maximum = 10000

            spinbox = QtWidgets.QSpinBox(self.app_limits_groupbox)
            spinbox.setGeometry(x_axis_value, box_y_axis_value, 68, 22)
            spinbox.setFont(self.s_font)
            spinbox.setObjectName(f"{application}_spinBox")
            spinbox.setMinimum(minimum)
            spinbox.setMaximum(maximum)

            return spinbox

        def current_values_application(application, spinbox, capital_app):
            """Updates the dictionary with the current values for an application.

            Parameters:
                application (str): The name of the application.
                spinbox (QtWidgets.QSpinBox): The spin box widget associated
                with the application.
                capital_app (str): The capitalized name of the application.

            Returns:
                None
            """

            current_value = self.contents_dict["Limits"][application]["SiteMax"]
            spinbox.setValue(current_value)
            self.current_values_full_dict.update({capital_app: current_value})

        for application in self.applications:

            capital_app = application.capitalize()
            label = label_creation(
                capital_app,
                label_y_axis_value,
                x_axis_value,
            )
            labels_list.append(label)
            spin_box = spin_box_creation(application, box_y_axis_value, x_axis_value)
            self.spin_boxes_list.append(spin_box)

            # Getting current Percentages per application to be able to pass it
            # to the Confirmation Window
            current_values_application(application, spin_box, capital_app)

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

    def info_label_creation(self):
        """Creates information labels within the application limits group box.

        Parameters:
            self (object): The class object where the labels will be added.

        Returns:
            None
        """

        # Main Definition label
        def_label = QtWidgets.QLabel(
            "To the right side you will see a list of all current available "
            "applications with license limits with their current values.",
            self.app_limits_groupbox,
        )
        def_label.setGeometry(10, 50, 200, 71)  # 10, 50, 200, 71
        def_label.setFont(self.s_font)
        def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        def_label.setScaledContents(False)
        def_label.setWordWrap(True)
        # def_label.setObjectName("def_label")

        # Second Definition Label
        def_label_boxes = QtWidgets.QLabel(
            "Utilizing the available spin boxes, please change the amount "
            "of licenses of any application accordingly: ",
            self.app_limits_groupbox,
        )
        def_label_boxes.setGeometry(10, 140, 201, 81)
        def_label_boxes.setFont(self.s_font)
        def_label_boxes.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        def_label_boxes.setScaledContents(False)
        def_label_boxes.setWordWrap(True)

    def button_creation(self):
        """Creates 'submit' and 'cancel' buttons within the application limits
        group box.

        Parameters:
            self (object): The class object where the buttons will be added.

        Returns:
            None
        """

        # Name can be changed here
        submit_push_button = QtWidgets.QPushButton("Submit", self.app_limits_groupbox)
        submit_push_button.setGeometry(735, 380, 91, 22)
        submit_push_button.setFont(self.s_font)

        submit_push_button.clicked.connect(self.submit_button_clicked)
        submit_push_button.clicked.connect(self.close)

        # Name can be changed here
        cancel_push_button = QtWidgets.QPushButton("Cancel", self.app_limits_groupbox)
        cancel_push_button.setGeometry(835, 380, 91, 22)
        cancel_push_button.setFont(self.s_font)
        # cancel_push_button.setObjectName("cancel_push_button")

        cancel_push_button.clicked.connect(self.cancel_button_clicked)
        cancel_push_button.clicked.connect(self.close)

    def submit_button_clicked(self):
        """Calls upon the Confirmation Window to check the values changed in
        this window and continue the process.

        Parameters:
            self (object): The class object for managing the confirmation process.

        Returns:
            None
        """

        new_values_list = []
        capital_apps_list = []
        for app in self.applications:
            capital_apps_list.append(app.capitalize())

        for box in self.spin_boxes_list:
            new_value = box.value()
            new_values_list.append(new_value)

        new_values_full_dict = dict(zip(capital_apps_list, new_values_list))
        changes_confirmation_window = UiConfirmFarmChangesMainWindow(
            self.current_values_full_dict,
            new_values_full_dict,
            self.contents_dict,
            self.config_file_path_name,
            self.temp_folder,
            self.backup_folder,
        )

        changes_confirmation_window.show()
        self.close()

    def cancel_button_clicked(self):
        """Calls upon the main window of the UI if the user decides to cancel
        the process.

        Parameters:
            self (object): The class object for managing the UI transition.

        Returns:
            None
        """

        from main_limits_selection_window import UiAtomicCartoonsLimitsMainWindow

        farm_selection_windows = UiAtomicCartoonsLimitsMainWindow()
        farm_selection_windows.show()
