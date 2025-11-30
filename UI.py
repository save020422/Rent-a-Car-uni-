import flet as ft
import Abtsration as ab

def torist_seccion(infomanager):
    tourist = ab.Tourist()
    
    # Campos de entrada estilizados
    tourist.name_ = ft.TextField(
        label="Nombre del turista",
        height=40,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )

    tourist.passport_number = ft.TextField(
        label="Número de pasaporte",
        height=40,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )

    tourist.country = ft.TextField(
        label="Nacionalidad",
        height=40,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )

    # Tabla visual
    visual_data_table = ab.ShowDataTable()
    visual_data_table.import_cincro(infomanager=infomanager)

    # Columna con scroll
    column = ft.Column(
        controls=[
            tourist.name_,
            tourist.passport_number,
            tourist.country,
            ft.ElevatedButton(
                text="Add",
                icon=ft.Icons.ADD,
                on_click=lambda _: visual_data_table.add_data(tourist, infomanager)
            ),
            visual_data_table
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll="auto",
        expand=True
    )

    # Refrescar tabla al montar
    ''' def on_column_mount(e):
            visual_data_table.import_cincro(infomanager)

        column.on_mount = on_column_mount'''

    # Envolver en fila centrada
    return ft.Tab(
        text="Users",
        icon=ft.Icons.PEOPLE,
        content=ft.Row(
            controls=[column],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )


def cars_seccion(infomanager):
    tourist = ab.Car()
    
    # Campos de entrada estilizados
    tourist.name_ = ft.TextField(
        label="Nombre del turista",
        height=40,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )

    tourist.passport_number = ft.TextField(
        label="Número de pasaporte",
        height=40,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )

    tourist.country = ft.TextField(
        label="Nacionalidad",
        height=40,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        label_style=ft.TextStyle(color=ft.Colors.WHITE)
    )

    # Tabla visual
    visual_data_table = ab.ShowDataTable()
    visual_data_table.import_cincro(infomanager=infomanager)

    # Columna con scroll
    column = ft.Column(
        controls=[
            tourist.name_,
            tourist.passport_number,
            tourist.country,
            ft.ElevatedButton(
                text="Add",
                icon=ft.Icons.ADD,
                on_click=lambda _: visual_data_table.add_data(tourist, infomanager)
            ),
            visual_data_table
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll="auto",
        expand=True
    )

    '''# Refrescar tabla al montar
    def on_column_mount(e):
        visual_data_table.import_cincro(infomanager)

    column.on_mount = on_column_mount'''

    
    return ft.Tab(
        text="Users",
        icon=ft.Icons.CAR_CRASH,
        content=ft.Row(
            controls=[column],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

