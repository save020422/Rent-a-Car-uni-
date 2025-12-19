
from importAll import *


def main(page: ft.Page):
    page.title = "Sistema de Alquiler de Autos"
    page.bgcolor = ft.Colors.WHITE
    country_panel = CountryPanel()
    user_data = InfoManager()
    
    formulari = Formulary( country_panel= CountryPanel)
    users_tab = torist_seccion(infomanager=user_data )

    
    page.add(ft.Row( controls= [formulari]))
    page.update()

ft.app(target=main)
