---
name: Tim Sullivan product folio
description: Actual software interfaces and inspectable decisions.
colors:
  paper: "#eeeee7"
  ink: "#222720"
  muted: "#575e53"
  forest: "#173d33"
  line: "#c7cbc0"
  accent: "#9e4427"
typography:
  body:
    fontFamily: "Instrument Sans, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  display:
    fontFamily: "Instrument Sans, sans-serif"
    fontSize: "clamp(50px,5.3vw,84px)"
    fontWeight: 500
    lineHeight: 1.04
    letterSpacing: "-.035em"
---
# Design System: Product folio

## Overview
The portfolio combines a Boston building study, product screenshots, fictional report examples and public code. Lasting Ground is the main project.

## Colors
Paper and ink carry the page. Forest frames product captures; pale source and output surfaces separate supplied input from generated text. The rust accent is reserved for small punctuation and focus.

## Typography
Self-hosted Instrument Sans is used throughout the portfolio. Headings use medium weight and close tracking; body text uses regular weight. Source excerpts retain their exact words.

## Layout
The opening desktop composition places the title beside a dimensional product scene. At 720px the scene follows the heading; at 400px the heading becomes a single column. The existing evidence and report grids retain their 680px and 1000px breakpoints. Side space is clamp(22px,4vw,72px). The maximum main width is 1600px.

## Product scene
The opening scene uses local Three.js geometry: a beveled interface frame, source card and separate report sheets. The screen dominates the overview. Each focused view brings one artifact forward; desktop drag rotates the group. Actual desktop and mobile product captures are used at their respective sizes. The source card is drawn from the exact fictional input; the report uses the existing PDF page renders. Soft procedural contact shadows and restrained metal reflections provide depth.

Native buttons, canvas arrow keys and desktop object selection operate the same four views. Reduced motion applies the target pose immediately. Touch scrolling is retained. Rendering occurs on interaction, short focus transitions, resize and visibility return; no idle animation. A settled frame is cached as an exact renderer image so the composition stays stable through browser compositing changes. Graphics failure exposes the original artifact image and direct links. A persisted pagehide preserves the scene for browser Back navigation; ordinary unload releases its resources.

## Shapes
Product images have gently rounded corners. Layout divisions use single rules. The report and example output use a paper treatment.

## Components
The capture selector changes actual product images and their context captions. The source example changes between two precomputed fictional cases; it does not retrieve records. Preserve visible states, keyboard focus, useful defaults without JavaScript and error text. Supporting engineering notes share the type and surface treatment.

## Do's and Don'ts
Show actual work and label fictional examples. Keep source dates and access limits attached to captures. Keep Lasting Ground as the flagship and GroundTruth-Geo as supporting evaluation. Do not replace truthful evidence with decorative terrain or invent production outcomes.

## Building study
The homepage opens with a separate model of 540 City of Boston building records. Visitors can switch between volume and plan, select a building and follow its city-record link. The model uses simplified building shapes and is not a survey.
