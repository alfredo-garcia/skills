# Residencia fiscal y obligaciones formales (España–Colombia)

Esta referencia cubre **quién puede gravar y qué hay que presentar**. La estrategia sobre inversiones (qué productos, cuándo vender) es del finance-advisor. Verifica cada año tramos, valores de la UVT, umbrales y calendarios en la fuente oficial.

## Criterios de residencia

**España (art. 9 LIRPF)** — es residente quien, en el año natural:
- permanece más de 183 días en territorio español (las ausencias esporádicas se computan salvo que acredite residencia fiscal en otro país con certificado), o
- tiene en España el núcleo principal o la base de sus actividades o intereses económicos, o
- (presunción, salvo prueba en contrario) tiene en España a su cónyuge no separado legalmente y a sus hijos menores dependientes.
- Ojo a la regla de paraísos fiscales (art. 8.2 LIRPF): comprueba que Colombia no figure en la lista vigente de jurisdicciones no cooperativas.
- La residencia en España es por **año natural completo**, sin fraccionamiento (salvo casos especiales).

**Colombia (art. 10 Estatuto Tributario)** — es residente quien:
- permanece en el país más de 183 días calendario, continuos o discontinuos, incluyendo días de entrada y salida, **dentro de cualquier periodo de 365 días consecutivos**. Si ese periodo abarca dos años gravables, es residente en el segundo.
- Los criterios adicionales (familia, patrimonio, ingresos de fuente nacional) aplican sobre todo a nacionales colombianos.
- Los residentes tributan por su **renta mundial** y patrimonio mundial; los no residentes, solo por la de fuente colombiana.

**Conteo**: usa `scripts/contar_dias.py`. Pide certificado de movimientos migratorios a Migración Colombia si Al no tiene un registro fiable.

## Doble residencia: Convenio España–Colombia

Convenio para evitar la doble imposición entre España y Colombia (firmado en 2005, en vigor desde 2008; verifica protocolos posteriores).
- **Art. 4 (desempate)**: vivienda permanente → centro de intereses vitales → morada habitual → nacionalidad → acuerdo amistoso. Ojo: la nacionalidad española de Al juega a favor de España solo si los criterios anteriores no deciden.
- **Rentas del trabajo dependiente (art. 15 en el modelo)**: en general tributan donde se **realiza físicamente** el trabajo. Si Al reside en Colombia y trabaja desde Colombia para una empresa española, Colombia puede gravar el salario; España solo en casos limitados. Comprueba la redacción concreta del convenio y si hay excepciones (183 días, pagador, establecimiento permanente).
- **Retenciones en España**: si Al deja de ser residente en España, su empleador debería dejar de aplicar retenciones de IRPF y, en su caso, aplicar IRNR o ninguna según el convenio. Se comunica con el **modelo 147** (comunicación de cambio de residencia a efectos de retenciones) y se acredita con el **certificado de residencia fiscal** colombiano (de la DIAN). Verifica modelo y procedimiento vigentes.
- **Eliminación de la doble imposición**: en Colombia, descuento por impuestos pagados en el exterior (art. 254 E.T.); en España, deducción por doble imposición internacional (art. 80 LIRPF) si sigue siendo residente.

## Obligaciones formales típicas

### España
- **Cambio de domicilio fiscal**: modelo 030 (o la vía vigente en la sede de la AEAT) para comunicar el domicilio en el extranjero.
- **Si sigue siendo residente**: IRPF anual (renta mundial), modelo 720 (bienes en el extranjero por encima de 50.000 € por bloque) y 721 (cripto en el extranjero), según proceda.
- **Si es no residente**: IRNR (modelo 210) por rentas obtenidas en España: alquileres, imputación de rentas por inmuebles no alquilados (no vivienda habitual), ganancias en España. Bancos: comunicar la no residencia para que apliquen la fiscalidad correcta.
- **Año del cambio**: en el año en que se marcha puede seguir siendo residente en España todo el año si pasa allí más de 183 días o mantiene el centro de intereses. Planifica la fecha de salida.
- **Impuesto de salida** (art. 95 bis LIRPF): afecta a quien tiene participaciones de gran valor y ha sido residente mucho tiempo; comprueba umbrales si Al tiene participaciones relevantes.

### Colombia
- **RUT** (Registro Único Tributario, DIAN): necesario para declarar, facturar, abrir ciertos productos financieros y para el certificado de residencia fiscal.
- **Declaración de renta de personas naturales** (formulario 210 para residentes; 110 para no residentes, verifica): obligada si supera topes de patrimonio, ingresos, consumos o consignaciones expresados en UVT. Calendario según los últimos dígitos del NIT.
- **Declaración anual de activos en el exterior** (formulario 160): para residentes con activos en el exterior por encima del umbral en UVT.
- **Impuesto al patrimonio**: personas naturales con patrimonio líquido por encima del umbral en UVT (Ley 2277 de 2022).
- **Régimen cambiario** (Banco de la República): la residencia cambiaria tiene su propio criterio (permanencia continua de más de 6 meses, verifica). Determina cómo canalizar divisas, si las cuentas en el exterior deben registrarse como "cuentas de compensación" y cómo se registran inversiones.
- **Información exógena y facturación electrónica** si tiene actividad económica en Colombia.

## Señales de riesgo a vigilar en el perfil

- Empadronado en España + residente fiscal en Colombia sin certificado: riesgo de que la AEAT le reclame como residente.
- Empresa española aplica retenciones de IRPF a un empleado que ya es residente en Colombia: doble tributación sin corregir.
- Más de 183 días en Colombia y sin RUT ni declaración de renta: incumplimiento ante la DIAN.
- Activos en España (cuentas, fondos, inmueble) sin formulario 160 cuando procede.
- Cambios de residencia a mitad de año sin planificar.

Fuentes: agenciatributaria.es (residencia fiscal, modelos 030, 147, 210, 720, 721; texto del convenio), boe.es (LIRPF, convenio), dian.gov.co (RUT, formularios, calendario, valor de la UVT, certificado de residencia fiscal), secretariasenado.gov.co (Estatuto Tributario), banrep.gov.co (régimen cambiario).
