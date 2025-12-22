from PyQt5.uic.properties import QtWidgets

import sys
import requests
from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QLineEdit,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout,
                             QShortcut, QTextEdit,
                             QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence

import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

class EmailGen(QWidget):
    def configure(self):
        load_dotenv()

    def __init__(self):
        super().__init__()
        self.user_email_request_label = QLabel("Enter your email: ", self)
        self.user_email_input = QLineEdit(self)
        self.user_email_submit = QPushButton("Submit", self)
        self.user_email = ""

        self.app_password_inquiry = QLabel("Do you have an app password set up?",self)
        self.app_password_yes = QPushButton("Yes", self)
        self.app_password_no = QPushButton("No", self)
        self.app_password_instructions_description = QLabel("App Password Instructions", self)
        self.app_password_step_one = QLabel(self)
        self.app_password_step_two = QLabel(self)
        self.app_password_step_three = QLabel(self)
        self.app_password_step_four = QLabel(self)
        self.app_password_step_one_raw = QPixmap("app_password_step1.png")
        self.app_password_step_two_raw = QPixmap("app_password_step2.png")
        self.app_password_step_three_raw = QPixmap("app_password_step3.png")
        self.app_password_step_four_raw = QPixmap("app_password_step4.png")
        self.app_password_step_one.setPixmap(self.app_password_step_one_raw)
        self.app_password_step_two.setPixmap(self.app_password_step_two_raw)
        self.app_password_step_three.setPixmap(self.app_password_step_three_raw)
        self.app_password_step_four.setPixmap(self.app_password_step_four_raw)
        self.app_password_instructions_done = QPushButton("Done", self)

        self.app_password_ask = QLabel("Enter your app password", self)
        self.app_password_input = QLineEdit(self)
        self.app_password_submit = QPushButton("Submit", self)
        self.app_password = ""

        self.receiving_email = ""
        self.receiving_email_inquiry = QLabel("Enter the receiving email: ", self)
        self.receiving_email_input = QLineEdit(self)
        self.receiving_email_submit = QPushButton("Submit", self)

        self.email_subject_line = ""
        self.email_subject_line_inquiry = QLabel("Enter your subject line: ", self)
        self.email_subject_line_input = QLineEdit(self)
        self.email_subject_line_submit = QPushButton(self, text="Submit")

        self.email_body = ""
        self.email_description = ""
        self.email_body_inquiry = QLabel("Input the information (Write me an email about ___, include your name and the recipient's name. Be as specific as possible): ", self)
        self.email_body_inquiry.setWordWrap(True)
        self.email_body_input = QTextEdit(self)
        self.email_body_submit = QPushButton(self, text="Submit")

        self.body_email_display = QLabel(self)
        self.body_email_display.setWordWrap(True)
        self.body_email_edit_inquiry = QLabel("Would you like to edit the email?", self)
        self.body_email_edit_yes = QPushButton("Yes", self)
        self.body_email_edit_no = QPushButton("No", self)

        self.edit_type_inquiry = QLabel("How would you like to edit? AI or Manual?")
        self.edit_type_ai = QPushButton("AI", self)
        self.edit_type_manual = QPushButton("Manual", self)

        self.manual_edit_textbox = QTextEdit(self)
        self.manual_edit_textbox_submit = QPushButton("Submit", self)

        self.ai_edit_textbox = QTextEdit(self)
        self.ai_edit_textbox_submit = QPushButton("Submit", self)
        self.ai_edit_review_email_label = QTextEdit(self)
        self.ai_edit_review_email_label.setReadOnly(True)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Email Generation Software")
        self.setWindowIcon(QIcon("email_icon.jpg"))
        self.setGeometry(400,200,900,900)
        # Press keyboard instead of buttons
        enter_shortcut = QKeySequence(Qt.Key_Return)
        self.enter_shortcut = QShortcut(enter_shortcut, self)
        y_shortcut = QKeySequence(Qt.Key_Y)
        self.y_shortcut = QShortcut(y_shortcut, self)
        n_shortcut = QKeySequence(Qt.Key_N)
        self.n_shortcut = QShortcut(n_shortcut, self)

        self.setStyleSheet("""
                   QLabel, QPushButton, QLineEdit{
                       font-family: calibri;
                       qproperty-alignment: AlignCenter;
                   }
                   QLabel{
                       font-size: 40px;
                   }
                   QLineEdit{
                       font-size: 30px;
                   }
                   QPushButton{
                       font-size: 30px;
                       font-weight: bold;
                   }
                   QLabel#body_email_display{
                       font-size: 12px;
                   }
               """)

        self.body_email_display.setStyleSheet("font-size: 12px;")
        self.ai_edit_review_email_label.setStyleSheet("font-size: 12px;")
        # Request User Email
        self.vbox1 = QVBoxLayout()

        self.vbox1.addWidget(self.user_email_request_label)
        self.vbox1.addWidget(self.user_email_input)
        self.vbox1.addWidget(self.user_email_submit)
        self.vbox1_widget = QWidget(self)
        self.vbox1_widget.setLayout(self.vbox1)
        self.user_email_input.setFocus()
        self.vbox1_widget.show()

        # Do they have an app password?
        # If yes, moves on to next question
        # If no, gives instructions
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.app_password_inquiry)
        self.hbox_app_pass = QHBoxLayout()
        self.hbox_app_pass.addWidget(self.app_password_yes)
        self.hbox_app_pass.addWidget(self.app_password_no)
        self.vbox2.addLayout(self.hbox_app_pass)
        self.vbox2_widget = QWidget(self)
        self.vbox2_widget.setLayout(self.vbox2)
        self.vbox2_widget.hide()

        self.vbox_pass = QVBoxLayout()
        self.vbox_pass.addWidget(self.app_password_ask)
        self.vbox_pass.addWidget(self.app_password_input)
        self.vbox_pass.addWidget(self.app_password_submit)
        self.vbox_pass_widget = QWidget(self)
        self.vbox_pass_widget.setLayout(self.vbox_pass)
        self.vbox_pass_widget.hide()

        # App password Instructions
        self.vbox_instructions = QVBoxLayout()
        self.hbox_instructions_1 = QHBoxLayout()
        self.hbox_instructions_1.addWidget(self.app_password_step_one)
        self.hbox_instructions_1.addWidget(self.app_password_step_two)
        self.hbox_instructions_2 = QHBoxLayout()
        self.hbox_instructions_2.addWidget(self.app_password_step_three)
        self.hbox_instructions_2.addWidget(self.app_password_step_four)
        self.vbox_instructions.addWidget(self.app_password_instructions_description)
        self.app_password_instructions_description.setAlignment(Qt.AlignCenter)
        self.vbox_instructions.addLayout(self.hbox_instructions_1)
        self.vbox_instructions.addLayout(self.hbox_instructions_2)
        self.vbox_instructions.addWidget(self.app_password_instructions_done)
        self.vbox_instructions_widget = QWidget(self)
        self.vbox_instructions_widget.setLayout(self.vbox_instructions)
        self.vbox_instructions_widget.hide()

        self.vbox_receiving_email = QVBoxLayout()
        self.vbox_receiving_email.addWidget(self.receiving_email_inquiry)
        self.vbox_receiving_email.addWidget(self.receiving_email_input)
        self.vbox_receiving_email.addWidget(self.receiving_email_submit)
        self.vbox_receiving_email_widget = QWidget(self)
        self.vbox_receiving_email_widget.setLayout(self.vbox_receiving_email)
        self.vbox_receiving_email_widget.hide()

        # Email Subject line
        self.vbox3 = QVBoxLayout()
        self.vbox3.addWidget(self.email_subject_line_inquiry)
        self.vbox3.addWidget(self.email_subject_line_input)
        self.vbox3.addWidget(self.email_subject_line_submit)
        self.vbox3_widget = QWidget(self)
        self.vbox3_widget.setLayout(self.vbox3)
        self.vbox3_widget.hide()

        # Email Body
        self.vbox4 = QVBoxLayout()
        self.vbox4.addWidget(self.email_body_inquiry)
        self.vbox4.addWidget(self.email_body_input)
        self.vbox4.addWidget(self.email_body_submit)
        self.vbox4_widget = QWidget(self)
        self.vbox4_widget.setLayout(self.vbox4)
        self.vbox4_widget.hide()

        self.vbox_email_edit = QVBoxLayout()
        self.vbox_email_edit.addWidget(self.body_email_display)
        self.vbox_email_edit.addWidget(self.body_email_edit_inquiry)
        self.hbox10 = QHBoxLayout()
        self.hbox10.addWidget(self.body_email_edit_yes)
        self.hbox10.addWidget(self.body_email_edit_no)
        self.vbox_email_edit.addLayout(self.hbox10)
        self.vbox_email_edit_widget = QWidget(self)
        self.vbox_email_edit_widget.setLayout(self.vbox_email_edit)
        self.vbox_email_edit_widget.hide()

        self.vbox_edit_type = QVBoxLayout()
        self.hbox11 = QHBoxLayout()
        self.vbox_edit_type.addWidget(self.edit_type_inquiry)
        self.hbox11.addWidget(self.edit_type_ai)
        self.hbox11.addWidget(self.edit_type_manual)
        self.vbox_edit_type.addLayout(self.hbox11)
        self.vbox_edit_type_widget = QWidget(self)
        self.vbox_edit_type_widget.setLayout(self.vbox_edit_type)
        self.vbox_edit_type_widget.hide()

        self.body_email_display.setGeometry(200, 200, 200, 200)
        self.body_email_display.setMaximumSize(2000, 1000)

        self.vbox_manual_edit = QVBoxLayout()
        self.vbox_manual_edit.addWidget(self.manual_edit_textbox)
        self.vbox_manual_edit.addWidget(self.manual_edit_textbox_submit)
        self.manual_edit_textbox.setFixedSize(500,300)
        self.vbox_manual_edit_widget = QWidget(self)
        self.vbox_manual_edit_widget.setLayout(self.vbox_manual_edit)
        self.vbox_manual_edit_widget.hide()

        self.vbox_ai_edit = QVBoxLayout()
        self.vbox_ai_edit.addWidget(self.ai_edit_review_email_label)
        self.vbox_ai_edit.addWidget(self.ai_edit_textbox)
        self.vbox_ai_edit.addWidget(self.ai_edit_textbox_submit)
        self.vbox_ai_edit_widget = QWidget(self)
        self.vbox_ai_edit_widget.setLayout(self.vbox_ai_edit)
        self.vbox_ai_edit_widget.hide()

        self.ai_edit_review_email_label.resize(400,400)
        self.ai_edit_review_email_label.setMaximumSize(2000, 1000)

        self.user_email_inquiry()

    def user_email_inquiry(self):
        self.user_email = self.user_email_input.text()
        # Hide the first layout (with user email inquiries)
        # Shows the next question
        self.user_email_submit.clicked.connect(self.app_password_yn)
        self.enter_shortcut.activated.connect(self.app_password_yn)

    def app_password_yn(self):
        self.retreive_text("user_email")
        self.enter_shortcut.activated.disconnect()
        self.app_password_input.setFocus()
        self.vbox2_widget.show()
        self.vbox1_widget.hide()
        self.app_password_yes.clicked.connect(self.app_password_yes_clicked)
        self.y_shortcut.activated.connect(self.app_password_yes_clicked)
        self.app_password_no.clicked.connect(self.app_password_instructions)
        self.n_shortcut.activated.connect(self.app_password_instructions)

    def app_password_instructions(self):
        self.vbox2_widget.hide()
        self.vbox_instructions_widget.show()

        self.app_password_instructions_done.clicked.connect(self.app_password_yes_clicked)
        self.enter_shortcut.activated.connect(self.app_password_yes_clicked)

    def app_password_yes_clicked(self):
        self.vbox2_widget.hide()
        self.vbox_instructions_widget.hide()
        self.vbox_pass_widget.show()

        self.app_password = self.app_password_input.text()

        self.app_password_submit.clicked.connect(self.receiving_email_function)
        self.enter_shortcut.activated.connect(self.receiving_email_function)

    def receiving_email_function(self):
        self.retreive_text("app_password")
        self.enter_shortcut.activated.disconnect()

        self.receiving_email_input.setFocus()
        self.vbox_pass_widget.hide()
        self.vbox_receiving_email_widget.show()

        self.receiving_email = self.receiving_email_input.text()

        self.receiving_email_submit.clicked.connect(self.subject_line_function)
        self.enter_shortcut.activated.connect(self.subject_line_function)

    def subject_line_function(self):
        self.retreive_text("receiving_email")
        self.enter_shortcut.activated.disconnect()

        self.email_subject_line_input.setFocus()
        self.vbox_receiving_email_widget.hide()
        self.vbox3_widget.show()

        self.email_subject_line = self.email_subject_line_input.text()

        self.email_subject_line_submit.clicked.connect(self.get_email_description)
        self.enter_shortcut.activated.connect(self.get_email_description)

    def get_email_description(self):
        self.retreive_text("subject_line")
        self.enter_shortcut.activated.disconnect()

        self.email_body_input.setFocus()
        self.vbox3_widget.hide()
        self.vbox4_widget.show()

        self.email_body_submit.clicked.connect(self.write_email)
        self.enter_shortcut.activated.connect(self.write_email)

    def retreive_text(self, stage):
        if stage == "user_email":
            self.user_email = self.user_email_input.text()
        if stage == "app_password":
            self.app_password = self.app_password_input.text()
        if stage == "receiving_email":
            self.receiving_email = self.receiving_email_input.text()
        if stage == "subject_line":
            self.email_subject_line = self.email_subject_line_input.text()
        if stage == "email_description":
            self.email_description = self.email_body_input.toPlainText()
        if stage == "manual_edit":
            self.email_body = self.manual_edit_textbox.toPlainText()
        if stage == "ai_edit_label":
            self.ai_edit_review_email_label.setText(f"{self.email_body}")
        if stage == "ai_edit":
            self.email_description = self.email_description + "\n" + self.ai_edit_textbox.toPlainText()

    def write_email(self):
        self.retreive_text("email_description")
        self.enter_shortcut.activated.disconnect()
        self.vbox_ai_edit_widget.hide()
        self.vbox4_widget.hide()

        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")

        client = Groq(api_key=api_key)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{self.email_description}\n"
                               f"In your response, don't include the subject at the top of the email\n"
                               f"Fill in the names in Dear [recipient name] and best regards [sender name]",
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        # Print the completion returned by the LLM.

        self.email_body = chat_completion.choices[0].message.content
        self.body_email_display.setText(f"{self.email_body}")
        self.vbox_email_edit_widget.show()

        self.body_email_edit_yes.clicked.connect(self.edit_AI_or_manual)
        self.body_email_edit_no.clicked.connect(self.send_email)

    def edit_AI_or_manual(self):
        self.vbox_email_edit_widget.hide()
        self.vbox_edit_type_widget.show()

        self.edit_type_ai.clicked.connect(self.edit_AI)
        self.edit_type_manual.clicked.connect(self.edit_manual)

    def edit_AI(self):
        self.vbox_edit_type_widget.hide()
        self.vbox_ai_edit_widget.show()
        self.retreive_text("ai_edit_label")

        self.ai_edit_textbox.setFocus()

        self.retreive_text("ai_edit")

        self.ai_edit_textbox_submit.clicked.connect(self.write_email)
        self.enter_shortcut.activated.connect(self.write_email)

    def edit_manual(self):
        self.vbox_edit_type_widget.hide()
        self.vbox_manual_edit_widget.show()
        self.manual_edit_textbox.setText(self.email_body)
        self.manual_edit_textbox.setFocus()

        self.retreive_text("manual_edit")

        self.manual_edit_textbox_submit.clicked.connect(self.send_email)
        self.enter_shortcut.activated.connect(self.send_email)



    def send_email(self):
        self.enter_shortcut.activated.disconnect()
        message = MIMEMultipart()
        message['From'] = self.user_email
        message['To'] = self.receiving_email
        message['Subject'] = self.email_subject_line
        message.attach(MIMEText(self.email_body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com',587) as server:
            server.starttls()
            server.login(self.user_email, self.app_password)
            server.send_message(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailGen()
    window.show()
    sys.exit(app.exec_())