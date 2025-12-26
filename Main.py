
from importAll import *


def main(page: ft.Page):
    
    page.title = "Formulario con Países y Autos"
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = ft.AppBar(
        title=ft.Text("Rent a Car - Control de Alquiler"),
        bgcolor=ft.Colors.BLACK,
        color=ft.Colors.WHITE,
        center_title=True,
        elevation=0
    )
    
    page.add(UI.layout(page))
    page.update()

ft.app(target=main)
