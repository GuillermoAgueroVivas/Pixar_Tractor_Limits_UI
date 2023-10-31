#!/sw/bin/python

# This is the Changes Confirmation window of the Atomic Farm UI. Helps the user
# see the changes to be made before they are applied.
# Created using PyQt5
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

import json

from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QApplication
from functools import partial
from changes_applied_window import Ui_changesApplied_MainWindow

class ui_confirmFarmChanges_MainWindow(object):

    def setupUi(self, confirmFarmChanges_MainWindow, current_values_dict,
                new_values_full_dict, contents_dict, config_file_path_name,
                temp_folder, backup_folder):

        """ Sets up the user interface for the confirmFarmChanges_MainWindow

            Parameters:
                self (object): The current instance of the class.
                confirmFarmChanges_MainWindow (QtWidgets.QMainWindow): The
                main window object.
                current_values_dict (dict): The dictionary of current values.
                new_values_full_dict (dict): The dictionary of new values.
                contents_dict (dict): The dictionary of contents.
                config_file_path_name (str): The path and name of the
                configuration file.
                temp_folder (str): The path to the temporary folder.
                backup_folder (str): The path to the backup folder.

            Returns:
                None
        """

        # This is needed to translate the Python strings into a 'language' the UI
        # from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS

        self.create_fonts()
        changes_confirm_window = \
            self.changes_confirm_window_setup(confirmFarmChanges_MainWindow,
                                              _translate)

        changes_confirm_groupBox = self.groupBox_creation(_translate)
        self.textBrowser_creation(changes_confirm_groupBox, current_values_dict,
                                  new_values_full_dict)
        self.label_creation(_translate, changes_confirm_groupBox)
        self.button_creation(_translate, changes_confirm_window,
                             changes_confirm_groupBox, config_file_path_name,
                             temp_folder, contents_dict, backup_folder,
                             new_values_full_dict)

        QtCore.QMetaObject.connectSlotsByName(confirmFarmChanges_MainWindow)

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

    def changes_confirm_window_setup(self, changes_confirm_window, _translate):
        """ Sets up the main window of the Windows Farm application.

            Parameters:
                changes_confirm_window (QtWidgets.QMainWindow): The main
                window widget of the application.
                _translate (function): The function to translate Python
                strings into a 'language' the PyQt UI understands.

            Returns:
                changes_confirm_window (QtWidgets.QMainWindow): The main
                window widget of the application.
        """

        changes_confirm_window.setObjectName("changes_confirm_window")
        # Window Size can be adjusted here
        changes_confirm_window.setFixedSize(463, 349)
        # Using this style sheet the theme can be changed
        changes_confirm_window.setStyleSheet("background-color: rgb(46, 52, 54);"
                                             "\n""color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(changes_confirm_window)
        # Title of the Main Window can be changed here.
        changes_confirm_window.setWindowTitle(_translate(
            "changes_confirm_window", "Changes Confirmation Window"))
        changes_confirm_window.setCentralWidget(self.centralwidget)

        def center(confirmFarmChanges_MainWindow):
            qr = confirmFarmChanges_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            confirmFarmChanges_MainWindow.move(qr.topLeft())

        center(changes_confirm_window)

        return changes_confirm_window

    def groupBox_creation(self, _translate):
        """ Creates a Group Box widget within the main window to hold all the UI
            elements related to the change confirmation window.

           Parameters:
               self (object): instance of a class.
               _translate (function): translation function.
               box after cleaning up the farm_name.

           Returns:
               linuxFarm_groupBox (QGroupBox): the created group box.
        """

        review_changes_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        review_changes_groupBox.setGeometry(QtCore.QRect(10, 10, 441, 331))
        review_changes_groupBox.setFont(self.l_font)
        # Title of the Group Box
        review_changes_groupBox.setTitle(
            _translate("confirmFarmChanges_MainWindow", "Review Your Changes"))

        return review_changes_groupBox

    def textBrowser_creation(self, changes_confirm_groupBox, current_values_dict,
                             new_values_full_dict):
        """ Creates and configures a text browser widget to display the values
            before and after changes.

            Parameters:
                changes_confirm_groupBox (QtWidgets.QGroupBox): The group box
                where the QTextBrowser widgets will be added.
                current_values_dict (dict): A dictionary containing the
                current values for each application.
                new_values_full_dict (dict): A dictionary containing the
                new values for each application.

            Returns:
                None
        """

        before_textBrowser = QtWidgets.QTextBrowser(changes_confirm_groupBox)
        before_textBrowser.setGeometry(QtCore.QRect(10, 140, 141, 131))
        before_textBrowser.setFont(self.s_font)
        before_textBrowser.setReadOnly(True)
        before_textBrowser.setObjectName("before_textBrowser")

        for application, limits in current_values_dict.items():
            before_textBrowser.append('{}: {}'.format(application, limits))

        after_textBrowser = QtWidgets.QTextBrowser(changes_confirm_groupBox)
        after_textBrowser.setGeometry(QtCore.QRect(230, 140, 141, 131))
        after_textBrowser.setFont(self.s_font)
        after_textBrowser.setReadOnly(True)
        after_textBrowser.setObjectName("after_textBrowser")

        for application, limits in new_values_full_dict.items():
            after_textBrowser.append('{}: {}'.format(application, limits))

    def label_creation(self, _translate, changes_confirm_groupBox):
        """ Creates all labels with specified properties and text.

            Parameters:
                _translate (QTranslator): A function that returns a
                translated version of a string.
                changes_confirm_groupBox (QGroupBox): group box widget the
                label will be added to.

            Returns:
                None
        """
        
        review_changes_label = QtWidgets.QLabel(changes_confirm_groupBox)
        review_changes_label.setGeometry(QtCore.QRect(10, 40, 421, 61))
        review_changes_label.setFont(self.s_font)
        review_changes_label.setWordWrap(True)
        review_changes_label.setObjectName("review_changes_label")
        # Text inside the label can be changed here
        review_changes_label.setText(
            _translate("confirmFarmChanges_MainWindow",
                       "Please take a close look below to compare the changes "
                       "you have made against the previous settings before you "
                       "fully apply them:"))
        
        before_label = QtWidgets.QLabel(changes_confirm_groupBox)
        before_label.setGeometry(QtCore.QRect(10, 110, 61, 20))
        before_label.setFont(self.l_font)
        before_label.setWordWrap(True)
        before_label.setObjectName("before_label")
        before_label.setStyleSheet('color : #D21404')
        before_label.setText(_translate("confirmFarmChanges_MainWindow",
                                        "Before:"))

        after_label = QtWidgets.QLabel(changes_confirm_groupBox)
        after_label.setGeometry(QtCore.QRect(230, 110, 51, 20))
        after_label.setFont(self.l_font)
        after_label.setWordWrap(True)
        after_label.setObjectName("after_label")
        after_label.setStyleSheet('color : #A7F432')
        after_label.setText(_translate("confirmFarmChanges_MainWindow",
                                       "After:"))

    def button_creation(self, _translate, changes_confirm_window,
                        changes_confirm_groupBox, config_file_path_name,
                        temp_folder, contents_dict, backup_folder,
                        new_values_full_dict):
        """ Creates and configures QPushButton widgets for user interaction.

            Parameters:
                self: The object instance.
                _translate (function): A translation function used for text
                localization.
                changes_confirm_window (QtWidgets.QMainWindow): The main window
                where the QPushButton widgets are placed.
                changes_confirm_groupBox (QtWidgets.QGroupBox): The group box
                where the QPushButton widgets will be added.
                config_file_path_name (str): The path and name of the
                configuration file.
                temp_folder (str): The path to the temporary folder.
                contents_dict (dict): A dictionary containing the current
                values of the configuration file.
                backup_folder (str): The path to the backup folder.
                new_values_full_dict (dict): A dictionary containing the new
                values for the configuration file.

            Returns:
                None
        """

        temp_file_pushButton = QtWidgets.QPushButton(changes_confirm_groupBox)
        temp_file_pushButton.setGeometry(QtCore.QRect(170, 300, 121, 22))
        temp_file_pushButton.setFont(self.s_font)
        temp_file_pushButton.setObjectName("applyChanges_pushButton")
        temp_file_pushButton.setText(_translate("confirmFarmChanges_MainWindow", "Stage"))
        temp_file_pushButton.setStyleSheet('color: yellow')

        # config_file_path_name, temp_folder, contents_dict, backup_folder,
        # new_values_full_dict
        def tmp_pushButton_clicked(cfpn, tf, cd, bf, nvfd):

            tmp_file_name = '{}temp.config'.format(tf)

            for application, limit in nvfd.items():
                cd['Limits'][application.lower()]['SiteMax'] = limit

            with open(tmp_file_name, mode='w') as created_file:
                json.dump(cd, created_file, indent=4)

            self.changesApplied_window = QtWidgets.QMainWindow()
            self.ui = Ui_changesApplied_MainWindow()
            self.ui.setupUi(self.changesApplied_window, cfpn,
                            tf, cd, bf, nvfd)
            self.changesApplied_window.show()

        temp_file_pushButton.clicked.connect(
            partial(tmp_pushButton_clicked, config_file_path_name, temp_folder,
                    contents_dict, backup_folder, new_values_full_dict))
        temp_file_pushButton.clicked.connect(changes_confirm_window.close)

        cancel_pushButton = QtWidgets.QPushButton(changes_confirm_groupBox)
        cancel_pushButton.setGeometry(QtCore.QRect(310, 300, 121, 22))
        cancel_pushButton.setFont(self.s_font)
        cancel_pushButton.setObjectName("cancel_pushButton")
        cancel_pushButton.setText(_translate("confirmFarmChanges_MainWindow", "Cancel"))
        cancel_pushButton.clicked.connect(self.cancel_button_clicked)
        cancel_pushButton.clicked.connect(changes_confirm_window.close)

    def cancel_button_clicked(self):
        from main_limits_selection_window import ui_AtomicCartoonsLimits_MainWindow
        self.farm_selection_window = QtWidgets.QMainWindow()
        self.ui = ui_AtomicCartoonsLimits_MainWindow()
        self.ui.setupUi(self.farm_selection_window)
        self.farm_selection_window.show()



