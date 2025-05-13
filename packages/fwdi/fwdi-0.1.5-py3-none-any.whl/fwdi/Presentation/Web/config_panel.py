import logging
import gradio as gr
import pandas as pd

from ...Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI

from ...Utilites.ext_global_setting import ExtGlobalSetting
from ...Utilites.ext_dict import ExtDict
from ...Domain.Configure.global_setting_service import GlobalSettingService
from ...Application.Abstractions.base_panel import BaseWebPage

class ConfigPanel(BaseWebPage):
    def __init__(self):
        super().__init__()
        self.__config_page = gr.Blocks()
        self.__lvl_log:list[str] = ["INFO",
                                    "DEBUG",
                                    "ERROR",
                                    "WARNING",
                                    "CRITICAL"]
    def _get_all_users(self, 
                       user_repository:BaseUserRepositoryFWDI)->list[dict]:
        users = user_repository.get_all()

        return users

    def __load_users(self)->pd.DataFrame:
        users = self._get_all_users()
        df = pd.DataFrame(users)
        
        return gr.Dataframe(df, label='Elastic config:', show_row_numbers=True)
    
    def __save_users(self, data:gr.Dataframe)->bool:
        return f"Users save."

    def __save(self, 
               tb_name:str,
               tb_description:str,
               dd_log_lvl:str,
               cb_log_to_elastic:bool,
               cb_log_split_by_name:bool,
               data_elastic_log_conf:pd.DataFrame,
               cb_log_to_console:bool,
               cb_log_to_file:bool,
               tb_queue_name:str,
               data_broker_conf:pd.DataFrame,
               cb_to_zipkin:bool,
               data_zipkin_conf:pd.DataFrame):
        
        GlobalSettingService.name = tb_name
        GlobalSettingService.description = tb_description
        GlobalSettingService.log_lvl = logging._nameToLevel[dd_log_lvl]
        GlobalSettingService.log_to_elastic = cb_log_to_elastic
        GlobalSettingService.log_split_by_name = cb_log_split_by_name
        GlobalSettingService.elastic_log_conf = data_elastic_log_conf.to_dict('records')[0]
        GlobalSettingService.log_to_console = cb_log_to_console
        GlobalSettingService.log_to_file = cb_log_to_file
        GlobalSettingService.queue_name = tb_queue_name
        GlobalSettingService.broker_conf = data_broker_conf.to_dict('records')[0]
        GlobalSettingService.to_zipkin = cb_to_zipkin
        GlobalSettingService.zipkin_conf = data_zipkin_conf.to_dict('records')[0]

        if ExtGlobalSetting.save(GlobalSettingService):
            return f"Save setting to file."
        else:
            return f"Error saving setting file."

    def __load(self):
        tb_name = GlobalSettingService.name
        tb_description = GlobalSettingService.description
        dd_log_lvl = logging._levelToName[GlobalSettingService.log_lvl]
        cb_log_to_elastic = GlobalSettingService.log_to_elastic
        cb_log_split_by_name = GlobalSettingService.log_split_by_name
        data_elastic_log_conf = gr.Dataframe(ExtDict.to_pandas(GlobalSettingService.elastic_log_conf), label='Elastic config:', show_row_numbers=True)
        cb_log_to_console = GlobalSettingService.log_to_console
        cb_log_to_file = GlobalSettingService.log_to_file
        tb_queue_name = GlobalSettingService.queue_name
        data_broker_conf = gr.Dataframe(ExtDict.to_pandas(GlobalSettingService.broker_conf), label='Broker config:', show_row_numbers=True)
        cb_to_zipkin = GlobalSettingService.to_zipkin
        data_zipkin_conf = gr.Dataframe(ExtDict.to_pandas(GlobalSettingService.zipkin_conf), label='Zipkin config:', show_row_numbers=True)

        return tb_name, tb_description, dd_log_lvl, cb_log_to_elastic, cb_log_split_by_name, cb_log_to_console, cb_log_to_file, tb_queue_name, cb_to_zipkin, data_elastic_log_conf, data_broker_conf, data_zipkin_conf
    
    def create_panel(self)->gr.Blocks:
        
        with self.__config_page:
            head_footer = gr.Markdown(value="User not logged in")
            gr.Markdown("""
                        # Config Service Page
                        """)
            with gr.Row():
                with gr.Column():
                    tb_name = gr.Textbox(label='Name service:')
                    tb_description = gr.Textbox(label='Description service:')
                    dd_log_lvl = gr.Dropdown(choices=self.__lvl_log, label='Login level:')
                    cb_log_to_elastic = gr.Checkbox(label='Enable elastic:')
                    cb_log_split_by_name = gr.Checkbox(label='Login file split by name:')
                    data_elastic_log_conf = gr.Dataframe(label='Elastic login config:')
                    cb_log_to_console = gr.Checkbox(label='Login to console:')
                    cb_log_to_file = gr.Checkbox(label='Login to file:')
                    tb_queue_name = gr.Textbox(label='Queue name:')
                    data_broker_conf = gr.Dataframe(label='Broker config:')
                    cb_to_zipkin = gr.Checkbox(label='Enable zipkin service:')
                    data_zipkin_conf = gr.Dataframe(label='Zipkin config:')

                    bt_save = gr.Button(value='Save')
                
                with gr.Column():
                    data_users = gr.Dataframe(label='Users:', show_row_numbers=True)

                    with gr.Column():
                        bt_users_add = gr.Button(value='Add')
                    with gr.Column():
                        bt_users_del = gr.Button(value='Del')
                    with gr.Column():
                        bt_users_save = gr.Button(value='Save')
                
                with gr.Column():
                    lb_save = gr.Label()
            
            bt_users_save.click(self.__save_users, inputs=[data_users], outputs=[lb_save])
            bt_save.click(self.__save, inputs=[tb_name, 
                                               tb_description, 
                                               dd_log_lvl, 
                                               cb_log_to_elastic,
                                               cb_log_split_by_name,
                                               data_elastic_log_conf,
                                               cb_log_to_console,
                                               cb_log_to_file,
                                               tb_queue_name,
                                               data_broker_conf,
                                               cb_to_zipkin,
                                               data_zipkin_conf], outputs=[lb_save])

            self.__config_page.load(self.__load_users, None, data_users)
            self.__config_page.load(self._session.get_user, None, head_footer)
            self.__config_page.load(self.__load, outputs=[tb_name, 
                                                tb_description, 
                                                dd_log_lvl, 
                                                cb_log_to_elastic,
                                                cb_log_split_by_name,
                                                cb_log_to_console,
                                                cb_log_to_file,
                                                tb_queue_name,
                                                cb_to_zipkin,
                                                data_elastic_log_conf,
                                                data_broker_conf,
                                                data_zipkin_conf])

        return self.__config_page