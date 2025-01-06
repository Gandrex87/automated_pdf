# Generador de Recibos en PDF

Una herramienta para generar recibos de pago en formato PDF a partir de datos almacenados en archivos CSV/Excel. Este proyecto está diseñado para facilitar la emisión de recibos para administradores de propiedades, condominios o cualquier entorno donde se requiera crear recibos de forma automatizada.

---

## Características

- **Generación automática de recibos en PDF:**
  - Incluye detalles como fecha, propietario, departamento, teléfono y conceptos de pago (expensas, agua, multas).
  - Calcula automáticamente el total de los conceptos proporcionados.

- **Procesamiento de archivos CSV:**
  - Lee datos desde un archivo CSV y verifica que contenga las columnas requeridas.
  - Maneja archivos CSV con codificación `utf-8-sig` (soporte para BOM).

- **Formato profesional:**
  - Utiliza tablas y estilos personalizados para generar recibos claros y visualmente atractivos.

- **Gestión de directorios:**
  - Almacena los recibos generados en un directorio llamado `recibos`.

---

## Requisitos

- **Python 3.x**
- Librerías:
  - [`reportlab`](https://pypi.org/project/reportlab/)

Para instalar la dependencia necesaria:

```bash
pip install reportlab
```

## Mejoras Futuras

- [ ] Anexar valor variable del precio del agua.
- [ ] Generacion y anexar QR al recibo de pago.
- [ ] Funcionalidad para enviar recibos por WhatsApp automáticamente.
