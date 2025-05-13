#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from ..Presentation.Web.session_manager import SessionManager
from ..Presentation.Web.config_panel import ConfigPanel
from ..Application.Abstractions.base_http_auth import BaseHttpAuth
from ..Presentation.DefaultControllers.http_auth import HttpAuthFWDI
from ..Presentation.Web.default_page import DefaultPage
from ..WebApp.web_application import WebApplication
from .DefaultControllers.home_controller import Controller
from .DefaultControllers.token_controller import TokenController
from .DefaultControllers.health_checks_controller import HealthChecksController


class DependencyInjection():
    from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI

    def AddEndpoints(app:WebApplication)->None:
        #------------- HOME ENDPOINTS -----------------------------
        app.map_get(path="/home", endpoint=Controller().index)
        
        #-------------/HOME ENDPOINTS -----------------------------
        app.map_post(path='/token', endpoint=TokenController.post)

        #-------------/WEB PAGES ENDPOINTS-------------------------
        default_page = DefaultPage().create_panel()
        app.add_web_page(default_page, path="/default")

        config_page = ConfigPanel().create_panel()
        app.add_web_page(config_page, path="/config", is_auth=True)


    def AddHealthChecks(app:WebApplication)->None:
        app.map_get(path="/health_checks", endpoint=HealthChecksController().index)

    def AddPresentation(services:BaseServiceCollectionFWDI)->None:
        services.AddTransient(BaseHttpAuth, HttpAuthFWDI)
        services.AddSingleton(SessionManager)
        services.AddSingleton(DefaultPage)
        services.AddSingleton(ConfigPanel)