# Prompt library

Each prompt below is a sentence a client can send as it stands. The tools this fork adds carry prompts; an inherited tool is described by its parameters and its own page.

## Element registers

### Export element ID register

```text
Export the ID register of drawn model components to Excel, ordered by category, family and type
```

## Model editing

### Create level

```text
Create a level named 4F at 15000 mm
```

### Create floor

```text
Create a floor on 2F from these four points
```

## Phases

### Set element phases

```text
Mark these elements as demolished in the Existing phase
```

### Merge project phases

```text
Merge phase 1 into New Construction
```

## Id management

### Replace IDs in place

```text
Give these 27 standalone components new ids
```

### Rebuild IDs in new models

```text
Rebuild the selectable components into E:\out\copy-{n}.rvt, ten copies, no id shared between them
```

```text
Rehearse the rebuild first: how many components, which new id range, write nothing yet
```

## View settings

### Set view lighting

```text
Turn on shadows in the 3D view, set the shadow intensity to 60, use a sky background and light the rendering with exterior sun
```

```text
Set the sun in {3D} to 2026-06-21 15:00 with a sunlight intensity of 80, and rehearse it first
```

```text
Fix the sun in lighting mode at azimuth 135° and altitude 45°, and turn on the ground plane at level 01
```

[Feature overview](index.md) · [Version support matrix](matrix.md) · [Prompt library](prompts.md)
