import flet as ft
from ui import *
from Abtsration import InfoManager, Tourist ,Formulary
from  system_of_the_db import const 


def main(page: ft.Page):
    page.title = "Sistema de Alquiler de Autos"
    page.bgcolor = ft.Colors.WHITE

    user_data = InfoManager()
    #const.init()
    #bd.TouristBD.insertar_turistas_demo()
    #bd.TouristBD.cargar_turistas(user_data.turistas)

    formulari = Formulary()

    
    users_tab = torist_seccion(infomanager=user_data )

    # Obtener la tabla desde el contenido de la pestaña
    #visual_data_table = users_tab.content.controls[-1]

    # Agregar Tabs a la página 
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[users_tab],
        expand=1
    )
    page.add(ft.Row( controls= [formulari]))
    page.update()

    #page_init[0] = True
    # Ejecutar import_cincro cuando la página termine de cargar
    

ft.app(target=main)
