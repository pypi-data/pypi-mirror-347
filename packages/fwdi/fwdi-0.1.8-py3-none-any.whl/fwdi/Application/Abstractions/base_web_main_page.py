from abc import ABC, abstractmethod
from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem

class BaseWebMainPage(ABC):

    @abstractmethod
    def add_page(self, item:BaseWebTabItem):
        ...
    
    @abstractmethod
    def create(self):
        ...