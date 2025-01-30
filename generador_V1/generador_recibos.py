import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

class GeneradorRecibos:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=1,
            spaceAfter=30
        )
        self.columnas_requeridas = ['FECHA', 'NOMBRE', 'DEPTO', 'TELF', 'EXPENSA', 'MULTA']
        self.datos_agua = self.cargar_datos_agua('resultado_agua.csv')  # Nueva línea

    # --- NUEVO MÉTODO PARA CARGAR DATOS DE AGUA ---
    def cargar_datos_agua(self, csv_path):
        """Carga los datos de agua desde el CSV generado"""
        datos_agua = {}
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    datos_agua[row['Depto']] = row['Monto']
            print("Datos de agua cargados correctamente")
            return datos_agua
        except Exception as e:
            print(f"Error cargando datos de agua: {e}")
            return {}
        
    def generar_recibo(self, datos_apartamento, nombre_archivo):
        """
        Genera un recibo de pago en PDF para un apartamento.
        """
        doc = SimpleDocTemplate(
            nombre_archivo,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        elementos = []
        
        titulo = Paragraph(
            f"Recibo de Pago - Departamento {datos_apartamento['DEPTO']}",
            self.titulo_style
        )
        elementos.append(titulo)
        
        info_basica = [
            ["Fecha:", datos_apartamento[self.limpiar_nombre_columna('FECHA')]],
            ["Departamento:", datos_apartamento['DEPTO']],
            ["Propietario:", datos_apartamento['NOMBRE']],
            ["Teléfono:", datos_apartamento['TELF']]
        ]
        
        detalles_pago = [
            ["Concepto", "Monto"]
        ]

        # Agregar conceptos solo si tienen valor
        if datos_apartamento['EXPENSA']:
            detalles_pago.append(["Expensa", f"${float(datos_apartamento['EXPENSA']):.2f}"])
        
        if datos_apartamento['AGUA']:
            detalles_pago.append(["Agua", f"${float(datos_apartamento['AGUA']):.2f}"])
        
        if datos_apartamento.get('MULTA'):
            detalles_pago.append(["Multa", f"${float(datos_apartamento['MULTA']):.2f}"])
        
        # Calcular total solo de los valores que existen
        total = 0
        for concepto in ['EXPENSA', 'AGUA', 'MULTA']:
            if datos_apartamento.get(concepto) and datos_apartamento[concepto]:
                try:
                    total += float(datos_apartamento[concepto])
                except ValueError:
                    pass
                    
        detalles_pago.append(["Total", f"${total:.2f}"])
        
        tabla_info = Table(info_basica, colWidths=[100, 300])
        tabla_info.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        tabla_pago = Table(detalles_pago, colWidths=[200, 200])
        tabla_pago.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTWEIGHT', (0, 0), (-1, 0), 'BOLD'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTWEIGHT', (0, -1), (-1, -1), 'BOLD'),
        ]))
        
        elementos.append(tabla_info)
        elementos.append(Spacer(1, 20))
        elementos.append(tabla_pago)
        
        doc.build(elementos)

    def limpiar_nombre_columna(self, nombre):
        """
        Limpia el nombre de la columna eliminando el BOM si existe
        """
        return nombre.replace('\ufeff', '')

    def obtener_valor_columna(self, row, nombre):
        """
        Obtiene el valor de una columna considerando posible BOM
        """
        nombre_limpio = self.limpiar_nombre_columna(nombre)
        return row.get(nombre_limpio) or row.get('\ufeff' + nombre_limpio)

    # --- MODIFICACIÓN EN PROCESAR_CSV ---
    def procesar_csv(self, archivo_csv):
        """Lee un archivo CSV y genera recibos para todos los apartamentos."""
        if not os.path.exists(archivo_csv):
            print(f"Error: No se encontró el archivo {archivo_csv}")
            return

        # Crear directorio para los recibos
        directorio_recibos = 'recibos'
        if not os.path.exists(directorio_recibos):
            os.makedirs(directorio_recibos)

        try:
            with open(archivo_csv, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file, delimiter=';')
                
                # Verificar columnas requeridas
                columnas_encontradas = [self.limpiar_nombre_columna(col) for col in reader.fieldnames]
                print(f"Columnas en el archivo (limpias): {columnas_encontradas}")
                
                columnas_faltantes = [col for col in self.columnas_requeridas 
                                    if col not in columnas_encontradas]
                
                if columnas_faltantes:
                    print(f"Error: Faltan las siguientes columnas: {columnas_faltantes}")
                    return

                for row in reader:
                    try:
                        row_limpia = {self.limpiar_nombre_columna(k): v for k, v in row.items()}
                        
                        # --- NUEVA LÓGICA DE INTEGRACIÓN DE AGUA ---
                        depto = row_limpia['DEPTO']
                        if depto in self.datos_agua:
                            row_limpia['AGUA'] = self.datos_agua[depto]
                            print(f"Actualizado valor de agua para departamento {depto}")
                        else:
                            print(f"Advertencia: No se encontró agua para departamento {depto}")
                            row_limpia['AGUA'] = '0.00'  # Valor por defecto
                        
                        nombre_archivo = f"recibos/recibo_depto_{depto}_{row_limpia['FECHA'].replace('/', '_')}.pdf"
                        self.generar_recibo(row_limpia, nombre_archivo)
                        print(f"Recibo generado: {nombre_archivo}")
                    except Exception as e:
                        print(f"Error al procesar fila: {e}")
                        print(f"Datos de la fila: {row}")

        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    generador = GeneradorRecibos()
    generador.procesar_csv('apartamentos.csv')
    