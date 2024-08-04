#!/sw/pipeline/rendering/python3/venv/bin/python

""" 
This is the Changes Applied window of the Atomic Farm UI. Shows message saying
the changes made have been applied and asks if you would like to do more changes.
Created using PyQt5
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

import json
import os

import subprocess
import sys
from urllib.request import urlopen
from time import sleep
import datetime
from datetime import date
from functools import partial
from qtpy import QtGui, QtWidgets


class UiChangesAppliedMainWindow(QtWidgets.QMainWindow):
    """Main window for the 'Changes Applied' interface in the application.

    This class represents the main window that is displayed to the user after changes
    have been applied to the configuration. It allows the user to write changes to the
    configuration file, make additional changes, or exit/discard changes. The class
    handles the initialization of the user interface components, including setting up
    the main window, creating UI elements such as group boxes, labels, and buttons.

    Args:
        config_file_path_name (str): Path to the main configuration file.
        temp_folder (str): Path to the temporary folder.
        contents_dict (dict): Dictionary containing the contents of the configuration file.
        backup_folder (str): Path to the backup folder.
        new_values_full_dict (dict): Dictionary containing the new license
        values for each application.

    Methods:
        __init__(config_file_path_name, temp_folder, contents_dict, backup_folder,
        new_values_full_dict): Initializes the main window and sets up the user interface.
        setup_ui(): Configures the user interface components including window setup,
        group box creation, labels, and buttons.
        changes_applied_window_setup(): Configures the main window's title, size,
        style, and centers it on the screen.
        groupbox_creation(): Creates and configures a group box for the changes
        applied section.
        label_creation(): Creates and configures labels within the changes
        applied group box.
        button_creation(): Creates and configures buttons within the changes
        applied group box and connects them to their respective actions.
    """

    def __init__(
        self,
        config_file_path_name,
        temp_folder,
        contents_dict,
        backup_folder,
        new_values_full_dict,
    ):
        """Initializes an instance of the UiChangesAppliedMainWindow class.

        This constructor sets up the initial state and user interface components for the
        'Changes Applied' main window. It initializes the necessary UI components and fonts,
        and loads the provided configuration data.

        Args:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            contents_dict (dict): Dictionary containing the contents of the configuration file.
            backup_folder (str): Path to the backup folder.
            new_values_full_dict (dict): Dictionary containing the new license
            values for each application.

        Attributes:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            contents_dict (dict): Dictionary containing the contents of the configuration file.
            backup_folder (str): Path to the backup folder.
            new_values_full_dict (dict): Dictionary containing the new license
            values for each application.

        UI Components:
            centralwidget (QWidget): Central widget for the main window.
            changes_applied_groupbox (QGroupBox): Group box for the changes applied UI components.

        Fonts:
            l_font (QFont): Large, bold, italic font with underline for headings.
            s_font (QFont): Smaller font for other text elements.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # Incoming Variables
        self.config_file_path_name = config_file_path_name
        self.temp_folder = temp_folder
        self.contents_dict = contents_dict
        self.backup_folder = backup_folder
        self.new_values_full_dict = new_values_full_dict

        # Sections of the window
        self.centralwidget = ""
        self.changes_applied_groupbox = None

        # Fonts
        self.l_font = QtGui.QFont(
            "Cantarell", 14, QtGui.QFont.Bold, QtGui.QFont.StyleItalic
        )
        self.l_font.setUnderline(True)
        self.s_font = QtGui.QFont("Cantarell", 12)  # Smaller Font for most text

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the 'Changes Applied' main window.

        This method initializes and configures various UI components such as the main window setup,
        group boxes, labels, and buttons to provide a functional and interactive interface for
        applying changes.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """
        self.changes_applied_window_setup()
        self.groupbox_creation()
        self.label_creation()
        self.button_creation()

    def changes_applied_window_setup(self):
        """Sets up the main window of the 'Changes Applied' application.

        This method configures the main window's title, size, and style. It also
        centers the window on the screen.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Write File Window")
        # Window Size can be adjusted here
        self.setFixedSize(463, 161)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        def center_window(window):
            """Centers the given window on the screen.

            This method adjusts the position of the specified window to center it on the screen.
            It replaces a deprecated centering method by utilizing the current screen geometry.

            Parameters:
                window (QWidget): The window to be centered.

            Returns:
                None
            """

            # New method to replace the deprecated centering method

            frame = window.frameGeometry()
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())

            if screen is None:
                screen = QtGui.QGuiApplication.primaryScreen()

            frame.moveCenter(screen.geometry().center())
            window.move(frame.topLeft())

        center_window(self)

    def groupbox_creation(self):
        """Creates a group box for the "Changes Applied" window.

        This method sets up the group box within the main window. The group box contains
        UI elements related to writing changes to a file or making further modifications.
        It sets the title, geometry, and font for the group box.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """

        # Title of the Group Box
        self.changes_applied_groupbox = QtWidgets.QGroupBox(
            "Write to File Or Make More Changes", self.centralwidget
        )
        self.changes_applied_groupbox.setGeometry(10, 10, 441, 141)
        self.changes_applied_groupbox.setFont(self.l_font)

    def label_creation(self):
        """Creates labels within the "Changes Applied" group box.

        This method adds a label to the group box that asks the user if they would like
        to make more changes. It configures the label's text, geometry, font, and text
        wrapping properties to ensure proper display within the UI.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """

        question_label = QtWidgets.QLabel(
            "Would you like to make more changes?", self.changes_applied_groupbox
        )
        question_label.setGeometry(10, 35, 271, 61)
        question_label.setFont(self.s_font)
        question_label.setWordWrap(True)

    def button_creation(self):
        """Creates and configures the action buttons within the "Changes Applied" group box.

        This method sets up three buttons: "More Changes", "Exit/Discard", and "Write".
        Each button is configured with its respective text, geometry, font, and style.
        Additionally, the method connects each button to its corresponding slot or
        callback function to handle user interactions.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """

        # Text can be changed here
        more_changes_pushbutton = QtWidgets.QPushButton(
            "More Changes", self.changes_applied_groupbox
        )
        more_changes_pushbutton.setGeometry(160, 110, 121, 22)
        more_changes_pushbutton.setFont(self.s_font)
        more_changes_pushbutton.setStyleSheet("color : yellow")

        def more_changes_button_clicked():
            """Opens the main limits selection window for further modifications.

            This method imports the `UiAtomicCartoonsLimitsMainWindow` class from the
            `main_limits_selection_window` module and creates an instance of it.
            It then displays the limits selection window, allowing the user to
            make additional changes.

            Parameters:
                None

            Returns:
                None
            """

            from main_limits_selection_window import UiAtomicCartoonsLimitsMainWindow

            farm_selection_window = UiAtomicCartoonsLimitsMainWindow()
            farm_selection_window.show()

        more_changes_pushbutton.clicked.connect(more_changes_button_clicked)
        more_changes_pushbutton.clicked.connect(self.close)

        # Text can be changed here
        exit_pushbutton = QtWidgets.QPushButton(
            "Exit/Discard", self.changes_applied_groupbox
        )
        exit_pushbutton.setGeometry(310, 110, 121, 22)
        exit_pushbutton.setFont(self.s_font)
        exit_pushbutton.setStyleSheet("color : #D21404")

        def delete_tmp(tf):  # temp_folder
            tmp_file_name = f"{tf}temp.config"
            os.remove(tmp_file_name)

        exit_pushbutton.clicked.connect(partial(delete_tmp, self.temp_folder))
        exit_pushbutton.clicked.connect(self.close)

        # Text can be changed here
        write_button = QtWidgets.QPushButton("Write", self.changes_applied_groupbox)
        write_button.setGeometry(10, 110, 121, 22)
        write_button.setFont(self.s_font)
        write_button.setStyleSheet("color : #A7F432")

        def write_to_config():
            """Applies changes to the configuration file and updates the system.

            This method performs several tasks:
            1. It backs up the current configuration file if it exists.
            2. It removes a temporary configuration file.
            3. It writes the updated configuration data to the main configuration file.
            4. It reloads the configuration by running an external script.
            5. It verifies the successful application of changes by comparing
            values on a remote website.

            Parameters:
                None

            Returns:
                None
            """

            print("The write_to_config() method has started")

            # Move this to the next window
            if os.path.exists(self.config_file_path_name):

                backup_file_name = (
                    f"{self.backup_folder}D{date.today()}"
                    f"-T{datetime.datetime.now().strftime('%H:%M:%S')}.config"
                )

                final_backup_file = backup_file_name.replace(":", "")
                os.rename(self.config_file_path_name, final_backup_file)

                tmp_file_name = f"{self.temp_folder}temp.config"
                os.remove(tmp_file_name)

            json.dump(
                self.contents_dict, open(self.config_file_path_name, mode="w"), indent=4
            )

            # Reloads config file
            reload_process = subprocess.Popen(
                "/bin/bash /sw/pipeline/rendering/"
                "tractor-config-tools/reloadconfig_bash.sh",
                shell=True,
            )
            reload_process.wait()
            index = 1

            # Checking if the command was completed successfully
            if reload_process.returncode == 0:
                print("The first reload of the config file has just occurred :)")
                print("Command succeeded!")
            else:
                print("Command failed")

            # Loading website containing the updated '.config' file info
            web_info = urlopen("http://tractor-engine/Tractor/queue?q=limits")
            sleep(5)
            web_info_dict = json.load(web_info)
            print("Config-file website has just been fully loaded!")

            # Iterates through the 'New Values Directory' sent from the
            # previous window and compares every value to those in the
            # 'Tractor Limits' website.
            for application, limit in self.new_values_full_dict.items():
                web_value = web_info_dict["Limits"][application.lower()]["SiteMax"]
                index = 1
                print(web_value, limit)

                while web_value != limit:

                    web_info = urlopen("http://tractor-engine/Tractor/queue?q=limits")
                    sleep(5)
                    web_info_dict = json.load(web_info)
                    index += 1

                    if 1 < index < 7:
                        reload_process = subprocess.Popen(
                            "/bin/bash /sw/pipeline/rendering/"
                            "tractor-config-tools/reloadconfig_bash.sh",
                            shell=True,
                        )
                        reload_process.wait()

                        if reload_process.returncode == 0:
                            print("Command apparently succeeded in 'while' loop")
                        else:
                            print("Command failed")

                        print(f"Amount of config-reloads: {index}")

                    elif index == 8:
                        print(
                            "The Config was reloaded too many times before "
                            "this change could be properly applied. Attempt "
                            "to reload manually."
                        )
                        sys.exit()

        write_button.clicked.connect(write_to_config)
        write_button.clicked.connect(self.close)
