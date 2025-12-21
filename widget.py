import flet as ft

# ───────────────
# Clase Tourist
# ───────────────
class Tourist:
    def __init__(self, name: str, passport_number: str, country: str):
        self.name = name
        self.passport_number = passport_number
        self.country = country


# ───────────────
# Datos de ejemplo
# ───────────────
COUNTRIES = [
    "Argentina", "Brasil", "Chile", "Colombia", "México",
    "Perú", "España", "Francia", "Italia", "Alemania",
    "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia",
    "India", "China", "Rusia", "Sudáfrica", "Egipto", "Portugal", "Suiza",
    "Bélgica", "Holanda", "Noruega", "Suecia", "Dinamarca", "Polonia", "Turquía"
]

CARS = [
    "Toyota Corolla", "Honda Civic", "Ford Focus", "Volkswagen Golf",
    "BMW Serie 3", "Mercedes C-Class", "Audi A4", "Hyundai Elantra",
    "Nissan Sentra", "Chevrolet Cruze", "Kia Forte", "Mazda 3",
    "Tesla Model 3", "Subaru Impreza", "Renault Megane", "Peugeot 308",
    "Fiat Tipo", "Suzuki Swift", "Toyota Yaris", "Volkswagen Polo"
]

SAMPLE_TOURISTS = [
    Tourist("Ana López", "ES123456", "España"),
    Tourist("Carlos Mendoza", "MX789012", "México"),
    Tourist("Sophie Dubois", "FR345678", "Francia"),
    Tourist("Hiroshi Tanaka", "JP901234", "Japón"),
    Tourist("Liam O'Connor", "IE567890", "Irlanda"),
    Tourist("Amina Nkosi", "ZA234567", "Sudáfrica"),
    Tourist("Raj Patel", "IN890123", "India"),
    Tourist("Emma Johansson", "SE456789", "Suecia"),
    Tourist("Luca Rossi", "IT012345", "Italia"),
    Tourist("Yara Silva", "BR678901", "Brasil"),
    Tourist("Mohamed Al-Fayed", "EG234567", "Egipto"),
    Tourist("Chen Wei", "CN890123", "China"),
    Tourist("Olga Petrova", "RU456789", "Rusia"),
    Tourist("Fatima Benali", "MA012345", "Marruecos"),
    Tourist("James Wilson", "US678901", "Estados Unidos"),
    Tourist("Lars Andersen", "DK234567", "Dinamarca"),
    Tourist("Ingrid Müller", "DE890123", "Alemania"),
    Tourist("Nina Kowalski", "PL456789", "Polonia"),
    Tourist("Ahmet Yılmaz", "TR012345", "Turquía"),
    Tourist("Sven Eriksson", "NO678901", "Noruega"),
]


class SelectablePanel(ft.Container):
    def __init__(self, items, input_field=None, on_select=None, search_label="Buscar", item_color=ft.Colors.BLUE_700):
        super().__init__()
        self.input = input_field
        self.on_select = on_select
        self.all_items = items
        self.item_color = item_color

        self.search_field = ft.TextField(
            label=search_label,
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

        content = ft.Column(
            controls=[self.search_field, self.grid_view],
            spacing=10,
            tight=True
        )

        self.content = content
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
            filtered = [item for item in self.all_items if query in item.lower()]
        else:
            filtered = self.all_items.copy()

        cards = []
        for item in filtered:
            cards.append(
                ft.Container(
                    content=ft.Text(item, size=13, weight="bold", color=ft.Colors.WHITE),
                    padding=10,
                    margin=ft.margin.only(left=2, right=2),
                    bgcolor=self.item_color,
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
        selected = e.control.data
        if self.input is not None:
            self.input.value = selected
            self.input.update()
        if self.on_select:
            self.on_select(selected)


class CountryPanel(SelectablePanel):
    def __init__(self, input_field=None, on_select=None):
        super().__init__(
            items=COUNTRIES,
            input_field=input_field,
            on_select=on_select,
            search_label="Buscar país",
            item_color=ft.Colors.BLUE_700
        )


class CarPanel(SelectablePanel):
    def __init__(self, input_field=None, on_select=None):
        super().__init__(
            items=CARS,
            input_field=input_field,
            on_select=on_select,
            search_label="Buscar auto",
            item_color=ft.Colors.GREEN_700
        )


class InfoTable(ft.DataTable):
    def __init__(self, tourists=None, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Pasaporte", weight="bold")),
            ft.DataColumn(ft.Text("Nombre", weight="bold")),
            ft.DataColumn(ft.Text("País", weight="bold"))
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY),
            border_radius=15,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            divider_thickness=0,
            column_spacing=20,
            **kwargs
        )

        if tourists:
            for t in tourists:
                self.add_tourist(t.name, t.passport_number, t.country)

    def add_tourist(self, name: str, passport: str, country: str):
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(passport, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(name, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(country, color=ft.Colors.BLACK))
            ]
        )
        self.rows.append(new_row)


class Formulary(ft.Container):
    def __init__(self, page, info_table):
        self.page = page
        self.info_table = info_table
        self.is_country_panel_open = False
        self.is_car_panel_open = False

        self.name_field = ft.TextField(label="Nombre", dense=True, content_padding=5)
        self.passport_field = ft.TextField(label="Pasaporte", dense=True, content_padding=5)
        self.country_input = ft.TextField(
            label="País", dense=True, content_padding=5,
            read_only=True, bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK, border_color=ft.Colors.GREY_500
        )
        self.car_input = ft.TextField(
            label="Auto", dense=True, content_padding=5,
            read_only=True, bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK, border_color=ft.Colors.GREY_500
        )
        self.driver_switch = ft.Switch(label="Con conductor", value=False)

        self.add_btn = ft.Container(
            content=ft.ElevatedButton(
                "Add",
                on_click=lambda e: self.formulary_set(e),
                height=36,
                width=100
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=8)
        )

        self.select_country_btn = ft.TextButton("Seleccionar país", on_click=lambda e: self._toggle_country_panel(e))
        self.select_car_btn = ft.TextButton("Seleccionar auto", on_click=lambda e: self._toggle_car_panel(e))

        self.country_panel = CountryPanel(input_field=self.country_input)
        self.car_panel = CarPanel(input_field=self.car_input)

        self.form_column = ft.Column(
            controls=[
                self.name_field,
                self.passport_field,
                self.country_input,
                self.car_input,
                self.driver_switch,
                self.select_country_btn,
                self.country_panel,
                self.select_car_btn,
                self.car_panel,
                self.add_btn
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            tight=True
        )

        super().__init__(
            content=self.form_column,
            padding=14,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=12,
            height=800,
            width=280,
            expand=False
        )

    def _toggle_country_panel(self, e):
        self.is_country_panel_open = not self.is_country_panel_open
        self.country_panel.visible = self.is_country_panel_open

        if self.is_country_panel_open:
            self.width = 460
            self.select_country_btn.text = "▲ Ocultar países"
            self.country_panel.search_field.focus()
        else:
            self.width = 280
            self.select_country_btn.text = "Seleccionar país"
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
            self.select_car_btn.text = "▲ Ocultar autos"
            self.car_panel.search_field.focus()
        else:
            self.width = 280
            self.select_car_btn.text = "Seleccionar auto"
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

        if not name or not passport or not country:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("❌ Faltan campos obligatorios"),
                bgcolor=ft.Colors.RED_200
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.info_table.add_tourist(name=name, passport=passport, country=country)
        self.info_table.page.update()

        self.name_field.value = ""
        self.passport_field.value = ""
        self.country_input.value = ""
        self.name_field.update()
        self.passport_field.update()
        self.country_input.update()

        print(f"✅ Guardando: {name}, {passport}, {country}, {car}, con conductor: {with_driver}")


def main(page: ft.Page):
    page.title = "Formulario con Países y Autos"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = ft.AppBar(
        title=ft.Text("Rent a Car - Control de Alquiler"),
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        center_title=True,
        elevation=0
    )

    info_table = InfoTable(tourists=SAMPLE_TOURISTS)

    table_container = ft.Container(
        content=ft.Column(
            controls=[info_table],
            scroll=ft.ScrollMode.AUTO,
            height=750,
        ),
        height=800,
        expand=False,
        bgcolor=ft.Colors.WHITE,
        padding=ft.padding.all(0),
    )

    form = Formulary(page=page, info_table=info_table)

    layout = ft.Row(
        controls=[form, table_container],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=False
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)