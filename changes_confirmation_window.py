#!/usr/bin/python3

""" 
This is the Changes Confirmation window of the Farm UI. Helps the user
see the changes to be made before they are applied.
Created using PyQt5
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

import json
from qtpy import QtGui, QtWidgets

from changes_applied_window import UiChangesAppliedMainWindow
from main_limits_selection_window import UiLimitsMainWindow


class UiConfirmFarmChangesMainWindow(QtWidgets.QMainWindow):
    """The main window class for confirming changes in application limits.

    This class sets up the initial state and user interface components for the
    'Confirm Changes' main window. It defines paths for the configuration,
    temporary, and backup folders, initializes necessary UI components and
    fonts, and loads the provided configuration data.

    Args:
        current_values_full_dict (dict): Dictionary containing the current
        license values for each application.
        new_values_full_dict (dict): Dictionary containing the new license
        values for each application.
        contents_dict (dict): Dictionary containing the contents of the
        configuration file.
        config_file_path_name (str): Path to the main configuration file.
        temp_folder (str): Path to the temporary folder.
        backup_folder (str): Path to the backup folder.

    Methods:
        setup_ui(): Sets up the user interface components.
        changes_confirm_window_setup(): Configures the main window for the
        changes confirmation interface.
        groupbox_creation(): Creates a group box for the 'Review Your Changes'
        section of the window.
        text_browser_creation(): Creates text browsers for displaying current
        and new application limits.
        label_creation(): Creates labels for the 'Review Your Changes' group box.
        button_creation(): Creates and configures buttons for the
        'Review Your Changes' group box.
        cancel_button_clicked(): Opens the main Farm Selection Window if the
        user decides to cancel the process.
    """

    def __init__(
        self,
        current_values_full_dict,
        new_values_full_dict,
        contents_dict,
        config_file_path_name,
        temp_folder,
        backup_folder,
    ):
        """Initializes an instance of the class.

        This constructor sets up the initial state and user interface components
        for the 'Confirm Changes' main window. It defines the paths for the configuration,
        temporary, and backup folders, initializes the necessary UI components and fonts,
        and loads the provided configuration data.

        Args:
            current_values_full_dict (dict): Dictionary containing the current
            license values for each application.
            new_values_full_dict (dict): Dictionary containing the new license
            values for each application.
            contents_dict (dict): Dictionary containing the contents of the configuration file.
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.

        Attributes:
            current_values_full_dict (dict): Dictionary containing the current
            license values for each application.
            new_values_full_dict (dict): Dictionary containing the new license
            values for each application.
            contents_dict (dict): Dictionary containing the contents of the
            configuration file.
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.
            centralwidget (QWidget): Central widget for the main window.
            confirm_changes_groupbox (QGroupBox): Group box for the confirm
            changes UI components.

        Fonts:
            l_font (QFont): Large, bold, italic font with underline for headings.
            s_font (QFont): Smaller font for other text elements, set to thin weight.

        Calls:
            setup_ui(): Configures the user interface components.
        """

        super().__init__()

        # Variables
        self.current_values_full_dict = current_values_full_dict
        self.new_values_full_dict = new_values_full_dict
        self.contents_dict = contents_dict
        self.config_file_path_name = config_file_path_name
        self.temp_folder = temp_folder
        self.backup_folder = backup_folder

        # Sections of the window
        self.centralwidget = ""
        self.confirm_changes_groupbox = None

        # Fonts
        self.l_font = QtGui.QFont(
            "Cantarell", 14, QtGui.QFont.Bold, QtGui.QFont.StyleItalic
        )
        self.l_font.setUnderline(True)

        self.s_font = QtGui.QFont("Cantarell", 12)  # Smaller Font for most text
        self.s_font.setWeight(QtGui.QFont.Thin)

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the App Limits application.

        This method initializes and configures the changes confirmation
        window of the App Limits UI. It sets up various UI components such as
        the applications list, group boxes, information labels, and buttons to
        provide a functional and interactive interface for the application
        limits management.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.changes_confirm_window_setup()
        # Create the groupbox
        self.groupbox_creation()
        # Create Text Browser
        self.text_browser_creation()
        # Label Creation
        self.label_creation()
        # Button Creation
        self.button_creation()

    def changes_confirm_window_setup(self):
        """Sets up the changes confirmation window, including the window's size,
        style, and title, and centers it on the screen.

        This method configures the main window for the changes confirmation
        interface by setting its title, fixed size, and style sheet. It also
        initializes the central widget and centers the window on the screen
        using a method that replaces the deprecated centering technique.

        Parameters:
            self (object): The object instance

        Returns:
            None
        """

        # Title of the Window can be changed here.
        self.setWindowTitle("Changes Confirmation Window")
        # Window Size can be adjusted here
        self.setFixedSize(463, 349)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )
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
        """Creates a group box for the "Review Your Changes" section of the window.

        This method sets up the group box within the main window. The group box contains
        UI elements related to reviewing the changes made by the user. It sets the title,
        geometry, and font for the group box.

        Parameters:
            self (object): The object instance

        Returns:
            None
        """
        # Title of the Group Box
        self.confirm_changes_groupbox = QtWidgets.QGroupBox(
            "Review Your Changes", self.centralwidget
        )
        self.confirm_changes_groupbox.setFont(self.l_font)
        self.confirm_changes_groupbox.setGeometry(10, 10, 441, 331)

    def text_browser_creation(self):
        """
        Creates text browsers for displaying current and new application limits.

        This method sets up two read-only QTextBrowser widgets within the
        "Review Your Changes" group box. The first text browser displays the
        current application limits, and the second text browser displays the
        new application limits. It configures the geometry and font for each
        text browser and populates them with the respective data.

        Parameters:
            self (object): The object instance

        Returns:
            None
        """

        before_text_browser = QtWidgets.QTextBrowser(self.confirm_changes_groupbox)
        before_text_browser.setGeometry(10, 140, 141, 131)
        before_text_browser.setFont(self.s_font)
        before_text_browser.setReadOnly(True)

        for application, limits in self.current_values_full_dict.items():
            before_text_browser.append(f"{application}: {limits}")

        after_text_browser = QtWidgets.QTextBrowser(self.confirm_changes_groupbox)
        after_text_browser.setGeometry(230, 140, 141, 131)
        after_text_browser.setFont(self.s_font)
        after_text_browser.setReadOnly(True)
        after_text_browser.setObjectName("after_text_browser")

        for application, limits in self.new_values_full_dict.items():
            after_text_browser.append(f"{application}: {limits}")

    def label_creation(self):
        """Creates labels for the "Review Your Changes" group box.

        This method sets up and configures several QLabel widgets within
        the "Review Your Changes" group box. These labels provide instructional
        text and headings for the text browsers that display the current and
        new application limits. The method configures the text, geometry, font,
        word wrap, and style for each label.

        Parameters:
            self (object): The object instance

        Returns:
            None
        """

        # Text inside the label can be changed here
        review_changes_label = QtWidgets.QLabel(
            "Please take a close look below to compare the changes "
            "you have made against the previous settings before you fully "
            "apply them:",
            self.confirm_changes_groupbox,
        )
        review_changes_label.setGeometry(10, 40, 421, 61)
        review_changes_label.setFont(self.s_font)
        review_changes_label.setWordWrap(True)

        before_label = QtWidgets.QLabel("Before:", self.confirm_changes_groupbox)
        before_label.setGeometry(10, 110, 61, 20)
        before_label.setFont(self.l_font)
        before_label.setWordWrap(True)
        before_label.setStyleSheet("color : #D21404")

        after_label = QtWidgets.QLabel("After:", self.confirm_changes_groupbox)
        after_label.setGeometry(230, 110, 51, 20)
        after_label.setFont(self.l_font)
        after_label.setWordWrap(True)
        after_label.setStyleSheet("color : #A7F432")

    def button_creation(self):
        """Creates and configures buttons for the "Review Your Changes" group box.

        This method sets up two buttons: "Stage" and "Cancel" within the
        "Review Your Changes" group box. It configures each button's text,
        geometry, font, and style. The "Stage" button is connected to a
        function that stages the changes by writing them to a temporary
        configuration file and then opens the "Changes Applied" window. The
        "Cancel" button is connected to a function that cancels the operation.

        Parameters:
            self (object): The object instance

        Returns:
            None
        """

        stage_push_button = QtWidgets.QPushButton(
            "Stage", self.confirm_changes_groupbox
        )
        stage_push_button.setGeometry(170, 300, 121, 22)
        stage_push_button.setFont(self.s_font)
        stage_push_button.setStyleSheet("color: yellow")

        def tmp_push_button_clicked():
            """Stages changes and opens the "Changes Applied" window.

            This method performs the following tasks:
            1. Creates a temporary configuration file and updates it with the new values.
            2. Writes the updated configuration data to the temporary file.
            3. Initializes and displays the "Changes Applied" window, passing necessary
            configuration details for further processing.

            Parameters:
                self (object): The object instance

            Returns:
                None
            """

            tmp_file_name = f"{self.temp_folder}temp.config"

            for application, limit in self.new_values_full_dict.items():
                self.contents_dict["Limits"][application.lower()]["SiteMax"] = limit

            with open(tmp_file_name, mode="w") as created_file:
                json.dump(self.contents_dict, created_file, indent=4)

            changes_applied_window = UiChangesAppliedMainWindow(
                self.config_file_path_name,
                self.temp_folder,
                self.contents_dict,
                self.backup_folder,
                self.new_values_full_dict,
            )

            changes_applied_window.show()

        stage_push_button.clicked.connect(tmp_push_button_clicked)
        stage_push_button.clicked.connect(self.close)

        cancel_push_button = QtWidgets.QPushButton(
            "Cancel", self.confirm_changes_groupbox
        )
        cancel_push_button.setGeometry(310, 300, 121, 22)
        cancel_push_button.setFont(self.s_font)
        cancel_push_button.clicked.connect(self.cancel_button_clicked)
        cancel_push_button.clicked.connect(self.close)

    def cancel_button_clicked(self):
        """Opens up the main Farm Selection Window if the user decided to
        cancel the process.

        Parameters:
            self: The object instance.

        Returns:
            None
        """

        main_limits_window = UiLimitsMainWindow()
        main_limits_window.show()  # Sections of the window
