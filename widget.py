import flet as ft
from datetime import date, timedelta
from collections import defaultdict
from system_of_the_db import dataAbstration as ab
from system_of_the_db import init as i

# ================================
# CONFIGURACIÓN Y DATOS DE EJEMPLO
# ================================
i.info_manager

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
    ab.Car("ABC123", "Toyota", "Corolla", "Rojo", "disponible"),
    ab.Car("XYZ789", "Honda", "Civic", "Azul", "disponible"),
    ab.Car("DEF456", "Ford", "Focus", "Blanco", "disponible"),
    ab.Car("GHI012", "Volkswagen", "Golf", "Gris", "disponible"),
    ab.Car("JKL345", "BMW", "Serie 3", "Negro", "disponible"),
    ab.Car("MNO678", "Mercedes", "C-Class", "Plateado", "disponible"),
    ab.Car("PQR901", "Audi", "A4", "Rojo", "disponible"),
    ab.Car("STU234", "Hyundai", "Elantra", "Azul", "disponible"),
    ab.Car("VWX567", "Nissan", "Sentra", "Blanco", "disponible"),
    ab.Car("YZA890", "Chevrolet", "Cruze", "Gris", "disponible"),
]

SAMPLE_TOURISTS = [
    ab.Tourist("Ana López", "ES123456", "España"),
    ab.Tourist("Carlos Mendoza", "MX789012", "México"),
    ab.Tourist("Sophie Dubois", "FR345678", "Francia"),
    ab.Tourist("Hiroshi Tanaka", "JP901234", "Japón"),
    ab.Tourist("Liam O'Connor", "IE567890", "Irlanda"),
    ab.Tourist("Amina Nkosi", "ZA234567", "Sudáfrica"),
    ab.Tourist("Raj Patel", "IN890123", "India"),
    ab.Tourist("Emma Johansson", "SE456789", "Suecia"),
    ab.Tourist("Luca Rossi", "IT012345", "Italia"),
    ab.Tourist("Yara Silva", "BR678901", "Brasil"),
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


def create_sample_contracts(tourists, cars, num=5):
    """Crea contratos de ejemplo para testing"""
    sample_contracts = []
    today = date.today()
    
    for i in range(min(num, len(tourists), len(cars))):
        if cars[i].status != "disponible":
            continue
            
        tourist = tourists[i]
        car = cars[i]
        start = today - timedelta(days=10)
        end = start + timedelta(days=3)
        
        contract = ab.RentalContract(
            tourist=tourist,
            car=car,
            start_date=start,
            end_date=end,
            extension_days=0 if i % 3 != 0 else 2,
            with_driver=(i % 2 == 0),
            payment_method="efectivo" if i % 3 == 0 else "tarjeta de crédito"
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
    def __init__(self, items, input_field=None, on_select=None):
        super().__init__(
            items=items,
            input_field=input_field,
            on_select=on_select,
            search_label="Buscar auto",
            item_color=None
        )


class InfoTable(ft.DataTable):
    def __init__(self, tourists_list, **kwargs):
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

        for t in tourists_list:
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
    def __init__(self, contracts_list, **kwargs):
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

        for c in contracts_list:
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
    def __init__(self, contracts_list, cars_list, **kwargs):
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
        self.populate(contracts_list, cars_list)

    def populate(self, contracts, cars):
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
    """Reporte 1: Listado de usuarios por país"""
    def __init__(self, contracts_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("País", weight="bold")),
            ft.DataColumn(ft.Text("Usuarios", weight="bold", text_align=ft.TextAlign.RIGHT)),
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
        self.populate(contracts_list)

    def populate(self, contracts):
        unique_tourists_by_country = defaultdict(set)
        for c in contracts:
            country = c.tourist.country
            passport = c.tourist.passport_number
            unique_tourists_by_country[country].add(passport)

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
            ft.DataColumn(ft.Text("Placa", weight="bold")),
            ft.DataColumn(ft.Text("Marca", weight="bold")),
            ft.DataColumn(ft.Text("Modelo", weight="bold")),
            ft.DataColumn(ft.Text("Color", weight="bold")),
            ft.DataColumn(ft.Text("Km", weight="bold", text_align=ft.TextAlign.RIGHT)),
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
        self.populate(cars_list)

    def populate(self, cars):
        for car in sorted(cars, key=lambda x: x.plate):
            km = getattr(car, 'total_km', 0)
            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(car.plate, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(car.brand, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(car.model, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(car.color, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(str(km), color=ft.Colors.BLACK, text_align=ft.TextAlign.RIGHT)),
                    ]
                )
            )


class SummaryByCountryTable(ft.DataTable):
    def __init__(self, contracts_list, **kwargs):
        columns = [
            ft.DataColumn(ft.Text("País", weight="bold")),
            ft.DataColumn(ft.Text("Marca-Modelo", weight="bold")),
            ft.DataColumn(ft.Text("Días", weight="bold", text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Prórroga", weight="bold", text_align=ft.TextAlign.RIGHT)),
            ft.DataColumn(ft.Text("Efectivo", weight="bold", text_align=ft.TextAlign.RIGHT)),
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
        self.populate(contracts_list)

    def populate(self, contracts):
        by_country_model = defaultdict(lambda: defaultdict(list))
        for c in contracts:
            country = c.tourist.country
            model_key = f"{c.car.brand} {c.car.model}"
            by_country_model[country][model_key].append(c)

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
    def __init__(self, page, info_table, contracts_table,
                 users_by_country_table, summary_by_country_table, cars_list_table,
                 tourists_list, cars_list, contracts_list):
        self.page = page
        self.info_table = info_table
        self.contracts_table = contracts_table
        self.users_by_country_table = users_by_country_table
        self.summary_by_country_table = summary_by_country_table
        self.cars_list_table = cars_list_table
        self.tourists_list = tourists_list
        self.cars_list = cars_list
        self.contracts_list = contracts_list
        self.is_country_panel_open = False
        self.is_car_panel_open = False
        self.selected_car = None
        self.is_form_expanded = True

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

        self.toggle_form_btn = ft.TextButton("▲ Ocultar formulario", on_click=self._toggle_form)

        def on_car_select(car):
            found_car = None
            for c in self.cars_list:
                if c.plate == car.plate:
                    found_car = c
                    break
            if found_car and found_car.status != "disponible":
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"❌ El auto {found_car} no está disponible ({found_car.status})"),
                    bgcolor=ft.Colors.RED_200
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            self.selected_car = found_car

        self.country_panel = CountryPanel(input_field=self.country_input)
        self.car_panel = CarPanel(items=self.cars_list, input_field=self.car_input, on_select=on_car_select)

        self.select_country_btn = ft.TextButton("Seleccionar país", on_click=lambda e: self._toggle_country_panel(e))
        self.select_car_btn = ft.TextButton("Seleccionar auto", on_click=lambda e: self._toggle_car_panel(e))

        self.form_column = ft.Column(
            controls=[
                self.toggle_form_btn,
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

        self.country_panel.visible = False
        self.car_panel.visible = False

        super().__init__(
            content=self.form_column,
            padding=14,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=12,
            height=800,
            width=280,
            expand=False
        )

    def _toggle_form(self, e):
        self.is_form_expanded = not self.is_form_expanded
        if self.is_form_expanded:
            self.width = 280
            self.toggle_form_btn.text = "▲ Ocultar formulario"
            for control in self.form_column.controls[1:]:
                control.visible = True
        else:
            self.width = 150
            self.toggle_form_btn.text = "▼ Mostrar formulario"
            for control in self.form_column.controls[1:]:
                control.visible = False
        self.update()

    def _toggle_country_panel(self, e):
        self.is_country_panel_open = not self.is_country_panel_open
        self.country_panel.visible = self.is_country_panel_open

        if self.is_country_panel_open:
            self.width = 460
            self.select_country_btn.text = "▲ Ocultar países"
            self.country_panel.search_field.focus()
        else:
            self.width = 280 if self.is_form_expanded else 150
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
            self.width = 280 if self.is_form_expanded else 150
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

        car_obj.status = "alquilado"

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

        tourist = ab.Tourist(name, passport, country)  # ✅
        try:
            contract = ab.RentalContract(  # ✅
                tourist=tourist,
                car=car_obj,
                start_date=start_date,
                end_date=end_date,
                extension_days=extension_days,
                with_driver=with_driver,
                payment_method=payment_method
            )

            contract.print_all_attributes()

            self.contracts_list.append(contract)
            print_all_contracts()

            self.info_table.add_tourist(name=name, passport=passport, country=country)
            self.contracts_table.add_contract(contract)

            self.users_by_country_table.populate(self.contracts_list)
            self.summary_by_country_table.populate(self.contracts_list)
            self.cars_list_table.populate(self.cars_list)
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

    if not contracts:
        sample_contracts = create_sample_contracts(SAMPLE_TOURISTS, SAMPLE_CARS, num=6)
        contracts.extend(sample_contracts)
        print("✅ Contratos de ejemplo creados para testing")
        print_all_contracts()

    info_table = InfoTable(tourists_list=SAMPLE_TOURISTS)
    contracts_table = ContractsTable(contracts_list=contracts)
    brand_model_table = BrandModelReportTable(contracts_list=contracts, cars_list=SAMPLE_CARS)
    users_by_country_table = UsersByCountryTable(contracts_list=contracts)
    cars_list_table = CarsListTable(cars_list=SAMPLE_CARS)
    summary_by_country_table = SummaryByCountryTable(contracts_list=contracts)

    turistas_scroll = ft.Column(controls=[info_table], scroll=ft.ScrollMode.AUTO, expand=True)
    contratos_scroll = ft.Column(controls=[contracts_table], scroll=ft.ScrollMode.AUTO, expand=True)
    marca_modelo_scroll = ft.Column(controls=[brand_model_table], scroll=ft.ScrollMode.AUTO, expand=True)
    usuarios_pais_scroll = ft.Column(controls=[users_by_country_table], scroll=ft.ScrollMode.AUTO, expand=True)
    autos_lista_scroll = ft.Column(controls=[cars_list_table], scroll=ft.ScrollMode.AUTO, expand=True)
    resumen_pais_scroll = ft.Column(controls=[summary_by_country_table], scroll=ft.ScrollMode.AUTO, expand=True)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Turistas", content=ft.Container(content=turistas_scroll, padding=10, expand=True)),
            ft.Tab(text="Contratos", content=ft.Container(content=contratos_scroll, padding=10, expand=True)),
            ft.Tab(text="Marca/Modelo", content=ft.Container(content=marca_modelo_scroll, padding=10, expand=True)),
            ft.Tab(text="Usuarios x País", content=ft.Container(content=usuarios_pais_scroll, padding=10, expand=True)),
            ft.Tab(text="Lista de Autos", content=ft.Container(content=autos_lista_scroll, padding=10, expand=True)),
            ft.Tab(text="Resumen x País", content=ft.Container(content=resumen_pais_scroll, padding=10, expand=True)),
        ],
        expand=True,
    )

    form = Formulary(
        page=page,
        info_table=info_table,
        contracts_table=contracts_table,
        users_by_country_table=users_by_country_table,
        summary_by_country_table=summary_by_country_table,
        cars_list_table=cars_list_table,
        tourists_list=SAMPLE_TOURISTS,
        cars_list=SAMPLE_CARS,
        contracts_list=contracts
    )

    layout = ft.Row(
        controls=[form, tabs],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)