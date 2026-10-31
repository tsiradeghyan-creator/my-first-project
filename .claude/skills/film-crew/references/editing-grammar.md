# Editing grammar — the rules that make shots cut

Classical continuity editing, written for AI generation. Break a rule only on purpose, and write the purpose down.

## Space

- **180° rule (axis).** Between two characters (or along a direction of travel) there is a line. Keep the camera
  on one side for the whole scene so left stays left. Cross only: on a visible camera move across the line, via a
  neutral shot straight on the line, via a cutaway, or deliberately for disorientation.
- **Screen direction.** A character exiting frame-right enters the next shot frame-left. A car driving L→R keeps
  driving L→R until we see it turn.
- **Eyeline match.** If A looks frame-right at B, B's reverse looks frame-left at A, at a matching height (look up
  to the standing, down to the seated).
- **Establish, then go closer.** A wide/establishing shot fixes geography before close coverage — unless the lens
  or the director wants disorientation (then withhold it on purpose).

## Size and angle

- **30° rule.** Between two shots of the same subject change the angle by at least 30°, or
- **Two-step size change.** Change the shot size by at least two steps (WS → MS, MS → CU). Same size + same angle
  = jump cut. Use a jump cut only as a style (Godard, Wong Kar-wai, Scorsese montage).
- Shot sizes: EWS · WS · FS (full) · MWS (cowboy) · MS · MCU · CU · ECU · insert.

## Time and action

- **Cut on action.** Cut in the middle of a movement (hand reaching, door opening, head turning); the motion hides
  the cut. Let A show the start of the motion and B its completion, overlapping by a few frames.
- **Match on action.** The same action continues across a size/angle change.
- **Entrances and exits.** Let a character clear frame (or enter an empty frame) to make a clean cut and an
  ellipsis of time.
- **Reaction is a shot.** Cut to the listener; the line is heard, then the face reacts.
- **Inserts and cutaways** compress time and hide continuity problems.

## Match cuts and transitions

- **Graphic match:** shape/colour/composition of A's last frame matches B's first (moon → coin, eye → tunnel).
- **Motion match / whip:** the motion vector at A's end continues into B's start (swing right → swing right).
- **Smash cut:** abrupt contrast in sound and image, usually after a held quiet moment.
- **Dissolve / fade:** time passing, memory, ending. Overuse kills it.
- **Mask/wipe:** an object or body covers the lens and reveals the next shot.
- **Title card / chapter:** structural break (Tarantino, Wes Anderson, Parajanov).

## Sound across cuts

- **J-cut:** B's sound starts under the end of A (we hear the next scene first).
- **L-cut:** A's sound continues over the start of B (the line finishes over the listener's reaction).
- **Sound bridge:** one continuous sound (rain, train, music) carries a scene change.
- **Constant ambience** inside a set makes picture cuts invisible.

## Rhythm

- Average shot length (ASL) is a style decision: very long (Tarkovsky, Kubrick, Parajanov tableaux) → long
  holds; fast (action, Scorsese montage) → 1-3 s bursts. Vary rhythm inside a scene: hold → accelerate → hold.
- A shot is as long as its action plus the beat after it. Do not cut away from a reaction before it lands.

## The handoff contract (one per cut)

```
CUT N→N+1 | type: <cut type>
A ends: <the exact last frame: who, where in frame, size, pose, motion state>
B starts: <the exact first frame>
axis: <side kept / crossed how> | screen direction: <kept> | eyeline: <direction and height>
size/angle change: <from → to, why it is not a jump cut>
light: <key side, quality, colour — same/changed and why>
wardrobe/props: <states at the cut>
motion: <vector carried across, speed>
sound: <J / L / bridge / hard / constant ambience>
generation: <same call | first-frame chain | extension | bridge | independent>
```

## Virtual-cut checklist (table read)

For each cut: axis · screen direction · eyeline · size/angle change · light · wardrobe · props · motion · sound ·
generation method feasible. Any "no" is fixed before hand-over.
