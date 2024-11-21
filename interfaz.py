import flet as ft

def main(page: ft.Page):
    # Configuración inicial de la ventana
    page.title = "Gestor de Estacionamiento"
    page.theme_mode = ft.ThemeMode.DARK  # Opcional, puedes cambiarlo a DARK
    page.padding = 10
    
    # Función para cambiar de pestaña
    def cambiar_tab(index):
        tabs_control.selected_index = index
        page.update()
    
    def construir_tabla():
        registros = ['prueba']#obtener_datos()
        if not registros:
            return ft.Text("No hay registros en la base de datos.")
        
        # Construcción de DataTable
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Vehículo")),
                ft.DataColumn(ft.Text("Hora de Entrada")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(fila[0]))),
                        ft.DataCell(ft.Text(fila[1])),
                        ft.DataCell(ft.Text(fila[2])),
                        ft.DataCell(ft.Text(fila[3])),
                    ],
                )
                for fila in registros
            ],
        )
    
    # Barra de aplicación
    page.appbar = ft.AppBar(
        title=ft.Text("Gestor de Estacionamiento"),
        center_title=True,
        bgcolor=ft.colors.BLUE,
    )
    
    # Pestañas
    tabs_control = ft.Tabs(
        tabs=[
            ft.Tab(text="Tab 1", content=ft.Text("Lógica del alta")),
            ft.Tab(text="Tab 2", content=ft.Text("Lógica de la baja")),
            ft.Tab(
                text="Tab 3", 
                content=ft.Column([
                    ft.Text("Dashboard", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    construir_tabla(),
                ])
            ),
        ],
        selected_index=0,
    )
    
    # Botones para cambiar entre pestañas
    botones = ft.Row(
        controls=[
            ft.ElevatedButton(
                text="Ingresar Vehículo",
                on_click=lambda _: cambiar_tab(0),
            ),
            ft.ElevatedButton(
                text="Retirar Vehículo",
                on_click=lambda _: cambiar_tab(1),
            ),
            ft.ElevatedButton(
                text="Dashboard",
                on_click=lambda _: cambiar_tab(2),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Layout principal
    page.add(botones, tabs_control)

# Iniciar aplicación
ft.app(target=main)
 