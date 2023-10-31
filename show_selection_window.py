#!/sw/bin/python

# This window is the Initial Window of the Atomic Farm UI.
# Created using PyQt5
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

from collections import OrderedDict
import json
from functools import partial
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QApplication
# These are all the other windows being imported
from show_limits_window import ui_ShowLimits_MainWindow

class ui_ShowSelectionLimits_MainWindow(object):

    # Window Main Settings
    def setupUi(self, show_select_limits_window, config_file_path_name,
                temp_folder, backup_folder):
        """ Sets up the user interface for the show select limits window.

            Parameters:
                show_select_limits_window (QMainWindow): The main window for show select limits.
                config_file_path_name (str): The path and name of the configuration file.
                temp_folder (str): The path to the temporary folder.
                backup_folder (str): The path to the backup folder.

            Returns:
                None
        """

        # Opening config file
        with open(config_file_path_name, 'r') as i:
            self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        # the UI from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS

        self.create_fonts()
        shows = self.create_shows_list()
        show_select_limits_window = \
            self.show_select_limits_window_setup(show_select_limits_window,
                                                 _translate)
        show_select_limits_groupBox = self.groupBox_creation(_translate)
        self.label_creation(_translate, show_select_limits_groupBox)
        show_limits_select_comboBox = \
            self.combo_box_creation(_translate, show_select_limits_groupBox,
                                    shows)

        self.button_creation(_translate, show_select_limits_window,
                             show_select_limits_groupBox,
                             show_limits_select_comboBox, shows,
                             config_file_path_name, temp_folder, backup_folder)

        QtCore.QMetaObject.connectSlotsByName(show_select_limits_window)

    def create_fonts(self):
        """ Creates the Large and Small fonts used throughout the window.

            Parameters:
                self: Main object.

            Returns:
                l_font (QFont): larger size font used for titles.
                s_font (QFont): smaller size font used for everything else.
        """

        self.l_font = QtGui.QFont()  # Larger Font for Titles
        self.l_font.setFamily("Cantarell")
        self.l_font.setPointSize(14)
        self.l_font.setBold(True)
        self.l_font.setItalic(True)
        self.l_font.setUnderline(True)
        self.s_font = QtGui.QFont()  # Smaller Font for most text
        self.s_font.setFamily("Cantarell")
        self.s_font.setPointSize(11)

    def create_shows_list(self):
        """ Creates a list of shows based on the contents of the configuration
            file.

            Parameters:
                self: The object itself.

            Returns:
                shows (list): A list of shows.
        """

        shows = []
        avoid = ['MollyOfDenali', 'NightAtTheMuseum', 'RND', 'DGF', 'default']
        for key in self.contents_dict['Limits']['linuxfarm']['Shares'].keys():
            if all(word not in key for word in avoid):
                shows.append(key)

        return shows

    def show_select_limits_window_setup(self, show_select_limits_window,
                                        _translate):
        """ Sets up the show selection window with the specified properties.

            Parameters:
                self: The object itself.
                show_select_limits_window: The show selection window object.
                _translate: A function for translating text.

            Returns:
                show_select_limits_window: The configured show selection window
                object.
        """

        show_select_limits_window.setObjectName(
            "AtomicCartoonsShowLimitsUI_MainWindow")
        # Window Size can be adjusted here
        show_select_limits_window.setFixedSize(463, 182)
        # Using this style sheet the theme can be changed
        show_select_limits_window.setStyleSheet(
            "background-color: rgb(46, 52, 54);\n""color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(show_select_limits_window)
        # Title of the Main Window can be changed here.
        show_select_limits_window.setWindowTitle(
            _translate("show_select_limits_window", "Show Selection Window"))
        show_select_limits_window.setCentralWidget(self.centralwidget)

        def center(sslw):
            qr = sslw.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            sslw.move(qr.topLeft())

        center(show_select_limits_window)

        return show_select_limits_window

    def groupBox_creation(self, _translate):
        """ Creates and configures a group box for show limits selection.

            Parameters:
                self: The object itself.
                _translate: A function for translating text.

            Returns:
                show_select_limits_groupBox: The configured group box object.
        """

        show_select_limits_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        show_select_limits_groupBox.setGeometry(QtCore.QRect(10, 10, 441, 161))
        show_select_limits_groupBox.setFont(self.l_font)
        # Title of the Group Box
        show_select_limits_groupBox.setTitle(
            _translate("AtomicCartoonsShowLimitsUI_MainWindow",
                       "Show Limits Selection"))

        return show_select_limits_groupBox

    def label_creation(self, _translate, show_select_limits_groupBox):
        """ Creates and configures the main label for show limits selection.

            Parameters:
                self: The object itself.
                _translate: A function for translating text.
                show_select_limits_groupBox: The group box in which the label
                will be placed.

            Returns:
                show_limits_select_label: The configured label object.
        """

        show_limits_select_label = QtWidgets.QLabel(show_select_limits_groupBox)
        show_limits_select_label.setGeometry(QtCore.QRect(10, 40, 421, 61))
        show_limits_select_label.setFont(self.s_font)
        show_limits_select_label.setWordWrap(True)
        show_limits_select_label.setObjectName("show_limits_select_label")
        # Text inside the label can be changed here
        show_limits_select_label.setText(
            _translate("AtomicCartoonsShowLimitsUI_MainWindow",
                       "Utilizing the dropdown menu below, please select what "
                       "show you would like to change the limits for:"))

    def combo_box_creation(self, _translate, show_select_limits_groupBox, shows):
        """ Creates and configures a combo box for show limits selection.

            Parameters:
                self: The object itself.
                _translate: A function for translating text.
                show_select_limits_groupBox: The group box in which the combo
                box will be placed.
                shows: A list of shows for populating the combo box.

            Returns:
                show_limits_select_comboBox: The configured combo box object.
        """

        show_limits_select_comboBox = QtWidgets.QComboBox(show_select_limits_groupBox)
        show_limits_select_comboBox.setGeometry(QtCore.QRect(10, 120, 201, 22))
        show_limits_select_comboBox.setFont(self.s_font)
        show_limits_select_comboBox.setStyleSheet('color : #A7F432')
        show_limits_select_comboBox.setObjectName("show_limits_select_comboBox")

        index = 0
        for show in shows:
            show_limits_select_comboBox.addItem("")
            capital_show = show.upper()
            show_limits_select_comboBox.setItemText(
                index, _translate("AtomicCartoonsShowLimitsUI_MainWindow",
                                  capital_show))
            index += 1

        return show_limits_select_comboBox

    def button_creation(self, _translate, show_select_limits_window,
                        show_select_limits_groupBox, show_limits_select_comboBox,
                        shows, config_file_path_name, temp_folder, backup_folder):
        """ Creates and configures a button for confirming show limits selection.

            Parameters:
                self: The object itself.
                _translate: A function for translating text.
                show_select_limits_window: The window where the button is placed.
                show_select_limits_groupBox: The group box where the button
                is placed.
                show_limits_select_comboBox: The combo box for show limits
                selection.
                shows: A list of shows for matching the selection.
                config_file_path_name: The path and name of the configuration
                file.
                temp_folder: The path of the temporary folder.
                backup_folder: The path of the backup folder.

            Returns:
                None
        """

        show_limits_confirm_pushButton = QtWidgets.QPushButton(
            show_select_limits_groupBox)
        show_limits_confirm_pushButton.setGeometry(QtCore.QRect(250, 120, 171, 22))
        show_limits_confirm_pushButton.setFont(self.s_font)
        show_limits_confirm_pushButton.setObjectName(
            "show_limits_confirm_pushButton")
        # Text inside the button can be changed here
        show_limits_confirm_pushButton.setText(
            _translate("AtomicCartoonsShowLimitsUI_MainWindow",
                       "Confirm My Selection"))

        def open_show_limits_window(show, cfpn, tf, bf):
            """ Opens a new show limits window with the selected show and
                passes the necessary parameters.

                Parameters:
                    show (str): The selected show.
                    cfpn (str): The path and name of the configuration file.
                    tf (str): The path of the temporary folder.
                    bf (str): The path of the backup folder.

                Returns:
                    None
            """
            self.showLimits_window = QtWidgets.QMainWindow()
            self.ui = ui_ShowLimits_MainWindow()
            self.ui.setupUi(self.showLimits_window, show, cfpn, tf, bf)
            self.showLimits_window.show()

        # Opening the other windows according to the selection of the Combo Box
        # config_file_path_name, temp_folder, backup_folder
        def limits_select_button_clicked(cfpn, tf, bf):
            """ Checks the selected show from the combo box and opens the
                corresponding show limits window.

                Parameters:
                    cfpn (str): The path and name of the configuration file.
                    tf (str): The path of the temporary folder.
                    bf (str): The path of the backup folder.

                Returns:
                    None
            """
            for show in shows:
                if show_limits_select_comboBox.currentText() == show.upper():
                    open_show_limits_window(show, cfpn, tf, bf)

        # IMPORTANT: This is what happens when the button is pressed to
        #confirm selection
        show_limits_confirm_pushButton.clicked.connect(
            partial(limits_select_button_clicked, config_file_path_name,
                    temp_folder, backup_folder))
        show_limits_confirm_pushButton.clicked.connect(
            show_select_limits_window.close)
