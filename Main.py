
from importAll import *


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

    # ✅ Crear contratos de ejemplo si no hay ninguno
    #if not contracts:
        #sample_contracts = create_sample_contracts(SAMPLE_TOURISTS, SAMPLE_CARS, num=6)
       # contracts.extend(sample_contracts)
       # print("✅ Contratos de ejemplo creados para testing")
        #print_all_contracts()

    info_table = InfoTable(tourists_list=info_manager.tourist)
    contracts_table = ContractsTable(contracts_list=info_manager.contracts)
    brand_model_table = BrandModelReportTable(contracts_list=info_manager.contracts, cars_list=info_manager.cars)
    users_by_country_table = UsersByCountryTable(contracts_list=info_manager.contracts)
    cars_list_table = CarsListTable(cars_list=info_manager.cars)
    summary_by_country_table = SummaryByCountryTable(contracts_list=info_manager.contracts)

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