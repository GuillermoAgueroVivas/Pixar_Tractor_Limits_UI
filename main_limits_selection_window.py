#!/usr/bin/python3

""" 
This window is the Initial Window of the Farm UI for Show & License Limits.
Created using QtPy
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

from functools import partial
from qtpy import QtWidgets, QtGui, QtCore


class UiLimitsMainWindow(QtWidgets.QMainWindow):
    """Main window class for the Limit Selection Farm UI.

    This class creates the main window of the Limits UI application using QtPy.
    It initializes
    and configures the main window, including UI components like group boxes, labels,
    combo boxes, and buttons. It also manages the transition between different windows
    based on user selections.

    Methods:
        __init__(): Initializes the main window and its UI components.
        setup_ui(): Sets up the user interface components for the application.
        limit_selection_window_setup(): Configures the main window, including
        its title, size, and style.
        groupbox_creation(): Creates and configures the group box for limit selection.
        combo_box_creation(): Creates and configures the combo box for limit selection.
        label_creation(): Creates and configures the instructional label for
        the limits selection.
        button_creation(): Creates and configures the "Confirm My Selection" button.
        open_show_selection_window(): Opens the Show Selection Limits window.
        open_application_limits_window(): Opens the Application Limits window.
    """

    def __init__(self):
        """
        Initializes an instance of the class.

        This constructor sets up the initial state and user interface components
        for the application. It defines the paths for the configuration, temporary,
        and backup folders, and initializes the necessary UI components and fonts.

        Attributes:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder.
            backup_folder (str): Path to the backup folder.
            show_select_window_ui (object): UI object for the show selection window.
            app_selection_limits_ui (object): UI object for the application selection limits.

        UI Components:
            centralwidget (QWidget): Central widget for the main window.
            limits_select_groupbox (QGroupBox): Group box for limit selection UI components.
            limits_select_push_button (QPushButton): Push button for limit selection.
            limits_select_combo_box (QComboBox): Combo box for limit selection.

        Fonts:
            l_font (QFont): Large, bold, italic font with underline for headings.
            s_font (QFont): Smaller font for other text elements.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # These are the location of both the main Config file and where
        # the temp file and backup files will be created

        # All Folders
        self.config_file_path_name = "/sw/tractor/config/limits.config"
        self.temp_folder = "/sw/tractor/config/tmp/"
        self.backup_folder = "/sw/tractor/config/limits_backup/"

        # Sections of the window
        self.centralwidget = ""
        self.limits_select_groupbox = None
        self.limits_select_push_button = None
        self.limits_select_combo_box = None

        # Windows
        self.show_select_window_ui = None
        self.app_selection_limits_ui = None

        # Fonts
        self.l_font = QtGui.QFont(
            "Cantarell", 14, QtGui.QFont.Bold, QtGui.QFont.StyleItalic
        )
        self.l_font.setUnderline(True)
        self.s_font = QtGui.QFont("Cantarell", 12)

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface components for the application.

        This method initializes and configures the main window and its elements,
        including the limit selection window, group box, labels, combo box, and buttons.
        It calls several helper methods to create and arrange these components.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.limit_selection_window_setup()
        self.groupbox_creation()
        self.label_creation()
        self.combo_box_creation()
        self.button_creation()

    def limit_selection_window_setup(self):
        """Configures the main window for the limit selection interface.

        This method sets the title, size, and style sheet for the main window.
        It also initializes the central widget and centers the window on the screen.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Main Limits Selection Window")
        # Window Size can be adjusted here
        self.setFixedSize(463, 182)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # This is what centers the
        def center_window(window):

            frame = window.frameGeometry()
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())

            if screen is None:
                screen = QtGui.QGuiApplication.primaryScreen()

            frame.moveCenter(screen.geometry().center())
            window.move(frame.topLeft())

        center_window(self)

    def groupbox_creation(self):
        """Creates and configures the group box for the limit selection window.

        This method initializes the 'Limits Selection' group box, sets its font, and
        defines its geometry within the central widget.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Group Box
        self.limits_select_groupbox = QtWidgets.QGroupBox(
            "Limits Selection", self.centralwidget
        )

        self.limits_select_groupbox.setFont(self.l_font)
        self.limits_select_groupbox.setGeometry(10, 10, 441, 161)

    def combo_box_creation(self):
        """Creates and configures the combo box for limit selection.

        This method initializes the combo box within the 'Limits Selection' group box,
        sets its geometry, font, and style, and populates it with predefined items.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.limits_select_combo_box = QtWidgets.QComboBox(self.limits_select_groupbox)
        self.limits_select_combo_box.setGeometry(10, 120, 201, 22)
        self.limits_select_combo_box.setFont(self.s_font)
        self.limits_select_combo_box.addItem("Show Defined Limits")
        self.limits_select_combo_box.addItem("License/Application Limits")
        self.limits_select_combo_box.setStyleSheet("color : #A7F432")

    def label_creation(self):
        """Creates and configures the instructional label for the limits selection.

        This method initializes the QLabel widget within the 'Limits Selection' group box,
        sets its properties such as alignment, word wrap, geometry, and font, and provides
        instructions to the user for selecting the type of limits to modify.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        limits_select_label = QtWidgets.QLabel(
            "Utilizing the dropdown menu below, please select if you would "
            "like to change the License Limits or the Show Limits:",
            self.limits_select_groupbox,
        )

        limits_select_label.setAlignment(QtCore.Qt.AlignLeft)
        limits_select_label.setWordWrap(True)
        limits_select_label.setGeometry(10, 50, 421, 61)  # 40
        limits_select_label.setFont(self.s_font)

    def button_creation(self):
        """Creates and configures the "Confirm My Selection" button within the
        'Limits Selection' group box.

        This method initializes a QPushButton widget, sets its properties such as
        geometry and font, and connects its click event to a handler that opens
        different windows based on the user's selection from the combo box.

        When the button is clicked, the method checks the current text of the combo box
        to determine which window to open:
        - If "Show Defined Limits" is selected, it opens the show selection window.
        - If "License/Application Limits" is selected, it opens the application limits window.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.limits_select_push_button = QtWidgets.QPushButton(
            "Confirm My Selection", self.limits_select_groupbox
        )
        self.limits_select_push_button.setGeometry(250, 120, 171, 22)
        self.limits_select_push_button.setFont(self.s_font)

        # Opening the other windows according to the selection of the Combo Box
        # config_file_path_name, temp_folder, backup_folder
        def limits_select_button_clicked():
            selected = self.limits_select_combo_box.currentText()

            if selected == "Show Defined Limits":
                self.open_show_selection_window()
            elif selected == "License/Application Limits":
                self.open_application_limits_window()

        # IMPORTANT: This is what happens when the button is pressed to
        # confirm selection
        self.limits_select_push_button.clicked.connect(
            partial(limits_select_button_clicked)
        )

    def open_show_selection_window(self):
        """Opens the Show Selection Limits window.

        This method imports the `UiShowSelectionLimitsMainWindow` class from the
        `show_selection_window` module, creates an instance of it, and displays it to
        the user. The method passes the configuration file path, temporary folder,
        and backup folder to the new window. After opening the new window, the current
        window is closed.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        from show_selection_window import UiShowSelectionLimitsMainWindow

        self.show_select_window_ui = UiShowSelectionLimitsMainWindow(
            self.config_file_path_name, self.temp_folder, self.backup_folder
        )
        self.show_select_window_ui.show()
        self.close()

    def open_application_limits_window(self):
        """Opens the Application Limits window.

        This method imports the `UiApplicationLimitsMainWindow` class from the
        `application_limits_window` module, creates an instance of it with the
        necessary configuration, temporary, and backup folder paths, and displays
        it to the user. After opening the new window, the current window is closed.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        from application_limits_window import UiApplicationLimitsMainWindow

        self.app_selection_limits_ui = UiApplicationLimitsMainWindow(
            self.config_file_path_name, self.temp_folder, self.backup_folder
        )
        self.app_selection_limits_ui.show()
        self.close()


if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window_ui = UiLimitsMainWindow()
    main_window_ui.show()
    sys.exit(app.exec_())
