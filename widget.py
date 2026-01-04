import flet as ft
from datetime import date, timedelta
from collections import defaultdict
from init_ import *

DAILY_RATE = 50.0
EXTENSION_RATE = 70.0
VALID_PAYMENT_METHODS = {"efectivo", "cheque", "tarjeta de crédito"}

COUNTRIES = [
    "Argentina", "Brasil", "Chile", "Colombia", "México", "Perú", "España", "Francia", "Italia", "Alemania",
    "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia", "India", "China", "Rusia", "Sudáfrica",
    "Egipto", "Portugal", "Suiza", "Bélgica", "Holanda", "Noruega", "Suecia", "Dinamarca", "Polonia", "Turquía"
]

SAMPLE_CARS = [
    Car("ABC123", "Toyota", "Corolla", "Rojo", "disponible"),
    Car("XYZ789", "Honda", "Civic", "Azul", "disponible"),
    Car("DEF456", "Ford", "Focus", "Blanco", "disponible"),
    Car("GHI012", "Volkswagen", "Golf", "Gris", "disponible"),
    Car("JKL345", "BMW", "Serie 3", "Negro", "disponible"),
    Car("MNO678", "Mercedes", "C-Class", "Plateado", "disponible"),
    Car("PQR901", "Audi", "A4", "Rojo", "disponible"),
    Car("STU234", "Hyundai", "Elantra", "Azul", "disponible"),
    Car("VWX567", "Nissan", "Sentra", "Blanco", "disponible"),
    Car("YZA890", "Chevrolet", "Cruze", "Gris", "disponible"),
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
]

contracts = []


def print_all_contracts():
    print("\n" + "=" * 60)
    print(f"📋 LISTA ACTUAL DE CONTRATOS ({len(contracts)} en total)")
    print("=" * 60)
    if not contracts:
        print("  (No hay contratos registrados)")
    else:
        for i, c in enumerate(contracts, 1):
            resumen = f"#{i}: [{c.tourist.name}] - {c.car.plate} - ${c.total_amount:.2f}"
            if c.extension_days > 0:
                resumen += f" (Prórroga: {c.extension_days}d)"
            print(f"  {resumen}")
    print("=" * 60 + "\n")


def create_sample_contracts(tourists, cars, num=5):
    sample_contracts = []
    today = date.today()
    for i in range(min(num, len(tourists), len(cars))):
        if cars[i].status != "disponible":
            continue
        tourist = tourists[i]
        car = cars[i]
        start = today - timedelta(days=10)
        end = start + timedelta(days=3)
        contract = RentalContract(
            tourist=tourist,
            car=car,
            start_date=start,
            end_date=end,
            extension_days=0 if i % 3 != 0 else 2,
            with_driver=(i % 2 == 0),
            payment_method="efectivo" if i % 3 == 0 else "tarjeta de crédito",
        )
        sample_contracts.append(contract)
        car.status = "alquilado"
    return sample_contracts


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
            content_padding=8,
            border_radius=8,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_700,
            width=240,
        )

        self.grid_view = ft.GridView(max_extent=140, spacing=8, run_spacing=8, padding=10, height=280)

        self._filter_and_update("")

        self.content = ft.Column(controls=[self.search_field, self.grid_view], spacing=10, tight=True)
        self.padding = 12
        self.bgcolor = ft.Colors.GREY_50
        self.border = ft.border.all(1, ft.Colors.GREY_300)
        self.border_radius = 10
        self.visible = False

    def _on_search(self, e):
        query = e.control.value.strip().lower()
        self._filter_and_update(query)

    def _filter_and_update(self, query: str):
        filtered = [item for item in self.all_items if query in str(item).lower()] if query else self.all_items.copy()
        cards = []
        for item in filtered:
            display_text = str(item)
            bg_color = item.get_status_color() if hasattr(item, "get_status_color") else (self.default_item_color or ft.Colors.BLUE_600)
            cards.append(
                ft.Container(
                    content=ft.Text(display_text, size=13, weight="bold", color=ft.Colors.WHITE),
                    padding=10,
                    margin=ft.margin.symmetric(horizontal=2),
                    bgcolor=bg_color,
                    border_radius=8,
                    alignment=ft.alignment.center,
                    on_click=self._on_item_click,
                    data=item,
                    tooltip=f"{display_text} ({getattr(item, 'status', '')})" if hasattr(item, "status") else display_text,
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
            items=info_manager.countries,
            input_field=input_field,
            on_select=on_select,
            search_label="Buscar país",
            item_color=ft.Colors.BLUE_700,
        )


class CarPanel(SelectablePanel):
    def __init__(self, items, input_field=None, on_select=None):
        super().__init__(items=items, input_field=input_field, on_select=on_select, search_label="Buscar auto", item_color=None)


class InfoTable(ft.DataTable):
    def __init__(self, tourists_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Nombre", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Pasaporte", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("País", weight="bold", color=ft.Colors.BLUE_900)),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            heading_row_color=ft.Colors.BLUE_50,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            divider_thickness=0,
            column_spacing=14,
            data_row_min_height=40,
            **kwargs,
        )
        for t in tourists_list:
            self.add_tourist(t.name, t.passport_number, t.country)

    def add_tourist(self, name: str, passport: str, country: str):
        self.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(name, color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Text(passport, color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Text(country, color=ft.Colors.BLACK)),
                ]
            )
        )


class ContractsTable(ft.DataTable):
    def __init__(self, contracts_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Turista", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Auto", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Marca", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Modelo", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Pago", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Inicio", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Fin", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Prórroga", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Chofer", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Total", weight="bold", color=ft.Colors.BLUE_900)),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            heading_row_color=ft.Colors.BLUE_50,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            divider_thickness=0,
            column_spacing=10,
            data_row_min_height=40,
            **kwargs,
        )
        for c in contracts_list:
            self.add_contract(c)

    def add_contract(self, contract):
        chofer = "Sí" if contract.with_driver else "No"
        self.rows.append(
            ft.DataRow(
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
        )


class BrandModelReportTable(ft.DataTable):
    def __init__(self, contracts_list, cars_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Marca", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Modelo", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Autos", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Días", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Efectivo", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Cheque", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Tarjeta", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Total", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            heading_row_color=ft.Colors.BLUE_50,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            divider_thickness=0,
            column_spacing=10,
            data_row_min_height=40,
            **kwargs,
        )
        self.populate(contracts_list, cars_list)

    def populate(self, contracts, cars):
        self.rows.clear()
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


class UsersByCountryTable(ft.DataTable):
    def __init__(self, contracts_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("País", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Usuarios", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            heading_row_color=ft.Colors.BLUE_50,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            divider_thickness=0,
            column_spacing=12,
            data_row_min_height=40,
            **kwargs,
        )
        self.populate(contracts_list)

    def populate(self, contracts):
        self.rows.clear()
        unique_tourists_by_country = defaultdict(set)
        for c in contracts:
            unique_tourists_by_country[c.tourist.country].add(c.tourist.passport_number)
        for country in sorted(unique_tourists_by_country.keys()):
            count = len(unique_tourists_by_country[country])
            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(country, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(str(count), color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                    ]
                )
            )


class CarsListTable(ft.DataTable):
    def __init__(self, cars_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("Placa", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Marca", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Modelo", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Color", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Km", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Estado", weight="bold", color=ft.Colors.BLUE_900)),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            heading_row_color=ft.Colors.BLUE_50,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            divider_thickness=0,
            column_spacing=12,
            data_row_min_height=40,
            **kwargs,
        )
        self.populate(cars_list)

    def populate(self, cars):
        self.rows.clear()
        for i, car in enumerate(sorted(cars, key=lambda x: x.plate)):
            km = getattr(car, "total_km", 0)
            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(car.plate, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(car.brand, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(car.model, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(car.color, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(str(km), color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(car.status, color=ft.Colors.BLACK)),
                    ],
                    color=ft.Colors.WHITE if i % 2 else ft.Colors.BLUE_50,
                )
            )


class SummaryByCountryTable(ft.DataTable):
    def __init__(self, contracts_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("País", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Marca-Modelo", weight="bold", color=ft.Colors.BLUE_900)),
            ft.DataColumn(ft.Text("Días", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Prórroga", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Efectivo", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Total", weight="bold", color=ft.Colors.BLUE_900, text_align=ft.TextAlign.RIGHT)),
        ]
        super().__init__(
            columns=columns,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            heading_row_color=ft.Colors.BLUE_50,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
            divider_thickness=0,
            column_spacing=12,
            data_row_min_height=40,
            **kwargs,
        )
        self.populate(contracts_list)

    def populate(self, contracts):
        self.rows.clear()
        by_country_model = defaultdict(lambda: defaultdict(list))
        for c in contracts:
            by_country_model[c.tourist.country][f"{c.car.brand} {c.car.model}"].append(c)
        for country in sorted(by_country_model.keys()):
            for model_key, contract_list in sorted(by_country_model[country].items()):
                dias = sum((c.end_date - c.start_date).days + 1 for c in contract_list)
                extension = sum(c.extension_days for c in contract_list)
                efectivo = sum(c.total_amount for c in contract_list if c.payment_method == "efectivo")
                total = sum(c.total_amount for c in contract_list)
                self.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(country, color=ft.Colors.BLACK)),
                            ft.DataCell(ft.Text(model_key, color=ft.Colors.BLACK)),
                            ft.DataCell(ft.Text(str(dias), color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                            ft.DataCell(ft.Text(str(extension), color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                            ft.DataCell(ft.Text(f"${efectivo:.2f}", color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                            ft.DataCell(ft.Text(f"${total:.2f}", color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                        ]
                    )
                )

class Formulary(ft.Container):
    def __init__(self, page: ft.Page,
                 info_table: InfoTable,
                 contracts_table: ContractsTable,
                 users_by_country_table: UsersByCountryTable,
                 summary_by_country_table: SummaryByCountryTable,
                 cars_list_table: CarsListTable,
                 info_manager: InfoManager):
        self.page = page
        self.info_table = info_table
        self.contracts_table = contracts_table
        self.users_by_country_table = users_by_country_table
        self.summary_by_country_table = summary_by_country_table
        self.cars_list_table = cars_list_table
        self.info_manager = info_manager

        self.is_form_expanded = False
        self.selected_car = None

        # --- Botón compacto inicial ---
        self.expand_button = ft.ElevatedButton(
            "Formulario",
            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self._toggle_form,
        )

        # --- contenido expandido ---
        self.name_field = ft.TextField(label="Nombre", dense=True)
        self.passport_field = ft.TextField(label="Pasaporte", dense=True)
        self.country_input = ft.TextField(label="País", dense=True, read_only=True)
        self.car_input = ft.TextField(label="Auto", dense=True, read_only=True)
        self.rental_days_field = ft.TextField(label="Días de contrato", dense=True,
                                              input_filter=ft.NumbersOnlyInputFilter())
        self.extension_field = ft.TextField(label="Prórroga (días)", dense=True,
                                            input_filter=ft.NumbersOnlyInputFilter())
        self.payment_dropdown = ft.Dropdown(
            label="Forma de pago",
            options=[ft.dropdown.Option("efectivo"),
                     ft.dropdown.Option("cheque"),
                     ft.dropdown.Option("tarjeta de crédito")],
            value="efectivo",
        )
        self.driver_switch = ft.Switch(label="Con conductor")
        self.add_btn = ft.ElevatedButton("Agregar contrato", icon=ft.Icons.ADD,
                                         on_click=self.formulary_set)

        self.form_column = ft.Column(
            controls=[
                ft.Row([
                    ft.Text("Formulario de contrato", weight="bold"),
                    ft.IconButton(ft.Icons.CLOSE, tooltip="Colapsar",
                                  on_click=self._toggle_form)
                ]),
                self.name_field,
                self.passport_field,
                self.country_input,
                self.car_input,
                self.rental_days_field,
                self.extension_field,
                self.payment_dropdown,
                self.driver_switch,
                self.add_btn,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

        # inicial: solo botón
        super().__init__(
            content=self.expand_button,
            width=120,
            height=40,
            border_radius=8,
        )

    def _toggle_form(self, e=None):
        self.is_form_expanded = not self.is_form_expanded
        if self.is_form_expanded:
            self.content = self.form_column
            self.width = 360
            self.height = 600
            self.padding = 16
        else:
            self.content = self.expand_button
            self.width = 120
            self.height = 40
            self.padding = 0
        self.update()

    def formulary_set(self, e):
        name = self.name_field.value or ""
        passport = self.passport_field.value or ""
        country = self.country_input.value or ""
        car_obj = self.selected_car
        with_driver = self.driver_switch.value

        if not name or not passport or not country:
            self.page.snack_bar = ft.SnackBar(ft.Text("❌ Faltan campos obligatorios"), bgcolor=ft.Colors.RED_200)
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not car_obj:
            self.page.snack_bar = ft.SnackBar(ft.Text("❌ Debes seleccionar un auto"), bgcolor=ft.Colors.RED_200)
            self.page.snack_bar.open = True
            self.page.update()
            return

        if car_obj.status != "disponible":
            self.page.snack_bar = ft.SnackBar(ft.Text("❌ Auto no disponible para alquilar"), bgcolor=ft.Colors.RED_200)
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
                payment_method=payment_method,
            )

            self.info_manager.incert_contrats(contract)
            car_obj.status = "alquilado"

            self.info_table.add_tourist(name=name, passport=passport, country=country)
            self.contracts_table.add_contract(contract)

            self.users_by_country_table.populate(self.info_manager.contracts)
            self.summary_by_country_table.populate(self.info_manager.contracts)
            self.cars_list_table.populate(self.info_manager.cars)
            self.page.update()

            # limpiar campos
            self.name_field.value = ""
            self.passport_field.value = ""
            self.country_input.value = ""
            self.car_input.value = ""
            self.rental_days_field.value = ""
            self.extension_field.value = ""
            self.selected_car = None
            for field in [
                self.name_field,
                self.passport_field,
                self.country_input,
                self.car_input,
                self.rental_days_field,
                self.extension_field,
            ]:
                field.update()

            self.page.snack_bar = ft.SnackBar(ft.Text("✅ Contrato agregado"), bgcolor=ft.Colors.GREEN_200)
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {str(ex)}"), bgcolor=ft.Colors.RED_200)
            self.page.snack_bar.open = True
            self.page.update()
