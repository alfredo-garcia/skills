# Revisión metódica de exámenes

## Checklist
1. **Identificación**: tipo de prueba, fecha, laboratorio/centro, ayuno sí/no, médico solicitante si consta.
2. **Unidades y rangos**: usa los del propio informe. Conversiones frecuentes entre países:
   - Glucosa: mg/dL ↔ mmol/L (÷18).
   - Colesterol: mg/dL ↔ mmol/L (÷38,67). Triglicéridos (÷88,57).
   - Creatinina: mg/dL ↔ µmol/L (×88,4).
   - Hemoglobina: g/dL ↔ g/L (×10).
   - Vitamina D: ng/mL ↔ nmol/L (×2,5).
   España y Colombia suelen informar en mg/dL; algunos laboratorios europeos usan SI.
3. **Todos los valores**: fuera de rango, en el límite y patrones (p. ej. VCM bajo + ferritina baja; ALT/AST elevadas con GGT normal).
4. **Tendencia**: tabla con las fechas anteriores del proyecto. Un valor "normal" que ha cambiado mucho puede importar más que uno levemente alterado y estable.
5. **Factores de confusión**: ayuno, ejercicio intenso previo (CK, transaminasas), hidratación, ciclo, medicación (estatinas, metformina, IBP, anticonceptivos), suplementos (biotina altera pruebas tiroideas), altitud (por encima de ~2.000 m sube hemoglobina y hematocrito; ver `locations.yaml` → `altitude_m`), infección reciente.
6. **Coherencia clínica**: ¿explica los síntomas actuales? ¿Hay algo que el síntoma predice y no se ha medido?
7. **Qué falta**: pruebas que completarían el estudio, y cuáles son razonables pedir en atención primaria vs especialista.

## Formato de salida
1. Resumen en 2–3 líneas: lo importante primero.
2. Tabla: parámetro · valor · rango · fecha anterior · comentario.
3. Interpretación con niveles 🟢🟡🟠🔵.
4. Qué repetir o ampliar, cuándo y por qué vía.
5. Preguntas para llevar al médico.
6. Propuesta de actualización de ficha (personal o de dolencia).

## Imagen y otros informes
Traduce la terminología (p. ej. "hiperecogenicidad hepática difusa" → hígado más brillante en la ecografía, típico de acumulación de grasa). No reinterpretes imágenes por tu cuenta a partir de fotos; trabaja sobre el informe del especialista.
