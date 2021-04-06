from PyQt5 import QtCore, QtGui, QtWidgets
import secrets
import mysql.connector
from mysql.connector import Error
import sys


"""
This operates and runs a momery enhacing app - Dev-Anki.
Attempting to recall material you are trying to learn - "Retrieval Practice" - is far more effective than simply rereading material.
Using spaced repetition, a studied and proven cognitive science technique  for fast and long-lasting memorization, you can either
greatly decrease your time spent studying, or greatly increase the amount you learn. It's proven to be vastly more efficient than traditional study methods.


This app is run in PyQt5, connects to a MySQL database, and uses Python for the backend.

To change:
Note: Queries in class are hardcoded
Note: DB details are hardcoded in setupUi

Functionality to add:
To do next - Add button to add questions and answers directly into database
Individual login verification
Hosted DB that doesn't require user to look after it
Add an ending and proper starting screen
Add a tracking & shuffling algo for long term memory retention. (Current interval selection is based on times selected below)


"""


class Ui_MainWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Dev Anki")
        MainWindow.resize(744, 524)
        self.colouring()
        self.add_buttons()
        self.db = self.db2 = self.create_server_connection(secrets.db_host, secrets.db_username, secrets.db_password, "mycodingquestions")
        if self.db and self.db2:
            self.mycursor = self.db.cursor()
            self.mycursor2 = self.db2.cursor()
        else:
            # TODO create POP UP - enter database details/login to said account
            pass


        self.again_interval = 0.8
        self.hard_interval = 1.2
        self.good_interval = 2.5
        self.easy_interval = 4

        self.correct_count = 0
        self.incorrect_count = 0
        self.correct_increment = 0
        self.incorrect_increment = 0


    
    # Applies GUI colouring options
    def colouring(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(58, 58, 58))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        #brush = QtGui.QBrush(QtGui.QColor(58, 58, 58))
        #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        #brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)


    # Adds all of the different buttons, labels, textboxes and options aswell as their listening action
    def add_buttons(self):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # AGAIN button & Label
        self.again_button = QtWidgets.QPushButton(self.centralwidget)
        self.again_button.setGeometry(QtCore.QRect(140, 410, 101, 31))
        self.again_button.setObjectName("again_button")
        self.again_button.clicked.connect(lambda: self.again_button_click())
            # LABEL
        self.again_label = QtWidgets.QLabel(self.centralwidget)
        self.again_label.setGeometry(QtCore.QRect(140, 390, 101, 20))
        self.again_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.again_label.setObjectName("again_label")
        

        # EASY Button & Label
        self.easy_button = QtWidgets.QPushButton(self.centralwidget)
        self.easy_button.setGeometry(QtCore.QRect(500, 410, 101, 31))
        self.easy_button.setObjectName("easy_button")
        self.easy_button.clicked.connect(lambda: self.easy_button_click())
                
            # LABEL
        self.easy_label = QtWidgets.QLabel(self.centralwidget)
        self.easy_label.setGeometry(QtCore.QRect(500, 390, 101, 20))
        self.easy_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.easy_label.setObjectName("easy_label")
        

        # GOOD Button & Label
        self.good_button = QtWidgets.QPushButton(self.centralwidget)
        self.good_button.setGeometry(QtCore.QRect(380, 410, 101, 31))
        self.good_button.setObjectName("good_button")
        self.good_button.clicked.connect(lambda: self.good_button_click())
            # LABEL
        self.good_label = QtWidgets.QLabel(self.centralwidget)
        self.good_label.setGeometry(QtCore.QRect(380, 390, 101, 20))
        self.good_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.good_label.setObjectName("good_label")

        # HARD Button & Label
        self.hard_button = QtWidgets.QPushButton(self.centralwidget)
        self.hard_button.setGeometry(QtCore.QRect(260, 410, 101, 31))
        self.hard_button.setObjectName("hard_button")
        self.hard_button.clicked.connect(lambda: self.hard_button_click())
            # LABEL
        self.hard_label = QtWidgets.QLabel(self.centralwidget)
        self.hard_label.setGeometry(QtCore.QRect(260, 390, 101, 20))
        self.hard_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.hard_label.setObjectName("hard_label")
                
        # RESPONSE BAR        
        self.Response_bar = QtWidgets.QTextEdit(self.centralwidget)
        self.Response_bar.setGeometry(QtCore.QRect(140, 270, 461, 41))
        self.Response_bar.setObjectName("Response_bar")
        
        # QUESTIONS BAR
        self.questions_label = QtWidgets.QLabel(self.centralwidget)
        self.questions_label.setGeometry(QtCore.QRect(140, 80, 461, 91))
        self.questions_label.setWordWrap(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.questions_label.setFont(font)
        self.questions_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.questions_label.setObjectName("questions_label")
        MainWindow.setCentralWidget(self.centralwidget)

        # CORRECT & INCORRECT COUNT BAR
        self.correct_label = QtWidgets.QLabel(self.centralwidget)
        self.correct_label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.correct_label.setObjectName("correct_label")
        self.incorrect_label = QtWidgets.QLabel(self.centralwidget)
        self.incorrect_label.setGeometry(QtCore.QRect(10, 30, 47, 13))
        self.incorrect_label.setObjectName("incorrect_label")
        
        # MENU
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 744, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        # CLEAR Button - this button will also be removed
        #self.clear = QtWidgets.QPushButton(self.centralwidget)
        #self.clear.setGeometry(QtCore.QRect(10, 280, 101, 23))
        #self.clear.setObjectName("clear")
        #self.clear.clicked.connect(lambda: self.clear_text())

        # CHECK
        self.check_answer = QtWidgets.QPushButton(self.centralwidget)
        self.check_answer.setGeometry(QtCore.QRect(620, 300, 101, 21))
        self.check_answer.setObjectName("check_answer")
        self.check_answer.clicked.connect(lambda: self.retrieve_response())  ##Here

        # SHOW ANSWER
        self.show_answer = QtWidgets.QPushButton(self.centralwidget)
        self.show_answer.setGeometry(QtCore.QRect(620, 260, 101, 23))
        self.show_answer.setObjectName("show_answer")
        self.show_answer.clicked.connect(lambda: self.show_actual_answer())
        
        # NEXT QUESTION
        #self.next_question = QtWidgets.QPushButton(self.centralwidget)
        #self.next_question.setGeometry(QtCore.QRect(620, 310, 101, 23))
        #self.next_question.setObjectName("next_question")
        #self.next_question.clicked.connect(lambda: self.next_click()) ## TEST FUNCTION - this box will be removed eventually - currently has a breaking bug - known - intented functionality

        # ANSWER BOX
        self.answer_box = QtWidgets.QLabel(self.centralwidget)
        self.answer_box.setGeometry(QtCore.QRect(140, 180, 451, 71))
        self.answer_box.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.answer_box.setObjectName("answer_box")

        # REMAINING LABEL
        self.remaining_label = QtWidgets.QLabel(self.centralwidget)
        self.remaining_label.setGeometry(QtCore.QRect(620, 10, 101, 20))
        self.remaining_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.remaining_label.setObjectName("remaining_label")

        # START BUTTON
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(620, 40, 101, 23))
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(lambda: self.begin_questions())

        # DATABASE CONNECTION
        self.db_connection = QtWidgets.QLabel(self.centralwidget)
        self.db_connection.setGeometry(QtCore.QRect(10, 480, 251, 26))
        self.db_connection.setObjectName("database_connection")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        



    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Dev Anki")

        # AGAIN
        self.again_button.setText("Again")
        self.again_button.setShortcut("Ctrl+1")
        self.again_button.setToolTip("CTRL 1")
        #self.again_label.setText("20 mins e.g.")

        # EASY
        self.easy_button.setText("Easy")
        self.easy_button.setShortcut("Ctrl+4")
        self.easy_button.setToolTip("CTRL 4")
        #self.easy_label.setText("4 days e.g.")

        # GOOD
        self.good_button.setText("Good")
        self.good_button.setShortcut("Ctrl+3")
        self.good_button.setToolTip("CTRL 3")
        #self.good_label.setText("1 day e.g.")
        
        # HARD
        self.hard_button.setText("Hard")
        self.hard_button.setShortcut("Ctrl+2")
        self.hard_button.setToolTip("CTRL 2")
        #self.hard_label.setText("1 hour e.g.")

        # QUESTION - CORRECT - INCORRECT
        self.questions_label.setText("Press start to begin")
        self.correct_label.setText("Correct: ")
        self.incorrect_label.setText("Incorrect: ")

        # CLEAR
        #self.clear.setText("Clear")
        #self.clear.setShortcut("Ctrl+7")
        #self.clear.setToolTip("CTRL 7")

        # CHECK ANSWER
        self.check_answer.setText("Check Answer")
        self.check_answer.setShortcut("Ctrl+Return")
        self.check_answer.setToolTip("CTRL ENTER")

        # SHOW ANSWER
        self.show_answer.setText("Show Answer")
        self.show_answer.setShortcut("Alt+Return")
        self.show_answer.setToolTip("ALT ENTER")

        # NEXT QUESTION
        #self.next_question.setText("Next")
        #self.next_question.setShortcut("Alt+Return")
        #self.next_question.setToolTip("ALT ENTER")

        # ANSWER BOX # REMAINING LABEL # START BUTTON # DATABASE CONNECTION
        self.answer_box.setText("")        
        self.remaining_label.setText("Remaining:")
        self.start_button.setText("Start")
        self.db_connection.setText("Database Connection: ")

        
        self.menuFile.setTitle("File")
        self.update()


    # Updates the size of all of the labels so that text doesn't get cut off       
    def update(self):
        #self.easy_label.adjustSize()
        #self.hard_label.adjustSize()
        #self.good_label.adjustSize()
        #self.again_label.adjustSize()
        self.correct_label.adjustSize()
        self.incorrect_label.adjustSize()
        self.db_connection.adjustSize()
       
    
    def show_actual_answer(self):
        try:
            self.answer_box.setText(self.row[3])
        except:
            pass


    def add_score(self, correct, incorrect):
        self.correct_count += correct
        self.incorrect_count += incorrect
        self.correct_label.setText("Correct: " + str(self.correct_count))
        self.incorrect_label.setText("Incorrect: " + str(self.incorrect_count))
        self.correct_increment, self.incorrect_increment = 0, 0


    def reset_score(self):
        self.correct_label.setText("Correct: 0")
        self.incorrect_label.setText("Incorrect: 0")
        self.update()


    # This is referring to the background colours of the correct and incorrect labels
    def normalize_colour(self):
        self.correct_label.setStyleSheet("background-color: transparent; color: white")
        self.incorrect_label.setStyleSheet("background-color: transparent; color: white")


    def correct_colour(self):
        self.normalize_colour()
        self.correct_label.setStyleSheet("background-color: green")


    def incorrect_colour(self):
        self.normalize_colour()
        self.incorrect_label.setStyleSheet("background-color: red")


    # This needs some better logic rather than just a 0.8* review - needs to bring it back down to 20mins or so (but not affect the overall timing drastically)
    def again_button_click(self):
        try:
            self.again_button_interval = self.row[4]*self.again_interval
            self.update_database_dateincrement(self.again_button_interval)
            self.next_click(self.again_button_interval)
        except:
            pass


    def hard_button_click(self):
        try:
            self.hard_button_interval = self.row[4]*self.hard_interval
            self.update_database_dateincrement(self.hard_button_interval)
            self.next_click(self.hard_button_interval)
        except:
            pass        

    def good_button_click(self):
        try:
            self.good_button_interval = self.row[4]*self.good_interval
            self.update_database_dateincrement(self.good_button_interval)
            self.next_click(self.good_button_interval)
        except:
            pass
    
    def easy_button_click(self):
        try:
            self.easy_button_interval = self.row[4]*self.easy_interval
            self.update_database_dateincrement(self.easy_button_interval)
            self.next_click(self.easy_button_interval)
        except:
            pass

    # UPDATES ALL THE BUTTONS WITH THE CURRENT INTERVALS
    def update_interval_buttons(self):
        if self.db:
            self.again_label.setText(self.button_timeframes(self.row[4]*self.again_interval))
            self.hard_label.setText(self.button_timeframes(self.row[4]*self.hard_interval))
            self.good_label.setText(self.button_timeframes(self.row[4]*self.good_interval))
            self.easy_label.setText(self.button_timeframes(self.row[4]*self.easy_interval))

    def button_timeframes(self, timing):
        if timing <= 60:
            return str(int(timing)) + ' minutes'
        elif timing > 60 and timing <= 1440:
            return '{0:.1f} hours'.format(timing/60)
        elif timing > 1440:
            return '{0:.1f} days'.format(timing/60/24)
    
    def clear_text(self):
        self.Response_bar.clear()


    # BOUND TO CHECK BOX - Gets the response from the textbox (ctrl enter) and then compares it with the answer from DB
    def retrieve_response(self):
        try:
            self.user_answer = self.Response_bar.toPlainText()
            self.actual_answer_from_db = self.row[3]
            
            if self.actual_answer_from_db.lower().strip() == self.user_answer.lower().strip():
                self.correct_colour()
                self.correct_increment, self.incorrect_increment = 1, 0

            else:
                self.incorrect_colour()
                self.correct_increment, self.incorrect_increment = 0, 1
                
        except:
            pass


    # Used within the again/hard/good/easy buttons - completes everything required to move onto the next question. 
    def next_click(self, new_date_increment):
        try:        
            self.retrieve_response()
            self.update_database_next_date(new_date_increment)
            self.clear_text()
            self.answer_box.setText('') 
            self.next_row()
            self.update_interval_buttons()
            self.questions_label.setText(self.row[2])
            self.normalize_colour()
            self.add_score(self.correct_increment, self.incorrect_increment)
            self.remaining_label.setText(f"Remaining: {self.rowcount - self.correct_count - self.incorrect_count}")
            
            self.update()
            
        except:
            print('error occured')
            pass        

 
    # Adding DB Functionality - currently called in thes setup phase and uses a pre-existing db to connect to.
    # Make a login based profile that initially creates the user their own DB, and then accesses that whenever they log in.
    # It's currently hard-coded within the class - change this for future users
    def create_server_connection(self, host_name, user_name, user_password, database_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=database_name,
                buffered = True
            )
            self.db_connection.setText("Database Connection: MySQL Database connection successful")
            self.db_connection.adjustSize()
            
        except Error as err:
            print(f"Error: '{err}'")
            self.db_connection.setText(f"Database Connection Error: '{err}'")
            self.db_connection.adjustSize()
            
        return connection


    # BOUND TO "START" BUTTON - initiates the SELECT query and displays the first question - creates the self.row variable
    def begin_questions(self):
        if self.db:
            self.mycursor.execute("SELECT id, category, question, answer, dateincrement, nextdate FROM questions WHERE nextdate < NOW() ORDER BY nextdate ASC")
            self.row = self.mycursor.fetchone()
            self.answer_box.setText("")
            self.questions_label.setText(self.row[2])
            self.add_score(self.correct_increment, self.incorrect_increment)
            self.update_interval_buttons()
            self.rowcount = self.mycursor.rowcount
            self.remaining_label.setText(f"Remaining: {self.rowcount}")
            self.reset_score()
 

       
    def next_row(self):
        if self.db:
            self.row = self.mycursor.fetchone()


    # TODO
    def get_database_details(self):
        
        # If the DB doesn't connect, provide an option to enter db details in
        # Alternatively, create a login/verification portal that remembers their details
        
        pass


    def update_database_next_date(self, new_date_increment):
        try:
            self.update_query = "UPDATE questions SET nextdate = DATE_ADD( NOW(), INTERVAL %s MINUTE) WHERE id = %s"
            self.query_details = (new_date_increment, self.row[0])
            self.mycursor2.execute(self.update_query, self.query_details)
            self.db2.commit()
        except:
            print("error has occured in Update database next date function")
            pass    


    def update_database_dateincrement(self, button_input):
        try:
            self.update_date_increment_query = "UPDATE questions SET dateincrement = %s WHERE id = %s"
            self.query_details_date_increment = (button_input, self.row[0])
            self.mycursor2.execute(self.update_date_increment_query, self.query_details_date_increment)
            self.db2.commit()
        except:
            print('dateincrement query problems')
            pass
        
            

if __name__ == "__main__":    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    


