from abc import ABC
import gradio as gr

from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem

class BaseWebTabsPanel(ABC):
    def add_tab(self, item:BaseWebTabItem):
        ...
    
    def create_panel(self)->gr.Blocks:
        ...