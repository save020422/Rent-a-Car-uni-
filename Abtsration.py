import flet as ft
from appstate import appState as _app


class Tourist:
    def __init__(self, name ="", passport_number = "",country = ""):
        self.name = name
        self.passport_number = passport_number
        self.country = country




class Car:
    def __init__(self, license_plate ="" , brand ="", model ="", color =" ",status=" "):
        self.license_plate = license_plate
        self.brand = brand
        self.model = model
        self.color = color
        self.kilometers_driven = 0
        self.carstatus = status





class RentalContract:
    def __init__(self, tourist, car, payment_method, start_date, end_date, extension_days, with_driver, total_amount):
        self.tourist = tourist
        self.car = car
        self.payment_method = payment_method  # 'cash', 'check', 'credit_card'
        self.start_date = start_date
        self.end_date = end_date
        self.extension_days = extension_days
        self.with_driver = with_driver
        self.total_amount = total_amount


class ContractViolator:
    def __init__(self, tourist, contract_end_date, actual_return_date):
        self.tourist = tourist
        self.contract_end_date = contract_end_date
        self.actual_return_date = actual_return_date

    def is_violation(self):
        return self.actual_return_date > self.contract_end_date
    

class InfoManager:
    def __init__(self):
        self.turistas = []
        self.autos = []
        self.contratos = []
        
        
        pass



class ShowDataTable(ft.DataTable):
    def __init__(self, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("passport_number", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("name", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("country", color=ft.Colors.WHITE))
        ]

        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY),
            border_radius=_app.app_state.border,
            vertical_lines= ft.border.BorderSide(1, ft.Colors.GREY),
            #data_row_color={"even": ft.Colors.BLUE_50, "odd": ft.Colors.WHITE},
            divider_thickness=1,
            column_spacing=20,
            #heading_row_color=ft.Colors.BLUE_200,
            **kwargs
        )

        #self.width = 10 # Limita el ancho de la tabla
        #self.bgcolor = ft.Colors.BLUE_100

    def add_data(self, entidad,infomanager = ""):
    # Asegúrate de que 'entidad' tenga los atributos necesarios
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(entidad.passport_number.value,color=ft.Colors.WHITE)),
                ft.DataCell(ft.Text(entidad.name_.value,color=ft.Colors.WHITE)),
                ft.DataCell(ft.Text(entidad.country.value,color=ft.Colors.WHITE))
            ]
        )
        tourits = Tourist(name=entidad.name_.value,
                          passport_number=entidad.passport_number.value,
                          country=entidad.country.value)
                          
        
        entidad.passport_number.value = entidad.name_.value =  entidad.country.value = ""
        entidad.name_.update()
        entidad.passport_number.update()
        entidad.country.update()

        infomanager.turistas.append(tourits)
        


        
        self.rows.append(new_row)
        self.update()
    
    def import_cincro(self, infomanager):
        for turista in infomanager.turistas:
            new_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(turista.passport_number, color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(turista.name, color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(turista.country, color=ft.Colors.WHITE))
                ]
            )
            self.rows.append(new_row)
        #self.update()


        

import flet as ft

class Formulary(ft.Container):
    def __init__(self):
        # Controles del formulario (inicialmente ocultos)
        self.name_field = ft.TextField(label="Nombre", dense=True, content_padding=5)
        self.passport_field = ft.TextField(label="Pasaporte", dense=True, content_padding=5)
        self.driver_switch = ft.Switch(label="Con conductor", value=False)
        self.select_country_button = ft.TextButton("Seleccionar país")
        self.select_car_button = ft.TextButton("Seleccionar auto")

        # Columna con el contenido del formulario
        self.form_column = ft.Column(
            controls=[
                self.name_field,
                self.passport_field,
                self.driver_switch,
                ft.Row(
                    controls=[self.select_country_button, self.select_car_button],
                    spacing=8
                )
            ],
            spacing=10,
            visible=False  # Inicia oculto
        )

        # Botón horizontal (en la parte superior)
        self.toggle_button = ft.TextButton(
            "▼ Reservar",
            on_click=self._toggle_form
        )

        # Contenido principal del Container: botón + formulario (oculto al inicio)
        main_content = ft.Column(
            controls=[
                self.toggle_button,
                self.form_column
            ],
            spacing=0
        )

        # Inicializar el Container
        super().__init__(
            content=main_content,
            padding=0,
            border=None,  # Sin borde al inicio (solo aparece cuando está desplegado)
            border_radius=8,
            expand=False
        )

    def _toggle_form(self, e):
        # Alternar visibilidad
        self.form_column.visible = not self.form_column.visible

        # Actualizar texto del botón
        if self.form_column.visible:
            self.toggle_button.text = "▲ Ocultar"
            self.border = ft.border.all(1, ft.Colors.GREY_400)
            self.padding = 12
        else:
            self.toggle_button.text = "▼ Reservar"
            self.border = None
            self.padding = 0

        self.update()




class CountryPanel(ft.Container):
    def __init__(self):
        # Lista de países de ejemplo (puedes ampliarla)
        self.countries = [
            "Argentina", "Brasil", "Chile", "Colombia", "México",
            "Perú", "España", "Francia", "Italia", "Alemania",
            "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia"
        ]

        # Crear botones (o tarjetas) clickeables para cada país
        country_cards = []
        for country in self.countries:
            card = ft.Container(
                content=ft.Text(country, size=14, weight="bold", color=ft.Colors.WHITE),
                padding=12,
                margin=4,
                bgcolor=ft.Colors.BLUE_600,
                border_radius=8,
                alignment=ft.alignment.center,
                on_click=self._on_country_click,
                data=country  # Guardamos el nombre del país aquí
            )
            country_cards.append(card)

        # GridView para mostrar en cuadrícula
        grid = ft.GridView(
            controls=country_cards,
            max_extent=120,  # Ancho máximo por ítem
            spacing=10,
            run_spacing=10,
            padding=10,
            expand=False
        )

        # Inicializar el Container
        super().__init__(
            content=grid,
            padding=0,
            expand=False,
            bgcolor=ft.Colors.GREY_100,
            border_radius=8
        )

    def _on_country_click(self, e):
        # Imprimir el nombre del país en la consola
        country_name = e.control.data
        print(f"País seleccionado: {country_name}")
        # Puedes agregar aquí: guardar en variable, mostrar snackbar, etc.