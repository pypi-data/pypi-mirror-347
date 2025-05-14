import gradio as gr
from abc import ABC, abstractmethod

class BaseWebTabItem(ABC):
    def __init__(self, name:str):
        from ...Presentation.Web.session_manager import SessionManager
        super().__init__()
        self.Name:str = name
        self.tab_blocks = gr.Blocks()
        self._session = SessionManager()

    @abstractmethod
    def create_gui_tab(self)->gr.Blocks:
        ...

    def to_tab(self)->gr.Blocks:
        return self.tab_blocks
