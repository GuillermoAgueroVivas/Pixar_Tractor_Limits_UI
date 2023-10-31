#!/sw/bin/python

# This is the Changes Applied window of the Atomic Farm UI. Shows message saying
# the changes made have been applied and asks if you would like to do more changes.
# Created using PyQt5
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

import json
import os
import urllib2
import subprocess
import sys
from time import sleep
from datetime import *
from functools import partial
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QApplication

class Ui_changesApplied_MainWindow(object):

    def setupUi(self, changesApplied_MainWindow, config_file_path_name,
                temp_folder, contents_dict, backup_folder, new_values_full_dict):

        """ Sets up the UI for the changes applied window.

            Parameters:
                changesApplied_MainWindow: The main window widget for the
                changes applied window.
                config_file_path_name: The path and name of the configuration
                file.
                temp_folder: The folder path for temporary files.
                contents_dict: A dictionary containing the contents of the
                configuration file.
                backup_folder: The folder path for backup files.
                new_values_full_dict: A dictionary containing the new license
                values for each application.

            Returns:
                None
        """

        self.contents_dict = contents_dict

        # This is needed to translate the Python strings into a 'language' the
        # UI from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS

        self.create_fonts()
        changes_applied_window = \
            self.changes_applied_window_setup(changesApplied_MainWindow,
                                              _translate)

        changes_applied_groupBox = self.groupBox_creation(_translate)
        self.label_creation(_translate, changes_applied_groupBox)
        self.button_creation(_translate, changes_applied_window,
                             changes_applied_groupBox, config_file_path_name,
                             temp_folder, backup_folder, new_values_full_dict)

        QtCore.QMetaObject.connectSlotsByName(changesApplied_MainWindow)

    def create_fonts(self):
        """ Creates the Large and Small fonts used throughout the window.

            Parameters:
                self: Main object.

            Returns:
                l_font (QFont): larger size font used for titles
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

    def changes_applied_window_setup(self, changes_applied_window, _translate):
        """ Sets up the main window of the Windows Farm application.

            Parameters:
                changes_applied_window (QtWidgets.QMainWindow): The main
                window widget of the application.
                _translate (function): The function to translate Python
                strings into a 'language' the PyQt UI understands.

            Returns:
                changes_applied_window (QtWidgets.QMainWindow): The main
                window widget of the application.
        """


        changes_applied_window.setObjectName("changesApplied_MainWindow")
        # Window Size can be adjusted here
        changes_applied_window.setFixedSize(463, 161)
        # Using this style sheet the theme can be changed
        changes_applied_window.setStyleSheet("background-color: rgb(46, 52, 54);"
                                             "\n""color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(changes_applied_window)

        # Title of the Main Window can be changed here.
        changes_applied_window.setWindowTitle(
            _translate("changesApplied_MainWindow", "Write File Window"))
        changes_applied_window.setCentralWidget(self.centralwidget)

        def center(changesApplied_MainWindow):
            qr = changesApplied_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            changesApplied_MainWindow.move(qr.topLeft())

        center(changes_applied_window)

        return changes_applied_window

    def groupBox_creation(self, _translate):
        """ Creates a Group Box widget within the main window to hold all the UI
            elements related to the Linux Farm.

            Parameters:
                self (object): instance of a class.
                _translate (function): translation function.
                box after cleaning up the farm_name.

            Returns:
                confirmation_groupBox (QGroupBox): the created group box.
        """

        confirmation_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        confirmation_groupBox.setGeometry(QtCore.QRect(10, 10, 441, 141))
        confirmation_groupBox.setFont(self.l_font)
        # Title of the Group Box
        confirmation_groupBox.setTitle(
            _translate("changesApplied_MainWindow",
                       "Write to File Or Make More Changes"))

        return confirmation_groupBox

    def label_creation(self, _translate, changes_applied_groupBox):
        """ Creates all labels in the changes applied group box.

            Parameters:
                _translate: The translation function for translating strings.
                changes_applied_groupBox: The changes applied group box widget.

            Returns:
                None
        """

        self.question_label = QtWidgets.QLabel(changes_applied_groupBox)
        self.question_label.setGeometry(QtCore.QRect(10, 35, 271, 61))
        self.question_label.setFont(self.s_font)
        self.question_label.setWordWrap(True)
        self.question_label.setObjectName("question_label")
        self.question_label.setText(_translate("changesApplied_MainWindow",
                                               "Would you like to make more "
                                               "changes?"))

    def button_creation(self, _translate, changes_applied_window,
                        changes_applied_groupBox, config_file_path_name,
                        temp_folder, backup_folder, new_values_full_dict):

        """ Creates and sets up the "More Changes", "Exit" and "Write" buttons.
            The "More Changes" button allows the user to go back to the first
            window and continues to do adjustments to a temporary file. The
            "Exit" button will close the window and discard the temporary
            changes. The "Write" button actually applies the changes made to the
            config file while also creating a backup of the previous config file.

                Parameters:
                    self (object): The current instance of the class.
                    _translate (function): A translation function for text
                    localization.
                    changes_applied_window (QtWidgets.QMainWindow): The main
                    window object.
                    changes_applied_groupBox (QtWidgets.QGroupBox): The group
                    box container for buttons.
                    config_file_path_name (str): The path and name of the
                    configuration file.
                    temp_folder (str): The path to the temporary folder.
                    backup_folder (str): The path to the backup folder.
                    new_values_full_dict (dict): A dictionary of new values.

                Returns:
                    None
        """

        moreChanges_pushButton = QtWidgets.QPushButton(changes_applied_groupBox)
        moreChanges_pushButton.setGeometry(QtCore.QRect(160, 110, 121, 22))
        moreChanges_pushButton.setFont(self.s_font)
        moreChanges_pushButton.setObjectName("moreChanges_pushButton")
        moreChanges_pushButton.setStyleSheet('color : yellow')
        # Text can be changed here
        moreChanges_pushButton.setText(
            _translate("changesApplied_MainWindow", "More Changes"))
        moreChanges_pushButton.clicked.connect(self.moreChanges_button_clicked)
        moreChanges_pushButton.clicked.connect(changes_applied_window.close)

        exit_pushButton = QtWidgets.QPushButton(changes_applied_groupBox)
        exit_pushButton.setGeometry(QtCore.QRect(310, 110, 121, 22))
        exit_pushButton.setFont(self.s_font)
        exit_pushButton.setObjectName("exit_pushButton")
        exit_pushButton.setStyleSheet('color : #D21404')
        # Text can be changed here
        exit_pushButton.setText(
            _translate("changesApplied_MainWindow", "Exit/Discard"))

        def delete_tmp(tf):  # temp_folder
            tmp_file_name = '{}temp.config'.format(tf)
            os.remove(tmp_file_name)

        exit_pushButton.clicked.connect(partial(delete_tmp, temp_folder))
        exit_pushButton.clicked.connect(changes_applied_window.close)

        write_button = QtWidgets.QPushButton(changes_applied_groupBox)
        write_button.setGeometry(QtCore.QRect(10, 110, 121, 22))
        write_button.setFont(self.s_font)
        write_button.setObjectName("write_button")
        write_button.setStyleSheet('color : #A7F432')
        # Text can be changed here
        write_button.setText(_translate("changesApplied_MainWindow", "Write"))

        # config_file_path_name, temp_folder, self.contents_dict, backup_folder,
        # new_values_full_dict
        def write_to_config(cfpn, tf, contents_dict, bf, nv_fd):

            print("The write_to_config() method has started")

            # Move this to the next window
            if os.path.exists(cfpn):

                backup_file_name = \
                    '{}{}-{}.config'.format(
                        bf, date.today(), datetime.now().strftime("%H:%M:%S"))

                os.rename(cfpn, backup_file_name)
                tmp_file_name = '{}temp.config'.format(tf)
                os.remove(tmp_file_name)

            json.dump(contents_dict, open(cfpn, mode='w'), indent=4)

            # Reloads config file
            reload_process = subprocess.Popen(
                "/bin/bash /sw/pipeline/rendering/"
                "tractor-config-tools/reloadconfig_bash.sh", shell=True)
            reload_process.wait()
            index = 1

            # Checking if the command was completed successfully
            if reload_process.returncode == 0:
                print("The first reload of the config file has just occurred :)")
                print("Command succeeded!")
            else:
                print("Command failed")

            # Loading website containing the updated '.config' file info
            web_info = urllib2.urlopen("http://tractor-engine/Tractor/queue?q=limits")
            sleep(5)
            web_info_dict = json.load(web_info)
            print("Config-file website has just been fully loaded!")

            # Iterates through the 'New Values Directory' sent from the
            # previous window and compares every value to those in the
            # 'Tractor Limits' website.
            for application, limit in nv_fd.items():
                web_value = web_info_dict['Limits'][application.lower()]['SiteMax']
                index = 1
                print(web_value, limit)

                while web_value != limit:

                    web_info = urllib2.urlopen(
                        "http://tractor-engine/Tractor/queue?q=limits")
                    sleep(5)
                    web_info_dict = json.load(web_info)
                    index += 1

                    if 1 < index < 7:
                        reload_process = subprocess.Popen(
                            "/bin/bash /sw/pipeline/rendering/"
                            "tractor-config-tools/reloadconfig_bash.sh",
                            shell=True)
                        reload_process.wait()

                        if reload_process.returncode == 0:
                            print("Command apparently succeeded in 'while' loop")
                        else:
                            print("Command failed")

                        print("Amount of config-reloads: {}".format(index))

                    elif index == 8:
                        print "The Config was reloaded too many times before " \
                              "this change could be properly applied. Attempt " \
                              "to reload manually."
                        sys.exit()

        write_button.clicked.connect(
            partial(write_to_config, config_file_path_name, temp_folder,
                    self.contents_dict, backup_folder, new_values_full_dict))
        write_button.clicked.connect(changes_applied_window.close)

    def moreChanges_button_clicked(self):
        from main_limits_selection_window import ui_AtomicCartoonsLimits_MainWindow
        self.farm_selection_window = QtWidgets.QMainWindow()
        self.ui = ui_AtomicCartoonsLimits_MainWindow()
        self.ui.setupUi(self.farm_selection_window)
        self.farm_selection_window.show()
