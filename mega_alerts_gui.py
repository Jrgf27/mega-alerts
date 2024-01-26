from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget, QMessageBox, QCheckBox, QFileDialog
from PyQt5 import QtGui
import sys, os
import requests
from sys import exit
import json
from mega_alerts import Alerts


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

class CheckBox(QMainWindow):
    def __init__(self,parent=None,labeltext=None,xposition=None,yposition=None, width=None, height=None):
        super(CheckBox,self).__init__()
        self.Checkbox=QCheckBox(labeltext,parent)
        self.Checkbox.setGeometry(xposition,yposition,width,height)
        self.Checkbox.setFont((QtGui.QFont("Arial",12,QtGui.QFont.Bold)))

class App(QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.title = 'Azeroth Auction Assassin'
        self.left = 0
        self.top = 0
        self.width = 1650
        self.height = 1000

        self.token_auth_url = "http://api.saddlebagexchange.com/api/wow/checkmegatoken"

        self.eu_connected_realms = os.path.join(os.getcwd(), "data", "eu-wow-connected-realm-ids.json")
        self.na_connected_realms = os.path.join(os.getcwd(), "data", "na-wow-connected-realm-ids.json")

        self.path_to_data = os.path.join(os.getcwd(), "data", "mega_data.json")
        self.path_to_desired_items = os.path.join(os.getcwd(), "data", "desired_items.json")
        self.path_to_desired_pets = os.path.join(os.getcwd(), "data", "desired_pets.json")
        self.path_to_desired_ilvl_items = os.path.join(os.getcwd(), "data", "desired_ilvl.json")
        self.path_to_desired_ilvl_list = os.path.join(os.getcwd(), "data", "desired_ilvl_list.json")

        self.pet_list = {}
        self.items_list = {}
        self.ilvl_list = []
        self.ilvl_items = {}

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.discord_webhook_input=LabelTextbox(self,"Discord Webhook",25,25,425,40)
        self.wow_client_id_input=LabelTextbox(self,"WoW Client ID",25,100,425,40)
        self.wow_client_secret_input=LabelTextbox(self,"WoW Client Secret",25,175,425,40)
        self.authentication_token=LabelTextbox(self,"Auction Assassin Token",25,250,425,40)

        self.wow_region_label = LabelText(self, 'Wow Region', 25, 325, 200, 40)
        self.wow_region=ComboBoxes(self,25,325,200,40)
        self.wow_region.Combo.addItems(['EU','NA'])

        self.show_bid_prices_label = LabelText(self, 'Show Bid Prices', 25, 400, 200, 40)
        self.show_bid_prices=ComboBoxes(self,25,400,200,40)
        self.show_bid_prices.Combo.addItems(['True','False'])

        self.number_of_mega_threads=LabelTextbox(self,"Number of Threads",250,325,200,40)

        self.wow_head_link_label = LabelText(self, 'Show WoWHead Link', 250, 400, 200, 40)
        self.wow_head_link=ComboBoxes(self,250,400,200,40)
        self.wow_head_link.Combo.addItems(['True','False'])

        self.import_config_button = UIButtons(self, "Import Config", 25, 750, 200, 50)
        self.import_config_button.Button.clicked.connect(self.import_configs)

        self.save_data_button = UIButtons(self, "Save Data", 25, 825, 200, 50)
        self.save_data_button.Button.clicked.connect(self.save_data_to_json)

        self.reset_data_button = UIButtons(self, "Reset Data", 250, 825, 200, 50)
        self.reset_data_button.Button.clicked.connect(self.reset_app_data)

        self.start_button = UIButtons(self, "Start Alerts", 25, 900, 200, 50)
        self.start_button.Button.clicked.connect(self.start_alerts)

        self.stop_button = UIButtons(self, "Stop Alerts", 250, 900, 200, 50)
        self.stop_button.Button.clicked.connect(self.stop_alerts)
        self.stop_button.Button.setEnabled(False)

        self.mega_alerts_progress = LabelText(self, 'Waiting for user to Start!', 25, 975, 1000, 40)

        ########################## PET STUFF ###################################################

        self.pet_id_input=LabelTextbox(self,"Pet ID",500,25,100,40)
        self.pet_price_input=LabelTextbox(self,"Price",625,25,100,40)

        self.add_pet_button = UIButtons(self, "Add Pet", 500, 100, 100, 50)
        self.add_pet_button.Button.clicked.connect(self.add_pet_to_dict)
        self.remove_pet_button = UIButtons(self, "Remove\nPet", 625, 100, 100, 50)
        self.remove_pet_button.Button.clicked.connect(self.remove_pet_to_dict)

        self.pet_list_display = ListView(self,500,175,225,400)
        self.pet_list_display.List.itemClicked.connect(self.pet_list_double_clicked)

        self.import_pet_data_button = UIButtons(self, "Import Pet Data", 500, 600, 225, 50)
        self.import_pet_data_button.Button.clicked.connect(self.import_pet_data)
        self.import_pet_data_button.Button.setToolTip('This is a tooltip')

        ########################## ITEM STUFF ###################################################

        self.item_id_input=LabelTextbox(self,"Item ID",750,25,100,40)
        self.item_price_input=LabelTextbox(self,"Price",875,25,100,40)

        self.add_item_button = UIButtons(self, "Add Item", 750, 100, 100, 50)
        self.add_item_button.Button.clicked.connect(self.add_item_to_dict)
        self.remove_item_button = UIButtons(self, "Remove\nItem", 875, 100, 100, 50)
        self.remove_item_button.Button.clicked.connect(self.remove_item_to_dict)

        self.item_list_display = ListView(self,750,175,225,400)
        self.item_list_display.List.itemClicked.connect(self.item_list_double_clicked)

        self.import_item_data_button = UIButtons(self, "Import Item Data", 750, 600, 225, 50)
        self.import_item_data_button.Button.clicked.connect(self.import_item_data)

        ########################## ILVL STUFF ###################################################

        self.ilvl_item_input=LabelTextbox(self,"Item ID",1000,25,100,40)
        self.ilvl_input=LabelTextbox(self,"Item level",1000,100,100,40)
        self.ilvl_price_input=LabelTextbox(self,"Buyout",1000,175,100,40)

        self.ilvl_sockets=CheckBox(self,"Sockets",1000,225,100,40)
        self.ilvl_speed=CheckBox(self,"Speed",1000,275,100,40)
        self.ilvl_leech=CheckBox(self,"Leech",1000,325,100,40)
        self.ilvl_avoidance=CheckBox(self,"Avoidance",1000,375,100,40)

        self.add_ilvl_button = UIButtons(self, "Add Item", 1000, 425, 100, 50)
        self.add_ilvl_button.Button.clicked.connect(self.add_ilvl_to_list)
        self.remove_ilvl_button = UIButtons(self, "Remove\nItem", 1000, 500, 100, 50)
        self.remove_ilvl_button.Button.clicked.connect(self.remove_ilvl_to_list)

        self.ilvl_list_display = ListView(self,1125,25,500,550)
        self.ilvl_list_display.List.itemClicked.connect(self.ilvl_list_double_clicked)

        self.import_ilvl_data_button = UIButtons(self, "Import ILvl Data", 1125, 600, 500, 50)
        self.import_ilvl_data_button.Button.clicked.connect(self.import_ilvl_data)

        self.check_for_settings()

        self.show()

    def check_config_file(self, path_to_config):
        raw_mega_data = json.load(open(path_to_config))

        try:
            if 'MEGA_WEBHOOK_URL' in raw_mega_data:
                self.discord_webhook_input.Text.setText(raw_mega_data['MEGA_WEBHOOK_URL'])

            if 'WOW_CLIENT_ID' in raw_mega_data:
                self.wow_client_id_input.Text.setText(raw_mega_data['WOW_CLIENT_ID'])
            
            if 'WOW_CLIENT_SECRET' in raw_mega_data:
                self.wow_client_secret_input.Text.setText(raw_mega_data['WOW_CLIENT_SECRET'])

            if 'AUTHENTICATION_TOKEN' in raw_mega_data:
                self.authentication_token.Text.setText(raw_mega_data['AUTHENTICATION_TOKEN'])

            if 'WOW_REGION' in raw_mega_data:
                index=self.wow_region.Combo.findText(raw_mega_data['WOW_REGION'])
                if index>=0:
                    self.wow_region.Combo.setCurrentIndex(index)

            if 'SHOW_BID_PRICES' in raw_mega_data:
                index=self.show_bid_prices.Combo.findText(str(raw_mega_data['SHOW_BID_PRICES']))
                if index>=0:
                    self.show_bid_prices.Combo.setCurrentIndex(index)

            if 'MEGA_THREADS' in raw_mega_data:
                self.number_of_mega_threads.Text.setText(str(raw_mega_data['MEGA_THREADS']))

            if 'WOWHEAD_LINK' in raw_mega_data:
                index=self.wow_head_link.Combo.findText(str(raw_mega_data['WOWHEAD_LINK']))
                if index>=0:
                    self.wow_head_link.Combo.setCurrentIndex(index)

        except:
            QMessageBox.critical(self, "Loading Error", "Could not load config settings from mega_data.json")

    def check_for_settings(self):

        data_folder = os.path.join(os.getcwd(), "data")
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        if not os.path.exists(self.eu_connected_realms):
            from utils.realm_data import EU_CONNECTED_REALMS_IDS

            with open(self.eu_connected_realms, 'w') as json_file:
                json.dump(EU_CONNECTED_REALMS_IDS, json_file, indent=4)

        if not os.path.exists(self.na_connected_realms):
            from utils.realm_data import NA_CONNECTED_REALMS_IDS

            with open(self.na_connected_realms, 'w') as json_file:
                json.dump(NA_CONNECTED_REALMS_IDS, json_file, indent=4)

        if os.path.exists(self.path_to_data):
            self.check_config_file(self.path_to_data)
                
        if os.path.exists(self.path_to_desired_pets):
            self.pet_list = json.load(open(self.path_to_desired_pets))
            for key,value in self.pet_list.items():
                self.pet_list_display.List.insertItem(self.pet_list_display.List.count() , f'Pet ID: {key}, Price: {value}')

        if os.path.exists(self.path_to_desired_items):
            self.items_list = json.load(open(self.path_to_desired_items))
            for key,value in self.items_list.items():
                self.item_list_display.List.insertItem(self.item_list_display.List.count() , f'Item ID: {key}, Price: {value}')

        if os.path.exists(self.path_to_desired_ilvl_list):
            self.ilvl_list = json.load(open(self.path_to_desired_ilvl_list))
            for ilvl_dict_data in self.ilvl_list:
                string_with_data = f"Item ID: {','.join(map(str, ilvl_dict_data['item_ids']))}; Price: {ilvl_dict_data['buyout']}; ILvl: {ilvl_dict_data['ilvl']}; Sockets: {ilvl_dict_data['sockets']}; Speed: {ilvl_dict_data['speed']}; Leech: {ilvl_dict_data['leech']}; Avoidance: {ilvl_dict_data['avoidance']}"
                self.ilvl_list_display.List.insertItem(self.ilvl_list_display.List.count() , string_with_data)


    def ilvl_list_double_clicked(self,item):
        item_split = item.text().replace(' ', '').split(':')

        item_id = item_split[1].split(';')[0]
        buyout = item_split[2].split(';')[0]
        ilvl = item_split[3].split(';')[0]
        sockets = item_split[4].split(';')[0]
        speed = item_split[5].split(';')[0]
        leech = item_split[6].split(';')[0]
        avoidance = item_split[7]

        self.ilvl_item_input.Text.setText(item_id)
        self.ilvl_price_input.Text.setText(buyout)

        self.ilvl_sockets.Checkbox.setChecked(sockets == "True")
        self.ilvl_speed.Checkbox.setChecked(speed == "True")
        self.ilvl_leech.Checkbox.setChecked(leech == "True")
        self.ilvl_avoidance.Checkbox.setChecked(avoidance == "True")

        self.ilvl_input.Text.setText(ilvl)

    def add_ilvl_to_list(self):
        if self.ilvl_input.Text.text() == "" or self.ilvl_price_input.Text.text() == "":
            return 0
        if self.ilvl_item_input.Text.text() == "":
            item_ids_list = []
        else:
            item_ids_list = list(map(int, self.ilvl_item_input.Text.text().replace(' ', '').split(',')))
        ilvl_dict_data = {
            'ilvl': int(self.ilvl_input.Text.text()),
            'buyout': int(self.ilvl_price_input.Text.text()),
            'sockets': self.ilvl_sockets.Checkbox.isChecked(),
            'speed': self.ilvl_speed.Checkbox.isChecked(),
            'leech': self.ilvl_leech.Checkbox.isChecked(),
            'avoidance': self.ilvl_avoidance.Checkbox.isChecked(),
            'item_ids': item_ids_list,

        }
        if ilvl_dict_data not in self.ilvl_list:
            self.ilvl_list.append(ilvl_dict_data)
            self.ilvl_list_display.List.insertItem(self.ilvl_list_display.List.count() ,
                                                   f"Item ID: {','.join(map(str, ilvl_dict_data['item_ids']))}; Price: {ilvl_dict_data['buyout']}; ILvl: {ilvl_dict_data['ilvl']}; Sockets: {ilvl_dict_data['sockets']}; Speed: {ilvl_dict_data['speed']}; Leech: {ilvl_dict_data['leech']}; Avoidance: {ilvl_dict_data['avoidance']}")

    def remove_ilvl_to_list(self):
        if len(self.ilvl_input.Text.text()) == 0:
            QMessageBox.critical(self, "Ilvl Removal Issue", "Please double click an ilvl json to remove it!")
            return
        if self.ilvl_item_input.Text.text() == "":
            item_ids_list = []
        else:
            item_ids_list = list(map(int, self.ilvl_item_input.Text.text().replace(' ', '').split(',')))

        ilvl_dict_data = {
            'ilvl': int(self.ilvl_input.Text.text()),
            'buyout': int(self.ilvl_price_input.Text.text()),
            'sockets': self.ilvl_sockets.Checkbox.isChecked(),
            'speed': self.ilvl_speed.Checkbox.isChecked(),
            'leech': self.ilvl_leech.Checkbox.isChecked(),
            'avoidance': self.ilvl_avoidance.Checkbox.isChecked(),
            'item_ids': item_ids_list,
        }

        if ilvl_dict_data in self.ilvl_list:
            string_with_data = f"Item ID: {','.join(map(str, ilvl_dict_data['item_ids']))}; Price: {ilvl_dict_data['buyout']}; ILvl: {ilvl_dict_data['ilvl']}; Sockets: {ilvl_dict_data['sockets']}; Speed: {ilvl_dict_data['speed']}; Leech: {ilvl_dict_data['leech']}; Avoidance: {ilvl_dict_data['avoidance']}"
            print(string_with_data)
            for x in range(self.ilvl_list_display.List.count()):
                if self.ilvl_list_display.List.item(x).text() == string_with_data:
                    self.ilvl_list_display.List.takeItem(x)
                    self.ilvl_list.remove(ilvl_dict_data)
                    return

    def import_ilvl_data(self):
        pathname=QFileDialog().getOpenFileName(self)[0]

        self.ilvl_list_display.List.clear()
        self.ilvl_list = {}

        self.ilvl_list = json.load(open(pathname))
        for ilvl_dict_data in self.ilvl_list:
            string_with_data = f"Item ID: {','.join(map(str, ilvl_dict_data['item_ids']))}; Price: {ilvl_dict_data['buyout']}; ILvl: {ilvl_dict_data['ilvl']}; Sockets: {ilvl_dict_data['sockets']}; Speed: {ilvl_dict_data['speed']}; Leech: {ilvl_dict_data['leech']}; Avoidance: {ilvl_dict_data['avoidance']}"
            self.ilvl_list_display.List.insertItem(self.ilvl_list_display.List.count() , string_with_data)


    def item_list_double_clicked(self,item):
        item_split = item.text().replace(' ', '').split(':')
        item_id = item_split[1].split(',')[0]
        self.item_id_input.Text.setText(item_id)
        self.item_price_input.Text.setText(item_split[2])

    def add_item_to_dict(self):
        if self.item_id_input.Text.text() == "" or self.item_price_input.Text.text() == "":
            return 0

        if self.item_id_input.Text.text() not in self.items_list:
            self.items_list[self.item_id_input.Text.text()] = self.item_price_input.Text.text()
            self.item_list_display.List.insertItem(self.item_list_display.List.count() , f'Item ID: {self.item_id_input.Text.text()}, Price: {self.item_price_input.Text.text()}')

    def remove_item_to_dict(self):
        if self.item_id_input.Text.text() in self.items_list:
            for x in range(self.item_list_display.List.count()):
                if self.item_list_display.List.item(x).text() == f'Item ID: {self.item_id_input.Text.text()}, Price: {self.items_list[self.item_id_input.Text.text()]}':

                    self.item_list_display.List.takeItem(x)
                    del self.items_list[self.item_id_input.Text.text()]
                    return

    def import_item_data(self):
        pathname=QFileDialog().getOpenFileName(self)[0]

        self.item_list_display.List.clear()
        self.items_list = {}

        self.items_list = json.load(open(pathname))
        for key,value in self.items_list.items():
            self.item_list_display.List.insertItem(self.item_list_display.List.count() , f'Item ID: {key}, Price: {value}')


    def pet_list_double_clicked(self,item):
        item_split = item.text().replace(' ', '').split(':')
        pet_id = item_split[1].split(',')[0]
        self.pet_id_input.Text.setText(pet_id)
        self.pet_price_input.Text.setText(item_split[2])

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

    def import_pet_data(self):
        pathname=QFileDialog().getOpenFileName(self)[0]

        self.pet_list_display.List.clear()
        self.pet_list = {}

        self.pet_list = json.load(open(pathname))
        for key,value in self.pet_list.items():
            self.pet_list_display.List.insertItem(self.pet_list_display.List.count() , f'Pet ID: {key}, Price: {value}')


    def import_configs(self):
        pathname=QFileDialog().getOpenFileName(self)[0]
        self.check_config_file(pathname)

    def reset_app_data(self):
        self.ilvl_list_display.List.clear()
        self.pet_list_display.List.clear()
        self.item_list_display.List.clear()

        self.pet_list = {}
        self.items_list = {}
        self.ilvl_list = []

        self.save_data_to_json()

    def save_data_to_json(self):
        config_json = {
            'MEGA_WEBHOOK_URL': self.discord_webhook_input.Text.text(),
            'WOW_CLIENT_ID': self.wow_client_id_input.Text.text(),
            'WOW_CLIENT_SECRET': self.wow_client_secret_input.Text.text(),
            'AUTHENTICATION_TOKEN': self.authentication_token.Text.text(),
            'WOW_REGION': self.wow_region.Combo.currentText(),
            'EXTRA_ALERTS': '[]',
            'SHOW_BID_PRICES': bool(self.show_bid_prices.Combo.currentText() == "True"),
            'MEGA_THREADS': int(self.number_of_mega_threads.Text.text()),
            'WOWHEAD_LINK': bool(self.wow_head_link.Combo.currentText() == "True")
        }

        with open(self.path_to_data, 'w') as json_file:
            json.dump(config_json, json_file, indent=4)

        with open(self.path_to_desired_pets, 'w') as json_file:
            json.dump(self.pet_list, json_file, indent=4)

        with open(self.path_to_desired_items, 'w') as json_file:
            json.dump(self.items_list, json_file, indent=4)

        with open(self.path_to_desired_ilvl_list, 'w') as json_file:
            json.dump(self.ilvl_list, json_file, indent=4)
        
        with open(self.path_to_desired_ilvl_items, 'w') as json_file:
            json.dump(self.ilvl_items, json_file, indent=4)

    def start_alerts(self):

        response = requests.post(self.token_auth_url, json={"token":f"{self.authentication_token.Text.text()}"})

        response_dict = response.json()

        if response.status_code != 200:
            QMessageBox.critical(self, "Request Error", f"Could not reach server, status code : {response.status_code}")
            return

        if len(response_dict) == 0:
            QMessageBox.critical(self, "Auction Assassin Token", "Please provide a valid Auction Assassin token!")
            return

        if not response_dict['succeeded']:
            QMessageBox.critical(self, "Auction Assassin Token", "Please provide a valid Auction Assassin token!")
            return

        self.start_button.Button.setEnabled(False)
        self.stop_button.Button.setEnabled(True)

        self.save_data_to_json()

        self.alerts_thread = Alerts(
            path_to_data_files = self.path_to_data,
            path_to_desired_items = self.path_to_desired_items,
            path_to_desired_pets = self.path_to_desired_pets,
            path_to_desired_ilvl_items = self.path_to_desired_ilvl_items,
            path_to_desired_ilvl_list = self.path_to_desired_ilvl_list
            )
        self.alerts_thread.start()
        self.alerts_thread.progress.connect(self.alerts_progress_changed)
        self.alerts_thread.finished.connect(self.alerts_thread_finished)

    def stop_alerts(self):
        self.alerts_thread.running=False
        self.stop_button.Button.setText('Stopping Process')
        self.alerts_progress_changed("Stopping alerts!")
        self.stop_button.Button.setEnabled(False)

    def alerts_thread_finished(self):
        self.stop_button.Button.setText("Stop Alerts")
        self.start_button.Button.setEnabled(True)
        self.alerts_progress_changed('Waiting for user to Start!')

    def alerts_progress_changed(self, progress_str):
        self.mega_alerts_progress.Label.setText(progress_str)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    exit(app.exec_())
