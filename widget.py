import flet as ft


class Formulary(ft.Container):
    def __init__(self, country_panel=None):
        self.country_panel = country_panel
        self.selected_country = ""

        self.name_field = ft.TextField(label="Nombre", dense=True, content_padding=5)
        self.passport_field = ft.TextField(label="Pasaporte", dense=True, content_padding=5)
        self.driver_switch = ft.Switch(label="Con conductor", value=False)

        self.add = ft.TextButton(
            "Add",
            on_click=lambda e: self.formulary_set(e),
        )

        self.select_country_button = ft.TextButton(
            "Seleccionar país",
            on_click=lambda e: self._show_country_panel(e)
        )
        self.select_car_button = ft.TextButton("Seleccionar auto")

        self.form_column = ft.Column(
            controls=[
                self.name_field,
                self.passport_field,
                self.driver_switch,
                self.select_country_button,
                self.select_car_button,
                self.add
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO  # ← permite scroll si el contenido sobrepasa 700px
        )

       
        super().__init__(
            content=self.form_column,
            padding=12,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8,
            height=700,       
            expand=False      
        )

        if self.country_panel is not None:
            self.country_panel.on_select = self._on_country_selected

    def _show_country_panel(self, e):
        if self.country_panel is not None and self.page is not None:
            if self.country_panel not in self.page.controls:
                self.page.add(self.country_panel)
            else:
                self.country_panel.visible = True
                self.page.update()

    def _on_country_selected(self, country_name: str):
        self.selected_country = country_name
        self.select_country_button.text = f"País: {country_name}"
        self.update()
        if self.country_panel is not None and self.page is not None:
            if self.country_panel in self.page.controls:
                self.page.controls.remove(self.country_panel)
                self.page.update()


    def formulary_set(self, e):
        name = self.name_field.value or ""
        passport = self.passport_field.value or ""
        country = self.selected_country
        with_driver = self.driver_switch.value

        print(f"Guardando: {name}, {passport}, {country}, con conductor: {with_driver}")

class CountryPanel(ft.Container):
    def __init__(self, on_select=None):
        self.on_select = on_select
        self.countries = [
            "Argentina", "Brasil", "Chile", "Colombia", "México",
            "Perú", "España", "Francia", "Italia", "Alemania",
            "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia"
        ]

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
                data=country
            )
            country_cards.append(card)

        grid = ft.GridView(
            controls=country_cards,
            max_extent=120,
            spacing=10,
            run_spacing=10,
            padding=10,
            height=220
        )

        super().__init__(
            content=grid,
            padding=10,
            bgcolor=ft.Colors.GREY_100,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8,
            visible=False  # Empieza oculto
        )

    def _on_country_click(self, e):
        country_name = e.control.data
        print(f"✅ País seleccionado: {country_name}")
        if self.on_select:
            self.on_select(country_name)
        self.visible = False
        if self.page:
            self.page.update()




