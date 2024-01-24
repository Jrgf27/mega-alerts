from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget
from PyQt5 import QtGui
import sys, os
from sys import exit
import json
from mega_alerts import alerts

class LabelTextbox(QMainWindow):

    def __init__(self,parent=None, labeltext=None,xposition=None,yposition=None, width=None, height=None):
        super(LabelTextbox,self).__init__()
        self.Label = QLabel(parent)
        self.Label.setText(labeltext)
        self.Label.move(xposition,yposition-30)
        self.Label.resize(width,height)
        self.Label.setFont((QtGui.QFont("Arial",12,QtGui.QFont.Bold)))
        self.Text = QLineEdit(parent)
        self.Text.move(xposition, yposition)
        self.Text.resize(width,height)
        self.Text.setFont((QtGui.QFont("Arial",12)))

class UIButtons(QMainWindow):

    def __init__(self, parent=None, title=None, xposition=None,yposition=None,width=None,heigth=None):
        super(UIButtons,self).__init__()
        self.Button=QPushButton(title, parent)
        self.Button.setFont((QtGui.QFont("Arial",12,QtGui.QFont.Bold)))
        self.Button.move(xposition,yposition)
        self.Button.resize(width,heigth)

class ComboBoxes(QMainWindow):
    def __init__(self,parent=None,xposition=None,yposition=None, width=None, height=None):
        super(ComboBoxes,self).__init__()
        self.Combo=QComboBox(parent)
        self.Combo.setGeometry(xposition,yposition,width,height)

class LabelText(QMainWindow):
    def __init__(self,parent=None, labeltext=None,xposition=None,yposition=None, width=None, height=None):
        super(LabelText,self).__init__()
        self.Label = QLabel(parent)
        self.Label.setText(labeltext)
        self.Label.move(xposition,yposition-30)
        self.Label.resize(width,height)
        self.Label.setFont((QtGui.QFont("Arial",12,QtGui.QFont.Bold)))

class ListView(QMainWindow):
    def __init__(self,parent=None, xposition=None,yposition=None, width=None, height=None):
        super(ListView,self).__init__()
        self.List = QListWidget(parent)
        self.List.move(xposition,yposition)
        self.List.resize(width,height)
        self.List.setFont((QtGui.QFont("Arial",12,QtGui.QFont.Bold)))

class App(QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.title = 'Mega Alerts App'
        self.left = 0
        self.top = 0
        self.width = 750
        self.height = 750

        self.path_to_data = os.path.join(os.getcwd(), "mega_data.json")
        self.path_to_desired_items = os.path.join(os.getcwd(), "desired_items.json")
        self.path_to_desired_pets = os.path.join(os.getcwd(), "desired_pets.json")
        self.path_to_desired_ilvl_items = os.path.join(os.getcwd(), "desired_ilvl.json")
        self.path_to_desired_ilvl_list = os.path.join(os.getcwd(), "desired_ilvl_list.json")

        self.pet_list = {}
        self.pet_list_labels = []

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.discord_webhook_input=LabelTextbox(self,"Discord Webhook",25,25,425,40)
        self.wow_client_id_input=LabelTextbox(self,"WoW Client ID",25,100,425,40)
        self.wow_client_secret_input=LabelTextbox(self,"WoW Client Secret",25,175,425,40)

        self.wow_region_label = LabelText(self, 'Wow Region', 25, 250, 200, 40)
        self.wow_region=ComboBoxes(self,25,250,200,40)
        self.wow_region.Combo.addItems(['EU','NA'])

        self.show_bid_prices_label = LabelText(self, 'Show Bid Prices', 25, 325, 200, 40)
        self.show_bid_prices=ComboBoxes(self,25,325,200,40)
        self.show_bid_prices.Combo.addItems(['True','False'])

        self.number_of_mega_threads=LabelTextbox(self,"Number of Threads",250,250,200,40)

        self.wow_head_link_label = LabelText(self, 'Show WoWHead Link', 250, 325, 200, 40)
        self.wow_head_link=ComboBoxes(self,250,325,200,40)
        self.wow_head_link.Combo.addItems(['True','False'])

        self.start_button = UIButtons(self, "Start Alerts", 25, 600, 200, 50)
        self.start_button.Button.clicked.connect(self.start_alerts)

        self.stop_button = UIButtons(self, "Stop Alerts", 250, 600, 200, 50)
        self.stop_button.Button.clicked.connect(self.stop_alerts)
        self.stop_button.Button.setEnabled(False)

        self.pet_id_input=LabelTextbox(self,"Pet ID",500,25,100,40)
        self.pet_price_input=LabelTextbox(self,"Price",625,25,100,40)

        self.add_pet_button = UIButtons(self, "Add Pet", 500, 100, 100, 50)
        self.add_pet_button.Button.clicked.connect(self.add_pet_to_dict)
        self.remove_pet_button = UIButtons(self, "Remove\nPet", 625, 100, 100, 50)
        self.remove_pet_button.Button.clicked.connect(self.remove_pet_to_dict)

        self.pet_list_display = ListView(self,500,175,225,400)
        self.pet_list_display.List.itemDoubleClicked.connect(self.pet_list_double_clicked)

        self.check_for_settings()

        self.show()

    def pet_list_double_clicked(self,item):
        item_split = item.text().replace(' ', '').split(':')
        pet_id = item_split[1].split(',')[0]
        self.pet_id_input.Text.setText(pet_id)
        self.pet_price_input.Text.setText(item_split[2])

    def check_for_settings(self):
        if os.path.exists(self.path_to_data):
            raw_mega_data = json.load(open(self.path_to_data))

            if len(raw_mega_data) == 8:
                self.discord_webhook_input.Text.setText(raw_mega_data['MEGA_WEBHOOK_URL'])
                self.wow_client_id_input.Text.setText(raw_mega_data['WOW_CLIENT_ID'])
                self.wow_client_secret_input.Text.setText(raw_mega_data['WOW_CLIENT_SECRET'])

                index=self.wow_region.Combo.findText(raw_mega_data['WOW_REGION'])
                if index>=0:
                    self.wow_region.Combo.setCurrentIndex(index)

                index=self.show_bid_prices.Combo.findText(str(raw_mega_data['SHOW_BID_PRICES']))
                if index>=0:
                    self.show_bid_prices.Combo.setCurrentIndex(index)

                self.number_of_mega_threads.Text.setText(str(raw_mega_data['MEGA_THREADS']))

                index=self.wow_head_link.Combo.findText(str(raw_mega_data['WOWHEAD_LINK']))
                if index>=0:
                    self.wow_head_link.Combo.setCurrentIndex(index)

    def add_pet_to_dict(self):
        if self.pet_id_input.Text.text() == "" or self.pet_price_input.Text.text() == "":
            return 0
        
        if self.pet_id_input.Text.text() not in self.pet_list:
            self.pet_list[self.pet_id_input.Text.text()] = self.pet_price_input.Text.text()
            self.pet_list_display.List.insertItem(self.pet_list_display.List.count() , f'Pet ID: {self.pet_id_input.Text.text()}, Price: {self.pet_price_input.Text.text()}')

    def remove_pet_to_dict(self):
        if self.pet_id_input.Text.text() in self.pet_list:
            for x in range(self.pet_list_display.List.count()):
                if self.pet_list_display.List.item(x).text() == f'Pet ID: {self.pet_id_input.Text.text()}, Price: {self.pet_list[self.pet_id_input.Text.text()]}':

                    self.pet_list_display.List.takeItem(x)
                    del self.pet_list[self.pet_id_input.Text.text()]
                    return

    def start_alerts(self):
        self.start_button.Button.setEnabled(False)
        self.stop_button.Button.setEnabled(True)

        config_json ={
            'MEGA_WEBHOOK_URL': self.discord_webhook_input.Text.text(),
            'WOW_CLIENT_ID': self.wow_client_id_input.Text.text(),
            'WOW_CLIENT_SECRET': self.wow_client_secret_input.Text.text(),
            'WOW_REGION': self.wow_region.Combo.currentText(),
            'EXTRA_ALERTS': '[]',
            'SHOW_BID_PRICES': bool(self.show_bid_prices.Combo.currentData()),
            'MEGA_THREADS': int(self.number_of_mega_threads.Text.text()),
            'WOWHEAD_LINK': bool(self.wow_head_link.Combo.currentData())
        }

        with open(self.path_to_data, 'w') as json_file:
            json.dump(config_json, json_file, indent=4)

        with open(self.path_to_desired_pets, 'w') as json_file:
            json.dump(self.pet_list, json_file, indent=4)

        self.alerts_thread = alerts(
            self.path_to_data,
            self.path_to_desired_items,
            self.path_to_desired_pets,
            self.path_to_desired_ilvl_items,
            self.path_to_desired_ilvl_list
            )
        self.alerts_thread.start()
        self.alerts_thread.finished.connect(self.alerts_thread_finished)

    def stop_alerts(self):
        self.alerts_thread.running=False
        self.stop_button.Button.setText('Stopping Process')
        self.stop_button.Button.setEnabled(False)

    def alerts_thread_finished(self):
        self.stop_button.Button.setText("Stop Alerts")
        self.start_button.Button.setEnabled(True)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()
    exit(app.exec_())
