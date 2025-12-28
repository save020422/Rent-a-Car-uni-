import flet as ft
from datetime import date, timedelta
from dataAbstration import *

DAILY_RATE = 50.0
EXTENSION_RATE = 70.0
VALID_PAYMENT_METHODS = {"efectivo", "cheque", "tarjeta de crédito"}

COUNTRIES = [
    "Argentina", "Brasil", "Chile", "Colombia", "México",
    "Perú", "España", "Francia", "Italia", "Alemania",
    "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia",
    "India", "China", "Rusia", "Sudáfrica", "Egipto", "Portugal", "Suiza",
    "Bélgica", "Holanda", "Noruega", "Suecia", "Dinamarca", "Polonia", "Turquía"
]

SAMPLE_CARS = [
    Car("ABC123", "Toyota", "Corolla", "Rojo", "disponible"),
    Car("XYZ789", "Honda", "Civic", "Azul", "disponible"),
    Car("DEF456", "Ford", "Focus", "Blanco", "alquilado"),
    Car("GHI012", "Volkswagen", "Golf", "Gris", "taller"),
    Car("JKL345", "BMW", "Serie 3", "Negro", "disponible"),
    Car("MNO678", "Mercedes", "C-Class", "Plateado", "alquilado"),
    Car("PQR901", "Audi", "A4", "Rojo", "disponible"),
    Car("STU234", "Hyundai", "Elantra", "Azul", "taller"),
    Car("VWX567", "Nissan", "Sentra", "Blanco", "disponible"),
    Car("YZA890", "Chevrolet", "Cruze", "Gris", "disponible"),
    Car("BCD123", "Kia", "Forte", "Negro", "alquilado"),
    Car("EFG456", "Mazda", "3", "Rojo", "disponible"),
    Car("HIJ789", "Tesla", "Model 3", "Blanco", "taller"),
    Car("KLM012", "Subaru", "Impreza", "Azul", "disponible"),
    Car("NOP345", "Renault", "Megane", "Gris", "alquilado"),
    Car("QRS678", "Peugeot", "308", "Negro", "disponible"),
    Car("TUV901", "Fiat", "Tipo", "Blanco", "taller"),
    Car("WXY234", "Suzuki", "Swift", "Rojo", "disponible"),
    Car("ZAB567", "Toyota", "Yaris", "Azul", "alquilado"),
    Car("CDE890", "Volkswagen", "Polo", "Gris", "disponible"),
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

contracts = []

def print_all_contracts():
    print("\n" + "="*60)
    print(f"📋 LISTA ACTUAL DE CONTRATOS ({len(contracts)} en total)")
    print("="*60)
    if not contracts:
        print("  (No hay contratos registrados)")
    else:
        for i, c in enumerate(contracts, 1):
            resumen = f"#{i}: [{c.tourist.name}] - {c.car.plate} - ${c.total_amount:.2f}"
            if c.extension_days > 0:
                resumen += f" (Prórroga: {c.extension_days}d)"
            print(f"  {resumen}")
    print("="*60 + "\n")


class SelectablePanel(ft.Container):
    def __init__(self, items, input_field=None, on_select=None, search_label="Buscar", item_color=None):
        super().__init__()
        self.input = input_field
        self.on_select = on_select
        self.all_items = items
        self.default_item_color = item_color

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
            filtered = [item for item in self.all_items if query in str(item).lower()]
        else:
            filtered = self.all_items.copy()

        cards = []
        for item in filtered:
            display_text = str(item)
            if hasattr(item, 'get_status_color'):
                bg_color = item.get_status_color()
            else:
                bg_color = self.default_item_color or ft.Colors.BLUE_700

            cards.append(
                ft.Container(
                    content=ft.Text(display_text, size=13, weight="bold", color=ft.Colors.WHITE),
                    padding=10,
                    margin=ft.margin.only(left=2, right=2),
                    bgcolor=bg_color,
                    border_radius=6,
                    alignment=ft.alignment.center,
                    on_click=self._on_item_click,
                    data=item,
                    tooltip=f"{display_text} ({item.status})" if hasattr(item, 'status') else display_text
                )
            )
        self.grid_view.controls = cards
        if self.visible and self.page:
            self.update()

    def _on_item_click(self, e):
        selected = e.control.data
        if self.input is not None:
            self.input.value = str(selected)
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
            items=SAMPLE_CARS,
            input_field=input_field,
            on_select=on_select,
            search_label="Buscar auto",
            item_color=None
        )


class InfoTable(ft.DataTable):
    def __init__(self, tourists=None, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Nombre", weight="bold")),
            ft.DataColumn(ft.Text("Pasaporte", weight="bold")),
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
                ft.DataCell(ft.Text(name, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(passport, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(country, color=ft.Colors.BLACK))
            ]
        )
        self.rows.append(new_row)


class ContractsTable(ft.DataTable):
    def __init__(self, contracts=None, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Turista", weight="bold")),
            ft.DataColumn(ft.Text("Auto", weight="bold")),
            ft.DataColumn(ft.Text("Marca", weight="bold")),
            ft.DataColumn(ft.Text("Modelo", weight="bold")),
            ft.DataColumn(ft.Text("Pago", weight="bold")),
            ft.DataColumn(ft.Text("Inicio", weight="bold")),
            ft.DataColumn(ft.Text("Fin", weight="bold")),
            ft.DataColumn(ft.Text("Prórroga", weight="bold")),
            ft.DataColumn(ft.Text("Chofer", weight="bold")),
            ft.DataColumn(ft.Text("Total", weight="bold")),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY),
            border_radius=15,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            divider_thickness=0,
            column_spacing=10,
            **kwargs
        )

        if contracts:
            for c in contracts:
                self.add_contract(c)

    def add_contract(self, contract):
        chofer = "Sí" if contract.with_driver else "No"
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(contract.tourist.name, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(contract.car.plate, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(contract.car.brand, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(contract.car.model, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(contract.payment_method, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(str(contract.start_date), color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(str(contract.end_date), color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(str(contract.extension_days), color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(chofer, color=ft.Colors.BLACK)),
                ft.DataCell(ft.Text(f"${contract.total_amount:.2f}", color=ft.Colors.BLACK)),
            ]
        )
        self.rows.append(row)


class BrandModelReportTable(ft.DataTable):
    def __init__(self, contracts, cars, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Marca", weight="bold")),
            ft.DataColumn(ft.Text("Modelo", weight="bold")),
            ft.DataColumn(ft.Text("Autos", weight="bold", text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Días", weight="bold", text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Efectivo", weight="bold", text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Cheque", weight="bold", text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Tarjeta", weight="bold", text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Total", weight="bold", text_align=ft.TextAlign.RIGHT)),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY),
            border_radius=15,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            divider_thickness=0,
            column_spacing=10,
            **kwargs
        )
        self.populate(contracts, cars)

    def populate(self, contracts, cars):
        from collections import defaultdict

        by_brand_model = defaultdict(list)
        for c in contracts:
            key = (c.car.brand, c.car.model)
            by_brand_model[key].append(c)

        car_count = defaultdict(int)
        for car in cars:
            car_count[(car.brand, car.model)] += 1

        total_general = 0.0

        for (brand, model), contract_list in sorted(by_brand_model.items()):
            dias = sum((c.end_date - c.start_date).days + 1 for c in contract_list)
            count = car_count.get((brand, model), 0)
            
            efectivo = sum(c.total_amount for c in contract_list if c.payment_method == "efectivo")
            cheque = sum(c.total_amount for c in contract_list if c.payment_method == "cheque")
            tarjeta = sum(c.total_amount for c in contract_list if c.payment_method == "tarjeta de crédito")
            subtotal = efectivo + cheque + tarjeta
            total_general += subtotal

            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(brand, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(model, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(str(count), color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(str(dias), color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${efectivo:.2f}", color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${cheque:.2f}", color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${tarjeta:.2f}", color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${subtotal:.2f}", color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                    ]
                )
            )

        # ✅ TOTAL GENERAL sin column_span
        self.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("TOTAL GENERAL", weight="bold", color=ft.Colors.BLUE_800)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text(f"${total_general:.2f}", weight="bold", color=ft.Colors.BLUE_800, text_align=ft.TextAlign.RIGHT)),
                ]
            )
        )


class Formulary(ft.Container):
    def __init__(self, page, info_table, contracts_table):
        self.page = page
        self.info_table = info_table
        self.contracts_table = contracts_table
        self.is_country_panel_open = False
        self.is_car_panel_open = False
        self.selected_car = None

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
        
        self.rental_days_field = ft.TextField(
            label="Días de contrato",
            dense=True,
            content_padding=5,
            input_filter=ft.NumbersOnlyInputFilter(),
            hint_text="Ej: 5"
        )
        self.extension_field = ft.TextField(
            label="Prórroga (días)",
            dense=True,
            content_padding=5,
            input_filter=ft.NumbersOnlyInputFilter(),
            hint_text="0 si no aplica"
        )
        self.payment_dropdown = ft.Dropdown(
            label="Forma de pago",
            dense=True,
            options=[
                ft.dropdown.Option("efectivo"),
                ft.dropdown.Option("cheque"),
                ft.dropdown.Option("tarjeta de crédito")
            ],
            value="efectivo"
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

        def on_car_select(car):
            if car.status != "disponible":
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"❌ El auto {car} no está disponible ({car.status})"),
                    bgcolor=ft.Colors.RED_200
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            self.selected_car = car

        self.country_panel = CountryPanel(input_field=self.country_input)
        self.car_panel = CarPanel(input_field=self.car_input, on_select=on_car_select)

        self.form_column = ft.Column(
            controls=[
                self.name_field,
                self.passport_field,
                self.country_input,
                self.car_input,
                self.rental_days_field,
                self.extension_field,
                self.payment_dropdown,
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
        car_obj = self.selected_car
        with_driver = self.driver_switch.value

        if not name or not passport or not country:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("❌ Faltan campos obligatorios"),
                bgcolor=ft.Colors.RED_200
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not car_obj:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("❌ Debes seleccionar un auto"),
                bgcolor=ft.Colors.RED_200
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if car_obj.status != "disponible":
            self.page.snack_bar = ft.SnackBar(
                ft.Text("❌ Auto no disponible para alquilar"),
                bgcolor=ft.Colors.RED_200
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        rental_days_str = self.rental_days_field.value or "1"
        extension_str = self.extension_field.value or "0"
        payment_method = self.payment_dropdown.value

        try:
            rental_days = int(rental_days_str)
            if rental_days <= 0:
                rental_days = 1
        except ValueError:
            rental_days = 1

        try:
            extension_days = int(extension_str)
            if extension_days < 0:
                extension_days = 0
        except ValueError:
            extension_days = 0

        start_date = date.today()
        end_date = start_date + timedelta(days=rental_days - 1)

        tourist = Tourist(name, passport, country)
        try:
            contract = RentalContract(
                tourist=tourist,
                car=car_obj,
                start_date=start_date,
                end_date=end_date,
                extension_days=extension_days,
                with_driver=with_driver,
                payment_method=payment_method
            )

            contract.print_all_attributes()

            contracts.append(contract)
            print_all_contracts()

            self.info_table.add_tourist(name=name, passport=passport, country=country)
            self.contracts_table.add_contract(contract)
            self.page.update()

            self.name_field.value = ""
            self.passport_field.value = ""
            self.country_input.value = ""
            self.rental_days_field.value = ""
            self.extension_field.value = ""
            self.selected_car = None
            for field in [self.name_field, self.passport_field, self.country_input,
                         self.rental_days_field, self.extension_field]:
                field.update()

        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"❌ Error: {str(ex)}"),
                bgcolor=ft.Colors.RED_200
            )
            self.page.snack_bar.open = True
            self.page.update()


def main(page: ft.Page):
    page.title = "Formulario con Países y Autos"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = ft.AppBar(
        title=ft.Text("Rent a Car - Control de Alquiler"),
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        center_title=True,
        elevation=0
    )

    info_table = InfoTable(tourists=SAMPLE_TOURISTS)
    contracts_table = ContractsTable()
    brand_model_table = BrandModelReportTable(contracts=contracts, cars=SAMPLE_CARS)

    # ✅ Scroll en cada pestaña
    turistas_scroll = ft.Column(
        controls=[info_table],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    contratos_scroll = ft.Column(
        controls=[contracts_table],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    marca_modelo_scroll = ft.Column(
        controls=[brand_model_table],  # ← CORRECTO: sin tilde
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Turistas",
                content=ft.Container(
                    content=turistas_scroll,
                    padding=10,
                    expand=True,
                ),
            ),
            ft.Tab(
                text="Contratos",
                content=ft.Container(
                    content=contratos_scroll,
                    padding=10,
                    expand=True,
                ),
            ),
            ft.Tab(
                text="Marca/Modelo",
                content=ft.Container(
                    content=marca_modelo_scroll,
                    padding=10,
                    expand=True,
                ),
            ),
        ],
        expand=True,
    )#ASA

    form = Formulary(page=page, info_table=info_table, contracts_table=contracts_table)

    layout = ft.Row(
        controls=[form, tabs],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)