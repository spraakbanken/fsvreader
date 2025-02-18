from typing import TypedDict


class Text(TypedDict):
    title: str
    commentary: str


class Metadata(TypedDict):
    title: str
    texts: dict[str, Text]


METADATA: dict[str, Metadata] = {
    "aldre_lagar": {
        "title": "Äldre lagar",
        "texts": {
            "SkL.html": {
                "title": "Skånelagen, enligt Holm B 76",
                "commentary": "txt 1203-12 / ms 1300-25",
            },
            "AVgL.html": {
                "title": "Äldre Västgötalagen, enligt Holm B 59",
                "commentary": "txt ca 1220 / ms ca 1280",
            },
            "GL.html": {
                "title": "Gutalagen, enligt Holm B 64",
                "commentary": "ms ca 1350",
            },
            "OgL.html": {
                "title": "Östgötalagen, enligt Holm B 50",
                "commentary": "txt 1280–90 / ms ca 1350",
            },
            "YVgL.html": {
                "title": "Yngre Västgötalagen, enligt Holm B 58",
                "commentary": "txt ca 1280 / ms ca 1350",
            },
            "DL.html": {
                "title": "Äldre Västmannalagen / Dalalagen, enligt Holm B 54",
                "commentary": "txt ca 1280",
            },
            "UL.html": {
                "title": "Upplandslagen, enligt Ups B 12",
                "commentary": "ms ca 1350",
            },
            "HL.html": {
                "title": "Hälsingelagen, enligt Ups B 49",
                "commentary": "ms 1350–1400",
            },
            "VmL.html": {
                "title": "Yngre Västmannalagen enligt Holm B 57",
                "commentary": "txt 1300–25 / ms 1300-50",
            },
            "BjR.html": {
                "title": "Bjärköarätten, enligt Holm B 58",
                "commentary": "ms ca 1350",
            },
            "SmL_Kb.html": {
                "title": "Smålandslagens Kyrkobalk",
                "commentary": "ms 1350–1400",
            },
            "SdmL.html": {
                "title": "Södermannalagen, enligt Holm B 53",
                "commentary": "txt 1327 / ms ca 1330",
            },
            "SdmL-A.html": {
                "title": "Södermannalagen, enligt Holm B 53 [Utdrag?]",
                "commentary": "txt 1327 / ms ca 1330",
            },
            "MEL.html": {
                "title": "Magnus Erikssons Landslag, enligt AM 51",
                "commentary": "txt ca 1350 / ms ca 1350",
            },
            "MESt.html": {
                "title": "Magnus Erikssons Stadslag, enligt Holm B 154",
                "commentary": "txt 1357 / ms 1400–50",
            },
        },
    },
    "aldre_profan": {
        "title": "Äldre övrigt profan prosa",
        "texts": {
            "Ks.html": {
                "title": "Kungastyrelsen, efter Bureus utgåva (förkommen handskrift)",
                "commentary": "Bureus 1632",
            }
        },
    },
    "aldre_religios": {
        "title": "Äldre religiös prosa",
        "texts": {
            "Legendarium-B.html": {
                "title": "Fornsvenska legendariet, enligt Ups C 528",
                "commentary": "txt 1276–1308 / ms 1400-50",
            },
            "Moses-B.html": {
                "title": "Pentateuchparafrasen, enligt Holm A1",
                "commentary": "txt 1300–50 / ms 1526",
            },
            "Birgitta_aut-B.html": {
                "title": "Birgittas uppenbarelser, fsv original",
                "commentary": "1340–1370",
            },
        },
    },
}
