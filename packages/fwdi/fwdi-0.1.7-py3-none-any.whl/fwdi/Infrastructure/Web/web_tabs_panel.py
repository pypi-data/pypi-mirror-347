import gradio as gr
from gradio.themes.base import Base
from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem
from ...Application.Abstractions.base_web_tabs_panel import BaseWebTabsPanel

class WebTabsPanel(BaseWebTabsPanel):
    def __init__(self, theme:Base=gr.themes.Glass()):
        self.__tabs:dict = {}
        self.__theme:Base = theme

    def add_tab(self, item:BaseWebTabItem):
        self.__tabs[item.Name] = item.to_tab()
    
    def create_panel(self)->gr.Blocks:
        tabs_item:list[gr.Blocks] = self.__tabs.values()
        tabs_name:list[str] = self.__tabs.keys()

        tabs = gr.TabbedInterface(tabs_item, tabs_name, theme=self.__theme)
        
        return tabs
