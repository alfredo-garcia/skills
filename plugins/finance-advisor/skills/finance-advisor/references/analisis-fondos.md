# Marco de análisis de fondos y ETFs

## 1. Entender la petición

Antes de analizar, aclara (o deduce del perfil) qué quiere el usuario:
- ¿Analizar un fondo concreto que ya tiene o que le recomendaron?
- ¿Comparar dos o más fondos?
- ¿Encontrar el mejor fondo para un hueco de la cartera (p. ej. "renta fija global", "emergentes")?
- ¿Decidir si vender/cambiar un fondo?

Y en qué plataforma lo compraría. Un fondo excelente que no se puede comprar en su bróker no sirve.

## 2. Obtener datos actuales (búsqueda web obligatoria)

Fuentes, por orden de preferencia:
1. Web oficial del gestor: ficha mensual (factsheet), KID/KIID, folleto.
2. justETF (ETFs UCITS), Morningstar, trackingdifferences.com.
3. Para fondos locales: regulador del país (CNMV, Superfinanciera, CNBV, CMF, SEC…) o la bolsa local.

Datos a recoger (sin inventar ninguno; si falta, dilo):
- Nombre, ISIN/ticker, gestora, domicilio, fecha de creación.
- Índice que replica (o estrategia si es activo).
- TER / gastos corrientes, y comisiones de entrada/salida/custodia de la plataforma.
- Patrimonio (tamaño) del fondo.
- Método de réplica: física completa, muestreo o sintética (swap).
- Política de dividendos: acumulación o distribución.
- Divisa del fondo y si está cubierto (hedged).
- Tracking difference de varios años (no solo el TER).
- Rentabilidad y volatilidad a 1, 3, 5, 10 años; máxima caída.
- Número de posiciones, top 10, reparto geográfico y sectorial.
- Para renta fija: duración, calidad crediticia media, rentabilidad a vencimiento.

## 3. Evaluarlo en contexto

| Criterio | Qué mirar | Por qué importa |
|---|---|---|
| Coste total | TER + tracking difference + comisiones de la plataforma | La comisión es la única variable garantizada; 1% anual durante 30 años se come ~25% del capital final |
| Solapamiento | Coincidencia de posiciones con lo que ya tiene | Dos fondos "distintos" pueden ser casi la misma apuesta |
| Encaje con la asignación objetivo | ¿Acerca o aleja la cartera de su perfil? | Comprar algo bueno puede desequilibrar el conjunto |
| Fiscalidad | Domicilio, acumulación/distribución, traspasos sin tributar, retenciones en origen, impuesto de sucesiones de EE. UU. | Varía mucho por país (ver jurisdicciones.md) |
| Riesgo divisa | Divisa del subyacente vs. divisa de gasto del usuario | Relevante sobre todo en renta fija y monedas volátiles |
| Tamaño y antigüedad | Fondos pequeños (<100 M) o muy nuevos tienen riesgo de cierre | Un cierre puede forzar una venta con impuestos |
| Gestión activa | Si es activo: ¿supera a su índice tras costes a 10+ años? | La mayoría no lo consigue (informes SPIVA de S&P Dow Jones Indices) |

## 4. Formato de respuesta

1. **Veredicto en una línea** (p. ej. "Buen fondo, pero duplica lo que ya tienes en X").
2. **Ficha resumida** del fondo (tabla con los datos clave y fuente).
3. **Encaje en tu cartera**: solapamiento, efecto en la asignación, fiscalidad.
4. **Alternativas** disponibles en sus plataformas si las hay mejores, con comparación en tabla.
5. **Próximos pasos** concretos (p. ej. "traspasar X a Y en MyInvestor, sin tributar").
6. **Fuentes** con enlace.

Para comparaciones, usa una tabla con las mismas filas para todos los fondos. Si calculas el impacto de las comisiones a largo plazo, hazlo con código y muestra los supuestos.

## 5. Señales de alerta

Señálalas siempre que aparezcan:
- TER > 1% en un fondo indexado, o > 1,5% en uno activo sin historial que lo justifique.
- Comisiones de entrada/salida o de éxito.
- Productos estructurados, fondos garantizados o seguros de ahorro con costes poco transparentes.
- Productos apalancados o inversos para largo plazo.
- Fondos recomendados por el propio banco cuyos costes son claramente superiores a alternativas equivalentes.
