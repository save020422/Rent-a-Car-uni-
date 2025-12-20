import flet as ft

# ───────────────────────────────────────────────
# CountryPanel: selección de países
# ───────────────────────────────────────────────
class CountryPanel(ft.Container):
    def __init__(self, input=None, on_select=None):
        super().__init__()
        self.input = input
        self.on_select = on_select
        self.all_items = [
            "Argentina", "Brasil", "Chile", "Colombia", "México",
            "Perú", "España", "Francia", "Italia", "Alemania",
            "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia",
            "India", "China", "Rusia", "Sudáfrica", "Egipto", "Portugal", "Suiza",
            "Bélgica", "Holanda", "Noruega", "Suecia", "Dinamarca", "Polonia", "Turquía"
        ]

        self.search_field = ft.TextField(
            label="Buscar país",
            hint_text="Escribe para filtrar...",
            dense=True,
            content_padding=6,
            on_change=self._on_search,
            width=220
        )

        self.grid_view = ft.GridView(
            max_extent=100,
            spacing=8,
            run_spacing=8,
            padding=10,
            height=260
        )

        self._filter_and_update("")

        content_col = ft.Column(
            controls=[self.search_field, self.grid_view],
            spacing=10,
            tight=True
        )

        self.content = content_col
        self.padding = 12
        self.bgcolor = ft.Colors.GREY_50
        self.border = ft.border.all(1, ft.Colors.GREY_400)
        self.border_radius = 8
        self.visible = False

    def _on_search(self, e):
        query = e.control.value.strip().lower()
        self._filter_and_update(query)

    def _filter_and_update(self, query: str):
        if query:
            filtered = [c for c in self.all_items if query in c.lower()]
        else:
            filtered = self.all_items.copy()

        cards = []
        for item in filtered:
            cards.append(
                ft.Container(
                    content=ft.Text(item, size=13, weight="bold", color=ft.Colors.WHITE),
                    padding=10,
                    margin=ft.margin.only(left=2, right=2),
                    bgcolor=ft.Colors.BLUE_700,
                    border_radius=6,
                    alignment=ft.alignment.center,
                    on_click=self._on_item_click,
                    data=item,
                    tooltip=item
                )
            )
        self.grid_view.controls = cards
        if self.visible and self.page:
            self.update()

    def _on_item_click(self, e):
        item_name = e.control.data
        if self.input is not None:
            self.input.value = item_name
            self.input.update()
        if self.on_select:
            self.on_select(item_name)



class CarPanel(ft.Container):
    def __init__(self, input=None, on_select=None):
        super().__init__()
        self.input = input
        self.on_select = on_select
        self.all_items = [
            "Toyota Corolla", "Honda Civic", "Ford Focus", "Volkswagen Golf",
            "BMW Serie 3", "Mercedes C-Class", "Audi A4", "Hyundai Elantra",
            "Nissan Sentra", "Chevrolet Cruze", "Kia Forte", "Mazda 3",
            "Tesla Model 3", "Subaru Impreza", "Renault Megane", "Peugeot 308",
            "Fiat Tipo", "Suzuki Swift", "Toyota Yaris", "Volkswagen Polo"
        ]

        self.search_field = ft.TextField(
            label="Buscar auto",
            hint_text="Escribe para filtrar...",
            dense=True,
            content_padding=6,
            on_change=self._on_search,
            width=220
        )

        self.grid_view = ft.GridView(
            max_extent=100,
            spacing=8,
            run_spacing=8,
            padding=10,
            height=260
        )

        self._filter_and_update("")

        content_col = ft.Column(
            controls=[self.search_field, self.grid_view],
            spacing=10,
            tight=True
        )

        self.content = content_col
        self.padding = 12
        self.bgcolor = ft.Colors.GREY_50
        self.border = ft.border.all(1, ft.Colors.GREY_400)
        self.border_radius = 8
        self.visible = False

    def _on_search(self, e):
        query = e.control.value.strip().lower()
        self._filter_and_update(query)

    def _filter_and_update(self, query: str):
        if query:
            filtered = [c for c in self.all_items if query in c.lower()]
        else:
            filtered = self.all_items.copy()

        cards = []
        for item in filtered:
            cards.append(
                ft.Container(
                    content=ft.Text(item, size=13, weight="bold", color=ft.Colors.WHITE),
                    padding=10,
                    margin=ft.margin.only(left=2, right=2),
                    bgcolor=ft.Colors.GREEN_700,
                    border_radius=6,
                    alignment=ft.alignment.center,
                    on_click=self._on_item_click,
                    data=item,
                    tooltip=item
                )
            )
        self.grid_view.controls = cards
        if self.visible and self.page:
            self.update()

    def _on_item_click(self, e):
        item_name = e.control.data
        if self.input is not None:
            self.input.value = item_name
            self.input.update()
        if self.on_select:
            self.on_select(item_name)



class Formulary(ft.Container):
    def __init__(self, page):
        self.page = page
        self.is_country_panel_open = False
        self.is_car_panel_open = False
        self.name_field = ft.TextField(label="Nombre", dense=True, content_padding=5)
        self.passport_field = ft.TextField(label="Pasaporte", dense=True, content_padding=5)
        self.country_input = ft.TextField(
            label="País",
            dense=True,
            content_padding=5,
            read_only=True,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            border_color=ft.Colors.GREY_500
        )
        self.car_input = ft.TextField(
            label="Auto",
            dense=True,
            content_padding=5,
            read_only=True,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            border_color=ft.Colors.GREY_500
        )
        self.driver_switch = ft.Switch(label="Con conductor", value=False)

        self.add = ft.ElevatedButton(
            "Add",
            on_click=lambda e: self.formulary_set(e),
            height=36
        )

        self.select_country_button = ft.TextButton(
            "Seleccionar país",
            on_click=lambda e: self._toggle_country_panel(e)
        )
        self.select_car_button = ft.TextButton(
            "Seleccionar auto",
            on_click=lambda e: self._toggle_car_panel(e)
        )

        self.country_panel = CountryPanel(input=self.country_input)
        self.car_panel = CarPanel(input=self.car_input)

        self.form_column = ft.Column(
            controls=[
                self.name_field,
                self.passport_field,
                self.country_input,
                self.car_input,
                self.driver_switch,
                self.select_country_button,
                self.country_panel,
                self.select_car_button,
                self.car_panel,
                self.add
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            tight=True
        )

        super().__init__(
            content=self.form_column,
            padding=14,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            height=800,
            width=280,
            expand=False
        )

    def _toggle_country_panel(self, e):
        self.is_country_panel_open = not self.is_country_panel_open
        self.country_panel.visible = self.is_country_panel_open

        if self.is_country_panel_open:
            self.width = 460
            self.select_country_button.text = "▲ Ocultar países"
            self.country_panel.search_field.focus()
        else:
            self.width = 280
            self.select_country_button.text = "Seleccionar país"
            self.country_panel.search_field.value = ""
            self.country_panel._filter_and_update("")
            if self.page:
                self.country_panel.search_field.update()
        self.update()

    def _toggle_car_panel(self, e):
        self.is_car_panel_open = not self.is_car_panel_open
        self.car_panel.visible = self.is_car_panel_open

        if self.is_car_panel_open:
            self.width = 460
            self.select_car_button.text = "Ocultar autos"
            self.car_panel.search_field.focus()
        else:
            self.width = 280
            self.select_car_button.text = "Seleccionar auto"
            self.car_panel.search_field.value = ""
            self.car_panel._filter_and_update("")
            if self.page:
                self.car_panel.search_field.update()
        self.update()

    def formulary_set(self, e):
        name = self.name_field.value or ""
        passport = self.passport_field.value or ""
        country = self.country_input.value or ""
        car = self.car_input.value or ""
        with_driver = self.driver_switch.value
        print(f"✅ Guardando: {name}, {passport}, {country}, {car}, con conductor: {with_driver}")



class ThemeToggle(ft.IconButton):
    def __init__(self, page: ft.Page):
        self.page = page
        icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        super().__init__(
            icon=icon,
            on_click=self._toggle_theme,
            tooltip="Cambiar tema"
        )

    def _toggle_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.icon = ft.Icons.DARK_MODE
        self.page.update()



def main(page: ft.Page):
    page.title = "Formulario con Países y Autos"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # Botón de tema en la esquina superior derecha
    theme_toggle = ThemeToggle(page)
    page.appbar = ft.AppBar(
        actions=[theme_toggle],
        bgcolor=ft.Colors.WHITE,
        center_title=False
    )

    form = Formulary(page=page)
    page.add(form)


# ───────────────────────────────────────────────
if __name__ == "__main__":
    ft.app(target=main)