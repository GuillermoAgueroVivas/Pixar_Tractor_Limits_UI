#!/usr/bin/python3

""" 
This window is the Initial Window of the Farm UI.
Created using PyQt5.
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

from collections import OrderedDict
import json
from qtpy import QtGui, QtWidgets, QtCore


class UiShowSelectionLimitsMainWindow(QtWidgets.QMainWindow):
    """
    The main window class for selecting and managing show limits.

    This class sets up the initial state and user interface components for the
    show selection limits window. It defines the paths for the configuration,
    temporary, and backup folders, initializes necessary UI components and
    fonts, and loads configuration data.

    Args:
        config_file_path_name (str): Path to the main configuration file.
        temp_folder (str): Path to the temporary folder.
        backup_folder (str): Path to the backup folder.

    Methods:
        setup_ui(): Sets up the user interface components.
        create_shows_list(): Creates a list of shows based on the config file.
        show_select_limits_window_setup(): Sets up the show selection window.
        groupbox_creation(): Creates a group box for show limits selection.
        combo_box_creation(): Creates a combo box for selecting shows.
        label_creation(): Creates the main label for show limits selection.
        button_creation(): Creates a button for confirming show limits selection.
    """

    def __init__(self, config_file_path_name, temp_folder, backup_folder):
        """Initializes an instance of the UiShowSelectionLimitsMainWindow class.

        This constructor sets up the initial state and user interface components
        for the application. It defines the paths for the configuration, temporary,
        and backup folders, and initializes the necessary UI components and fonts.

        Parameters:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.

        Attributes:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.
            contents_dict (dict): Contents of the configuration file as an ordered dictionary.
            show_select_window_ui (object): UI object for the show selection window.
            app_selection_limits_ui (object): UI object for the application selection limits.

        UI Components:
            centralwidget (QWidget): Central widget for the main window.
            show_select_limits_groupbox (QGroupBox): Group box for show limits
            selection UI components.
            show_limits_select_combobox (QComboBox): Combo box for show limits selection.
            show_limits_confirm_push_button (QPushButton): Push button to confirm show
            limits selection.
            shows (list): List of shows loaded from the configuration file.

        Fonts:
            l_font (QFont): Large, bold, italic font with underline for headings.
            s_font (QFont): Smaller font for other text elements, with thin weight.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # Folders
        self.temp_folder = temp_folder
        self.backup_folder = backup_folder

        # Sections of the window
        self.centralwidget = ""
        self.show_select_limits_groupbox = None
        self.show_limits_select_combobox = None
        self.show_limits_confirm_push_button = None
        self.shows = None
        self.config_file_path_name = config_file_path_name

        # Opening config file
        with open(config_file_path_name, "r") as i:
            self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        # Fonts
        self.l_font = QtGui.QFont(
            "Cantarell",
            14,
            QtGui.QFont.Bold,
            QtGui.QFont.StyleItalic,
        )
        self.l_font.setUnderline(True)

        self.s_font = QtGui.QFont("Cantarell", 12)  # Smaller Font for most text
        self.s_font.setWeight(QtGui.QFont.Thin)

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface for the show select limits window.

        This method initializes and configures the main window and its elements,
        including the show select limits window setup, shows list creation,
        group box, labels, combo box, and buttons.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.show_select_limits_window_setup()

        self.create_shows_list()
        self.groupbox_creation()
        self.label_creation()
        self.combo_box_creation()
        self.button_creation()

    def create_shows_list(self):
        """Creates a list of shows based on the contents of the configuration
        file.

        This method reads the configuration file and generates a list of shows,
        excluding certain predefined shows.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.shows = []
        avoid = ["MollyOfDenali", "NightAtTheMuseum", "RND", "DGF", "default"]
        for key in self.contents_dict["Limits"]["linuxfarm"]["Shares"].keys():
            if all(word not in key for word in avoid):
                self.shows.append(key)

    def show_select_limits_window_setup(self):
        """Sets up the show selection window with the specified properties.

        This method configures the main window for the show selection interface,
        including setting the title, size, and style sheet. It also initializes the
        central widget and centers the window on the screen.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Show Selection Window")
        # Window Size can be adjusted here
        self.setFixedSize(463, 182)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """
            background-color: rgb(46, 52, 54);
            color: rgb(238, 238, 236);
            """
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
        """Creates and configures a group box for show limits selection.

        This method initializes the 'Show Limits Selection' group box, sets its font,
        and defines its geometry within the central widget.

        Parameters:
            self (object): The object instance.

        Returns:
            show_select_limits_groupbox (QGroupBox): The configured group box object.
        """

        # Title of the Group Box
        self.show_select_limits_groupbox = QtWidgets.QGroupBox(
            "Show Limits Selection", self.centralwidget
        )
        self.show_select_limits_groupbox.setFont(self.l_font)
        self.show_select_limits_groupbox.setGeometry(10, 10, 441, 161)

    def combo_box_creation(self):
        """Creates and configures a combo box for show limits selection.

        This method initializes the combo box within the 'Show Limits Selection' group box,
        sets its geometry, font, and style, and populates it with a list of shows.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.show_limits_select_combobox = QtWidgets.QComboBox(
            self.show_select_limits_groupbox
        )
        self.show_limits_select_combobox.setGeometry(10, 120, 201, 22)
        self.show_limits_select_combobox.setFont(self.s_font)
        self.show_limits_select_combobox.setStyleSheet("color : #A7F432")

        for show in self.shows:
            if "ACG" in show:
                continue

            capital_show = show.upper()
            self.show_limits_select_combobox.addItem(f"{capital_show}")

    def label_creation(self):
        """Creates and configures the main label for show limits selection.

        This method initializes a QLabel widget within the 'Show Limits Selection' group box,
        sets its properties such as alignment, word wrap, geometry, and font, and provides
        instructions to the user for selecting the show to change limits.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Text inside the label can be changed here
        show_limits_select_label = QtWidgets.QLabel(
            "Utilizing the dropdown menu below, please select what "
            "show you would like to change the limits for:",
            self.show_select_limits_groupbox,
        )
        show_limits_select_label.setAlignment(QtCore.Qt.AlignLeft)
        show_limits_select_label.setGeometry(10, 50, 421, 61)
        show_limits_select_label.setFont(self.s_font)
        show_limits_select_label.setWordWrap(True)

    def button_creation(self):
        """Creates and configures a button for confirming show limits selection.

        This method initializes the QPushButton widget within the 'Show Limits Selection'
        group box, sets its properties such as geometry and font, and connects its click
        event to a handler that opens the appropriate window based on the user's selection
        from the combo box.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Text inside the button can be changed here
        self.show_limits_confirm_push_button = QtWidgets.QPushButton(
            "Confirm My Selection", self.show_select_limits_groupbox
        )
        self.show_limits_confirm_push_button.setGeometry(250, 120, 171, 22)
        self.show_limits_confirm_push_button.setFont(self.s_font)

        def open_show_limits_window(show):
            """Opens a new show limits window with the selected show and
            passes the necessary parameters.

            This method imports the UiShowLimitsMainWindow class, creates an instance
            of it with the selected show and configuration paths, and displays it to
            the user.

            Parameters:
                show (str): The selected show.

            Returns:
                None
            """
            from show_limits_window import UiShowLimitsMainWindow

            show_limits_window = UiShowLimitsMainWindow(
                show, self.config_file_path_name, self.temp_folder, self.backup_folder
            )
            show_limits_window.show()

        def limits_select_button_clicked():
            """Checks the selected show from the combo box and opens the
            corresponding show limits window.

            This method retrieves the current text from the combo box, matches it
            with the list of shows, and opens the corresponding window for the
            selected show. After opening the new window, the current window is closed.

            Parameters:
                None

            Returns:
                None
            """
            for show in self.shows:
                if self.show_limits_select_combobox.currentText() == show.upper():
                    open_show_limits_window(show)

            self.close()

        self.show_limits_confirm_push_button.clicked.connect(
            limits_select_button_clicked
        )
