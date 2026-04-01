# Enclosure Management Guide (JWE2)

## Comfort System
Dinosaur comfort is the core health metric of an enclosure. Low comfort causes fence attacks and escapes. Comfort is split into two categories:

**Environmental Needs** — food, water, terrain type, foliage
**Territorial Needs** — enclosure size, population count, cohabitation species

To view a dinosaur's needs: scan it with a Ranger Team, click the dinosaur, then click the cloud icon. Red bars indicate unmet needs.

Needs only have to be barely in the white (just above the threshold) to count as satisfied — you don't need to maximise every stat.

## Territory
When released, a dinosaur wanders the enclosure until it reaches 100% comfort, at which point its territory is fixed. It is unlikely to leave that territory once established. This means you can zone large enclosures — designing one area for species A and another for species B — and they will naturally separate once settled.

Territories decay faster when they overlap a disliked species' territory, or when the area doesn't meet the dinosaur's needs.

## Environmental Setup

### Terrain
Each species requires a specific terrain type. Use the Paint tool in the Environment menu to apply sand, rock, grassland, or wetland. Paintable terrain (sand, rock) is treated as open space.

A larger enclosure is more forgiving on terrain proportions — if a species is struggling to reach its terrain threshold, expanding the enclosure helps.

### Water
All dinosaurs require water. Add a pond or small lake. For marine reptiles, water requirements are much larger.

### Food
- Herbivores: ground fiber, ground leaf, or ground fruit placed around the enclosure. Add more than you think you need — these are consumed over time.
- Carnivores: a single live prey feeder (for large carnivores) or carnivore feeder (for small carnivores) is typically sufficient.
- Place multiple feeders in cohabitation enclosures — dominant animals will bully others away from a single feeder, causing stress and starvation.

### Foliage
Trees and plants serve two purposes: meeting forest requirements and providing cover. Pre-populate the enclosure with foliage before releasing dinosaurs — comfort values for forest coverage only update as the dinosaur moves through that area.

## Fence Types and Security
Fences have security ratings from 2 to 5. If a dinosaur's security rating exceeds the fence's, it can break out. Electrified fences increase the security rating; unpowered electric fences drop to a lower base rating.

- Small theropods (Velociraptor, Dilophosaurus) will climb non-electrified fences; electrifying prevents this
- Large theropods headbutt fences and gates
- Thyreophorans (Stegosaurus, Ankylosaur) use tail attacks
- Unhappy dinosaurs will continuously attack fences, injuring themselves if the fence holds

When replacing a fence panel, it temporarily disappears — dinosaurs can escape during this window. Plan replacements carefully.

## Cohabitation
Check the Territory tab of any dinosaur to see Liked, Neutral, and Disliked species.

- **Liked species** cohabit peacefully and never fight (with rare exceptions like Compies being eaten by small carnivores)
- **Neutral species** raise each other's cohabitation stress meter — too many neutral species together will trigger a Cohabitation Issue alert
- **Disliked species** will fight to the death

Most herbivores can tolerate one neutral species before hitting the stress threshold. The **Tolerant** trait gives +30% cohabitation comfort with neutral species, effectively allowing one extra neutral cohab.

Enclosure size matters for cohabitation — a dinosaur may not tolerate as many species in a small enclosure as it would in a large one.

## Population and Social Needs
Each species has a minimum and maximum social count (same species) and a population count (all species). Exceeding the maximum triggers stress. Falling below the minimum also triggers stress for social species.

Release enough of a species to meet social minimums before expecting stable comfort.

## Ranger Posts
Assign a Ranger Team to a post inside each enclosure. Rangers will automatically scan dinosaurs within the post's radius, keeping comfort data current. One scan covers all dinosaurs in the territory once completed.

## Enclosure Types
- **Land enclosures**: fenced areas for most species
- **Aviaries**: modular domed structures for flying reptiles; can be linked; require at least one internal Hatchery
- **Lagoons**: for marine reptiles; require large water areas

## Escape Prevention Checklist
- Fence security rating ≥ dinosaur security rating
- Enclosure is electrified and has reliable power
- All comfort needs are met (no red bars)
- Population is within min/max range
- No disliked species sharing the enclosure