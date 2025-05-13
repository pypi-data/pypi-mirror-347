from ...Application.Abstractions.base_web_tabs_panel import BaseWebTabsPanel
from ...Application.Abstractions.base_web_main_page import BaseWebMainPage
from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem
from ...Infrastructure.Web.web_tabs_panel import WebTabsPanel

class WebMainPage(BaseWebMainPage):
    def __init__(self):
        self.__panel:BaseWebTabsPanel = WebTabsPanel()
        self.__lst_page:list[BaseWebTabItem] = []

    def __create_tabs(self):
        for item in self.__lst_page:
            item.create_gui_tab()
            self.__panel.add_tab(item)

    def add_page(self, item:BaseWebTabItem):
        self.__lst_page.append(item)

    def create(self):
        self.__create_tabs()
        return self.__panel.create_panel()