from abc import ABC, abstractmethod
import gradio as gr

from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem

class BaseWebTabsPanel(ABC):

    @abstractmethod
    def add_tab(self, item:BaseWebTabItem):
        ...
    
    @abstractmethod
    def create_panel(self)->gr.Blocks:
        ...