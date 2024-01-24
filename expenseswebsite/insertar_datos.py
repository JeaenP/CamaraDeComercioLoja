import pandas as pd
from datetime import datetime
from expenses.models import Expense
import os
import sys

def insertar_datos_desde_excel(ruta_excel):
    # Carga el libro de trabajo de Excel
    libro_excel = openpyxl.load_workbook(ruta_excel)

    # Selecciona la hoja de trabajo (puedes cambiar el nombre de la hoja según tu archivo)
    hoja_excel = libro_excel['Hoja 1']

    # Itera sobre las filas de la hoja de trabajo
    for fila in hoja_excel.iter_rows(min_row=2, values_only=True):
        # Crea una instancia de Expense con los datos de la fila
        expense = Expense(
            cedula_ruc=fila[0],
            razon_social=fila[1],
            cuota_total=fila[2],
            cuota_ult_fecha=fila[3],
            emitidas = fila[4],
            cuota_nro = fila[5],
            fecha_nacimiento = fila[6],
            fecha_inscripcion = fila[7],
            nombre_comercial = fila[8],
            actividad = fila[9],
            telefonos = fila[10],
            email = fila[11],
            pertenece_comite = fila[12],
            ultimo_pago = fila[13],
            dir_comercial = fila[14],
            dir_domicilio = fila[15],
            nmesesaportados = fila[16],
            nmesesvigencia = fila[17],
            tipo_socio = fila[18],
            recaudador = fila[19],
            genero = fila[20],
            linea_negocio = fila[21],
            estado = fila[22],
            aseguradora = fila[23],
            nacionalidad = fila[24],
            estado_civil = fila[25],
            movil = fila[26],
            nombre = fila[27],
            representantelegal = fila[28],
            conyuge = fila[29],
            fechaactualizacion = fila[30],
            fechaultimafact = fila[31],
            idclase = fila[32],
            fecha_ultima_factura = fila[33],
            id = fila[34]
          
        )

        expense.save()

# Ruta al archivo Excel
ruta_excel = 'C:\\Users\\jpvpv\\Downloads\\LISTADO PARA UTPL.xlt'

# Llama a la función para insertar datos desde Excel
insertar_datos_desde_excel(ruta_excel)