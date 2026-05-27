# Draw.io Style Snippets (Thesis Technical Route)

Use black/white, solid boxes, dashed section frames, and orthogonal connectors.

## Box (module)

```
rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;
align=center;verticalAlign=middle;fontSize=14;
```

## Box (emphasis)

Add `fontStyle=1;` (bold).

## Text (title / section title)

```
text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;
fontSize=16;fontStyle=1;fontColor=#000000;
```

Main title: `align=center;fontSize=20;`.

## Dashed frame (outer or section)

```
rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=2;
dashed=1;dashPattern=6 4;
```

Outer frame can use a slightly longer dash: `dashPattern=8 4;`.

## Edge (solid)

```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;html=1;
strokeColor=#000000;strokeWidth=2;endArrow=classic;endSize=8;
```

## Edge (dashed / auxiliary)

Add `dashed=1;` (optional `dashPattern=6 4;`).
