#!/sw/bin/python

# This window opens up when selected through the 'Farm_Selection_Window' of the Atomic Farm UI.
# Represents the Linux Farm as a whole.
# Created using PyQt5.
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

import json
import os
from collections import OrderedDict
from functools import partial
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QApplication
from changes_confirmation_window import ui_confirmFarmChanges_MainWindow

class ui_ShowLimits_MainWindow(object):
    # Creates main interface for everything else to live on
    def setupUi(self, ShowLimitsUI_MainWindow, show, config_file_path_name,
                temp_folder, backup_folder):

        """ Sets up the user interface for the Show Limits application.

            Parameters:
                self: The object instance.
                ShowLimitsUI_MainWindow (QtWidgets.QMainWindow): The main window
                of the Show Limits application.
                show (str): The name of the show.
                config_file_path_name (str): The path and name of the
                configuration file.
                temp_folder (str): The path to the temporary folder.
                backup_folder (str): The path to the backup folder.

            Returns:
                None
        """

        if os.path.exists(temp_folder + 'temp.config'):
            # Opening config file
            with open(temp_folder + 'temp.config', 'r') as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)
        else:
            # Opening config file
            with open(config_file_path_name, 'r') as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        # This is needed to translate the Python strings into a
        # 'language' the UI from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS
        self.create_fonts()
        show_limit_sections = self.create_show_limit_sections(show)
        show_limits_window = \
            self.show_limits_window_setup(ShowLimitsUI_MainWindow, _translate)

        show_limits_groupBox = self.groupBox_creation(_translate)
        spinBoxes_list, current_values_full_dict = \
            self.groupBox_info_creation(_translate, show_limits_groupBox,
                                        show_limit_sections)

        self.info_label_creation(_translate, show, show_limits_groupBox)
        self.button_creation(_translate, show_limits_window,
                             show_limits_groupBox, spinBoxes_list,
                             current_values_full_dict, config_file_path_name,
                             temp_folder, backup_folder, show_limit_sections)
        # Upper Menu
        self.upper_menu_creation(show_limits_window, _translate)
        QtCore.QMetaObject.connectSlotsByName(show_limits_window)

    def create_fonts(self):
        """ Creates the Large and Small fonts used throughout the window.

            Parameters:
                self: Main object.

            Returns:
                l_font (QFont): larger size font used for titles.
                m_font (QFont): medium size font used for smaller titles
                s_font (QFont): smaller size font used for everything else.
        """

        # FONTS
        self.l_font = QtGui.QFont()  # Larger Font for Titles
        self.l_font.setFamily("Cantarell")
        self.l_font.setPointSize(14)
        self.l_font.setBold(True)
        self.l_font.setItalic(True)
        self.l_font.setUnderline(True)
        self.m_font = QtGui.QFont()  # Medium text with bold and underline for
        # smaller titles
        self.m_font.setFamily("Cantarell")
        self.m_font.setPointSize(11)
        self.m_font.setBold(True)
        self.m_font.setUnderline(True)
        self.s_font = QtGui.QFont()  # Smaller Font for most text
        self.s_font.setFamily("Cantarell")
        self.s_font.setPointSize(11)

    def create_show_limit_sections(self, show):
        """ Creates a list of show limit sections based on the provided show
            name.

            Parameters:
                self: The object instance.
                show (str): The name of the show.

            Returns:
                show_limit_sections (list): A list of show limit sections available for the given show.
        """

        low_cap_show = show.lower()
        show_search = '{}_'.format(low_cap_show)
        extras_pwp = 'yeti_'

        # This generates a list of all shows with limits available for change
        show_limit_sections = []
        for key in self.contents_dict['Limits'].keys():
            if show_search in key:
                show_limit_sections.append(key)

        # Adds any extra settings PWP has regarding Yeti
        if 'pwp' in show_search:
            for key in self.contents_dict['Limits'].keys():
                if extras_pwp in key:
                    show_limit_sections.append(key)

        return show_limit_sections

    def show_limits_window_setup(self, show_limits_window, _translate):
        """ Performs the initial setup for the show limits window.

            Parameters:
                self: The object instance.
                show_limits_window (QMainWindow): The show limits window object.
                _translate (function): The translation function for the UI.

            Returns:
                show_limits_window (QMainWindow): The configured show limits
                window object.
        """

        show_limits_window.setObjectName("ShowLimitsUI_MainWindow")
        show_limits_window.setFixedSize(730, 455)  # Window Size can be adjusted
        # here (312 original value for 'y' )
        show_limits_window.setStyleSheet(
            "background-color: rgb(46, 52, 54);\n""color: rgb(238, 238, 236);")
        # Using this style sheet the theme can be changed
        self.centralwidget = QtWidgets.QWidget(show_limits_window)

        # Title of the Main Window can be changed here.
        show_limits_window.setWindowTitle(
            _translate("show_limits_window", "Show Limits Window"))
        show_limits_window.setCentralWidget(self.centralwidget)

        def center(ShowLimitsUI_MainWindow):
            qr = ShowLimitsUI_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            ShowLimitsUI_MainWindow.move(qr.topLeft())

        center(show_limits_window)

        return show_limits_window

    def groupBox_creation(self, _translate):
        """ Creates a group box for displaying show limits.

            Parameters:
                self: The object instance.
                _translate (function): The translation function for the UI.

            Returns:
                show_limits_groupBox (QGroupBox): The created show limits group box.
        """

        show_limits_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        show_limits_groupBox.setGeometry(QtCore.QRect(10, 10, 710, 410))
        show_limits_groupBox.setFont(self.l_font)
        show_limits_groupBox.setObjectName("show_limits_groupBox")
        # Title of the Group Box
        show_limits_groupBox.setTitle(
            _translate("ShowLimitsUI_MainWindow", "Show Limits"))

        return show_limits_groupBox

    def groupBox_info_creation(self, _translate, show_limits_groupBox,
                               show_limit_sections):
        """ Creates labels and spin boxes within a group box to display show
            limit information.

                    Parameters:
                        self: The object instance.
                        _translate (function): The translation function for the UI.
                        show_limits_groupBox (QGroupBox): The show limits group
                        box object.
                        show_limit_sections (list): List of show limit sections.

                    Returns:
                        spinBoxes_list (list): List of created spin box objects.
                        current_values_full_dict (dict): Dictionary containing
                        current values for show limits.
        """

        # Y-axis values for both Labels and Boxes individually
        label_y_axis_value = 45  # Initial values for the first column
        label_y_axis_original = label_y_axis_value
        box_y_axis_value = 72
        box_y_axis_original = box_y_axis_value
        # X-axis value for both Labels and Boxes together
        x_axis_value = 270

        labels_list = []
        spinBoxes_list = []
        current_values_full_dict = dict()

        def label_creation(_translate, show_limits_groupBox, capital_limit,
                           label_y_axis_value, x_axis_value):
            """ Creates a label within the show limits group box.

                Parameters:
                    _translate (function): The translation function for the UI.
                    show_limits_groupBox (QGroupBox): The show limits group box
                    object.
                    capital_limit (str): The capitalized limit text.
                    label_y_axis_value (int): The y-axis position of the label.
                    x_axis_value (int): The x-axis position of the label.

                Returns:
                    label (QLabel): The created label object.
            """

            # Tests
            label = QtWidgets.QLabel(show_limits_groupBox)
            label.setGeometry(
                QtCore.QRect(x_axis_value, label_y_axis_value, 100, 20))
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)
            label.setText(_translate("ShowLimitsUI_MainWindow", capital_limit))

            return label

        # Creating all spin boxes
        def spin_box_creation(show_limits_groupBox, limit, box_y_axis_value,
                              x_axis_value):

            """ Creates a spin box within the show limits group box.

                Parameters:
                    show_limits_groupBox (QGroupBox): The show limits group box object.
                    limit (str): The limit identifier for the spin box.
                    box_y_axis_value (int): The y-axis position of the spin box.
                    x_axis_value (int): The x-axis position of the spin box.

                Returns:
                    spinBox (QSpinBox): The created spin box object.
            """

            # Minimum and Maximum for all spin boxes
            minimum = 0
            maximum = 10000

            spinBox = QtWidgets.QSpinBox(show_limits_groupBox)
            spinBox.setGeometry(
                QtCore.QRect(x_axis_value, box_y_axis_value, 68, 22))
            spinBox.setFont(self.s_font)
            spinBox.setObjectName("{}_spinBox".format(limit))
            spinBox.setMinimum(minimum)
            spinBox.setMaximum(maximum)

            return spinBox

        for limit in show_limit_sections:

            capital_limit = limit.capitalize()
            label = label_creation(_translate, show_limits_groupBox, capital_limit,
                                   label_y_axis_value, x_axis_value)
            labels_list.append(label)
            spin_box = spin_box_creation(show_limits_groupBox, limit,
                                         box_y_axis_value, x_axis_value)
            spinBoxes_list.append(spin_box)
            current_values_full_dict = \
                self.current_values_application(limit, spin_box,
                                                current_values_full_dict,
                                                capital_limit)

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

        return spinBoxes_list, current_values_full_dict

    def current_values_application(self, limit, spinbox,
                                   current_values_full_dict, capital_limit):
        """ Updates the 'current values' dictionary with the limit and its
            corresponding spin box value.

            Parameters:
                limit (str): The limit identifier.
                spinbox (QSpinBox): The spin box object.
                current_values_full_dict (dict): The dictionary of current
                values.
                capital_limit (str): The capitalized limit identifier.

            Returns:
                current_values_full_dict (dict): The updated dictionary of
                current values.
        """

        current_value = self.contents_dict['Limits'][limit]['SiteMax']
        spinbox.setValue(current_value)
        current_values_full_dict.update({capital_limit: current_value})

        return current_values_full_dict

    def info_label_creation(self, _translate, show, show_limits_groupBox):
        """ Creates information labels in the show limits group box.

            Parameters:
                _translate (function): The translation function for text localization.
                show (str): The name of the show.
                show_limits_groupBox (QGroupBox): The group box to contain the labels.

            Returns:
                None
        """

        # Main Definition label
        self.def_label = QtWidgets.QLabel(show_limits_groupBox)
        self.def_label.setGeometry(QtCore.QRect(10, 50, 200, 71))
        self.def_label.setFont(self.s_font)
        self.def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.def_label.setScaledContents(False)
        self.def_label.setWordWrap(True)
        self.def_label.setObjectName("def_label")
        self.def_label.setText(
            _translate("ShowLimitsUI_MainWindow",
                       "To the right side you will see a list of all current "
                       "available keys with license limits for {} with its "
                       "current values.".format(show)))

        # Second Definition Label
        self.def_label_boxes = QtWidgets.QLabel(show_limits_groupBox)
        self.def_label_boxes.setGeometry(QtCore.QRect(10, 140, 201, 81))
        self.def_label_boxes.setFont(self.s_font)
        self.def_label_boxes.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.def_label_boxes.setScaledContents(False)
        self.def_label_boxes.setWordWrap(True)
        self.def_label_boxes.setObjectName("def_label_boxes")
        self.def_label_boxes.setText(
            _translate("ShowLimitsUI_MainWindow",
                       "Utilizing the available spin boxes, please change the "
                       "limits per section accordingly: "))

    def button_creation(self, _translate, show_limits_window,
                        show_limits_groupBox, spinBoxes_list,
                        current_values_full_dict, config_file_path_name,
                        temp_folder, backup_folder, show_limit_sections):
        """ Creates submit and cancel buttons in the show limits group box.

            Parameters:
                _translate (function): The translation function for text
                localization.
                show_limits_window (QMainWindow): The main window for show
                limits.
                show_limits_groupBox (QGroupBox): The group box to contain the
                buttons.
                spinBoxes_list (list): The list of spin boxes.
                current_values_full_dict (dict): The dictionary of current
                values.
                config_file_path_name (str): The path and name of the
                configuration file.
                temp_folder (str): The path to the temporary folder.
                backup_folder (str): The path to the backup folder.
                show_limit_sections (list): The list of show limit sections.

            Returns:
                None
        """

        submit_pushButton = QtWidgets.QPushButton(show_limits_groupBox)
        submit_pushButton.setGeometry(QtCore.QRect(495, 375, 91, 22))
        submit_pushButton.setFont(self.s_font)
        submit_pushButton.setObjectName("submit_pushButton")
        # Name can be changed here
        submit_pushButton.setText(_translate("ShowLimitsUI_MainWindow", "Submit"))

        # Runs when submit button is clicked
        # config_file_path_name, temp_folder, backup_folder
        def submit_button_clicked(spinBoxes, show_limit_sections, cfpn, tf, bf):
            new_values_list = []
            capital_key_list = []
            for limit in show_limit_sections:
                capital_key_list.append(limit.capitalize())
            for box in spinBoxes:
                new_value = box.value()
                new_values_list.append(new_value)

            new_values_full_dict = dict(zip(capital_key_list, new_values_list))
            self.changesConfirmation_window = QtWidgets.QMainWindow()
            self.ui = ui_confirmFarmChanges_MainWindow()
            self.ui.setupUi(self.changesConfirmation_window,
                            current_values_full_dict, new_values_full_dict,
                            self.contents_dict, cfpn, tf, bf)
            self.changesConfirmation_window.show()

        submit_pushButton.clicked.connect(
            partial(submit_button_clicked, spinBoxes_list,
                    show_limit_sections, config_file_path_name, temp_folder,
                    backup_folder))
        submit_pushButton.clicked.connect(show_limits_window.close)

        cancel_pushButton = QtWidgets.QPushButton(show_limits_groupBox)
        cancel_pushButton.setGeometry(QtCore.QRect(605, 375, 91, 22))
        cancel_pushButton.setFont(self.s_font)
        cancel_pushButton.setObjectName("cancel_pushButton")
        # Name can be changed here
        cancel_pushButton.setText(_translate("ShowLimitsUI_MainWindow", "Cancel"))

        cancel_pushButton.clicked.connect(self.cancel_button_clicked)
        cancel_pushButton.clicked.connect(show_limits_window.close)

    def cancel_button_clicked(self):
        from main_limits_selection_window import ui_AtomicCartoonsLimits_MainWindow
        self.farm_selection_windows = QtWidgets.QMainWindow()
        self.ui = ui_AtomicCartoonsLimits_MainWindow()
        self.ui.setupUi(self.farm_selection_windows)
        self.farm_selection_windows.show()

    def upper_menu_creation(self, UI, _translate):
        # Main bar at the top
        self.menubar = QtWidgets.QMenuBar(UI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 22))
        self.menubar.setFont(self.s_font)
        self.menubar.setObjectName("menubar")
        UI.setMenuBar(self.menubar)

        self.menuLoad_Setup = QtWidgets.QMenu(self.menubar)
        self.menuLoad_Setup.setFont(self.s_font)
        self.menuLoad_Setup.setObjectName("menuLoad_Setup")
        self.menuLoad_Setup.setTitle(_translate("ShowLimitsUI_MainWindow", "Load Setup"))
        self.menubar.addAction(self.menuLoad_Setup.menuAction())

        self.actionSelect_file_to_load = QtWidgets.QAction(UI)
        self.actionSelect_file_to_load.setFont(self.s_font)
        self.actionSelect_file_to_load.setAutoRepeat(True)
        self.actionSelect_file_to_load.setObjectName("actionSelect_file_to_load")
        self.actionSelect_file_to_load.setText(_translate("ShowLimitsUI_MainWindow", "Select File to Load"))
        self.menuLoad_Setup.addAction(self.actionSelect_file_to_load)

