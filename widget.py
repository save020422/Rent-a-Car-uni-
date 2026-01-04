import flet as ft
from datetime import date, timedelta
from collections import defaultdict
from init_ import *  # Debe exponer: InfoManager (info_manager), listas de tourists, cars, contracts.


# ============================
# Paneles de selección (compactos)
# ============================

class SelectablePanel(ft.Container):
    def __init__(self, items, input_field=None, on_select=None, search_label="Buscar", item_color=None):
        super().__init__()
        self.input = input_field
        self.on_select = on_select
        self.all_items = list(items)
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
            on_change=self._on_search,  # filtro en tiempo real
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


# ============================
# Tablas con filtro on_change y colores
# ============================

class InfoTable(ft.Container):
    def __init__(self, tourists_list, **kwargs):
        self.search_field = ft.TextField(
            label="Filtrar nombre",
            dense=True,
            width=220,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700,
            on_change=self.apply_filter
        )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre", weight="bold", color=ft.Colors.BLUE_900)),
                ft.DataColumn(ft.Text("Pasaporte", weight="bold", color=ft.Colors.BLUE_900)),
                ft.DataColumn(ft.Text("País", weight="bold", color=ft.Colors.BLUE_900)),
            ],
            border=ft.border.all(2, ft.Colors.BLUE_200),
            border_radius=12,
            heading_row_color=ft.Colors.BLUE_50,
            column_spacing=14,
            data_row_min_height=40,
            **kwargs,
        )
        self.original_data = list(tourists_list)
        self.populate(tourists_list)
        super().__init__(
            content=ft.Column([self.search_field, self.table], spacing=8),
            padding=12,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.all(2, ft.Colors.BLUE_200),
            border_radius=12,
        )

    def populate(self, tourists_list):
        self.table.rows.clear()
        for t in tourists_list:
            self.table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(t.name)),
                    ft.DataCell(ft.Text(t.passport_number)),
                    ft.DataCell(ft.Text(t.country)),
                ])
            )

    def apply_filter(self, e):
        q = self.search_field.value.strip().lower()
        filtered = [t for t in self.original_data if q in t.name.lower()] if q else self.original_data
        self.populate(filtered)
        self.update()


class ContractsTable(ft.Container):
    def __init__(self, contracts_list, **kwargs):
        self.search_field = ft.TextField(
            label="Filtrar turista",
            dense=True,
            width=220,
            border_color=ft.Colors.GREEN_400,
            focused_border_color=ft.Colors.GREEN_700,
            on_change=self.apply_filter
        )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Turista", weight="bold", color=ft.Colors.GREEN_900)),
                ft.DataColumn(ft.Text("Auto", weight="bold", color=ft.Colors.GREEN_900)),
                ft.DataColumn(ft.Text("Marca", weight="bold", color=ft.Colors.GREEN_900)),
                ft.DataColumn(ft.Text("Modelo", weight="bold", color=ft.Colors.GREEN_900)),
                ft.DataColumn(ft.Text("Pago", weight="bold", color=ft.Colors.GREEN_900)),
                ft.DataColumn(ft.Text("Inicio", weight="bold", color=ft.Colors.GREEN_900)),
                ft.DataColumn(ft.Text("Fin", weight="bold", color=ft.Colors.GREEN_900)),
                ft.DataColumn(ft.Text("Total", weight="bold", color=ft.Colors.GREEN_900)),
            ],
            border=ft.border.all(2, ft.Colors.GREEN_300),
            border_radius=12,
            heading_row_color=ft.Colors.GREEN_50,
            column_spacing=12,
            data_row_min_height=40,
            **kwargs,
        )
        self.original_data = list(contracts_list)
        self.populate(contracts_list)
        super().__init__(
            content=ft.Column([self.search_field, self.table], spacing=8),
            padding=12,
            bgcolor=ft.Colors.GREEN_50,
            border=ft.border.all(2, ft.Colors.GREEN_300),
            border_radius=12,
        )

    def populate(self, contracts_list):
        self.table.rows.clear()
        for c in contracts_list:
            self.table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(c.tourist.name)),
                    ft.DataCell(ft.Text(c.car.plate)),
                    ft.DataCell(ft.Text(c.car.brand)),
                    ft.DataCell(ft.Text(c.car.model)),
                    ft.DataCell(ft.Text(c.payment_method)),
                    ft.DataCell(ft.Text(str(c.start_date))),
                    ft.DataCell(ft.Text(str(c.end_date))),
                    ft.DataCell(ft.Text(f"${c.total_amount:.2f}")),
                ])
            )

    def apply_filter(self, e):
        q = self.search_field.value.strip().lower()
        filtered = [c for c in self.original_data if q in c.tourist.name.lower()] if q else self.original_data
        self.populate(filtered)
        self.update()


class CarsListTable(ft.Container):
    def __init__(self, cars_list, **kwargs):
        self.search_field = ft.TextField(
            label="Filtrar placa",
            dense=True,
            width=220,
            border_color=ft.Colors.ORANGE_400,
            focused_border_color=ft.Colors.ORANGE_700,
            on_change=self.apply_filter
        )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Placa", weight="bold", color=ft.Colors.ORANGE_900)),
                ft.DataColumn(ft.Text("Marca", weight="bold", color=ft.Colors.ORANGE_900)),
                ft.DataColumn(ft.Text("Modelo", weight="bold", color=ft.Colors.ORANGE_900)),
                ft.DataColumn(ft.Text("Color", weight="bold", color=ft.Colors.ORANGE_900)),
                ft.DataColumn(ft.Text("Estado", weight="bold", color=ft.Colors.ORANGE_900)),
            ],
            border=ft.border.all(2, ft.Colors.ORANGE_300),
            border_radius=12,
            heading_row_color=ft.Colors.ORANGE_50,
            column_spacing=12,
            data_row_min_height=40,
            **kwargs,
        )
        self.original_data = list(cars_list)
        self.populate(cars_list)
        super().__init__(
            content=ft.Column([self.search_field, self.table], spacing=8),
            padding=12,
            bgcolor=ft.Colors.ORANGE_50,
            border=ft.border.all(2, ft.Colors.ORANGE_300),
            border_radius=12,
        )

    def populate(self, cars_list):
        self.table.rows.clear()
        for car in cars_list:
            self.table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(car.plate)),
                    ft.DataCell(ft.Text(car.brand)),
                    ft.DataCell(ft.Text(car.model)),
                    ft.DataCell(ft.Text(car.color)),
                    ft.DataCell(ft.Text(car.status)),
                ])
            )

    def apply_filter(self, e):
        q = self.search_field.value.strip().lower()
        filtered = [c for c in self.original_data if q in c.plate.lower()] if q else self.original_data
        self.populate(filtered)
        self.update()


class BrandModelReportTable(ft.Container):
    def __init__(self, contracts_list, cars_list, **kwargs):
        self.search_field = ft.TextField(
            label="Filtrar marca/modelo",
            dense=True,
            width=240,
            border_color=ft.Colors.PURPLE_400,
            focused_border_color=ft.Colors.PURPLE_700,
            on_change=self.apply_filter
        )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Marca", weight="bold", color=ft.Colors.PURPLE_900)),
                ft.DataColumn(ft.Text("Modelo", weight="bold", color=ft.Colors.PURPLE_900)),
                ft.DataColumn(ft.Text("Autos", weight="bold", color=ft.Colors.PURPLE_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Días", weight="bold", color=ft.Colors.PURPLE_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Efectivo", weight="bold", color=ft.Colors.PURPLE_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Cheque", weight="bold", color=ft.Colors.PURPLE_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Tarjeta", weight="bold", color=ft.Colors.PURPLE_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Total", weight="bold", color=ft.Colors.PURPLE_900, text_align=ft.TextAlign.RIGHT)),
            ],
            border=ft.border.all(2, ft.Colors.PURPLE_300),
            border_radius=12,
            heading_row_color=ft.Colors.PURPLE_50,
            column_spacing=10,
            data_row_min_height=40,
            **kwargs,
        )
        self.original_contracts = list(contracts_list)
        self.original_cars = list(cars_list)
        self.populate(contracts_list, cars_list)
        super().__init__(
            content=ft.Column([self.search_field, self.table], spacing=8),
            padding=12,
            bgcolor=ft.Colors.PURPLE_50,
            border=ft.border.all(2, ft.Colors.PURPLE_300),
            border_radius=12,
        )

    def populate(self, contracts, cars):
        self.table.rows.clear()
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
            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(brand)),
                        ft.DataCell(ft.Text(model)),
                        ft.DataCell(ft.Text(str(count), text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(str(dias), text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${efectivo:.2f}", text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${cheque:.2f}", text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${tarjeta:.2f}", text_align=ft.TextAlign.RIGHT)),
                        ft.DataCell(ft.Text(f"${subtotal:.2f}", text_align=ft.TextAlign.RIGHT)),
                    ]
                )
            )
        self.table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("TOTAL GENERAL", weight="bold", color=ft.Colors.PURPLE_800)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text(f"${total_general:.2f}", weight="bold", color=ft.Colors.PURPLE_800, text_align=ft.TextAlign.RIGHT)),
                ]
            )
        )

    def apply_filter(self, e):
        q = self.search_field.value.strip().lower()
        filtered_contracts = (
            [c for c in self.original_contracts if q in c.car.brand.lower() or q in c.car.model.lower()]
            if q else self.original_contracts
        )
        self.populate(filtered_contracts, self.original_cars)
        self.update()


class UsersByCountryTable(ft.Container):
    def __init__(self, contracts_list, **kwargs):
        self.search_field = ft.TextField(
            label="Filtrar país",
            dense=True,
            width=220,
            border_color=ft.Colors.TEAL_400,
            focused_border_color=ft.Colors.TEAL_700,
            on_change=self.apply_filter
        )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("País", weight="bold", color=ft.Colors.TEAL_900)),
                ft.DataColumn(ft.Text("Usuarios", weight="bold", color=ft.Colors.TEAL_900, text_align=ft.TextAlign.RIGHT)),
            ],
            border=ft.border.all(2, ft.Colors.TEAL_300),
            border_radius=12,
            heading_row_color=ft.Colors.TEAL_50,
            column_spacing=12,
            data_row_min_height=40,
            **kwargs,
        )
        self.original_contracts = list(contracts_list)
        self.populate(contracts_list)
        super().__init__(
            content=ft.Column([self.search_field, self.table], spacing=8),
            padding=12,
            bgcolor=ft.Colors.TEAL_50,
            border=ft.border.all(2, ft.Colors.TEAL_300),
            border_radius=12,
        )

    def populate(self, contracts):
        self.table.rows.clear()
        unique_tourists_by_country = defaultdict(set)
        for c in contracts:
            unique_tourists_by_country[c.tourist.country].add(c.tourist.passport_number)
        for country in sorted(unique_tourists_by_country.keys()):
            count = len(unique_tourists_by_country[country])
            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(country)),
                        ft.DataCell(ft.Text(str(count), text_align=ft.TextAlign.RIGHT)),
                    ]
                )
            )

    def apply_filter(self, e):
        q = self.search_field.value.strip().lower()
        filtered = self.original_contracts if not q else [c for c in self.original_contracts if q in c.tourist.country.lower()]
        self.populate(filtered)
        self.update()


class SummaryByCountryTable(ft.Container):
    def __init__(self, contracts_list, **kwargs):
        self.search_field = ft.TextField(
            label="Filtrar país",
            dense=True,
            width=240,
            border_color=ft.Colors.INDIGO_400,
            focused_border_color=ft.Colors.INDIGO_700,
            on_change=self.apply_filter
        )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("País", weight="bold", color=ft.Colors.INDIGO_900)),
                ft.DataColumn(ft.Text("Marca-Modelo", weight="bold", color=ft.Colors.INDIGO_900)),
                ft.DataColumn(ft.Text("Días", weight="bold", color=ft.Colors.INDIGO_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Prórroga", weight="bold", color=ft.Colors.INDIGO_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Efectivo", weight="bold", color=ft.Colors.INDIGO_900, text_align=ft.TextAlign.RIGHT)),
                ft.DataColumn(ft.Text("Total", weight="bold", color=ft.Colors.INDIGO_900, text_align=ft.TextAlign.RIGHT)),
            ],
            border=ft.border.all(2, ft.Colors.INDIGO_300),
            border_radius=12,
            heading_row_color=ft.Colors.INDIGO_50,
            column_spacing=12,
            data_row_min_height=40,
            **kwargs,
        )
        self.original_contracts = list(contracts_list)
        self.populate(contracts_list)
        super().__init__(
            content=ft.Column([self.search_field, self.table], spacing=8),
            padding=12,
            bgcolor=ft.Colors.INDIGO_50,
            border=ft.border.all(2, ft.Colors.INDIGO_300),
            border_radius=12,
        )

    def populate(self, contracts):
        self.table.rows.clear()
        by_country_model = defaultdict(lambda: defaultdict(list))
        for c in contracts:
            by_country_model[c.tourist.country][f"{c.car.brand} {c.car.model}"].append(c)
        for country in sorted(by_country_model.keys()):
            for model_key, contract_list in sorted(by_country_model[country].items()):
                dias = sum((c.end_date - c.start_date).days + 1 for c in contract_list)
                extension = sum(c.extension_days for c in contract_list)
                efectivo = sum(c.total_amount for c in contract_list if c.payment_method == "efectivo")
                total = sum(c.total_amount for c in contract_list)
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(country)),
                            ft.DataCell(ft.Text(model_key)),
                            ft.DataCell(ft.Text(str(dias), text_align=ft.TextAlign.RIGHT)),
                            ft.DataCell(ft.Text(str(extension), text_align=ft.TextAlign.RIGHT)),
                            ft.DataCell(ft.Text(f"${efectivo:.2f}", text_align=ft.TextAlign.RIGHT)),
                            ft.DataCell(ft.Text(f"${total:.2f}", text_align=ft.TextAlign.RIGHT)),
                        ]
                    )
                )

    def apply_filter(self, e):
        q = self.search_field.value.strip().lower()
        filtered = self.original_contracts if not q else [c for c in self.original_contracts if q in c.tourist.country.lower()]
        self.populate(filtered)
        self.update()


# ============================
# Formulario compacto (botón)
# ============================

class Formulary(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        info_table: InfoTable,
        contracts_table: ContractsTable,
        users_by_country_table: UsersByCountryTable,
        summary_by_country_table: SummaryByCountryTable,
        cars_list_table: CarsListTable,
        info_manager: InfoManager,
    ):
        self.page = page
        self.info_table = info_table
        self.contracts_table = contracts_table
        self.users_by_country_table = users_by_country_table
        self.summary_by_country_table = summary_by_country_table
        self.cars_list_table = cars_list_table
        self.info_manager = info_manager

        self.is_form_expanded = False
        self.selected_car = None

        self.expand_button = ft.ElevatedButton(
            "Formulario",
            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self._toggle_form,
        )

        self.name_field = ft.TextField(label="Nombre", dense=True)
        self.passport_field = ft.TextField(label="Pasaporte", dense=True)
        self.country_input = ft.TextField(label="País", dense=True, read_only=True)
        self.car_input = ft.TextField(label="Auto", dense=True, read_only=True)
        self.rental_days_field = ft.TextField(label="Días de contrato", dense=True, input_filter=ft.NumbersOnlyInputFilter())
        self.extension_field = ft.TextField(label="Prórroga (días)", dense=True, input_filter=ft.NumbersOnlyInputFilter())
        self.payment_dropdown = ft.Dropdown(
            label="Forma de pago",
            options=[ft.dropdown.Option("efectivo"), ft.dropdown.Option("cheque"), ft.dropdown.Option("tarjeta de crédito")],
            value="efectivo",
        )
        self.driver_switch = ft.Switch(label="Con conductor")
        self.add_btn = ft.ElevatedButton("Agregar contrato", icon=ft.Icons.ADD, on_click=self.formulary_set)

        def on_car_select(car):
            found_car = next((c for c in self.info_manager.cars if c.plate == car.plate), None)
            if found_car and found_car.status != "disponible":
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"❌ El auto {found_car.plate} no está disponible ({found_car.status})"),
                    bgcolor=ft.Colors.RED_200,
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            self.selected_car = found_car
            self.car_input.value = f"{found_car.plate} • {found_car.brand} {found_car.model}"
            self.car_input.update()

        self.country_panel_btn = ft.TextButton("Seleccionar país", on_click=self._toggle_country_panel)
        self.car_panel_btn = ft.TextButton("Seleccionar auto", on_click=self._toggle_car_panel)

        self.country_panel = CountryPanel(input_field=self.country_input)
        self.car_panel = CarPanel(items=self.info_manager.cars, input_field=self.car_input, on_select=on_car_select)
        self.country_panel.visible = False
        self.car_panel.visible = False

        self.form_column = ft.Column(
    controls=[
        ft.Text("Formulario de contrato", weight="bold"),
        ft.IconButton(ft.Icons.CLOSE, tooltip="Colapsar", on_click=self._toggle_form),

        # Campos uno debajo del otro
        self.name_field,
        self.passport_field,
        self.country_input,
        self.country_panel_btn,
        self.country_panel,
        self.car_input,
        self.car_panel_btn,
        self.car_panel,
        self.rental_days_field,
        self.extension_field,
        self.payment_dropdown,
        self.driver_switch,
        self.add_btn,
    ],
    spacing=8,
    scroll=ft.ScrollMode.AUTO,   # 👈 mantiene el scroll vertical
)


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
            self.width = 380
            self.height = 640
            self.padding = 16
            self.border = ft.border.all(2, ft.Colors.BLUE_300)
            self.bgcolor = ft.Colors.BLUE_50
        else:
            self.content = self.expand_button
            self.width = 120
            self.height = 40
            self.padding = 0
            self.border = None
            self.bgcolor = None
            # cerrar paneles si estaban abiertos
            self.country_panel.visible = False
            self.car_panel.visible = False
        self.update()

    def _toggle_country_panel(self, e):
        self.country_panel.visible = not self.country_panel.visible
        if self.country_panel.visible:
            self.country_panel.search_field.focus()
        else:
            self.country_panel.search_field.value = ""
            self.country_panel._filter_and_update("")
            if self.page:
                self.country_panel.search_field.update()
        self.update()

    def _toggle_car_panel(self, e):
        self.car_panel.visible = not self.car_panel.visible
        if self.car_panel.visible:
            self.car_panel.search_field.focus()
        else:
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

            # Actualiza datasets y vistas
            self.info_table.original_data.append(tourist)
            self.info_table.populate(self.info_table.original_data)

            self.contracts_table.original_data.append(contract)
            self.contracts_table.populate(self.contracts_table.original_data)

            self.users_by_country_table.populate(self.info_manager.contracts)
            self.summary_by_country_table.populate(self.info_manager.contracts)
            self.cars_list_table.populate(self.cars_list_table.original_data)

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


# ============================
# Main
# ============================

def main(page: ft.Page):
    page.title = "Rent a Car - Control de Alquiler"
    page.padding = 16
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_100

    page.appbar = ft.AppBar(
        title=ft.Text("🚘 Rent a Car", size=20, weight="bold"),
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        center_title=True,
        elevation=4,
    )

    info_table = InfoTable(tourists_list=info_manager.tourist)
    contracts_table = ContractsTable(contracts_list=info_manager.contracts)
    brand_model_table = BrandModelReportTable(contracts_list=info_manager.contracts, cars_list=info_manager.cars)
    users_by_country_table = UsersByCountryTable(contracts_list=info_manager.contracts)
    cars_list_table = CarsListTable(cars_list=info_manager.cars)
    summary_by_country_table = SummaryByCountryTable(contracts_list=info_manager.contracts)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Turistas", content=info_table),
            ft.Tab(text="Contratos", content=contracts_table),
            ft.Tab(text="Marca/Modelo", content=brand_model_table),
            ft.Tab(text="Usuarios x País", content=users_by_country_table),
            ft.Tab(text="Lista de Autos", content=cars_list_table),
            ft.Tab(text="Resumen x País", content=summary_by_country_table),
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
        info_manager=info_manager,
    )

    layout = ft.Row(
        controls=[form, ft.Column(controls=[tabs], expand=True, scroll=ft.ScrollMode.AUTO)],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)
