# Plantilla: perfil-legal.md

Usa esta estructura al crear o actualizar el perfil. Deja "Pendiente de confirmar" en lo que no se sepa; no inventes datos. Nunca anotes números de documento, NIF/NIE/NIT, IBAN ni contraseñas: solo tipos, vigencias y estados.

```markdown
# Perfil legal — [Nombre o alias]
Última actualización: AAAA-MM-DD

## Resumen de situación
3-5 líneas: nacionalidad, dónde vive, estatus migratorio, residencia fiscal probable en cada país, trabajo, gestiones abiertas más importantes.

## Calendario de vencimientos
| Fecha | Qué vence o toca | País | Acción necesaria | Estado |
|---|---|---|---|---|
| | Visa V | CO | Renovar / cambiar a M | |
| | Cédula de extranjería | CO | | |
| | Pasaporte | ES | Renovar en consulado | |
| | DNI | ES | | |
| | Declaración de renta | CO | Según últimos dígitos del NIT | |
| | Declaración IRPF / IRNR | ES | | |
| | Formulario 160 / modelo 720-721 | | | |
| | Seguro médico de la visa | CO | | |

## 1. Identidad y documentos
- Nacionalidad(es):
- Lugar y fecha de nacimiento (año basta):
- DNI: vigente hasta AAAA-MM-DD
- Pasaporte: vigente hasta AAAA-MM-DD
- Otros (licencia de conducir española, certificado digital FNMT, Cl@ve):

## 2. Situación migratoria en Colombia
- Visa: tipo V, subtipo [nómada digital / otro], expedida AAAA-MM-DD, vence AAAA-MM-DD
- Condiciones de la visa (actividades permitidas, beneficiarios):
- Cédula de extranjería: [sí/no], vigente hasta AAAA-MM-DD
- Primera entrada con esta visa:
- Seguro médico exigido: [aseguradora, cobertura, vencimiento]
- Plan migratorio: [renovar V / pasar a M / pasar a R / volver a España]
- Tiempo acumulado útil para visa R:

## 3. Domicilios y registros en España
- Empadronamiento: [municipio / dado de baja el AAAA-MM-DD]
- Matrícula consular: [no inscrito / no residente / residente desde AAAA-MM-DD] — consulado:
- PERE / CERA:
- Domicilio fiscal ante la AEAT: [España / Colombia — modelo 030 presentado AAAA-MM-DD]
- Bancos españoles informados de la no residencia: [sí/no]

## 4. Domicilio en Colombia
- Ciudad y tipo de vivienda: [arriendo / propia]
- Contrato de arrendamiento a su nombre: [sí/no]
- RUT (DIAN): [sí/no, responsabilidades]

## 5. Trabajo
- Tipo: [cuenta ajena / cuenta propia / ambas]
- Empleador: [nombre de la empresa, país, sector]
- Contrato: [indefinido / temporal], convenio colectivo:
- Lugar físico de trabajo: [Colombia / España / mixto]
- Autorización escrita de la empresa para teletrabajar desde Colombia: [sí/no/pendiente]
- Dónde se paga la nómina y en qué divisa:
- Otras actividades o clientes:

## 6. Seguridad Social y cobertura sanitaria
- Cotiza en: [España régimen general / RETA / Colombia / ninguno]
- Certificado de desplazamiento (convenio ES–CO): [sí/no, vigencia]
- Convenio especial con la Seguridad Social española: [sí/no]
- Cobertura sanitaria en España tras residir fuera:
- Cobertura en Colombia: [EPS / prepagada / seguro internacional] (detalle en la ficha del health-advisor)

## 7. Residencia fiscal
| Año | Días en Colombia | Días en España | Otros | Máx. 365 días en CO | Residente en ES | Residente en CO | Certeza |
|---|---|---|---|---|---|---|---|
- Fuente de los días: [viajes.csv actualizado AAAA-MM-DD / certificado de Migración]
- Centro de intereses económicos (dónde están ingresos y patrimonio principal):
- Familia (cónyuge/pareja e hijos menores, dónde residen):
- Certificados de residencia fiscal obtenidos: [DIAN / AEAT, año]
- Declaraciones presentadas: [año, país, modelo/formulario]
- Aplicación del Convenio España–Colombia (art. 4 desempate):

## 8. Familia
- Estado civil: [soltero / casado / unión marital de hecho / pareja]
- Pareja: nacionalidad, residencia, ¿beneficiaria de la visa?
- Hijos:
- Régimen económico / capitulaciones:
- Matrimonio inscrito en el Registro Civil Consular: [sí/no/n.a.]

## 9. Patrimonio con efectos legales
- Inmuebles: [país, uso (vivienda / alquiler / vacío)]
- Cuentas y valores en el exterior (país y orden de magnitud; detalle en perfil-inversor.md):
- Participaciones en empresas:
- Umbrales que pueden activar obligaciones: [formulario 160, modelo 720/721, impuesto al patrimonio]

## 10. Empresas y proyectos
| Sociedad / proyecto | País y forma | % | Rol (socio/administrador) | Desde dónde se administra | Estado |
|---|---|---|---|---|---|

## 11. Otros
- Licencia de conducir y situación en Colombia:
- Vehículos:
- Poderes notariales otorgados/recibidos:
- Testamento: [país, fecha]
- Procedimientos o requerimientos abiertos:

## Riesgos detectados
| Riesgo | Nivel de certeza | Consecuencia | Cómo resolverlo | Estado |
|---|---|---|---|---|

## Gestiones
| Expediente | Organismo | Abierto | Estado |
|---|---|---|---|

## Profesionales de referencia
- [Rol, país, cómo contactar] (solo si Al los ha indicado)

## Historial de cambios
- AAAA-MM-DD: Perfil creado a partir de [conversación / documentos].
```

## Reglas de actualización

- Cambia la fecha de "Última actualización" en cada versión y añade una línea al historial.
- Mantén el calendario de vencimientos ordenado por fecha; marca lo hecho como "Hecho" en vez de borrarlo hasta la siguiente renovación.
- Recalcula la tabla de residencia fiscal con `scripts/contar_dias.py` cada vez que cambie `viajes.csv`.
- Riesgos y gestiones: marca Resuelto / En curso / Pendiente / Descartado.
