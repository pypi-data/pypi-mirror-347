import gradio as gr
import pandas as pd

from ...Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI
from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem

class RightsManagementPanel(BaseWebTabItem):
    def __init__(self, name):
        super().__init__(name)

    def _get_all_users(self, 
                       user_repository:BaseUserRepositoryFWDI)->list[dict]:
        users = user_repository.get_all()

        return users

    def __load_users(self)->pd.DataFrame:
        users = self._get_all_users()
        df = pd.DataFrame(users)
        
        return gr.Dataframe(df, label='Elastic config:', show_row_numbers=True)

    def __save_users(self, data:gr.Dataframe)->bool:
        return f"# Users save."
    
    def create_gui_tab(self)->gr.Blocks:

        with self.tab_blocks:
            with gr.Row():
                head_footer = gr.Markdown(value="User not logged in")
                md_status = gr.Markdown(value="...")

            gr.Markdown("""
                        # Управление правами.
                        """)
            with gr.Row():
                with gr.Column(variant='compact'):
                    data_users = gr.Dataframe(label='Users:', show_row_numbers=True)

                    with gr.Row():
                        bt_users_add = gr.Button(value='Add')
                        bt_users_del = gr.Button(value='Del')
                    bt_users_save = gr.Button(value='Save')
            
            bt_users_save.click(self.__save_users, inputs=[data_users], outputs=[md_status])

            self.tab_blocks.load(self.__load_users, None, data_users)
            self.tab_blocks.load(self._session.get_user, None, head_footer)