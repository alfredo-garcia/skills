# Template: Claude Design prompt (Path A, Stage 1)

> **What this is:** the ready-to-paste prompt the user drops into Claude Design to get a good first prototype of one feature, built on the project's design system. ux-designer writes it at the start of Stage 1 on Path A, from the approved PRD, the agreed scope list, `ui_standards.md` and `ui_kit_registry.md`.
>
> **Language:** the prompt is written in `SDLC.md`'s `docs_language` (the UI copy too). Component, token and icon names stay exactly as in the registry and the design system.
>
> **Saved at:** `<features_root>/<id>_<slug>_claude_design_prompt.md`, with the feature's other documents (never in `prototypes/`, which projects usually gitignore), and shown in chat inside **one** fenced code block, nothing else inside it, so the user copies it in one go.

---

## Rules for writing it

- **Self-contained.** Claude Design hasn't seen the PRD or this conversation. Everything it needs is in the prompt; nothing like "see the PRD" or "as discussed".
- **Concrete, not descriptive.** Real copy (not "a title"), real example data that fits the product, exact component names from the registry, exact states.
- **Only what's in scope.** Screens and states from the PRD (§9 UI, §10 edge cases; Lite: §6, §7) and the agreed scope list. Nothing the PRD leaves out.
- **New components:** only those already announced and accepted in scoping, each with its `Tmp` name and one line on what it does. Anything else Claude Design would need must be flagged, not improvised.
- **Short.** Usually 30-70 lines. Bullets, not paragraphs.

## Structure (fill every block; drop a block only if it doesn't apply)

```text
Prototipo para [project name] · [project_id]/[id] · [Feature name]

DÓNDE
Trabaja en el lienzo "[App] · Screens". Crea una página nueva: "Propuesta [id] · [título]".
Parte de copias de estos artboards actuales y modifícalos: [página › artboard, …] (o "pantallas nuevas").
No toques las demás páginas.

DESIGN SYSTEM
Usa el design system "[claude_design_system]" (sobre "[claude_design_shared_system]"). Solo sus componentes, tokens e iconos.
Si necesitas algo que no existe, no lo improvises: márcalo en el lienzo como "COMPONENTE NUEVO" con una nota de qué hace.
Componentes nuevos ya aprobados para esta feature (puedes crearlos, con este nombre):
- TmpXxx: [qué hace, en una línea]

SUPERFICIE Y FORMATO
[web mobile-first 390×844 | Android | iOS | …]; [variantes de tamaño si las hay]; tema [claro/oscuro/ambos].
Voz: [del ui_standards: idioma, tratamiento, tono].

QUÉ ES ESTA FEATURE
[2-3 líneas: para quién, qué problema resuelve, qué cambia respecto a hoy.]
Fuera de alcance (no lo dibujes): [lista corta del PRD].

PANTALLAS (todas clicables entre sí)
1. [Nombre de pantalla] — [para qué sirve]
   - Contenido: [componentes del registry y copy real, en orden]
   - Estados: [vacío · cargando · éxito · error "[texto exacto]" · edge…]
   - Interacciones: [tap en X → pantalla N / abre sheet / …]
2. …

DATOS DE EJEMPLO
[valores realistas para rellenar las pantallas]

ENTREGA
- Un prototipo navegable con todas las pantallas enlazadas.
- Cada estado visible: un frame por estado o un selector de estado por pantalla.
- Al final, una lista: componentes del design system usados y cualquier "COMPONENTE NUEVO" que hayas marcado.
```

## What to tell the user around the block (outside it)

Before the block, one line: what it is. After it, the steps, in `docs_language`:

1. Abre el lienzo "[App] · Screens" ([claude_design_screens]). Si aún no existe: crea un lienzo de tipo Design con ese nombre, instala "[claude_design_shared_system]" y "[claude_design_system]", y pásame su URL para registrarla en `SDLC.md`.
2. Pega el prompt tal cual (crea la página de propuesta).
3. Itera allí lo que quieras; si quieres, tráeme los comentarios y te preparo el prompt de ajuste.
4. Cuando te guste, tráeme el resultado: link de compartir, export (HTML/PDF) o capturas.

## Follow-up prompts (Stage 2, feedback on Path A)

When the user brings feedback to apply in Claude Design, check it first (SKILL.md Stage 2), then give the change as another single copy-pasteable block:

```text
Cambios sobre el prototipo de [project_id]/[id]:
1. [Pantalla › elemento]: [cambio concreto, con el copy exacto si cambia].
2. …
Solo en la página "Propuesta [id] · [título]". Mantén el design system "[claude_design_system]"; no cambies nada más.
```

## Integration prompt (Stage 4, after merge)

```text
Integra la feature [project_id]/[id] en el lienzo "[App] · Screens":
0. Antes de nada, compara la propuesta con las páginas actuales que toca y dime si han cambiado desde que se hizo (otra feature integrada en medio); si es así, no sigas hasta que te diga cómo resolverlo.
1. Página "[Pantalla]": sustituye el artboard "[x]" por "[y]" de "Propuesta [id] · [título]"; añade "[z]".
2. Página nueva "[Pantalla nueva]" (si hay): con sus artboards en todos los estados y formatos, como las demás páginas.
3. Aplica estos cambios hechos durante la implementación: [desviaciones aprobadas, o "ninguno"].
4. Borra la página "Propuesta [id] · [título]".
No cambies nada más.
```
