"""
rita/inflector.py — Inflector for RiTa

Python port of ritajs/src/inflector.js
"""

import re
import json
import os


# ---------------------------------------------------------------------------
# Rule helpers (mirrors Util.RE in ritajs/src/util.js)
# ---------------------------------------------------------------------------

class _Rule:
    """A pattern/replacement rule pair."""
    __slots__ = ("pattern", "trim", "add")

    def __init__(self, pattern, trim, add=""):
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.trim = trim
        self.add = add

    def applies(self, word):
        return bool(self.pattern.search(word))

    def fire(self, word):
        if self.trim == 0 and self.add == "":
            return word
        return word[: len(word) - self.trim] + self.add


def _RE(pattern, trim, add=""):
    return _Rule(pattern, trim, add)


# ---------------------------------------------------------------------------
# MASS_NOUNS (mirrors RiTa.MASS_NOUNS in ritajs/src/rita.js)
# ---------------------------------------------------------------------------

MASS_NOUNS = {
    "abalone", "asbestos", "barracks", "bathos", "breeches", "beef", "britches",
    "chaos", "chinese", "cognoscenti", "clippers", "corps", "cosmos", "crossroads",
    "diabetes", "ethos", "gallows", "graffiti", "herpes", "innings", "lens",
    "means", "measles", "mews", "mumps", "news", "pasta", "pathos", "pincers",
    "pliers", "proceedings", "rabies", "rhinoceros", "sassafras", "scissors",
    "series", "shears", "species", "tuna", "acoustics", "aesthetics", "aquatics",
    "basics", "ceramics", "classics", "cosmetics", "dialectics", "deer",
    "dynamics", "ethics", "harmonics", "heroics", "mechanics", "metrics", "ooze",
    "optics", "physics", "polemics", "pyrotechnics", "statistics", "tactics",
    "tropics", "bengalese", "bengali", "bonsai", "booze", "cellulose", "mess",
    "moose", "burmese", "colossus", "congolese", "discus", "electrolysis",
    "emphasis", "expertise", "flu", "fructose", "gauze", "glucose", "grease",
    "guyanese", "haze", "incense", "japanese", "lebanese", "malaise", "mayonnaise",
    "maltese", "music", "money", "menopause", "merchandise", "olympics", "overuse",
    "paradise", "poise", "potash", "portuguese", "prose", "recompense", "remorse",
    "repose", "senegalese", "siamese", "singhalese", "sleaze", "sioux", "sudanese",
    "suspense", "swiss", "taiwanese", "vietnamese", "unease", "aircraft", "anise",
    "antifreeze", "applause", "archdiocese", "apparatus", "asparagus", "bellows",
    "bison", "bluefish", "bourgeois", "bream", "brill", "butterfingers", "cargo",
    "carp", "catfish", "chassis", "clone", "clones", "clothes", "chub", "cod",
    "codfish", "coley", "contretemps", "crawfish", "crayfish", "cuttlefish",
    "dice", "dogfish", "doings", "dory", "downstairs", "eldest", "earnings",
    "economics", "electronics", "firstborn", "fish", "flatfish", "flounder",
    "fowl", "fry", "fries", "works", "goldfish", "golf", "grand", "grief",
    "haddock", "hake", "halibut", "headquarters", "herring", "hertz", "honey",
    "horsepower", "goods", "hovercraft", "ironworks", "kilohertz", "ling",
    "shrimp", "swine", "lungfish", "mackerel", "macaroni", "megahertz", "moorfowl",
    "moorgame", "mullet", "myrrh", "nepalese", "offspring", "pants", "patois",
    "pekinese", "perch", "pickerel", "pike", "potpourri", "precis", "quid", "rand",
    "rendezvous", "roach", "salmon", "samurai", "seychelles", "shad", "sheep",
    "shellfish", "smelt", "spaghetti", "spacecraft", "starfish", "stockfish",
    "sunfish", "superficies", "sweepstakes", "smallpox", "swordfish", "tennis",
    "tobacco", "triceps", "trout", "tunafish", "turbot", "trousers", "turf",
    "dibs", "undersigned", "waterfowl", "waterworks", "waxworks", "wildfowl",
    "woodworm", "yen", "aries", "pisces", "forceps", "jeans", "mathematics",
    "odds", "politics", "remains", "aids", "wildlife", "shall", "would", "may",
    "might", "ought", "should", "acne", "admiration", "advice", "air", "anger",
    # always-plural / collective nouns
    "tidings",
    "anticipation", "assistance", "awareness", "bacon", "baggage", "blood",
    "bravery", "chess", "clay", "clothing", "coal", "compliance", "comprehension",
    "confusion", "consciousness", "cream", "darkness", "diligence", "dust",
    "education", "empathy", "enthusiasm", "envy", "equality", "equipment",
    "evidence", "feedback", "fitness", "flattery", "foliage", "fun", "furniture",
    "garbage", "gold", "gossip", "grammar", "gratitude", "gravel", "guilt",
    "happiness", "hardware", "hate", "hay", "health", "heat", "help",
    "hesitation", "homework", "honesty", "honor", "honour", "hospitality",
    "hostility", "humanity", "humility", "ice", "immortality", "independence",
    "information", "integrity", "intimidation", "jargon", "jealousy", "jewelry",
    "justice", "knowledge", "literacy", "logic", "luck", "lumber", "luggage",
    "mail", "management", "milk", "morale", "mud", "nonsense", "oppression",
    "optimism", "oxygen", "participation", "pay", "peace", "perseverance",
    "pessimism", "pneumonia", "poetry", "police", "pride", "privacy", "propaganda",
    "public", "punctuation", "recovery", "rice", "rust", "satisfaction", "schnapps",
    "shame", "slang", "software", "stamina", "starvation", "steam", "steel",
    "stuff", "support", "sweat", "thunder", "timber", "toil", "traffic", "tongs",
    "training", "trash", "valor", "vehemence", "violence", "warmth", "waste",
    "weather", "wheat", "wisdom", "work", "accommodation", "advertising", "aid",
    "art", "bread", "business", "butter", "calm", "cash", "cheese", "childhood",
    "clothing ", "coffee", "content", "corruption", "courage", "currency",
    "damage", "danger", "determination", "electricity", "employment", "energy",
    "entertainment", "failure", "fame", "fire", "flour", "food", "freedom",
    "friendship", "fuel", "genetics", "hair", "harm", "hospitality ",
    "housework", "humour", "imagination", "importance", "innocence", "intelligence",
    "juice", "kindness", "labour", "lack", "laughter", "leisure", "literature",
    "litter", "love", "magic", "metal", "motherhood", "motivation", "nature",
    "nutrition", "obesity", "oil", "old age", "paper", "patience", "permission",
    "pollution", "poverty", "power", "production", "progress", "pronunciation",
    "publicity", "quality", "quantity", "racism", "rain", "relaxation", "research",
    "respect", "room (space)", "rubbish", "safety", "salt", "sand", "seafood",
    "shopping", "silence", "smoke", "snow", "soup", "speed", "spelling",
    "stress ", "sugar", "sunshine", "tea", "time", "tolerance", "trade",
    "transportation", "travel", "trust", "understanding", "unemployment", "usage",
    "vision", "water", "wealth", "weight", "welfare", "width", "wood", "yoga",
    "youth", "homecare", "childcare", "fanfare", "healthcare", "medicare",
}


def is_mass_noun(word):
    """Return True if word is uncountable (mass noun, -ness, or -ism form)."""
    w = word.lower().strip()
    return w.endswith("ness") or w.endswith("ism") or w in MASS_NOUNS


# ---------------------------------------------------------------------------
# Lazy-loaded rita_dict for nn lookup (used by isPlural)
# ---------------------------------------------------------------------------

_DICT = None


def _get_dict():
    global _DICT
    if _DICT is None:
        path = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'rita_dict.json')
        with open(path) as f:
            _DICT = json.load(f)
    return _DICT


def _is_nn_in_dict(word):
    """Return True if word has an 'nn' tag in the rita dictionary."""
    d = _get_dict()
    entry = d.get(word.lower())
    if entry and len(entry) > 1:
        return "nn" in entry[1]
    return False


# ---------------------------------------------------------------------------
# Noun lists (from inflector.js)
# ---------------------------------------------------------------------------

_NOUNS_ENDING_IN_E = set("""abeyance|abode|aborigine|abrasive|absence|absentee|absolute|abstinence|abundance|abuse|acceptance|accolade|accomplice|accordance|ace|acetate|acetone|acetylene|ache|acolyte|acquaintance|acquiescence|acquire|acre|acreage|active|acupuncture|acute|adage|additive|addressee|adherence|adhesive|adjective|admittance|adobe|adolescence|adoptee|adrenaline|advance|advantage|adventure|advocate|aerospace|affiliate|affirmative|affluence|agate|age|aggregate|agriculture|aide|airfare|airframe|airline|airplane|airtime|airwave|aisle|alcove|ale|algae|allegiance|alliance|allowance|allure|alternate|alternative|altitude|ambiance|ambivalence|ambulance|amphetamine|amplitude|analogue|anchorage|anecdote|angle|ankle|annoyance|anode|ante|antelope|antidote|antihistamine|antique|anyone|ape|aperture|apocalypse|apogee|apostle|appearance|appellate|appendage|appetite|apple|appliance|appointee|apprentice|approximate|aptitude|aquamarine|arbitrage|arcade|archetype|architecture|archive|armistice|arrearage|arrogance|artichoke|article|artifice|assemblage|associate|assurance|athlete|atmosphere|attache|attendance|attendee|attire|attitude|attribute|audience|audiophile|auspice|autoclave|automobile|avalanche|avarice|avenue|average|avoidance|awe|axe|axle|babble|babe|backbone|backhoe|backside|badge|bagpipe|bakeware|balance|bale|bandage|bane|banshee|barbecue|barge|baritone|barnacle|baroque|barrage|barricade|base|baseline|bathrobe|battle|bauble|beadle|bedside|bedtime|bee|beehive|beetle|belligerence|beneficence|benevolence|benzene|beverage|bible|bicarbonate|bicycle|biggie|bike|bile|billionaire|binge|biplane|birdie|birthplace|birthrate|bisque|bite|blade|blame|blanche|blase|blaze|blockade|blockage|bloke|blonde|blouse|blue|boardinghouse|boilerplate|bondage|bone|bonfire|boogie|bookcase|bookie|bookstore|boondoggle|borderline|bore|bottle|bounce|bourgeoisie|boutique|bovine|brace|brake|bramble|breakage|breeze|bribe|bride|bridge|bridle|brie|briefcase|brigade|brilliance|brindle|brine|bristle|broadside|brocade|brochure|brokerage|bromide|bronze|brownie|bruise|brunette|brute|bubble|buckle|bugle|bulge|bundle|bustle|butane|buttonhole|byline|byte|cabbage|cable|cache|cadence|cadre|cafe|caffeine|cage|cake|calorie|camaraderie|camouflage|campfire|campsite|candidate|candle|cane|canine|canoe|cantaloupe|capacitance|cape|capsule|captive|capture|carbide|carbine|carbohydrate|carbonate|care|caricature|carnage|carnivore|carriage|cartilage|cartridge|cascade|case|cashmere|cassette|caste|castle|catalogue|catastrophe|cathode|cattle|cause|cave|cayenne|ceasefire|cellophane|censure|centerpiece|centre|centrifuge|certificate|chaise|challenge|champagne|chance|change|chaperone|charge|charlotte|chase|cheekbone|cheese|cheesecake|chemise|childcare|chimpanzee|chive|chloride|chlorine|chocolate|choice|choke|chore|chrome|chromosome|chronicle|chuckle|chute|cigarette|ciliate|circle|circumference|circumstance|clairvoyance|classmate|clause|clearance|clearinghouse|cleavage|cliche|clientele|climate|clime|clique|closure|cloture|clove|clozapine|clubhouse|clue|coastline|cobblestone|cocaine|code|coexistence|coffee|cognizance|coherence|coincidence|coke|collage|collapse|collarbone|colleague|collective|college|collie|cologne|colonnade|columbine|combine|comeuppance|comfortable|commemorative|commerce|committee|commonplace|commune|communique|commute|comparative|compare|competence|composite|composure|compote|compromise|comrade|concentrate|concessionaire|concierge|conclave|concrete|concurrence|condensate|condolence|cone|conferee|conference|confidante|confidence|confluence|conformance|conglomerate|congruence|conjecture|connivance|conscience|consequence|conservative|consistence|constable|consulate|continuance|contraceptive|contrivance|convalescence|convenience|converse|convertible|conveyance|cookie|cookware|cooperative|coordinate|cope|core|cornerstone|corpse|correspondence|corsage|cortisone|corvette|costume|coterie|cottage|countenance|counterbalance|counterforce|countermeasure|countryside|coupe|couple|courage|course|courthouse|couture|cove|coverage|cowardice|coyote|crackle|cradle|crane|crate|craze|crease|creature|credence|creole|crevice|crime|cripple|critique|crocodile|crone|crossfire|crucible|crude|cruise|crusade|cubbyhole|cube|cue|cuisine|culture|curbside|cure|curse|curve|cyanide|cycle|dale|damage|dame|daminozide|dance|dare|database|date|daytime|daze|deadline|debacle|debate|debutante|decade|decadence|decline|decrease|decree|defense|defensive|deference|defiance|degree|delegate|deliverance|deluge|demagogue|demise|denture|departure|dependence|deportee|deregulate|derivative|designate|designee|desire|detective|detente|deterrence|deviance|device|devotee|dialogue|diatribe|die|difference|dike|dime|dinnertime|dinnerware|dioxide|dipole|directive|directorate|dirge|disadvantage|disallowance|disappearance|discharge|disciple|discipline|disclosure|discontinuance|discotheque|discourse|disease|disgrace|disguise|disincentive|diskette|dislike|disobedience|displeasure|disposable|dispute|disrepute|disservice|dissolve|dissonance|distance|distaste|distillate|disturbance|dive|divergence|divestiture|divide|divine|divorce|divorcee|dockside|doctorate|doctrinaire|doctrine|dodge|doe|doghouse|dole|dome|dominance|dope|dosage|dose|double|dove|downgrade|downside|downtime|draftee|drainage|drape|drawbridge|dribble|drive|drizzle|drone|drove|drugstore|due|duke|dune|dye|dyke|dynamite|eagle|earphone|earthenware|earthquake|ease|eave|eclipse|edge|edifice|effective|electorate|electrode|elegance|eligible|elite|eloquence|else|elsewhere|embrace|emcee|emergence|emigre|eminence|empire|employee|enclave|enclosure|encore|endurance|engine|enrage|enrollee|ensemble|enterprise|entire|entourage|entrance|entre|envelope|enzyme|epicure|epilogue|episode|epitome|equine|equivalence|escapade|escape|escapee|espionage|esplanade|essence|estate|estimate|ethane|ethylene|etiquette|eve|everyone|example|excellence|exchange|excise|exclusive|excuse|executive|exercise|exile|existence|expanse|expatriate|expenditure|expense|experience|expletive|explosive|expose|exposure|extravagance|extreme|exuberance|eye|eyepiece|eyesore|fable|facade|face|facsimile|fade|failure|faire|fake|fame|famine|fanfare|farce|fare|farmhouse|fashionable|fate|fatigue|favorite|feature|fee|female|feminine|fence|fiance|fiancee|fiddle|figure|file|filigree|finale|finance|fine|finesse|finite|fire|firehouse|fireplace|fixture|flagpole|flake|flame|flange|flare|flatware|fleece|flextime|floe|flue|fluke|fluoride|flute|foe|foible|folklore|foodservice|footage|footnote|forage|forbearance|force|fore|foreclosure|forfeiture|forge|formaldehyde|formative|fortitude|fortune|foursome|foxhole|fracture|fragrance|frame|franchise|franchisee|freebie|freeze|fridge|frieze|frigate|fringe|frontage|frostbite|fudge|fugitive|fumble|fungicide|furnace|fuse|fuselage|fusillade|future|gabardine|gable|gaffe|gage|gaggle|gale|gallstone|gamble|game|garage|gasoline|gate|gauge|gaze|gazelle|gemstone|gendarme|gene|genie|genocide|genome|genre|gentile|gesture|giggle|girdle|girlie|glade|glance|glare|glassware|glaze|glee|glimpse|globe|glove|glue|glutamate|gnome|goatee|gobble|goggle|goodbye|google|goose|gorge|governance|grace|grade|graduate|granite|grape|grapevine|graphite|grate|grave|greenhouse|grenade|grievance|grille|grime|grindstone|gripe|groove|grouse|grove|grudge|guarantee|guesstimate|guidance|guide|guideline|guile|guillotine|guise|gunfire|gurgle|gyroscope|habitue|hackle|haggle|hairline|halftime|handle|handshake|happenstance|harborside|hardcore|hardline|hare|hassle|haste|have|headache|headline|headphone|healthcare|hearse|heave|hectare|hedge|heliotrope|hellfire|hemisphere|hemline|hemorrhage|herbicide|heritage|heroine|hide|hike|hillside|hindrance|hinge|hippie|hire|hive|hodgepodge|hoe|hole|homage|home|homicide|hone|honeybee|honorable|hope|horde|hormone|horoscope|horrible|horse|horticulture|hose|hospice|hostage|hostile|hotline|house|houseware|housewife|huddle|hue|hurdle|hurricane|hustle|hydride|hygiene|hype|hyperbole|hypocrite|ideologue|ignorance|image|imbalance|immense|immune|impasse|impatience|imperative|imponderable|importance|impotence|imprudence|impulse|incapable|incentive|incidence|incline|incoherence|income|incompetence|incomprehensible|inconvenience|increase|indefinite|indenture|indifference|indispensable|inductee|indulgence|ineptitude|inexperience|infallible|inference|infinite|influence|infrastructure|inheritance|initiate|initiative|injustice|inmate|innocence|insecticide|inside|insignificance|insistence|insolence|insoluble|instance|institute|insurance|intake|intangible|intelligence|intelligible|intensive|interchange|intercourse|interdependence|interestrate|interface|interference|interlude|interstate|interviewee|intestine|intimate|intolerance|intransigence|intrigue|invective|inverse|invertebrate|invite|invoice|iodide|iodine|ire|irresponsible|irreverence|isle|issuance|issue|jade|jailhouse|jasmine|jawbone|jibe|jingle|joke|joyride|judge|juice|jumble|juncture|jungle|junkie|jute|juvenile|kale|kaleidoscope|kamikaze|karaoke|keepsake|kerosene|kettle|keyhole|keynote|keystone|kiddie|kilobyte|kitchenette|kitchenware|kite|knee|knife|knuckle|lace|ladle|lake|lance|landscape|landslide|lane|language|lapse|largesse|lathe|latitude|lattice|laureate|laxative|league|leakage|lease|leave|lecture|ledge|legislature|legume|leisure|lemonade|lettuce|levamisole|levee|leverage|libertine|license|licensee|lie|life|lifeline|lifestyle|lifetime|lighthouse|lignite|lime|limestone|limousine|linage|line|lineage|lingerie|linkage|liposome|literature|litle|loave|lobe|lobule|locale|locomotive|lodge|longitude|longtime|loophole|lope|lore|lounge|louse|love|lube|luminescence|lunchtime|lure|lustre|lute|lye|lymphocyte|machete|machine|madhouse|madstone|magazine|magistrate|magnate|magnitude|mainframe|mainline|maintenance|make|male|malice|malpractice|mandate|mane|manganese|manhole|manmade|mantle|manufacture|manure|maple|marble|mare|margarine|marine|marketplace|marmalade|marque|marquee|marriage|martingale|masculine|masquerade|massacre|massage|masterpiece|mate|matte|maze|mealtime|meantime|meanwhile|measure|medicare|medicine|megabyte|melamine|melange|melee|membrane|menace|merge|message|methadone|methane|methylene|mettle|microbe|micromanage|microphone|microscope|microwave|middle|midrange|midwife|migraine|mile|mileage|milestone|millionaire|mine|miniature|miniscule|minute|miracle|mire|misadventure|misanthrope|miscarriage|miscue|misfortune|missile|missive|mistake|mistletoe|misuse|mite|mitre|mixture|mode|module|moisture|mole|molecule|mollycoddle|monologue|monotone|montage|moraine|more|morgue|morphine|mortgage|mosque|motive|motorbike|motorcade|motorcycle|mottle|mountainside|mouse|mousse|moustache|mouthpiece|movable|move|movie|moxie|muddle|mule|multiple|multistate|multitude|mumble|muscle|musculature|muse|mustache|muzzle|myrtle|mystique|naive|naivete|name|nameplate|namesake|narrative|native|nature|necklace|necktie|needle|negative|negligence|neophyte|nerve|newswire|nibble|niche|nickname|nicotine|niece|nightingale|nightmare|nighttime|nitrate|node|nodule|noise|nomenclature|nominee|noncompliance|none|nonviolence|noodle|noose|nose|nosedive|note|notice|novice|nowhere|nozzle|nuance|nude|nudge|nuisance|nuke|nurse|nurture|obedience|objective|oblige|observance|obsessive|obstacle|obverse|occurrence|ochre|octane|ode|offense|offensive|office|ogre|ole|olive|omnipotence|omnipresence|onstage|operative|opposite|opulence|oracle|orange|ordinance|ordnance|ore|orifice|orphanage|ounce|outage|outcome|outhouse|outline|outrage|outshone|outside|overdose|overdrive|override|oversize|overtime|overtone|overture|oxide|ozone|pace|package|paddle|page|palace|palate|pale|palette|palisade|panache|pancake|pane|panhandle|pantie|pantomime|parable|parachute|parade|paraphrase|parasite|parentage|parlance|parole|parolee|parsonage|particle|passage|passive|paste|pastime|pasture|pate|patience|patronage|pause|peacetime|pebble|pedigree|penance|pence|penthouse|people|percentage|perchlorate|performance|perfume|permanence|permissible|peroxide|perquisite|persistence|perspective|pesticide|pestilence|petulance|phase|phone|phosphate|phrase|physique|pickle|picture|picturesque|pie|piece|pile|pilgrimage|pimple|pine|pineapple|pinhole|pinnacle|pipe|pipeline|pique|pirate|pittance|place|plague|plane|plaque|plate|platitude|plausible|playhouse|playmate|pleasure|pledge|plumage|plume|plunge|poke|pole|polyurethane|poodle|poolside|pope|populace|porcupine|pore|porpoise|porridge|portable|pose|positive|posse|postage|posture|potentate|pothole|poultice|powerhouse|practice|prairie|praise|prattle|preamble|precedence|precipice|precipitate|predominance|preface|prefecture|preference|prejudice|prelude|premiere|premise|preponderance|preppie|prerequisite|prerogative|presale|presence|preserve|pressure|prestige|pretense|prevalence|preventive|price|primate|prime|primetime|prince|principle|private|privilege|prize|probate|probe|procedure|produce|profile|progressive|projectile|promenade|prominence|promise|propane|propylene|prostate|prostitute|protective|protege|prototype|provenance|providence|province|prude|prudence|prune|psyche|puddle|pulse|purchase|purge|purple|purpose|purse|puzzle|quagmire|quake|questionnaire|queue|quiche|quickie|quince|quinine|quote|rabble|race|racehorse|radiance|rage|ragtime|railbike|raise|rake|rampage|range|rape|rapture|rate|rationale|rattle|rattlesnake|rawhide|realestate|reappearance|reassurance|rebate|rebuke|receivable|receptacle|recharge|recipe|recluse|recognizance|reconfigure|reconnaissance|recourse|rectangle|rectitude|recurrence|redone|referee|reference|refuge|refugee|refuse|reggae|regime|reignite|reinsurance|reissue|relapse|relative|release|relevance|reliance|relocate|reluctance|remade|remembrance|reminiscence|remittance|renaissance|renegade|repartee|repentance|repertoire|reportage|representative|reprieve|reptile|repurchase|repute|resale|rescue|resemblance|reserve|reshuffle|residence|residue|resilience|resistance|resolve|resonance|resource|respite|response|restructure|resume|resurgence|reticence|retinue|retiree|retrospective|revenge|revenue|reverence|reverie|reverse|rewrite|rhinestone|rhyme|riddance|riddle|ride|ridge|ridicule|rifle|ringside|rinse|ripple|rite|riverside|roadside|robe|role|romance|rooftree|rookie|roommate|rope|rose|rosette|rote|rouge|roulette|roundhouse|route|routine|rubble|ruble|rue|rule|rumble|rupee|rupture|ruse|russe|rye|sable|sabotage|sabre|sacrifice|sacrilege|saddle|safe|sage|sake|sale|saline|salute|salvage|salve|sample|sanguine|sardine|satellite|satire|sauce|sausage|savage|saxophone|scale|scare|scene|schedule|scheme|schoolhouse|schoolmate|science|scope|score|scourge|scramble|scrape|scribe|scrimmage|scripture|scuffle|sculpture|seashore|seaside|sedative|seepage|seizure|semblance|senate|sense|sensible|sensitive|sentence|sequence|serenade|serene|serve|service|servitude|sesame|severance|sewage|shade|shake|shape|share|shave|shinbone|shine|shingle|shipmate|shirtsleeve|shoe|shoelace|shore|shoreline|shortage|shortcake|shove|showcase|showpiece|shrine|shrinkage|shuffle|shuttle|side|sideline|siege|sieve|signature|significance|silence|silhouette|silicate|silicone|silverware|simile|simple|sine|single|sinkhole|site|size|sizzle|skyline|skywave|slate|slaughterhouse|slave|sleeve|slice|slide|slime|slippage|slope|sludge|sluice|smile|smoke|smudge|snake|snare|snowflake|socialite|solace|sole|solicitude|solitude|some|someone|someplace|somewhere|sophisticate|sophomore|sore|souffle|source|space|spade|spangle|spate|spectacle|spectre|sphere|spice|spike|spindle|spine|spire|spite|spittle|splice|splurge|spoilage|spoke|sponge|spore|spouse|spree|springtime|sprinkle|spruce|squabble|square|squeegee|squeeze|squire|stable|stage|staircase|stake|stalemate|stampede|stance|staple|stare|state|statue|stature|statute|steakhouse|steppe|stereotype|stethoscope|stockpile|stone|stoneware|stooge|stoppage|storage|store|storehouse|storyline|stove|stratosphere|stricture|stride|strife|strike|stripe|striptease|strobe|stroke|structure|struggle|strychnine|stubble|stumble|stumpage|style|styrene|subcommittee|sublease|sublime|submarine|subordinate|subservience|subsidence|subsistence|substance|substantive|substitute|substrate|subterfuge|subtitle|suburbanite|suede|suffrage|suffragette|sugarcane|suicide|suitcase|suite|sulfide|summertime|sunrise|sunshine|superstore|superstructure|supine|supreme|surcharge|surface|surge|surname|surprise|surrogate|surveillance|susceptible|sustenance|suture|swerve|swipe|sycamore|syllable|synagogue|syndicate|syndrome|syringe|table|tableware|tackle|tadpole|tagline|tailgate|tailpipe|take|tale|tambourine|tangle|tape|taste|teammate|tease|technique|tee|telephone|telescope|teletype|telltale|temperance|temperature|template|temple|tempore|tense|tentacle|tentative|tenure|termite|terrace|testicle|testosterone|textile|texture|theme|thimble|thistle|thoroughfare|threesome|throne|throttle|tide|tie|tightrope|tile|timbre|time|timepiece|timetable|tincture|tine|tintype|tirade|tire|tissue|titanate|title|toe|toffee|tole|tolerance|tombstone|tome|tone|tongue|tonnage|toothpaste|torque|tortoise|torture|touchstone|townhouse|trace|trackage|trade|trance|tranche|transcendence|transience|transverse|trapeze|travelogue|treasure|treatise|treble|tree|tremble|trestle|triage|triangle|tribe|tribute|trickle|trifle|triglyceride|tripe|triple|triumvirate|trombone|trouble|troupe|trove|truce|trudge|trundle|trustee|tube|tumble|tune|turbine|turbulence|turnpike|turntable|turpentine|turquoise|turtle|tussle|tutelage|twaddle|twine|twinge|twinkle|twosome|tyke|type|typeface|umbrage|umpire|unattainable|uncle|undergraduate|underperformance|underscore|underside|undertone|underwrote|undesirable|unfortunate|unique|universe|unlike|unthinkable|update|upgrade|upscale|upside|upsurge|urethane|urge|urine|usage|use|utterance|vaccine|value|valve|vampire|vane|vantage|variable|variance|vase|vaudeville|vegetable|vehicle|venerable|vengeance|venture|venue|verbiage|verge|verisimilitude|verse|vertebrate|verve|vestige|vibe|vice|vicissitude|videocassette|videotape|vigilance|vignette|village|vine|vintage|virtue|virulence|visage|vise|vogue|voice|voltage|volume|vote|voyage|vulture|waffle|wage|waggle|wale|wane|wardrobe|ware|warehouse|warfare|wartime|wattle|wave|wayside|weave|wedge|welcome|welfare|whale|wheeze|while|whine|whistle|white|whole|wholesale|whore|wife|wiggle|wile|wince|windowpane|wine|wintertime|wire|wobble|woe|workforce|workhorse|workplace|wreckage|wrinkle|yardage|yoke|yuppie|zombie|zone""".split("|"))

_NOUNS_ENDING_IN_S = set("""abruptness|abscess|absoluteness|abyss|access|actress|address|aegis|aerobics|aggressiveness|albatross|alertness|alias|aloofness|alumnus|amicus|analysis|annals|antithesis|apotheosis|apparatus|appropriateness|arrears|arthritis|asbestos|asparagus|ass|assertiveness|astuteness|attractiveness|avionics|awareness|awfulness|awkwardness|axis|backwardness|backwoods|badness|baldness|basis|bass|bearishness|bellows|bias|bigness|billiards|bitterness|blackness|blandness|blindness|bliss|bluntness|boldness|bonus|boss|brashness|brass|brightness|bronchitis|bullishness|bus|business|bypass|cactus|calculus|calisthenics|callousness|calmness|campus|canvas|carcass|carelessness|catharsis|caucus|cautiousness|census|chaos|chassis|chess|chorus|circus|cirrhosis|citrus|class|cleanliness|cleverness|clones|closeness|cockiness|cohesiveness|coldness|colossus|commons|compass|competitiveness|completeness|congress|conscious|consciousness|consensus|contretemps|coolness|corpus|correctness|cosmos|countess|coziness|craziness|creativeness|crisis|crispness|cross|crossroads|cuteness|cutlass|cypress|dais|darkness|deadliness|deafness|debris|decisiveness|defensiveness|deliveries|diabetes|diagnosis|dialysis|dibs|digitalis|directness|discus|distinctiveness|distress|divisiveness|dizziness|doldrums|dominoes|downstairs|dramas|draughts|dreariness|dress|dross|drunkenness|dryness|dullness|duress|eagerness|earnestness|economics|edginess|effectiveness|electrodynamics|electrolysis|electronics|elusiveness|emeritus|emphasis|emptiness|encephalitis|epidermis|esophagus|ethics|ethos|eucalyptus|excess|exodus|express|eyeglasses|eyewitness|fairness|fastness|fetus|fiberglass|fibrosis|fickleness|firmness|fitness|flatness|focus|fondness|foolishness|forcefulness|forgiveness|forthrightness|fortress|fracas|frankness|freshness|friendliness|fullness|fungus|fuss|gallows|gas|gass|gauss|genesis|genius|gentleness|genus|givenness|glass|gloss|goddess|goodness|governess|grass|greatness|grimness|gross|guess|happiness|hardness|harness|harshness|headdress|headquarters|headwaters|heaves|heiress|helplessness|hepatitis|hiatus|highness|hoarseness|homeless|homelessness|homesickness|hopelessness|hoss|hostess|hubris|humanness|hustings|hydraulics|hydrolysis|hypnosis|hypothesis|idleness|ignoramus|illness|impatiens|impetus|impress|inches|indebtedness|indecisiveness|indoors|ineffectiveness|innards|institutes|inventiveness|isthmus|jackass|jeans|jitters|joblessness|joss|kindness|kiss|landes|largess|lass|lawlessness|leggings|lens|lightness|likeness|litmus|liveliness|locus|loneliness|loss|lotus|madness|mandamus|mass|mathematics|mattress|meanness|means|measles|mess|metamorphosis|metaphysics|metropolis|microeconomics|miniseries|minus|miss|mistress|molasses|morass|mortis|moss|mucus|narrowness|neatness|necrosis|nemesis|nervousness|news|nexus|nitrous|nothingness|nucleus|numbness|oasis|octopus|ogress|omnibus|oneness|onus|oodles|openness|opus|orderliness|outdoors|overpass|overseas|pancreas|pandanus|paralysis|parenthesis|pass|pathos|pediatrics|pelvis|persuasiveness|pervasiveness|pettiness|photosynthesis|physics|piles|playfulness|plus|pneumocystis|polis|politeness|politics|pompousness|powerlessness|preparedness|press|princess|proboscis|process|prognosis|progress|prospectus|prowess|psoriasis|psychoanalysis|quadriceps|queasiness|quickness|quietness|radius|randomness|readiness|reassess|recess|recklessness|redress|religious|remoteness|rendezvous|resourcefulness|responsiveness|restlessness|retrovirus|rhinoceros|riches|richness|righteousness|rightness|riskiness|robustness|roominess|rowdiness|ruckus|rudeness|ruthlessness|sadness|sameness|sassafras|scarves|schnapps|sclerosis|seamstress|selfishness|separateness|sepsis|series|seriousness|shallowness|shambles|sharpness|shortness|shortsightedness|sickness|silliness|sinus|skittishness|sloppiness|slovenliness|slowness|sluggishness|slyness|smallness|smithereens|smoothness|softness|soundness|species|spyglass|squeamishness|status|steadfastness|steadiness|steepness|stewardess|stiffness|stillness|stimulus|strangeness|stress|stubbornness|subconscious|success|suddenness|suds|summons|sunglasses|surfaceness|surplus|sweepstakes|sweetness|swiftness|swoops|synopsis|synthesis|tardiness|telecommunications|tenderness|tennis|terminus|tetanus|thermos|thesaurus|thesis|thickness|thinness|thoroughness|thrips|thrombosis|tidings|tightness|timeliness|togetherness|tongs|toss|toughness|trespass|tress|truss|truthfulness|tuberculosis|typhus|ugliness|unconscious|undress|uneasiness|unfairness|unhappiness|uniqueness|unpleasantness|unwillingness|upstairs|usefulness|uterus|vagueness|virus|vividness|waitress|walrus|wariness|waterworks|weakness|weariness|weightlessness|wellness|wetness|whereabouts|whiteness|wickedness|wilderness|wildness|willingness|witness|wonderfulness|worthiness""".split("|"))

# ---------------------------------------------------------------------------
# IS_PLURAL_RULES (from inflector.js)
# ---------------------------------------------------------------------------

_IS_PLURAL_RES = [
    re.compile(r"(houses|pluses|cases)$"),
    re.compile(r"^(apices|cortices)$"),
    re.compile(r"^(meninges|phalanges)$"),
    re.compile(r"^(octopus|pinch|fetus|genus|sinus|tomato|kiss|pelvis)es$"),
    re.compile(r"^(whizzes)$"),
    re.compile(r"(l|w)ives$"),
    re.compile(r"^(appendices|matrices)$"),
    re.compile(r"^(indices|apices|cortices)$"),
    re.compile(r"^(media|millennia|consortia|septa|memorabilia|data|femora)$"),
    re.compile(r"^(memoranda|bacteria|curricula|minima|maxima|referenda|spectra|phenomena|criteria)$"),
    re.compile(r"^[lm]ice$"),
    re.compile(r"feet$"),
    re.compile(r"teeth$"),
    re.compile(r"children$"),
    re.compile(r"geese$"),
    re.compile(r"^concerti$"),
    re.compile(r"people$"),
    re.compile(r"^oxen"),
    re.compile(r"(treatises|chemises)$"),
    re.compile(r"(human|german|roman|femur)s"),
    # agent nouns ending in -ess → -esses
    re.compile(r"[a-z]esses$"),
]

# ---------------------------------------------------------------------------
# SING_RULES and PLUR_RULES (from inflector.js)
# ---------------------------------------------------------------------------

_NE_PAT = "(" + "|".join(sorted(_NOUNS_ENDING_IN_E, key=len, reverse=True)) + ")"
_NS_PAT = "(" + "|".join(sorted(_NOUNS_ENDING_IN_S, key=len, reverse=True)) + ")"

_SING_RULES = [
    _RE(r"^(stimul|alumn|termin|emerit)i$", 1, "us"),
    _RE(r"(houses|pluses|cases)$", 1, ""),
    _RE(r"^(apices|cortices)$", 4, "ex"),
    _RE(r"^(meninges|phalanges)$", 3, "x"),
    _RE(r"^(octopus|pinch|fetus|genus|sinus|tomato|kiss|pelvis)es$", 2),
    _RE(r"^(whizzes)$", 3),
    _RE(r"^" + _NE_PAT + r"s$", 1, ""),
    _RE(r"^" + _NS_PAT + r"es$", 2, ""),
    _RE(r"(l|w|kn)ives$", 3, "fe"),
    _RE(r"(men|women)$", 2, "an"),
    _RE(r"ves$", 3, "f"),
    _RE(r"^(appendices|matrices)$", 3, "x"),
    _RE(r"^(indices|apices|cortices)$", 4, "ex"),
    _RE(r"^(gas|bus)es$", 2),
    _RE(r"([a-z]+osis|[a-z]+itis|[a-z]+ness)$", 0),
    _RE(r"^(stimul|alumn|termin)i$", 1, "us"),
    _RE(r"^(media|millennia|consortia|septa|memorabilia|data)$", 1, "um"),
    _RE(r"^(memoranda|bacteria|curricula|minima|maxima|referenda|spectra|phenomena|criteria)$", 1, "um"),
    _RE(r"ora$", 3, "us"),
    _RE(r"^[lm]ice$", 3, "ouse"),
    _RE(r"[bcdfghjklmnpqrstvwxyz]ies$", 3, "y"),
    _RE(r"(ces)$", 1),
    _RE(r"^feet$", 3, "oot"),
    _RE(r"^teeth$", 4, "ooth"),
    _RE(r"children$", 3),
    _RE(r"geese$", 4, "oose"),
    _RE(r"^concerti$", 1, "o"),
    _RE(r"people$", 4, "rson"),
    _RE(r"^(vertebr|larv|minuti)ae$", 1),
    _RE(r"^oxen", 2),
    _RE(r"esses$", 2),
    _RE(r"(treatises|chemises)$", 1),
    _RE(r"(sh|ch|o|ss|x|z|us)es$", 2),
    _RE(r"ses$", 2, "is"),
    _RE(r"([vs]is|gas|[im]nus|genus|[ptbl]us|[ai]ss|[dr]ess)$", 0),
    # DEFAULT_SING
    _RE(r"^.*[^s]s$", 1),
]

_PLUR_RULES = [
    _RE(r"(human|german|roman)$", 0, "s"),
    _RE(r"^(monarch|loch|stomach|epoch|ranch)$", 0, "s"),
    _RE(r"^(piano|photo|solo|ego|tobacco|cargo|taxi)$", 0, "s"),
    _RE(r"(chief|proof|ref|relief|roof|belief|spoof|golf|grief)$", 0, "s"),
    _RE(r"^(appendix|index|matrix|apex|cortex)$", 2, "ices"),
    _RE(r"^concerto$", 1, "i"),
    _RE(r"^prognosis", 2, "es"),
    _RE(r"[bcdfghjklmnpqrstvwxyz]o$", 0, "es"),
    _RE(r"[bcdfghjklmnpqrstvwxyz]y$", 1, "ies"),
    _RE(r"^ox$", 0, "en"),
    _RE(r"^(stimul|alumn|termin|emerit)us$", 2, "i"),
    _RE(r"^corpus$", 2, "ora"),
    _RE(r"(xis|sis)$", 2, "es"),
    _RE(r"whiz$", 0, "zes"),
    _RE(r"motif$", 0, "s"),
    _RE(r"[lraeiou]fe$", 2, "ves"),
    _RE(r"[lraeiou]f$", 1, "ves"),
    _RE(r"(eu|eau)$", 0, "x"),
    _RE(r"(man|woman)$", 2, "en"),
    _RE(r"person$", 4, "ople"),
    _RE(r"^meninx|phalanx$", 1, "ges"),
    _RE(r"schema$", 0, "ta"),
    _RE(r"^(bus|gas)$", 0, "es"),
    _RE(r"child$", 0, "ren"),
    _RE(r"^(vertebr|larv|minuti)a$", 0, "e"),
    _RE(r"^(maharaj|raj|myn|mull)a$", 0, "hs"),
    _RE(r"^aide-de-camp$", 8, "s-de-camp"),
    _RE(r"^weltanschauung$", 0, "en"),
    _RE(r"^lied$", 0, "er"),
    _RE(r"^tooth$", 4, "eeth"),
    _RE(r"^[lm]ouse$", 4, "ice"),
    _RE(r"^foot$", 3, "eet"),
    _RE(r"goose", 4, "eese"),
    _RE(r"^(co|no)$", 0, "'s"),
    _RE(r"^blond$", 0, "es"),
    _RE(r"^datum", 2, "a"),
    _RE(r"([a-z]+osis|[a-z]+itis)$", 0),
    _RE(r"([zsx]|ch|sh)$", 0, "es"),
    _RE(r"^(medi|millenni|consorti|sept|memorabili)um$", 2, "a"),
    _RE(r"^(memorandum|bacterium|curriculum|minimum|maximum|referendum|spectrum|phenomenon|criterion)$", 2, "a"),
    # DEFAULT_PLUR
    _RE(r"^((\w+)(-\w+)*)(\s((\w+)(-\w+)*))*$", 0, "s"),
]

# ---------------------------------------------------------------------------
# Inflector class
# ---------------------------------------------------------------------------

_PLUR = 1
_SING = 2


class Inflector:
    """Pluralize and singularize English nouns."""

    def __init__(self, rita=None):
        self.rita = rita  # optional parent RiTa instance

    # ------------------------------------------------------------------

    def adjust_number(self, word, kind, dbug=False):
        if word and not isinstance(word, str):
            label = "singularize()" if kind == _SING else "pluralize()"
            raise TypeError(f"{label} requires a string as input")

        if not word:
            return ""
        word = word.strip()
        if not word:
            return ""

        check = word.lower()
        if is_mass_noun(check):
            dbug and print(f"{word} hit MASS_NOUNS")
            return word

        rules = _SING_RULES if kind == _SING else _PLUR_RULES
        for i, rule in enumerate(rules):
            if rule.applies(check):
                dbug and print(f"{word} hit rule #{i}")
                return rule.fire(word)

        return word

    # ------------------------------------------------------------------

    def singularize(self, word=None, opts=None):
        if word is None:
            return ""
        return self.adjust_number(word, _SING, bool(opts and opts.get("dbug")))

    def pluralize(self, word=None, opts=None):
        if word is None:
            return ""
        if self.is_plural(word, opts):
            opts and opts.get("debug") and print("pluralize returning via isPlural()")
            return word
        return self.adjust_number(word, _PLUR, bool(opts and opts.get("dbug")))

    # ------------------------------------------------------------------

    def is_plural(self, word=None, opts=None):
        if not word or not isinstance(word, str) or not word.strip():
            return False

        dbug = opts and opts.get("dbug")
        word = word.lower().strip()

        if is_mass_noun(word):
            dbug and print(f"{word} is mass noun")
            return True

        for i, rule in enumerate(_IS_PLURAL_RES):
            if rule.search(word):
                dbug and print(f"{word} (isPlural) hit plural rule #{i}")
                return True

        dbug and print(f"{word} (isPlural) hit no plural rules")

        # General -ness modal form
        if re.search(r"([a-z]+ness)$", word):
            dbug and print(f"{word} is general modal form")
            return True

        # Check if singularized form is different and known as 'nn'
        sing = self.singularize(word, opts)
        if sing != word:
            # Latin -a to -ae rule
            if word.endswith("ae") and word == sing + "e":
                dbug and print(f"{word}: latin rule -a to -ae")
                return True
            # Check dict for nn tag
            if _is_nn_in_dict(sing):
                dbug and print(f"{word}'s singular form {sing} is nn")
                return True

        dbug and print(f"{word} (isPlural) no matches, return false")
        return False

    # ------------------------------------------------------------------
    # Phrase support: pluralize/singularize last content word in phrase

    def pluralize_phrase(self, phrase, opts=None):
        words = phrase.split()
        if len(words) > 2 and words[1].lower() == "of":
            # "X of Y" -> pluralize Y
            words[-1] = self.pluralize(words[-1], opts)
            return " ".join(words)
        words[-1] = self.pluralize(words[-1], opts)
        return " ".join(words)

    def singularize_phrase(self, phrase, opts=None):
        words = phrase.split()
        words[-1] = self.singularize(words[-1], opts)
        return " ".join(words)
