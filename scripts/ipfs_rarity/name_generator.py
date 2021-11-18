from metadata.template_metadata import (
    super_rare_prompts,
    rare_prompts,
    description_prompts,
)
import random

from scripts.file_functions import update_prompts


def fantasy_name():
    return (
        (random.choice(FIRST) + random.choice(SECOND)).capitalize()
        + " "
        + (random.choice(SECOND) + random.choice(FIRST)).capitalize()
    )


def get_common_bio(familiar, status, name, clazz, land):
    career = [
        "banker",
        "store keeper",
        "craftmans",
        "guard",
        "musician",
        "dancer",
        "entertainer",
        "free-loader",
        "ship mate",
        "traveler",
        "farmer",
        "singer",
        "chef",
        "builder",
        "entertainer",
        "peasant",
    ]
    adjective = [
        "simple",
        "common",
        "respectable",
        "pleasant",
        "ordinary",
        "notorious",
        "smelling",
        "crude",
        "fair",
        "decent",
        "average",
        "kind",
        "decent",
    ]
    common_bio = [
        f"I was born before the war come to our town, it has ravage our town and destroyed our way of life.",
        f"I was a lowly {clazz}, when I was drafted into the war.",
        f"Hi, my given name is {name}, if you have seen my {random.choice(familiar)} tell them they are my greatest {random.choice(status)} I hold left in my life.",
        f"I just want to find my {random.choice(familiar)} when this is all over.",
        f"Greetings, some call me {name}. I work as a {clazz} if that's what your in search of.",
        f"If you are looking for a {clazz} keep looking, none here go away!",
        f"I was born in {land} or so I have been told, sometimes I wonder if that's where everything went wrong",
        f"I was born in {land} or so I have been told, I can't wait to get back their when this is all over",
        f"What does a person named {name} from {land} who is a {clazz} hold deer? {status}",
        "These are the people who were once a tribe; now are being hunted down because of their beliefs",
        "I was born without a story, pulled here and there. This is the life I have been given.",
        "Seek the moonstone.",
        f"Once nothing but a {random.choice(adjective)} {random.choice(career)}.",
        f"I just want to be a {random.choice(adjective)} {random.choice(career)}.",
    ]
    return common_bio


def get_uncommon_bio(familiar, status, name, clazz, land):
    uncommon_bio = [
        f"I was born before the war come to our town, it has ravage our town and destroyed our way of life. I feel only obligated to restore what was take from us.",
        f"I was a respected {clazz}, when I was drafted into the war. I will make my home land {land} proud of me.",
        f"Hi, my given name is {name}, if you have seen my {random.choice(familiar)} tell them they are my greatest {random.choice(status)} I hold in my life.",
        f"I will find my {random.choice(familiar)} when this is all over. When we win this war and things return to how they were.",
        f"Greetings, the name's {name}. I work as a {clazz} and the best at it.",
        f"If you are looking for a {clazz}, you best head on back where you came from, there's nothing here for you.",
        f"I was born in {land} or so I have been told, sometimes I wonder if {random.choice(familiar)} will still be there when I return.",
        f"I was born in {land} or so I have been told, that's where I learned about {clazz}, that's where I got good at my craft.",
        f"What does a person named {name} from {land} who is a {clazz} hold deer? {status}",
        f"I believe in Yves.",
    ]
    return uncommon_bio


def character_bios(
    bios_counter, rare_counter, super_rare_counter, rarity, name, clazz, land
):
    familiar = [
        "family",
        "brother",
        "mother",
        "sister",
        "wife",
        "husband",
        "daughter",
        "son",
    ]
    status = [
        "pride",
        "disappointment",
        "hope",
        "meaning",
        "love",
        "shame",
        "fear",
        "respect",
    ]
    bios = None
    if (
        rarity >= 11
        and super_rare_counter < len(super_rare_prompts)
        and random.choice([True, False])
    ):
        bios = super_rare_prompts[super_rare_counter]
        super_rare_counter = super_rare_counter + 1
        update_prompts(bios)
    if (
        rarity >= 8
        and bios == None
        and rare_counter < len(rare_prompts)
        and random.choice([True, False])
    ):
        bios = rare_prompts[rare_counter]
        rare_counter = rare_counter + 1
        update_prompts(bios)
    if (
        rarity >= 5
        and bios == None
        and bios_counter < len(description_prompts)
        and random.choice([True, False])
    ):
        bios = description_prompts[bios_counter]
        update_prompts(bios)
        bios_counter = bios_counter + 1
    if rarity >= 3 and bios == None and random.choice([True, False]):
        bios = random.choice(get_uncommon_bio(familiar, status, name, clazz, land))
    else:
        bios = random.choice(get_common_bio(familiar, status, name, clazz, land))
    return (bios, bios_counter, super_rare_counter, rare_counter)


FIRST = [
    "a",
    "ab",
    "ac",
    "ad",
    "add",
    "addr",
    "ag",
    "ar",
    "ash",
    "ara",
    "anu",
    "bal",
    "bil",
    "boro",
    "boo",
    "bern",
    "bra",
    "cam",
    "car",
    "cas",
    "cere",
    "co",
    "con",
    "cor",
    "da",
    "dag",
    "digi",
    "doo",
    "elen",
    "el",
    "en",
    "eo",
    "faf",
    "fan",
    "fara",
    "fre",
    "fro",
    "ga",
    "gala",
    "gi",
    "has",
    "he",
    "heim",
    "ho",
    "ja",
    "jan",
    "je",
    "jen",
    "jon",
    "jom",
    "jomi",
    "isil",
    "in",
    "ingerants",
    "ini",
    "is",
    "ka",
    "kuo",
    "lance",
    "len",
    "lin",
    "lo",
    "ma",
    "mangna",
    "mag",
    "mar",
    "mi",
    "mo",
    "moon",
    "mor",
    "mora",
    "nin",
    "o",
    "oaba",
    "obi",
    "og",
    "pelli",
    "poke",
    "por",
    "ran",
    "rud",
    "sam",
    "stein",
    "stine",
    "she",
    "sheel",
    "shin",
    "shog",
    "son",
    "sur",
    "theo",
    "tho",
    "thorna",
    "tris",
    "trent" "u",
    "uh",
    "ul",
    "vap",
    "vish",
    "ya",
    "yo",
    "yyr",
]

SECOND = [
    "a",
    "aar",
    "an",
    "ant",
    "and",
    "aft",
    "add",
    "ack",
    "ad",
    "amber",
    "ass",
    "ase",
    "arrt",
    "art",
    "amz",
    "ba",
    "bis",
    "bo",
    "bus",
    "da",
    "dal",
    "dagz",
    "den",
    "di",
    "dil",
    "din",
    "do",
    "dor",
    "dra",
    "dur",
    "gi",
    "gauble",
    "gen",
    "glum",
    "go",
    "gu",
    "gorn",
    "goth",
    "had",
    "hard",
    "is",
    "k",
    "ki",
    "koon",
    "ku",
    "lad",
    "ler",
    "li",
    "limeric",
    "lot",
    "lui",
    "ma",
    "man",
    "mir",
    "mon",
    "mus",
    "nan",
    "ni",
    "nim",
    "nor",
    "ny",
    "nyka",
    "nym",
    "nyt",
    "nu",
    "io",
    "pian",
    "ra",
    "rak",
    "ric",
    "rin",
    "rum",
    "rus",
    "rut",
    "sek",
    "sha",
    "thos",
    "thur",
    "toa",
    "tu",
    "tum",
    "tur",
    "tred",
    "varl",
    "wain",
    "wat",
    "wan",
    "win",
    "wise",
    "ya",
    "yi",
    "ye",
    "yio",
    "yim",
    "yoo",
    "yuti",
    "yoorn",
    "zel",
]
