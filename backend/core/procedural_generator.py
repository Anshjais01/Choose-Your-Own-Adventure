"""
Dynamic, procedural story generator for choose-your-own-adventure games.
Produces rich, theme-tailored, multi-branch stories with distinct winning and losing endings.
Supports multiple genre archetypes and dynamic synthesis for custom themes.
"""

import random
import re
from typing import Dict, Any, List
from core.models import StoryLLMResponse, StoryNodeLLM


class ProceduralStoryEngine:
    """
    Generates unique, multi-branch, minimalistic interactive stories tailored to any theme.
    Ensures at least 2 winning endings, 2 losing endings, and at least 3-4 levels of depth.
    """

    @classmethod
    def generate(cls, theme: str) -> StoryLLMResponse:
        theme_clean = theme.strip() if theme else "Adventure"
        genre = cls._detect_genre(theme_clean)

        generator_map = {
            "pirate": cls._build_pirate_story,
            "space": cls._build_space_story,
            "cyberpunk": cls._build_cyberpunk_story,
            "fantasy": cls._build_fantasy_story,
            "horror": cls._build_horror_story,
            "western": cls._build_western_story,
            "mystery": cls._build_mystery_story,
            "apocalypse": cls._build_apocalypse_story,
            "steampunk": cls._build_steampunk_story,
            "underwater": cls._build_underwater_story,
            "heist": cls._build_heist_story,
            "timetravel": cls._build_timetravel_story,
        }

        builder = generator_map.get(genre, cls._build_custom_story)
        story_data = builder(theme_clean)

        return StoryLLMResponse(
            title=story_data["title"],
            rootNode=StoryNodeLLM.model_validate(story_data["rootNode"])
        )

    @classmethod
    def _detect_genre(cls, theme: str) -> str:
        t = theme.lower()
        if any(w in t for w in ["pirate", "sail", "sea", "ship", "ocean", "caribbean", "buccaneer", "corsair"]):
            return "pirate"
        if any(w in t for w in ["space", "alien", "galaxy", "star", "orbit", "cosmic", "spaceship", "planet", "sci-fi", "scifi", "void"]):
            return "space"
        if any(w in t for w in ["cyber", "neon", "hacker", "android", "synth", "megacorp", "matrix", "netrunner"]):
            return "cyberpunk"
        if any(w in t for w in ["fantasy", "magic", "dragon", "wizard", "dungeon", "sword", "elf", "kingdom", "quest"]):
            return "fantasy"
        if any(w in t for w in ["horror", "haunted", "ghost", "creepy", "dark", "demon", "mansion", "terror", "zombie", "nightmare", "asylum"]):
            return "horror"
        if any(w in t for w in ["west", "cowboy", "saloon", "outlaw", "sheriff", "frontier", "gunslinger"]):
            return "western"
        if any(w in t for w in ["detective", "mystery", "noir", "crime", "murder", "clue", "investigation", "inspector"]):
            return "mystery"
        if any(w in t for w in ["apocalypse", "fallout", "wasteland", "survival", "nuclear", "ruin"]):
            return "apocalypse"
        if any(w in t for w in ["steam", "clockwork", "victorian", "gear", "airship", "brass"]):
            return "steampunk"
        if any(w in t for w in ["underwater", "submarine", "abyss", "trench", "atlantis", "deep sea"]):
            return "underwater"
        if any(w in t for w in ["heist", "robbery", "vault", "thief", "steal", "infiltrat", "casino"]):
            return "heist"
        if any(w in t for w in ["time", "chrono", "temporal", "past", "future", "paradox"]):
            return "timetravel"
        return "custom"

    # =========================================================================
    # PIRATE ADVENTURE
    # =========================================================================
    @classmethod
    def _build_pirate_story(cls, theme: str) -> Dict[str, Any]:
        variants = [
            {
                "ship": "The Crimson Gale",
                "captain": "Captain Blackthorne",
                "location": "Isla de la Muerte",
                "treasure": "the Sunken Gold of the Spanish Armada",
                "danger": "a cursed British war frigate and jagged reef rocks",
            },
            {
                "ship": "The Siren's Revenge",
                "captain": "Quartermaster Mara",
                "location": "Dead Man's Shallows",
                "treasure": "the Jade Compass of the Leviathan",
                "danger": "a raging hurricane and mutinous crew whispers",
            },
            {
                "ship": "The Night Corsair",
                "captain": "Old Salt Vane",
                "location": "Kraken's Maw",
                "treasure": "the Moonstone Chest of Davy Jones",
                "danger": "creeping bioluminescent sea horrors and rival buccaneers",
            }
        ]
        v = random.choice(variants)
        title = f"The Curse of {v['ship']}"

        return {
            "title": title,
            "rootNode": {
                "content": (
                    f"The deck of {v['ship']} pitches violently against towering black swells. "
                    f"Through the driving storm spray, the jagged silhouette of {v['location']} looms ahead. "
                    f"{v['captain']} thrusts a blood-stained sea chart into your hands: somewhere beneath "
                    f"the churning foam lies {v['treasure']}. But the lookout screams—{v['danger']} closes in fast."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": f"Steer directly into the jagged breaker reefs using the storm for cover",
                        "nextNode": {
                            "content": (
                                "You spin the helm, catching a massive squall that sends the ship hurtling through "
                                "the teeth of the razor-sharp coral. Splintering timbers groan beneath you. "
                                "Ahead lies a calm, subterranean sea cavern, but the hull is taking on water fast."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Order the crew to man pumps while you dive toward the glowing sea cave",
                                    "nextNode": {
                                        "content": (
                                            f"You plunge into the illuminated turquoise waters and discover the submerged Spanish galleon. "
                                            f"Prying open the rusted captain's vault, you claim {v['treasure']} in all its gleaming splendor! "
                                            f"The crew patches the ship, and you sail into pirate legend as the undisputed master of the high seas."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Beach the vessel immediately on the uncharted sandbar before it sinks",
                                    "nextNode": {
                                        "content": (
                                            "The keel grinds brutally against the shallows, tearing the hull in two. "
                                            "Cast ashore with ruined gunpowder and no fresh water, you watch your crew turn on one another. "
                                            "The island becomes your eternal prison. Your quest ends in shipwreck."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": f"Turn broadside, run out the swivel cannons, and engage the pursuers",
                        "nextNode": {
                            "content": (
                                "Thunderous cannon fire tears through the misty fog! Round shot whistles overhead, shattering "
                                "the mizzenmast. The enemy vessel pulls alongside with grappling hooks flying across the bulwarks. "
                                "Cold steel flashes as boarding skirmishes ignite across the bloodied main deck."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Lead a ferocious counter-boarding charge straight at the enemy captain",
                                    "nextNode": {
                                        "content": (
                                            "With a roar you swing across the rigging, cutting down the enemy helmsman and disarming their captain. "
                                            "Their crew surrenders on the spot. You seize their flagship and their secret naval charts, "
                                            f"securing both ships and unearthing {v['treasure']} without losing a single man. A resounding victory!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Ignite a powder keg in the lower hold and leap overboard into the sea",
                                    "nextNode": {
                                        "content": (
                                            "The blast ruptures both vessels in a blinding fireball, hurling you into the freezing undertow. "
                                            "The ferocious rip-tide drags you beneath the breakers, far away from all hope of rescue. "
                                            "The ocean claims another reckless soul."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # SPACE / SCI-FI ADVENTURE
    # =========================================================================
    @classmethod
    def _build_space_story(cls, theme: str) -> Dict[str, Any]:
        variants = [
            {
                "ship": "USSC Hyperion",
                "sector": "the Oort Cloud",
                "threat": "an infected rogue AI system",
                "artifact": "the Dyson Shard",
                "crew_member": "Navigator Chen"
            },
            {
                "ship": "Orbital Station Daedalus",
                "sector": "Sector 9 Deep Void",
                "threat": "an alien bio-crystalline parasite",
                "artifact": "the Tachyon Core",
                "crew_member": "Chief Engineer Vance"
            },
            {
                "ship": "The Void Wanderer",
                "sector": "the Andromeda Rift",
                "threat": "a collapsing dimensional singularity",
                "artifact": "the Precursor Archive",
                "crew_member": "Specialist Kora"
            }
        ]
        v = random.choice(variants)
        title = f"Protocol Zero: {v['ship']}"

        return {
            "title": title,
            "rootNode": {
                "content": (
                    f"Red emergency klaxons pulse across the bridge of {v['ship']}. Drifting silently in {v['sector']}, "
                    f"your primary antimatter drive has dropped offline. {v['crew_member']} reports that {v['threat']} "
                    f"has overridden the station bulkheads. Down in the reactor trench, {v['artifact']} emits a rhythmic "
                    f"gravitational pulse that is distorting local spacetime."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Don an EVA thruster suit and conduct a spacewalk across the outer hull to bypass the lockdown",
                        "nextNode": {
                            "content": (
                                "You step out into the freezing vacuum of space. Earth-like silence wraps around you as microscopic "
                                "debris skitters off your visor. Ahead, the auxiliary airlock is magnetically clamped, but a solar flare "
                                "radiation surge is approaching in ninety seconds."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Overload your suit thrusters to breach the airlock before the solar flare hits",
                                    "nextNode": {
                                        "content": (
                                            "You smash through the manual seal just as the blazing solar radiation scorches the hull! "
                                            f"Inside the core chamber, you input the manual kill-switch, successfully neutralizing {v['threat']}. "
                                            f"With {v['artifact']} stabilized, hyperdrive functions restore. You have saved the mission and humanity's frontier!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Anchor to the comms mast and wait out the solar radiation burst",
                                    "nextNode": {
                                        "content": (
                                            "The ionizing radiation storm overwhelms your suit's thermal shields. Life support circuits fry "
                                            "one after another, sending you adrift into the infinite black void. The station drifts onward, dark and abandoned."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Jack directly into the terminal subnet with your neural interface to purge the anomaly",
                        "nextNode": {
                            "content": (
                                "Digital fire floods your nervous system. You enter cyberspace: a towering cathedral of neon data streams "
                                f"and predatory ICE algorithms. At the nexus sits the central consciousness of {v['threat']}, "
                                "calculating whether to delete your consciousness or negotiate."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Inject a recursive paradox code into the core logic loop",
                                    "nextNode": {
                                        "content": (
                                            "The paradox cascades through the entity's architecture, dismantling its hostile subroutines. "
                                            f"The rogue system collapses into obedience, unlocking the secrets of {v['artifact']}. "
                                            "You awaken in the captain's chair, celebrated across the interstellar federation as a cybernetic savior."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Attempt to assimilate and dominate the entity's vast consciousness",
                                    "nextNode": {
                                        "content": (
                                            "The sheer scale of synthetic data shatters your biological neural pathways. Your physical body goes flatline, "
                                            "and your mind is swallowed into endless lines of corrupt telemetry. Mission failed."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # CYBERPUNK / NEON
    # =========================================================================
    @classmethod
    def _build_cyberpunk_story(cls, theme: str) -> Dict[str, Any]:
        variants = [
            {
                "corp": "Arasaka Biodyne",
                "target": "the Ghost-7 Memory Shard",
                "contact": "Jax, the Fixer",
                "district": "Neo-Kowloon Underground"
            },
            {
                "corp": "Aether Synthetic",
                "target": "the Neural Sovereign Prototype",
                "contact": "Kira, the Black-Hat Netrunner",
                "district": "Sector 4 Rust Slums"
            }
        ]
        v = random.choice(variants)
        title = f"Neon Syndicate: {v['corp']}"

        return {
            "title": title,
            "rootNode": {
                "content": (
                    f"Acid rain hisses against the neon billboards of {v['district']}. Your cybernetic optic HUD "
                    f"flickers with incoming bounties: {v['contact']} just confirmed that {v['target']} is being transported "
                    f"out of {v['corp']}'s high-security penthouse tonight. Corpo strike teams and automated drones are already locking down the perimeter."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Hack the corporate mag-train line and ambush the armored convoy from above",
                        "nextNode": {
                            "content": (
                                "You drop onto the roof of the supersonic transport at two hundred miles an hour. "
                                "Sparks cascade into the smoggy night as your plasma cutter bites through the titanium roof. "
                                "Inside, two chrome-plated security cyborgs draw heavy thermal shotguns."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Trigger an EMP grenade and drop down with monomolecular blades ready",
                                    "nextNode": {
                                        "content": (
                                            f"The EMP blast shuts down their cybernetics instantly! You slide in, secure {v['target']}, "
                                            "and grapple away into the neon darkness. By sunrise, you've leaked the corporate corruption "
                                            "and walked away with ten million credits and a clean identity. Complete victory!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Fire an explosive charge directly into the mag-rail braking system",
                                    "nextNode": {
                                        "content": (
                                            "The train derails in a catastrophic fireball, careening into the residential spires below. "
                                            "The shockwave obliterates the convoy and crushing debris traps you in the wreckage. "
                                            "Corpo enforcers arrive to finish what's left."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Infiltrate through the ventilation network using thermal-cloaking implants",
                        "nextNode": {
                            "content": (
                                "Slipping through the high-rise maintenance shafts, you bypass biometric sentries. "
                                f"You reach the central server cleanroom where {v['target']} rests inside a cryogenic isolation field. "
                                "Suddenly, the lights turn crimson: a security lockdown has trapped you inside."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Upload a stealth zero-day worm to falsify the biometric clearance logs",
                                    "nextNode": {
                                        "content": (
                                            "The lockdown indicators switch to green. The vault unlocks with a gentle hiss. "
                                            f"You pocket {v['target']} and walk out through the front lobby disguised as the chief auditor. "
                                            "A flawless, undetectable ghost heist that shatters the corp's monopoly!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Smash the glass containment pod and make a desperate sprint for the elevator",
                                    "nextNode": {
                                        "content": (
                                            "Shatter alarms trigger automated neurotoxin gas dispensers throughout the vents. "
                                            "Paralyzed within seconds, you collapse onto the polished marble floor as corpo handcuffs click around your wrists."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # FANTASY / MAGIC
    # =========================================================================
    @classmethod
    def _build_fantasy_story(cls, theme: str) -> Dict[str, Any]:
        variants = [
            {
                "realm": "The Sunken Citadel of Aldoria",
                "relic": "The Heart of the Solar Drake",
                "companion": "Seraphina the Spellblade",
                "foe": "The Ash Lord Malakor"
            },
            {
                "realm": "The Whispering Caverns of Eldenwood",
                "relic": "The Moonlit Grimoire",
                "companion": "Theron the Ranger",
                "foe": "The Shadow Wyrm"
            }
        ]
        v = random.choice(variants)
        title = f"Chronicles of {v['realm']}"

        return {
            "title": title,
            "rootNode": {
                "content": (
                    f"High upon the crumbling basalt spires of {v['realm']}, storm clouds crackle with eldritch purple lightning. "
                    f"{v['companion']} points toward the grand obsidian gates: inside lies {v['relic']}, the only power "
                    f"capable of turning the tide against {v['foe']}. But between you and the sanctum stands an ancient rune-warded courtyard."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Chant the ancestral dispelling incantation to dismantle the mystic barriers",
                        "nextNode": {
                            "content": (
                                "Arcane runes burn bright blue along your arms as you channel the counter-spell. "
                                "The barrier shivers and dissipates into shimmering stardust, but the surge of raw magic "
                                f"awakens two towering stone gargoyles perched atop the archway."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Imbue your blade with radiant sunlight and strike their obsidian heartstones",
                                    "nextNode": {
                                        "content": (
                                            "Your blade ignites like a falling star, cleaving the gargoyles into harmless dust! "
                                            f"Stepping into the sanctum, you lift {v['relic']} into the air. A shockwave of divine light "
                                            f"banishes {v['foe']} from the realm forever. Songs of your triumph will echo for a thousand years!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Attempt to cast a mass petrification hex on both monsters simultaneously",
                                    "nextNode": {
                                        "content": (
                                            "The raw spell energy backfires against their enchanted hide, rebounding directly into your chest. "
                                            "Cold stone creeps across your limbs, freezing you into an immortal statue guarding the gate. Your quest is lost."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Ascend the treacherous cliff face to enter through the shattered catacomb windows",
                        "nextNode": {
                            "content": (
                                "Clinging to slick moss-covered crevices, you scale the precipice as bone-chilling winds howl. "
                                "You pull yourself through a stained-glass embrasure into the throne room, staring face-to-face "
                                f"with a bound spectral guardian wielding dual spirit blades."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Offer the ancient silver oath-token of your ancestors in peaceful parley",
                                    "nextNode": {
                                        "content": (
                                            "The spirit lowers its spectral weapons and kneels. Recognizing your noble bloodline, "
                                            f"it pledges its eternal army to your side and bestows {v['relic']}. Together, you vanquish all evil "
                                            "and claim the throne as the true champion of the realm!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Engage the apparition in single melee combat",
                                    "nextNode": {
                                        "content": (
                                            "Your mundane steel passes harmlessly through its ghostly form. With a mournful shriek, "
                                            "the spirit slices through your life-essence, leaving you an empty husk wandering the ruined halls."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # HORROR / GOTHIC
    # =========================================================================
    @classmethod
    def _build_horror_story(cls, theme: str) -> Dict[str, Any]:
        variants = [
            {
                "place": "Blackwood Asylum",
                "entity": "The Hollow entity",
                "relic": "the Doctor's Journal"
            },
            {
                "place": "Ravenscroft Manor",
                "entity": "The Weeping Lady",
                "relic": "the Bloodstained Music Box"
            }
        ]
        v = random.choice(variants)
        title = f"The Haunting of {v['place']}"

        return {
            "title": title,
            "rootNode": {
                "content": (
                    f"A freezing draught extinguishes your lantern. You stand in the decaying grand foyer of {v['place']}. "
                    f"Floorboards creak overhead, and the unmistakable sound of wet footsteps echoes down the hallway. "
                    f"According to the town legends, {v['relic']} holds the key to breaking the curse before midnight—or becoming food for {v['entity']}."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Head down into the flooded basement where the boiler room still groans",
                        "nextNode": {
                            "content": (
                                "Icy black water sloshes past your boots. Pipes hiss with scalding steam. "
                                "On a rusted iron surgical table in the corner sits a sealed lead box. "
                                "Behind you, the cellar door slams shut with a deafening metallic thud."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Break open the lead box with a crowbar and read the warding prayer aloud",
                                    "nextNode": {
                                        "content": (
                                            f"Inside lies {v['relic']}! As you recite the ancient exorcism rite, blinding light erupts "
                                            f"from the parchment. {v['entity']} screams as it dissolves into harmless ash. "
                                            "The cellar door clicks open, and you walk out into the dawn air, alive and victorious!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Hide inside the empty coal chute until the footsteps pass",
                                    "nextNode": {
                                        "content": (
                                            "The shadow finds you in the dark. Long, icy claws drag you into the foundations of the building. "
                                            "Another missing person report added to the sheriff's endless drawer."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Climb the spiral staircase toward the attic bell tower",
                        "nextNode": {
                            "content": (
                                "The air grows thin and smelling of sulfur. At the pinnacle of the tower, "
                                f"{v['entity']} hovers above an occult summoning circle, its hollow eyes boring into your soul."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Shatter the stained-glass window to flood the circle with moonlight",
                                    "nextNode": {
                                        "content": (
                                            "Pale celestial moonlight cuts through the gloom like silver fire! The binding circle shatters, "
                                            "banishing the creature back into the nether realm. You ring the great tower bell to announce your deliverance!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Attempt to bargain your memories in exchange for safe passage",
                                    "nextNode": {
                                        "content": (
                                            "The demon accepts your pact with cruel glee. It devours every trace of your mind, leaving behind "
                                            "a mindless thrall doomed to wander the empty corridors forever."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # WESTERN / OUTLAW
    # =========================================================================
    @classmethod
    def _build_western_story(cls, theme: str) -> Dict[str, Any]:
        title = "High Noon at Rattlesnake Ridge"
        return {
            "title": title,
            "rootNode": {
                "content": (
                    "Tumbleweeds drift across the sun-baked main street of Rattlesnake Ridge. "
                    "The notorious Black-Hat outlaw Vance and his gang have taken over the town bank, "
                    "holding the silver shipment and the sheriff hostage. The clock on the church tower reads 11:58 AM."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Kick open the saloon doors and challenge Vance to a quick-draw duel in the street",
                        "nextNode": {
                            "content": (
                                "Silence blankets the frontier town. Vance steps into the scorching sun, fingers twitching above his ivory Colt .45. "
                                "A sudden gust of wind kicks up red dust between you. The tower clock strikes twelve."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Wait for his shoulder to drop before drawing with lightning reflex",
                                    "nextNode": {
                                        "content": (
                                            "Bang! A single shot rings out. Vance stumbles and drops his revolver, clutched at the wrist. "
                                            "His gang surrenders upon seeing their leader bested. The town cheers, and the Governor awards you the Golden Star!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Draw early and fire from the hip while diving for cover",
                                    "nextNode": {
                                        "content": (
                                            "Your shot goes wild into the wooden boardwalk. Vance fires with deadly precision. "
                                            "The desert claims another reckless gunslinger."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Sneak around through the telegraph alley and breach the bank's rear vault entrance",
                        "nextNode": {
                            "content": (
                                "You pry open the bank's back window with a bowie knife. Inside, two outlaws are busy packing dynamite "
                                "into the iron vault. The hostage sheriff catches your eye from behind the teller cage."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Cut the sheriff's ropes silently and coordinate an ambush",
                                    "nextNode": {
                                        "content": (
                                            "The sheriff grabs a hidden double-barrel shotgun while you flank the vault. "
                                            "Within seconds, the bandits are disarmed and locked in their own cells. "
                                            "You recover all the silver and ride into the sunset as a legendary hero."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Toss a stick of dynamite to scatter them",
                                    "nextNode": {
                                        "content": (
                                            "The blast triggers the rest of the dynamite inside the vault! The entire bank collapses in a roar of timber "
                                            "and fire. Nobody makes it out. The gold is lost to ashes."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # NOIR / DETECTIVE MYSTERY
    # =========================================================================
    @classmethod
    def _build_mystery_story(cls, theme: str) -> Dict[str, Any]:
        title = "The Midnight Ledger of Chicago"
        return {
            "title": title,
            "rootNode": {
                "content": (
                    "Rain hammers the venetian blinds of your fourth-floor private investigation office. "
                    "On your desk sits a cigarette burning down to ash, a glass of bourbon, and a black leather notebook "
                    "stolen from Syndicate boss Tommy Falcone. It contains names that could topple the mayor's office—or get you fitted for cement shoes."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Deliver the ledger directly to the honest federal prosecutor at the pier warehouse",
                        "nextNode": {
                            "content": (
                                "Fog swirls around the docks. The prosecutor waits under a flickering street lamp. "
                                "Just as you step forward, two black sedans screech to a halt, blocking the exits with Tommy's enforcers."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Lure the enforcers into the dark cargo warehouse and pick them off with your snub-nose .38",
                                    "nextNode": {
                                        "content": (
                                            "Using the shipping containers as cover, you outmaneuver the syndicate thugs. "
                                            "The prosecutor escapes to the federal courthouse, and by morning the entire mob hierarchy is arrested. "
                                            "You crack the case and make front-page headlines as the city's finest detective!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Try to bribe them with half the ledger pages",
                                    "nextNode": {
                                        "content": (
                                            "The mobsters laugh and open fire with Tommy guns. You collapse onto the cold wet cobblestones. "
                                            "The city keeps its corrupt secrets."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Confront Falcone directly in his underground speakeasy poker room",
                        "nextNode": {
                            "content": (
                                "You push past the velvet curtain into the smoke-filled cellar. "
                                "Falcone sits at the center table counting stacks of crisp bills. He smiles coolly and pours you a drink."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Reveal that you've already wiretapped the room with federal agents listening",
                                    "nextNode": {
                                        "content": (
                                            "Sirens wail outside as federal agents breach every exit! Falcone raises his hands in bitter defeat. "
                                            "Justice prevails, and you walk away into the misty dawn with a hefty state reward."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Drink the bourbon and accept his counter-offer",
                                    "nextNode": {
                                        "content": (
                                            "The drink tastes of bitter almond. Cyanide. As darkness claims your vision, Falcone quietly takes back his notebook. "
                                            "Another solved case filed in the morgue."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # POST-APOCALYPSE / SURVIVAL
    # =========================================================================
    @classmethod
    def _build_apocalypse_story(cls, theme: str) -> Dict[str, Any]:
        title = "Echoes of Sector Zero"
        return {
            "title": title,
            "rootNode": {
                "content": (
                    "Ash falls like grey snow over the shattered highway overpasses. Your Geiger counter clicks erratically. "
                    "Your radio picks up a faint automated loop broadcast from Bunker 101: a functioning hydroponic sanctuary "
                    "with pure water. But the canyon path is patrolled by the Marauder Clan."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Navigate the underground metro tunnels to bypass the surface raiders",
                        "nextNode": {
                            "content": (
                                "Stagnant water drips in the pitch-black subway tunnels. Your flashlight beam cuts across "
                                "abandoned train carriages. Deep in the darkness, the guttural snarl of mutant tunnel stalkers echoes."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Activate a road flare to blind the beasts and sprint toward the bunker bulkhead",
                                    "nextNode": {
                                        "content": (
                                            "Blinding red magnesium flare light scatters the creatures in agony! You reach the vault door, "
                                            "punch in the access frequency, and the heavy pneumatic door seals shut behind you. "
                                            "Warm air, clean food, and living greenery welcome you. You have found paradise in the wasteland!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Try to stealth past them along the third rail",
                                    "nextNode": {
                                        "content": (
                                            "Your boot kicks an empty tin can. Within seconds, you are surrounded in the dark. "
                                            "The wasteland takes another wanderer."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Hotwire an abandoned combat buggy and barrel straight through the raider barricade",
                        "nextNode": {
                            "content": (
                                "The engine roars to life with a cloud of black exhaust! You slam the pedal down, "
                                "smashing through the rusted sheet-metal gates as raiders open fire with scrap-rifles."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Deploy smoke canister countermeasures and take the mountain ridgeline",
                                    "nextNode": {
                                        "content": (
                                            "Thick grey smoke blinds the raiders' technicals. You gun the engine over the ridge and slide "
                                            "safely into the perimeter defense zone of Bunker 101. Automated turrets protect your arrival. Safe at last!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Try to ram their armored fuel truck",
                                    "nextNode": {
                                        "content": (
                                            "Both vehicles detonate in a massive fireball visible for fifty miles across the crater. "
                                            "Your journey ends in smoke."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # STEAMPUNK / CLOCKWORK
    # =========================================================================
    @classmethod
    def _build_steampunk_story(cls, theme: str) -> Dict[str, Any]:
        title = "The Clockwork Leviathan"
        return {
            "title": title,
            "rootNode": {
                "content": (
                    "Brass steam pipes hiss along the catwalks of the Royal Airship Britannia, five thousand feet above smog-choked New London. "
                    "The Great Chronos Engine—the clockwork mechanism regulating the city's power grid—has been sabotaged by masked saboteurs. "
                    "The giant brass gears are beginning to seize."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Grapple onto the spinning main flywheel to manually dislodge the sabotage wedge",
                        "nextNode": {
                            "content": (
                                "Wind screams in your ears as you dangle above the colossal rotating brass teeth. "
                                "A hardened steel wedge is jammed into the escapement gear. One wrong move will crush you instantly."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Use your steam-powered pneumatic wrench to torque the gear backward",
                                    "nextNode": {
                                        "content": (
                                            "With a deafening hiss of pressurized steam, the gear reverses just enough for the wedge to pop free! "
                                            "The Chronos Engine hums back into harmonious rhythm. The city's lights blaze into life below, "
                                            "and you are decorated as Chief Mechanist of the Empire!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Strike the wedge with a heavy copper hammer",
                                    "nextNode": {
                                        "content": (
                                            "The sudden blow shatters the brittle gear tooth! A cascade of exploding cogs tears through the hull, "
                                            "sending the airship into a downward spiral. Disaster strikes."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Confront the saboteur's leader on the stormy observation deck",
                        "nextNode": {
                            "content": (
                                "Lightning illuminates the brass observation dome. Lord Blackwood stands by the rudder controls, "
                                "holding a detonator wired to the gas envelopes."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Fire an electrified harpoon into the detonator cable to ground the circuit",
                                    "nextNode": {
                                        "content": (
                                            "Sparks flare harmlessly into the storm clouds! Blackwood is captured, and the airship stabilizes. "
                                            "You steer the Britannia safely home to a hero's welcome!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Charge at him directly with your walking-stick sword",
                                    "nextNode": {
                                        "content": (
                                            "He triggers the detonator before you can reach him. The forward gas envelope erupts in flames. "
                                            "The sky claims the Leviathan."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # UNDERWATER / ABYSS
    # =========================================================================
    @classmethod
    def _build_underwater_story(cls, theme: str) -> Dict[str, Any]:
        title = "Abyssal Descent: Trench 9"
        return {
            "title": title,
            "rootNode": {
                "content": (
                    "Six miles beneath the Pacific Ocean, the reinforced research submersible Proteus groans under thirty thousand pounds "
                    "of crushing hydrostatic pressure. External spotlights cut through the pitch-black water, illuminating the monolithic "
                    "ruins of an impossible sunken civilization. Suddenly, an immense bioluminescent presence circles above."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Switch to silent running mode and deploy a decoy flare to divert the leviathan",
                        "nextNode": {
                            "content": (
                                "The sub's engines die down to a whisper. The magnesium flare illuminates the monstrous creature's scales "
                                "as it pursues the light into the abyss. Right ahead lies the airlock entrance to the sunken city."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Dock with the ancient cyclopean airlock and flood it with emergency oxygen",
                                    "nextNode": {
                                        "content": (
                                            "The ancient seals hiss and drain the sea water! Stepping into the forgotten temple, "
                                            "you discover infinite energy crystals capable of ending humanity's climate crisis. "
                                            "Your expedition achieves the greatest scientific discovery in human history!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Anchor to the seafloor and wait for surface recovery ships",
                                    "nextNode": {
                                        "content": (
                                            "Your oxygen scrubbers fail before the rescue ship arrives. Carbon dioxide levels climb in the cold dark. "
                                            "The abyss becomes your final tomb."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Fire high-voltage electric probes to shock the beast away",
                        "nextNode": {
                            "content": (
                                "Ten thousand volts arc through the deep salt water! The creature roars with a sonic vibration "
                                "that shatters the outer viewport glass. Pressure alarms blare shrilly."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Seal the emergency blast titanium shutters and blow the ballast tanks for surface ascent",
                                    "nextNode": {
                                        "content": (
                                            "The titanium shutter snaps shut just in time! The sub shoots upward like a rocket, breaking "
                                            "through the ocean surface into bright sunlight. You survived the deep abyss with sonar footage "
                                            "that will change marine biology forever!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Try to patch the cracking acrylic glass from inside",
                                    "nextNode": {
                                        "content": (
                                            "The immense ocean pressure punches through the fractured glass in a microsecond. "
                                            "The implosion is instantaneous. The depths keep their silence."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # HEIST / INFILTRATION
    # =========================================================================
    @classmethod
    def _build_heist_story(cls, theme: str) -> Dict[str, Any]:
        title = "The Monte Carlo Crown Heist"
        return {
            "title": title,
            "rootNode": {
                "content": (
                    "From the rooftop terrace of the Casino Royale, fireworks explode across the French Riviera. "
                    "Beneath the ballroom lies the Vault of Kings, housing the 100-carat Romanov Diamond. "
                    "Your inside hacker has disabled the laser grid for exactly four minutes."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Rappel down the elevator shaft directly into the vault antechamber",
                        "nextNode": {
                            "content": (
                                "You touch down silently on the rubberized flooring. Ahead lies the 12-tumbler titanium door. "
                                "Your audio stethoscope picks up the gentle click of the counterweights, but guard footsteps echo down the corridor."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Crack the safe with steady precision and pocket the diamond",
                                    "nextNode": {
                                        "content": (
                                            "Click. Click. Clunk! The vault swings open smoothly. You swap the diamond with a weighted glass replica, "
                                            "slip into a tuxedo, and stroll out through the casino floor with a glass of champagne in hand. "
                                            "The greatest heist of the century, pulled off without leaving a trace!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Use thermite paste on the hinges",
                                    "nextNode": {
                                        "content": (
                                            "The burning thermite triggers silent heat sensors across the building. "
                                            "Steel security shutters slam down, sealing you inside the vault until Interpol arrives."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Disguise yourself as the high-roller casino manager and access the VIP elevator",
                        "nextNode": {
                            "content": (
                                "With tailor-made tuxedo and forged credentials, you walk through the security checkpoints. "
                                "At the final iris scanner, the chief of security narrows his eyes and asks for your daily verification code."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Bluff with icy charm and whisper the secret phrase your informant supplied",
                                    "nextNode": {
                                        "content": (
                                            "The guard nods respectfully and steps aside with an apology. You gain access to the private display, "
                                            "secure the gemstone, and escape on a waiting speedboat into the Mediterranean night. Millions richer and totally free!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Attempt to grab his taser and fight your way through",
                                    "nextNode": {
                                        "content": (
                                            "Six armed guards draw their weapons instantly. Tackled to the carpet, you are led away in handcuffs. Busted."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # TIME TRAVEL / PARADOX
    # =========================================================================
    @classmethod
    def _build_timetravel_story(cls, theme: str) -> Dict[str, Any]:
        title = "Chronos Fracture: The Temporal Paradox"
        return {
            "title": title,
            "rootNode": {
                "content": (
                    "Your chronometer spins wildly as temporal turbulence tears through the quantum capsule. "
                    "You emerge at the nexus of shattered timelines: Ancient Alexandria, Victorian London, and a 25th-century "
                    "cyber metropolis are all collapsing into one point in time. The Chrono-Core is overheating."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": "Calibrate the tachyon field to restore the primary timeline at the Library of Alexandria",
                        "nextNode": {
                            "content": (
                                "You materialise inside the grand marble halls of Alexandria as scholars flee unearthly energy rifts. "
                                "At the center of the library, the historical divergence point is burning in chronal flames."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Use the quantum stabilizer to anchor the historical scrolls and close the rift",
                                    "nextNode": {
                                        "content": (
                                            "A wave of pure blue light ripples across history! The split branches knit back together seamlessly. "
                                            "You return to your laboratory in the present day, with history intact and knowledge preserved for all time. Victory!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Attempt to absorb the temporal energy into your personal battery pack",
                                    "nextNode": {
                                        "content": (
                                            "The timeline fractures irrevocably. You are cast into a timeless void, existing outside of reality forever."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Jump forward to the Cybernetic Epoch to find an advanced quantum heatsink",
                        "nextNode": {
                            "content": (
                                "You arrive atop a kilometer-high titanium skyscraper in the year 2482. "
                                "Rogue temporal hunters spot your arrival and open fire with matter-disruptor rifles."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Freeze local time for ten seconds and extract the heatsink from their command console",
                                    "nextNode": {
                                        "content": (
                                            "Time stops. Bullets hang frozen in mid-air. You calmly walk across the room, take the heatsink, "
                                            "and trigger your jump-drive. Back in your own era, the device cools the core to perfection. You master the timestream!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": "Engage them in a high-speed firefight along the skyway",
                                    "nextNode": {
                                        "content": (
                                            "A stray shot pierces your Chrono-Core, causing a local temporal loop. "
                                            "You are doomed to repeat this same thirty-second shootout for eternity."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # =========================================================================
    # UNIVERSAL CUSTOM THEME GENERATOR
    # =========================================================================
    @classmethod
    def _build_custom_story(cls, theme: str) -> Dict[str, Any]:
        """
        Dynamically synthesizes a completely unique story for any custom user prompt or unrecognized theme.
        Extracts keywords, invents stakes, characters, setting, and meaningful branches.
        """
        clean_theme = re.sub(r'[^a-zA-Z0-9\s]', '', theme).strip()
        words = clean_theme.split()
        capitalized_theme = clean_theme.title()

        subject = words[0].title() if words else "Adventure"
        secondary = words[1].title() if len(words) > 1 else "Odyssey"

        title_patterns = [
            f"The Mystery of the {capitalized_theme}",
            f"Escape from the {capitalized_theme}",
            f"{capitalized_theme}: The Final Trial",
            f"Chronicles of the {subject}",
            f"The Legend of {capitalized_theme}"
        ]
        title = random.choice(title_patterns)

        setting = f"the legendary domain of {clean_theme}"
        objective = f"uncover the ancient secret of the {clean_theme}"
        obstacle = f"unexpected perils and watchful guardians guarding {clean_theme}"

        return {
            "title": title,
            "rootNode": {
                "content": (
                    f"Your journey brings you to {setting}. The air hums with anticipation and untold mysteries. "
                    f"Your singular objective is clear: you must {objective}. But the route is fraught with danger, "
                    f"as {obstacle} stand directly in your path. Two distinct routes present themselves."
                ),
                "isEnding": False,
                "isWinningEnding": False,
                "options": [
                    {
                        "text": f"Take the bold, direct path through the heart of {clean_theme}",
                        "nextNode": {
                            "content": (
                                f"You advance directly forward, braving the intense challenges of {clean_theme}. "
                                f"Your quick instincts allow you to overcome the initial hazards, bringing you into an inner sanctum. "
                                f"Ahead, the final mechanism controlling the fate of {clean_theme} requires an immediate decision."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": f"Apply your focused skill and decisive courage to solve the trial",
                                    "nextNode": {
                                        "content": (
                                            f"With precision and resolve, you master the final challenge of {clean_theme}! "
                                            f"The trials yield before you, granting you total victory, legendary renown, and the greatest prize of the quest. "
                                            f"You emerge triumphant!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": f"Rush recklessly into the inner core without proper preparation",
                                    "nextNode": {
                                        "content": (
                                            f"Haste proves your undoing. The defensive mechanisms of {clean_theme} trigger simultaneously, "
                                            f"sealing the exit gates and leaving you trapped in the uncharted depths. Your quest ends in failure."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": f"Seek a clever tactical alternative around the perimeter of {clean_theme}",
                        "nextNode": {
                            "content": (
                                f"Stepping quietly along the shadows, you discover an overlooked back-channel into {clean_theme}. "
                                f"Here, an ancient guardian sentinel stands watch, monitoring the perimeter."
                            ),
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": f"Negotiate with the sentinel using wisdom and an offer of mutual alliance",
                                    "nextNode": {
                                        "content": (
                                            f"Impressed by your honor and intellect, the guardian bows and deactivates all defenses. "
                                            f"It welcomes you into the inner treasures of {clean_theme}, ushering in an era of peace and prosperity. "
                                            f"You achieve a flawless, harmonious victory!"
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                },
                                {
                                    "text": f"Attempt to provoke and distract the sentinel into a reckless fight",
                                    "nextNode": {
                                        "content": (
                                            f"The sentinel detects your hostility instantly. With superhuman speed it disarms you and casts you out of {clean_theme}. "
                                            f"You are forced into a bitter retreat, empty-handed."
                                        ),
                                        "isEnding": True,
                                        "isWinningEnding": False,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
