from widget import *
def layout(page):

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
     
     
     return ft.Row(
        controls=[form, table_container],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=False
    )
