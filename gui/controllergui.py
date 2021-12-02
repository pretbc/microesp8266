import sys
import re

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QListWidget, QComboBox, QMainWindow,
    QTabWidget, QFormLayout
)
from PyQt6.QtGui import QFont

from controller.compiler import Compiler
from controller.config.load_genbin_config import get_custom_configs_only
from controller.esptool import EspTool
from controller.genbin import BootVersion, Bin, SpiSpeed, SpiMode, SpiSize


class TabABC(QWidget):
    def __init__(self):
        super().__init__()
        name = re.findall('[A-Z][^A-Z]*', f'{type(self).__name__}')
        self.setWindowTitle('-'.join([n.lower() for n in name if n.lower() != 'tab']))
        self.label = QLabel()
        self.create_list()
        vbox = QVBoxLayout()
        vbox.addWidget(self.list_wgt)
        vbox.addWidget(self.label)
        self.setLayout(vbox)

    def create_list(self):
        self.list_wgt = QListWidget()
        self.list_wgt.setFont(QFont('Times New Roman', 14))
        for i, option in enumerate(self._cfg.possible_options):
            [self.list_wgt.insertItem(i, val['name']) for val in option.values()]
        self.list_wgt.setCurrentRow(self._cfg.get_default)
        self.list_wgt.clicked.connect(self.item_selected_list)
        self.set_label(self.list_wgt.currentItem())

    def item_selected_list(self):
        self.set_label(self.list_wgt.currentItem())

    def set_label(self, set_value):
        self.label.setText(f'selected => {set_value.text()}')

    @property
    def name(self):
        return self.windowTitle()

    @property
    def get_value(self):
        return int(self.list_wgt.currentRow())


class BootTab(TabABC):
    def __init__(self):
        self._cfg = BootVersion()
        super().__init__()


class BinTab(TabABC):
    def __init__(self):
        self._cfg = Bin()
        super().__init__()


class SpiSpeedTab(TabABC):
    def __init__(self):
        self._cfg = SpiSpeed()
        super().__init__()


class SpiModeTab(TabABC):
    def __init__(self):
        self._cfg = SpiMode()
        super().__init__()


class SpiSizeTab(TabABC):
    def __init__(self):
        self._cfg = SpiSize()
        super().__init__()


class GeneralTab(QWidget):
    def __init__(self, config_rows):
        super().__init__()
        self.setWindowTitle('general')
        self.setFixedHeight(400)
        self.config_rows = config_rows
        self.label = QLabel('General tab to run configuration')
        self.label.setFixedHeight(20)
        self.label_cfg = QLabel()
        self.comboWidget = QTabWidget()
        self.currentCfgWidget = QTabWidget()
        self.create_compile_btn()
        self.create_regenerate()
        self.load_config_combo()
        self.current_configuration()
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.currentCfgWidget)
        vbox.addWidget(self.comboWidget)
        vbox.addWidget(self.btn_regen)
        vbox.addWidget(self.btn_cpr)
        self.setLayout(vbox)
        self.combo_signal()

    def create_regenerate(self):
        self.btn_regen = QPushButton('Regenerate', self)
        self.btn_regen.clicked.connect(self.btn_regen_clicked)

    def btn_regen_clicked(self):
        self.combo_signal()

    def create_compile_btn(self):
        self.btn_cpr = QPushButton('Compile', self)
        self.btn_cpr.clicked.connect(self.btn_compile_clicked)

    def btn_compile_clicked(self):
        cpr = Compiler()
        cpr.run(
            boot_input=self.config_rows[0][0],
            bin_input=self.config_rows[1][0],
            speed_input=self.config_rows[2][0],
            mode_input=self.config_rows[3][0],
            size_input=self.config_rows[4][0],
            load_config=self.combo_value
        )
        esp = EspTool()
        esp.run()

    def load_config_combo(self):
        vbox = QFormLayout()
        lable = QLabel('Load custom config:')
        self.combo = QComboBox()
        custom_cfgs = get_custom_configs_only()
        cfgs = [key for key in custom_cfgs.keys()]
        cfgs.insert(0, '')
        [self.combo.addItem(cfg) for cfg in cfgs]
        self.combo.currentTextChanged.connect(self.combo_signal)
        vbox.addWidget(lable)
        vbox.addWidget(self.combo)
        self.comboWidget.setFixedHeight(70)
        self.comboWidget.setLayout(vbox)

        self.combo_value = self.combo.currentText()

    def combo_signal(self):
        self.combo_value = self.combo.currentText()
        if self.combo_value:
            text = self.combo_value
        else:
            text = '\n'.join([f'{n}={v}' for v, n in self.config_rows])
        self.label_cfg.setText(f'Current configuration:\n{text}')

    def current_configuration(self):
        vbox = QFormLayout()
        vbox.addWidget(self.label_cfg)
        vbox.setVerticalSpacing(10)
        vbox.setHorizontalSpacing(10)
        self.currentCfgWidget.setFixedHeight(120)
        self.currentCfgWidget.setLayout(vbox)

    @property
    def name(self):
        return self.windowTitle()

    @property
    def load_custom_cfg(self):
        return self.combo.currentText()


class MainControllerWindow(QMainWindow):
    def __init__(self):
        super(MainControllerWindow, self).__init__()
        self.setGeometry(400, 200, 400, 600)
        self.setWindowTitle('MicroEsp8266App')
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet('font-size: 12,5pt;')
        self.cfg_tabs_obj = [BootTab(), BinTab(), SpiSpeedTab(), SpiModeTab(), SpiSizeTab()]
        self._general_tab = GeneralTab([(x.get_value, x.name) for x in self.cfg_tabs_obj])
        self.tabs.addTab(self._general_tab, self._general_tab.name)
        self.create_tabs()
        self.get_current_setup()

    def create_tabs(self):
        self.tabs.setMovable(True)
        [self.tabs.addTab(_obj, _obj.name) for i, _obj in enumerate(self.cfg_tabs_obj)]
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        self.tabs.setDocumentMode(True)
        self.setCentralWidget(self.tabs)
        self.tabs.currentChanged.connect(self.get_current_setup)

    def get_current_setup(self):
        self._general_tab.config_rows = [(x.get_value, x.name) for x in self.cfg_tabs_obj]
