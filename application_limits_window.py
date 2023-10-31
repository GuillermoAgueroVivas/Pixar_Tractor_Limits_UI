#!/sw/bin/python

# This window opens up when selected through the 'Application_Limits_Selection_Window' of the Atomic Limits UI.
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

class ui_ApplicationLimits_MainWindow(object):
    # Creates main interface for everything else to live on
    def setupUi(self, AppLimitsUI_MainWindow, config_file_path_name,
                temp_folder, backup_folder):
        """ Sets up the user interface for the App Limits application.

            Parameters:
                AppLimitsUI_MainWindow (QtWidgets.QMainWindow): The main
                window of the App Limits UI.
                config_file_path_name (str): The path to the main config file.
                temp_folder (str): The folder where the temporary file will be
                created.
                backup_folder (str): The folder where backup files will be stored.

            Returns:
                None
        """

        #  Temp. folder followed by the name of the temp. file
        temp_file_name = '{}temp.config'.format(temp_folder)

        if os.path.exists(temp_file_name):
            # Opening temp. config file
            with open(temp_file_name, 'r') as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)
        else:
            # Opening config file
            with open(config_file_path_name, 'r') as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        # This is needed to translate the Python strings into a 'language' the UI
        # from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS

        self.create_fonts()
        applications = self.create_applications_list()
        application_limits_window = \
            self.application_limits_window_setup(AppLimitsUI_MainWindow,
                                                 _translate)
        application_limits_groupBox = self.groupBox_creation(_translate)

        spinBoxes_list, current_values_full_dict = \
            self.groupBox_info_creation(_translate, application_limits_groupBox,
                                        applications)

        self.info_label_creation(_translate, application_limits_groupBox)
        self.button_creation(_translate, application_limits_window,
                             application_limits_groupBox, applications,
                             spinBoxes_list, current_values_full_dict,
                             config_file_path_name, temp_folder, backup_folder)

        self.upper_menu_creation(AppLimitsUI_MainWindow, _translate)
        QtCore.QMetaObject.connectSlotsByName(AppLimitsUI_MainWindow)

    def create_fonts(self):
        """ Creates the Large and Small fonts used throughout the window.

            Parameters:
                self: Main object.

            Returns:
                l_font (QFont): larger size font used for titles.
                m_font (QFont): medium size font used for smaller titles
                s_font (QFont): smaller size font used for everything else.
        """
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

    def create_applications_list(self):
        """ Creates a list of applications based on the contents of the config file.

            Returns:
                applications (list): A list of applications filtered from the
                config file, excluding unwanted shows and specific keywords.
        """

        # This generates a list of all shows in the linux farm
        unwanted_shows = []
        for key in self.contents_dict['Limits']['linuxfarm']['Shares'].keys():
            lower_key = str(key.lower())
            unwanted_shows.append(lower_key)

        # List for all applications in the config file (avoiding all unwanted
        # shows and others)
        applications = []
        avoid = ['linux', 'windows', 'yeti']
        for show in unwanted_shows:
            avoid.append(show)

        for key in self.contents_dict['Limits'].keys():
            if all(word not in key for word in avoid):
                applications.append(key)

        return applications

    def application_limits_window_setup(self, application_limits_window,
                                        _translate):
        """ This function sets up the application limits window, including the size,
            style, and title of the window, as well as centering it on the screen.

            Parameters:
                application_limits_window (QtWidgets.QMainWindow): The main
                window of the application limits window.
                _translate: Function used for translating Python strings to
                the UI language.

            Returns:
                application_limits_window (QtWidgets.QMainWindow): The configured
                application limits window.
        """

        application_limits_window.setObjectName("AppLimitsUI_MainWindow")
        # Window Size can be adjusted here
        application_limits_window.setFixedSize(955, 455)
        application_limits_window.setStyleSheet("background-color: rgb(46, 52, 54);"
                                                "\n""color: rgb(238, 238, 236);")
        # Using this style sheet the theme can be changed
        self.centralwidget = QtWidgets.QWidget(application_limits_window)

        # Title of the Main Window can be changed here.
        application_limits_window.setWindowTitle(
            _translate("AppLimitsUI_MainWindow", "Application Limits Window"))
        application_limits_window.setCentralWidget(self.centralwidget)

        def center(AppLimitsUI_MainWindow):
            qr = AppLimitsUI_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            AppLimitsUI_MainWindow.move(qr.topLeft())

        #  Centers the window as it appears on the screen
        center(application_limits_window)

        return application_limits_window

    def groupBox_creation(self, _translate):
        """ Creates a group box widget for limit selection.

            Parameters:
                self (QtWidgets.QGroupBox): The class object
                _translate (QTranslator): A function that returns a
                translated version of a string.

            Returns:
                limits_select_groupBox (QtWidgets.QGroupBox): the group box for
                limit selection.
        """

        app_limits_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        app_limits_groupBox.setGeometry(QtCore.QRect(10, 10, 935, 410))
        app_limits_groupBox.setFont(self.l_font)
        app_limits_groupBox.setObjectName("app_limits_groupBox")
        # Title of the Group Box
        app_limits_groupBox.setTitle(_translate("AppLimitsUI_MainWindow",
                                                "Application Limits"))

        return app_limits_groupBox

    def groupBox_info_creation(self, _translate, application_limits_groupBox,
                               applications):
        """ This function adjusts the size and position of the group box and
            creates sliders and spin boxes for each show.

            Parameters:
                _translate: Function used for translating Python strings to
                the UI language.
                application_limits_groupBox (QtWidgets.QGroupBox): The group
                box widget to which the labels and spin boxes will be added.
                applications (list): List of application names.

            Returns:
                spinBoxes_list (list): List of spin boxes created for each
                application.
                current_values_full_dict (dict): Dictionary containing the
                current values for each application.
        """

        label_y_axis_value = 45  # Initial values for the first column
        label_y_axis_original = label_y_axis_value
        box_y_axis_value = 72
        box_y_axis_original = box_y_axis_value
        x_axis_value = 270

        labels_list = []
        spinBoxes_list = []
        current_values_full_dict = dict()

        def label_creation(_translate, application_limits_groupBox, capital_app,
                           label_y_axis_value, x_axis_value):
            # Tests
            label = QtWidgets.QLabel(application_limits_groupBox)
            label.setGeometry(
                QtCore.QRect(x_axis_value, label_y_axis_value, 100, 20))
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)
            label.setText(_translate("AppLimitsUI_MainWindow", capital_app))

            return label

        def spin_box_creation(application_limits_groupBox, application,
                              box_y_axis_value, x_axis_value):
            # Minimum and Maximum for all spin boxes
            minimum = 0
            maximum = 10000

            spinBox = QtWidgets.QSpinBox(application_limits_groupBox)
            spinBox.setGeometry(
                QtCore.QRect(x_axis_value, box_y_axis_value, 68, 22))
            spinBox.setFont(self.s_font)
            spinBox.setObjectName("{}_spinBox".format(application))
            spinBox.setMinimum(minimum)
            spinBox.setMaximum(maximum)

            return spinBox

        for application in applications:

            capital_app = application.capitalize()
            label = label_creation(_translate, application_limits_groupBox,
                                   capital_app, label_y_axis_value, x_axis_value)
            labels_list.append(label)
            spin_box = spin_box_creation(application_limits_groupBox, application,
                                         box_y_axis_value, x_axis_value)
            spinBoxes_list.append(spin_box)

            # Getting current Percentages per application to be able to pass it
            # to the Confirmation Window
            current_values_full_dict = \
                self.current_values_application(application, spin_box,
                                                current_values_full_dict,
                                                capital_app)

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

    def current_values_application(self, application, spinbox,
                                   current_values_full_dict, capital_app):

        """ Updates the dictionary of with the current values for an application.

            Parameters:
                application (str): The name of the application.
                spinbox (QtWidgets.QSpinBox): The spin box widget associated
                with the application.
                current_values_full_dict (dict): The dictionary of current
                values for applications.
                capital_app (str): The capitalized name of the application.

            Returns:
                current_values_full_dict (dict): The updated dictionary
                of current values.
        """

        current_value = self.contents_dict['Limits'][application]['SiteMax']
        spinbox.setValue(current_value)
        current_values_full_dict.update({capital_app: current_value})

        return current_values_full_dict

    def info_label_creation(self, _translate, application_limits_groupBox):
        """ Creates information labels within the application limits group box.

            Parameters:
                _translate: A function for translating Python strings into
                a language understood by the UI.
                application_limits_groupBox: The group box widget where the
                labels will be placed.

            Returns:
                None
        """

        # Main Definition label
        self.def_label = QtWidgets.QLabel(application_limits_groupBox)
        self.def_label.setGeometry(QtCore.QRect(10, 50, 200, 71))
        self.def_label.setFont(self.s_font)
        self.def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.def_label.setScaledContents(False)
        self.def_label.setWordWrap(True)
        self.def_label.setObjectName("def_label")
        self.def_label.setText(
            _translate("AppLimitsUI_MainWindow", "To the right side you will "
                                                 "see a list of all current "
                                                 "available applications with "
                                                 "license limits with their "
                                                 "current values."))
        # Second Definition Label
        self.def_label_boxes = QtWidgets.QLabel(application_limits_groupBox)
        self.def_label_boxes.setGeometry(QtCore.QRect(10, 140, 201, 81))
        self.def_label_boxes.setFont(self.s_font)
        self.def_label_boxes.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.def_label_boxes.setScaledContents(False)
        self.def_label_boxes.setWordWrap(True)
        self.def_label_boxes.setObjectName("def_label_boxes")
        self.def_label_boxes.setText(
            _translate("AppLimitsUI_MainWindow", "Utilizing the available spin "
                                                 "boxes, please change the "
                                                 "amount of licenses of any "
                                                 "application accordingly: "))

    def button_creation(self, _translate, application_limits_window,
                        application_limits_groupBox, applications, spinBoxes_list,
                        current_values_full_dict, config_file_path_name,
                        temp_folder, backup_folder):

        """ Creates 'submit' and 'cancel' buttons within the application limits
            group box.

            Parameters:
                _translate: A function for translating Python strings into a
                language understood by the UI.
                application_limits_window: The main window of the application
                limits.
                application_limits_groupBox: The group box widget where the
                buttons will be placed.
                applications: A list of available applications.
                spinBoxes_list: A list of spin box widgets.
                current_values_full_dict: A dictionary containing the current
                values of license limits.
                config_file_path_name: The path and name of the configuration file.
                temp_folder: The path of the temporary folder.
                backup_folder: The path of the backup folder.

            Returns:
                None
        """

        submit_pushButton = QtWidgets.QPushButton(application_limits_groupBox)
        submit_pushButton.setGeometry(QtCore.QRect(735, 375, 91, 22))
        submit_pushButton.setFont(self.s_font)
        submit_pushButton.setObjectName("submit_pushButton")
        # Name can be changed here
        submit_pushButton.setText(_translate("AppLimitsUI_MainWindow", "Submit"))

        # Runs when submit button is clicked
        # config_file_path_name, temp_folder, backup_folder
        def submit_button_clicked(spinBoxes, apps, cfpn, tf, bf):
            new_values_list = []
            capital_apps_list = []
            for app in apps:
                capital_apps_list.append(app.capitalize())

            for box in spinBoxes:
                new_value = box.value()
                new_values_list.append(new_value)

            new_values_full_dict = dict(zip(capital_apps_list, new_values_list))
            self.changesConfirmation_window = QtWidgets.QMainWindow()
            self.ui = ui_confirmFarmChanges_MainWindow()
            self.ui.setupUi(self.changesConfirmation_window,
                            current_values_full_dict, new_values_full_dict,
                            self.contents_dict, cfpn, tf, bf)
            self.changesConfirmation_window.show()

        submit_pushButton.clicked.connect(
            partial(submit_button_clicked, spinBoxes_list, applications,
                    config_file_path_name, temp_folder, backup_folder))

        submit_pushButton.clicked.connect(application_limits_window.close)

        cancel_pushButton = QtWidgets.QPushButton(application_limits_groupBox)
        cancel_pushButton.setGeometry(QtCore.QRect(835, 375, 91, 22))
        cancel_pushButton.setFont(self.s_font)
        cancel_pushButton.setObjectName("cancel_pushButton")
        # Name can be changed here
        cancel_pushButton.setText(_translate("AppLimitsUI_MainWindow", "Cancel"))

        cancel_pushButton.clicked.connect(self.cancel_button_clicked)
        cancel_pushButton.clicked.connect(application_limits_window.close)

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
        self.menuLoad_Setup.setTitle(_translate("AppLimitsUI_MainWindow",
                                                "Load Setup"))
        self.menubar.addAction(self.menuLoad_Setup.menuAction())

        self.actionSelect_file_to_load = QtWidgets.QAction(UI)
        self.actionSelect_file_to_load.setFont(self.s_font)
        self.actionSelect_file_to_load.setAutoRepeat(True)
        self.actionSelect_file_to_load.setObjectName("actionSelect_file_to_load")
        self.actionSelect_file_to_load.setText(_translate("AppLimitsUI_MainWindow",
                                                          "Select File to Load"))
        self.menuLoad_Setup.addAction(self.actionSelect_file_to_load)
