#!/sw/bin/python

# This window is the Initial Window of the Atomic Farm UI for Show & License Limits.
# Created using PyQt5
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QApplication
from functools import partial
# These are all the other windows being imported
from application_limits_window import ui_ApplicationLimits_MainWindow
from show_selection_window import ui_ShowSelectionLimits_MainWindow

class ui_AtomicCartoonsLimits_MainWindow(object):

    # Window Main Settings
    def setupUi(self, limits_selection_window):
        """ Sets up the user interface for the limits' selection window.

            Parameters:
                limits_selection_window (QtWidgets.QMainWindow): The main
                limits' selection window.

            Returns:
                None
        """

        # These are the location of both the main Config file and where
        # the temp file and backup files will be created
        config_file_path_name = '/sw/tractor/config/limits.config'
        temp_folder = '/sw/tractor/config/tmp/'
        backup_folder = '/sw/tractor/config/limits_backup/'

        # This is needed to translate the Python strings into a 'language' the UI
        # from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS
        # Create all fonts
        self.create_fonts()
        limit_selection_window = \
            self.limit_selection_window_setup(limits_selection_window, _translate)

        limits_select_groupBox = self.groupBox_creation(_translate)
        limits_select_comboBox = \
            self.combo_box_creation(_translate, limits_select_groupBox)

        self.label_creation(_translate, limits_select_groupBox)
        self.button_creation(_translate, limit_selection_window,
                             limits_select_groupBox, limits_select_comboBox,
                             config_file_path_name, temp_folder, backup_folder)


        QtCore.QMetaObject.connectSlotsByName(limits_selection_window)

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

    def limit_selection_window_setup(self, limits_selection_window, _translate):
        """ This function sets up the limit selection window, including the size,
            style, and title of the window, as well as centering it on the screen.

            Parameters:
                limits_selection_window (QMainWindow): The main window
                object that
                the function will set up.
                _translate (QTranslator): A function that returns a
                translated version of a string.

            Returns:
                farm_selection_window (QMainWindow): The now set-up main window
                object.
        """

        limits_selection_window.setObjectName("AtomicCartoonsLimitsUI_MainWindow")
        # Window Size can be adjusted here
        limits_selection_window.setFixedSize(463, 182)
        # Using this style sheet the theme can be changed
        limits_selection_window.setStyleSheet("background-color: rgb(46, 52, 54);"
                                              "\n""color: rgb(238, 238, 236);")

        # Title of the Main Window can be changed here.
        limits_selection_window.setWindowTitle(_translate(
            'main_limits_selection_window', "Main Limits Selection Window"))

        self.centralwidget = QtWidgets.QWidget(limits_selection_window)

        limits_selection_window.setCentralWidget(self.centralwidget)

        def center(lsw):  # limits_selection_window
            qr = lsw.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            lsw.move(qr.topLeft())

        center(limits_selection_window)

        return limits_selection_window

    def groupBox_creation(self, _translate):
        """ Creates a group box widget for limit selection.

            Parameters:
                self (QtWidgets.QGroupBox): The class object
                _translate (QTranslator): A function that returns a translated
                version of a string.

            Returns:
                limits_select_groupBox (QtWidgets.QGroupBox): the group box for
                limit selection.
        """

        limits_select_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        limits_select_groupBox.setGeometry(QtCore.QRect(10, 10, 441, 161))
        limits_select_groupBox.setFont(self.l_font)
        # Title of the Group Box
        limits_select_groupBox.setTitle(
            _translate("AtomicCartoonsLimitsUI_MainWindow", "Limits Selection"))

        return limits_select_groupBox

    def combo_box_creation(self, _translate, limits_select_groupBox):
        """ Creates a QComboBox widget and two sections: one section for
            Application Limits and another for Show Limits

            Parameters:
                _translate (QTranslator): A function that returns a translated
                version of a string.
                limits_select_groupBox (QGroupBox): The groupbox where the
                combo box will be added

            Returns:
                limits_select_comboBox (QComboBox): The created and configured
                combo box widget
        """

        limits_select_comboBox = QtWidgets.QComboBox(
            limits_select_groupBox)
        limits_select_comboBox.setGeometry(QtCore.QRect(10, 120, 201, 22))
        limits_select_comboBox.setFont(self.s_font)
        limits_select_comboBox.setStyleSheet('color : #A7F432')
        limits_select_comboBox.setObjectName("limits_select_comboBox")
        # Creating all the slots to be allocated in the Combo Box.
        # Amount of sections this box is being separated by (one section for
        # Application Limits and another for Show Limits)
        selections = 2
        while selections > 0:
            limits_select_comboBox.addItem("")
            selections -= 1
        # All titles for all items in the Combo Box
        limits_select_comboBox.setItemText(0, _translate(
            "AtomicCartoonsLimitsUI_MainWindow", "Show Defined Limits"))
        limits_select_comboBox.setItemText(1, _translate(
            "AtomicCartoonsLimitsUI_MainWindow", "License/Application Limits"))
        
        return limits_select_comboBox

    def label_creation(self, _translate, limits_select_groupBox):
        """ Creates all labels with specified properties and text.

            Parameters:
                _translate (QTranslator): A function that returns a
                translated version of a string.
                limits_select_groupBox (QGroupBox): group box widget the label
                will be added to.

            Returns:
                limits_select_label (QLabel): the created label widget
        """

        limits_select_label = QtWidgets.QLabel(limits_select_groupBox)
        limits_select_label.setGeometry(QtCore.QRect(10, 40, 421, 61))
        limits_select_label.setFont(self.s_font)
        limits_select_label.setWordWrap(True)
        limits_select_label.setObjectName("limits_select_label")
        # Text inside the label can be changed here
        limits_select_label.setText(
            _translate("AtomicCartoonsLimitsUI_MainWindow",
                       "Utilizing the dropdown menu below, please select if you "
                       "would like to change the License Limits or the "
                       "Show Limits:"))

        return limits_select_label

    def button_creation(self, _translate, limits_selection_window,
                        limits_select_groupBox, limits_select_comboBox,
                        config_file_path_name, temp_folder, backup_folder):

        """ Create and set up the button for confirming the farm selection

            Parameters:
                _translate (QTranslator): A function that returns a
                translated version of a string.
                limits_selection_window (QtWidgets.QMainWindow): the parent
                window for the button.
                limits_select_groupBox (QtWidgets.QGroupBox): the group box
                containing the button.
                limits_select_comboBox (QtWidgets.QComboBox): the combo box
                where the selection is made.
                config_file_path_name (str): path and name of the config file
                temp_folder (str): path of the temp folder
                backup_folder (str): path of the backup folder

           Returns:
               none
        """

        self.limits_select_pushButton = \
            QtWidgets.QPushButton(limits_select_groupBox)
        self.limits_select_pushButton.setGeometry(QtCore.QRect(250, 120, 171, 22))
        self.limits_select_pushButton.setFont(self.s_font)
        self.limits_select_pushButton.setObjectName("limits_select_pushButton")
        # Text inside the button can be changed here
        self.limits_select_pushButton.setText(
            _translate("AtomicCartoonsLimitsUI_MainWindow",
                       "Confirm My Selection"))

        # Opening the other windows according to the selection of the Combo Box
        # config_file_path_name, temp_folder, backup_folder
        def limits_select_button_clicked(cfpn, tf, bf):
            if limits_select_comboBox.currentText() == \
                    'Show Defined Limits':
                self.open_ShowLimitsSelection_window(cfpn, tf, bf)
            elif limits_select_comboBox.currentText() == \
                    'License/Application Limits':
                self.open_ApplicationLimits_window(cfpn, tf, bf)

        # IMPORTANT: This is what happens when the button is pressed to
        # confirm selection
        self.limits_select_pushButton.clicked.connect(
            partial(limits_select_button_clicked, config_file_path_name,
                    temp_folder, backup_folder))
        self.limits_select_pushButton.clicked.connect(
            limits_selection_window.close)

    # Opens Show Selection Limits window
    def open_ShowLimitsSelection_window(self, cfpn, tf, bf):
        self.showLimits_window = QtWidgets.QMainWindow()
        self.ui = ui_ShowSelectionLimits_MainWindow()
        self.ui.setupUi(self.showLimits_window, cfpn, tf, bf)
        self.showLimits_window.show()

    # Opens Application Limits window
    def open_ApplicationLimits_window(self, cfpn, tf, bf):
        self.appLimits_window = QtWidgets.QMainWindow()
        self.ui = ui_ApplicationLimits_MainWindow()
        self.ui.setupUi(self.appLimits_window, cfpn, tf, bf)
        self.appLimits_window.show()

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    atomic_limits_selection_window = QtWidgets.QMainWindow()
    ui = ui_AtomicCartoonsLimits_MainWindow()
    ui.setupUi(atomic_limits_selection_window)
    atomic_limits_selection_window.show()
    sys.exit(app.exec_())
