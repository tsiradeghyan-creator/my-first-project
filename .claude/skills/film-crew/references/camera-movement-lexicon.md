# Camera movement lexicon — precise moves and how to write them for AI

Write every move as **rig + height + start → path + speed + motivation → end**. One dominant move per shot or
timed slice. "Static" is a choice, often the strongest one.

## Base moves

| Move | What it does | Write it as |
|---|---|---|
| Locked-off static | Lets action and composition speak; tension through stillness | "Locked-off tripod shot at eye level; the camera does not move." |
| Pan | Rotates horizontally from a fixed point; follows or reveals | "The camera pans slowly 40° left from the door to the window, following her walk, and settles." |
| Tilt | Rotates vertically; scale, reveal | "Slow tilt up from the boots to the face, ending in a medium close-up." |
| Push-in (dolly in) | Moves toward the subject; growing importance/pressure | "Slow dolly push-in from medium shot to close-up over 6 s, timed with her realisation." |
| Pull-out (dolly out) | Moves away; isolation, reveal of context | "The camera dollies straight back from his face, revealing the empty hall around him." |
| Tracking / trucking | Moves alongside or with a subject | "Lateral tracking shot at walking pace, camera-left of him, hip height, keeping him in the right third." |
| Follow (behind) | Moves behind a subject into space | "Steadicam follows one metre behind her shoulder through the corridor." |
| Lead (in front) | Moves backwards in front of a walking subject | "The camera walks backward ahead of them as they talk, two-shot, constant distance." |
| Crane / jib up/down | Height change; scale, opening/closing | "Crane rises from the table top to a high wide shot of the whole square." |
| Arc / orbit (partial) | Circles around a subject; shift of perspective | "Slow 90° arc to the right around the table, keeping both faces in frame." |
| Handheld | Instability, presence, documentary | "Handheld with slight breathing drift, close, reacting late to movement." |
| Zoom (optical) | Changes focal length, not position; flattens | "Slow optical zoom in from wide to medium, camera position fixed." |
| Rack focus | Shifts attention without moving | "Focus racks from the glass in the foreground to her face in the background." |

## Signature and non-standard moves (use with intent)

| Move | Typical owner (lens) | Write it as |
|---|---|---|
| One-point perspective glide | Kubrick | "Symmetrical one-point-perspective corridor, 18mm wide lens, Steadicam glides forward at hip height at a steady, unhurried pace." |
| Low Steadicam chase | Kubrick (The Shining) | "Steadicam 50 cm above the floor follows the boy's tricycle around the corridor corner, constant speed." |
| Slow reverse zoom from detail | Kubrick (Barry Lyndon) | "Starts on a close detail and slowly zooms out over 10 s to a painterly wide tableau; the camera does not move." |
| Trunk shot | Tarantino | "Low angle from inside an open car trunk, looking up at two men leaning in; sky behind them." |
| Circling dialogue shot | Tarantino (Reservoir Dogs diner) | "Slow continuous circling track around the seated group at table height while they talk." |
| Overhead god's-eye | Tarantino, Wes Anderson, Scorsese | "Directly overhead, top-down 90°, the figure lies centred in frame." |
| Crash / snap zoom | Tarantino (Kill Bill), Wes Anderson, Scorsese | "Sudden fast zoom in to an extreme close-up of her eyes, one beat, then hold." |
| Planimetric lateral track | Wes Anderson | "Camera faces the wall flat-on and tracks laterally left to right at constant speed past rooms like a dollhouse cross-section." |
| Whip pan | Wes Anderson, Scorsese, Spielberg | "Fast whip pan right with motion blur, landing on the second character in a centred medium shot." |
| Spielberg oner | Spielberg | "One continuous shot: the camera dollies and pans as the characters move, re-framing from wide to two-shot to close-up without a cut." |
| Push-in on a face (the reveal) | Spielberg | "Slow push-in on his face as he looks up in awe, backlit, ending in a close-up." |
| Dolly zoom (vertigo) | Hitchcock, Spielberg | "Dolly zoom: the camera dollies back while zooming in, so her face stays the same size and the corridor stretches behind her." |
| Long Steadicam/backstage oner | Scorsese (Goodfellas) | "One unbroken Steadicam shot follows the couple from the street, through the kitchen, into the club." |
| Freeze frame | Scorsese | (edit effect) "The frame freezes on his face mid-laugh." |
| Extreme close-up of eyes ↔ extreme wide | Leone | "Extreme close-up of the gunfighter's eyes, then cut to an extreme wide shot of three tiny figures in the arena." |
| Slow lateral track through elements | Tarkovsky | "Very slow lateral dolly along flooded ruins, water reflecting the light, 20 s, no cut." |
| Step-printed smear motion | Wong Kar-wai | "Handheld, low shutter speed and step-printed motion blur; the crowd smears, the subject stays readable." |
| Frame within a frame through obstructions | Wong Kar-wai | "Observed through a half-open doorway and a hanging curtain; she is framed small in the gap." |
| Precise motivated micro-move | Fincher | "Dolly moves exactly with the actor's step forward and stops when he stops; the move is almost invisible." |
| Impossible glide through objects | Fincher (Panic Room) | "Continuous camera glide through the stair rails and through the handle of the coffee pot, one take." (high AI risk — prefer a mask transition) |
| Monumental slow push | Villeneuve | "Extremely wide shot, a tiny figure in fog before a massive brutalist structure; very slow push-in over 12 s." |
| Static tableau, frontal | Parajanov | "Static frontal camera, flat staging like a living icon; figures face the lens and perform one ritual gesture." |

## Speed words the models follow

"imperceptibly slow", "slow and steady", "unhurried", "constant walking pace", "sudden", "snap", "ease in and
settle", "decelerates to a stop on her face".

## AI risk notes

- Full 360° orbits, very fast moves with several people, and moves through solid objects degrade identity and
  geometry — split them, shorten them, or hide the join with a mask/whip transition.
- Zoom and dolly are different; write "optical zoom, camera position fixed" when you mean zoom.
- Give the end of the move ("…and stops on her hands"): models drift if the move has no destination.
