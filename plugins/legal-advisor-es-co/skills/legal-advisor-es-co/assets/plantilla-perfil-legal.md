# Plantilla: perfil-legal.md

Es el **expediente de conocimiento** del usuario: todo lo que sabes de su situación legal, sus objetivos, lo que ya se ha concluido y la normativa comprobada, en un único archivo. El usuario lo descarga, lo guarda y lo mantiene en los archivos del proyecto para que cada conversación empiece sabiendo todo esto. Escríbelo para que cualquier sesión futura (o un abogado al que el usuario se lo pase) pueda trabajar con él sin preguntar de nuevo lo que ya está resuelto.

Usa esta estructura al crear o actualizar el perfil. Deja "Pendiente de confirmar" en lo que no se sepa; no inventes datos. Nunca anotes números de documento, NIF/NIE/NIT, IBAN ni contraseñas: solo tipos, vigencias y estados.

```markdown
# Perfil legal — [Nombre o alias]
Última actualización: AAAA-MM-DD

## Resumen de situación
3-5 líneas: nacionalidad, dónde vive, estatus migratorio, residencia fiscal probable en cada país, trabajo, gestiones abiertas más importantes.

## Objetivos del usuario
Lo que quiere conseguir. Toda recomendación se orienta a estos objetivos; si una gestión no sirve a ninguno, pregúntate si hace falta.

| # | Objetivo | Horizonte / fecha límite | Prioridad | Vía legal elegida o en estudio | Bloqueos / requisitos pendientes | Gestiones vinculadas | Estado |
|---|---|---|---|---|---|---|---|
| O1 | p. ej. Residencia permanente en Colombia (visa R) | 2032 | Alta | Visa M inversionista → R | Confirmar registro IED de inmueble | gestion-2026-11-visa-m | En curso |

**Preferencias y límites** (lo que el usuario quiere evitar o priorizar): p. ej. no perder derechos en España, mínima burocracia, no aportar más capital, privacidad, plazos personales (viajes, familia).

**Objetivos descartados o cumplidos**: [objetivo, fecha, motivo] — no los borres: explican decisiones pasadas.

## Calendario de vencimientos
| Fecha | Qué vence o toca | País | Acción necesaria | Estado |
|---|---|---|---|---|
| | Visa o autorización de residencia | CO / ES | Renovar o cambiar de tipo | |
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
| Expediente | Objetivo | Organismo | Abierto | Próximo paso | Estado |
|---|---|---|---|---|---|

## Conclusiones y decisiones
Lo ya analizado y decidido, para no repetir el estudio desde cero. Cada entrada con fecha, nivel de certeza y la norma en que se apoya.

| Fecha | Cuestión | Conclusión | Certeza | Base (norma / fuente) | Revisar si… |
|---|---|---|---|---|---|
| | p. ej. ¿La compra del inmueble es IED registrable? | | 🟡 | Decreto 1068/2015 art. 2.17.1.2 | cambia la circular DCIP-83 |

## Normativa verificada
Normas y cifras comprobadas en fuente oficial. Que algo esté aquí no exime de volver a comprobar su vigencia antes de basar una decisión en ello, pero sirve para citar con precisión y detectar cambios.

| Tema | Norma / dato | Contenido relevante para el usuario | Enlace oficial | Verificado | Cambios detectados |
|---|---|---|---|---|---|
| Visas CO | Resolución 5477 de 2022 y modificaciones | | | AAAA-MM-DD | |
| Tarifas visas CO | Resolución de tarifas del año | | | | |
| SMMLV / UVT del año | | | | | |
| Residencia cambiaria | Decreto 1068 de 2015, art. 2.17.1.2 | | | | |
| Residencia fiscal ES / CO | LIRPF art. 9 / E.T. art. 10 | | | | |

## Datos que faltan
Preguntas pendientes para el usuario, ordenadas por impacto en sus objetivos.
- [ ] 

## Profesionales de referencia
- [Rol, país, cómo contactar] (solo si el usuario los ha indicado)

## Historial de cambios
- AAAA-MM-DD: Perfil creado a partir de [conversación / documentos].
```

## Reglas de actualización

- Al final de cada conversación en la que hayas aprendido algo duradero (un dato, un objetivo, una conclusión, una norma verificada, un avance en una gestión), entrega la versión **completa** actualizada como archivo descargable (ver SKILL.md, "Guardar y entregar el expediente").
- Objetivos: actualiza su estado y sus bloqueos cuando avance una gestión; pasa a "descartados o cumplidos" en lugar de borrar.
- Conclusiones: si una conclusión cambia, no la sobrescribas: añade la nueva fila y marca la anterior como superada, con el motivo.

- Cambia la fecha de "Última actualización" en cada versión y añade una línea al historial.
- Mantén el calendario de vencimientos ordenado por fecha; marca lo hecho como "Hecho" en vez de borrarlo hasta la siguiente renovación.
- Recalcula la tabla de residencia fiscal con `scripts/contar_dias.py` cada vez que cambie `viajes.csv`.
- Riesgos y gestiones: marca Resuelto / En curso / Pendiente / Descartado.
