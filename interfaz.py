import sqlite3
import flet as ft
import matplotlib
import gestion_estacionamiento as ge


def main(page: ft.Page):
    matplotlib.use('agg')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    page.title = "Gestor de Estacionamiento"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    nombre_usuario = ft.TextField(label="DNI del Usuario")
    tipo_vehiculo = ft.TextField(label="Patente de Vehículo")
    id_ticket = ft.TextField(label="Ticket")
    mensaje = ft.Text("")

    def cambiar_tab(index):
        tabs_control.selected_index = index
        page.update()

    def mostrar_popup(mensaje_popup):
        dialog = ft.AlertDialog(
            title=ft.Text("Información"),
            content=ft.Text(mensaje_popup),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: cerrar_popup(dialog))
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def cerrar_popup(dialog):
        dialog.open = False
        page.update()

    def manejar_ingreso(e):
        if nombre_usuario.value and tipo_vehiculo.value:
            resultado = ge.ingresar_vehiculo(cursor, conn, nombre_usuario.value, f"'{tipo_vehiculo.value}'")
            if resultado != -1:
                mostrar_popup(f"Vehículo registrado exitosamente. Su número de trámite es: {resultado}")
            else:
                mostrar_popup("No quedan plazas disponibles.")
            nombre_usuario.value = ""
            tipo_vehiculo.value = ""
            page.update()
        else:
            mostrar_popup("Por favor, complete ambos campos.")

    def manejar_egreso(e):
        if id_ticket.value:
            resultado = ge.retirar_vehiculo(id_ticket.value, cursor, conn)
            if resultado:
                mostrar_popup("Vehículo retirado exitosamente.")
            else:
                mostrar_popup("El ticket no corresponde a una plaza ocupada.")
            id_ticket.value = ""
            page.update()
        else:
            mostrar_popup("Por favor, complete el campo del ticket.")

    page.appbar = ft.AppBar(
        title=ft.Text("Gestor de Estacionamiento"),
        center_title=True,
        bgcolor=ft.colors.BLUE,
    )

    tabs_control = ft.Tabs(
        tabs=[
            ft.Tab(
                text="",
                content=ft.Column([
                    ft.Text("Registro de Vehículos", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    nombre_usuario,
                    tipo_vehiculo,
                    ft.ElevatedButton("Registrar Vehículo", on_click=manejar_ingreso),
                    mensaje,
                ])
            ),
            ft.Tab(
                text="",
                content=ft.Column([
                    ft.Text("Baja de Vehículos", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    id_ticket,
                    ft.ElevatedButton("Retirar Vehículo", on_click=manejar_egreso),
                    mensaje,
                ])
            ),
        ],
        selected_index=0,
    )

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
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(botones, tabs_control)


# Iniciar aplicación
ft.app(target=main)
