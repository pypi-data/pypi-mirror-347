"""
Constants and enumerations shared across the pylegifrance package.

This module centralizes all shared constants and enumerations to avoid duplication
and ensure consistency across the codebase.
"""

from enum import Enum
from typing import Dict, List, Tuple


class CodeNom(str, Enum):
    """
    Enumeration of code names and their full titles.
    Used for code identification across the application.
    """

    # Common codes
    CCIV = "Code civil"
    CPRCIV = "Code de procédure civile"
    CCOM = "Code de commerce"
    CTRAV = "Code du travail"
    CPI = "Code de la propriété intellectuelle"
    CPEN = "Code pénal"
    CPP = "Code de procédure pénale"
    CASSUR = "Code des assurances"
    CCONSO = "Code de la consommation"
    CSI = "Code de la sécurité intérieure"
    CSP = "Code de la santé publique"
    CSS = "Code de la sécurité sociale"
    CESEDA = "Code de l'entrée et du séjour des étrangers et du droit d'asile"
    CGCT = "Code général des collectivités territoriales"
    CPCE = "Code des postes et des communications électroniques"
    CENV = "Code de l'environnement"
    CJA = "Code de justice administrative"

    # Additional codes
    CC = "Code civil"  # Alias for CCIV
    CDC = "Code des communes"
    CDDDA = "Code de déontologie des architectes"
    CDJA = "Code de justice administrative"  # Alias for CJA
    CDJM = "Code de justice militaire (nouveau)"
    CDSEDF = "Code de l'action sociale et des familles"
    CD = "Code de l'énergie"
    CDEDSDÉEDD = "Code de l'entrée et du séjour des étrangers et du droit d'asile"  # Alias for CESEDA
    CDPCP = "Code de l'expropriation pour cause d'utilité publique"
    CDJ = "Code de l'organisation judiciaire"
    CDLCP = "Code de la commande publique"
    CDLC = "Code de la consommation"  # Alias for CCONSO
    CDLCED = "Code de la construction et de l'habitation"
    CDLD = "Code de la défense"
    CDLFEDS = "Code de la famille et de l'aide sociale"
    CDLJPDM = "Code de la justice pénale des mineurs"
    CDLLDLMMEDNDM = "Code de la Légion d'honneur, de la Médaille militaire et de l'ordre national du Mérite"
    CDLM = "Code de la mutualité"
    CDLPI = "Code de la propriété intellectuelle"  # Alias for CPI
    CDLR = "Code de la route"
    CDLSP = "Code de la santé publique"  # Alias for CSP
    CDLSI = "Code de la sécurité intérieure"  # Alias for CSI
    CDLSS = "Code de la sécurité sociale"  # Alias for CSS
    CDLVR = "Code de la voirie routière"
    CDPC = "Code des procédures civiles d'exécution"
    CDPP = "Code de procédure pénale"  # Alias for CPP
    CDA = "Code des assurances"  # Alias for CASSUR
    CDCDL = "Code des communes de la Nouvelle-Calédonie"
    CDD = "Code des douanes"
    CDDDM = "Code des douanes de Mayotte"
    CDISLBES = "Code des impositions sur les biens et services"
    CDIMEDM = "Code des instruments monétaires et des médailles"
    CDJF = "Code des juridictions financières"
    CDPCEMDR = "Code des pensions civiles et militaires de retraite"
    CDPDRDMFDDPODP = "Code des pensions de retraite des marins français du commerce, de pêche ou de plaisance"
    CDPMEDVDG = "Code des pensions militaires d'invalidité et des victimes de guerre"
    CDPM = "Code des ports maritimes"
    CDPEDCÉ = "Code des postes et des communications électroniques"  # Alias for CPCE
    CDRELPE = "Code des relations entre le public et l'administration"
    CDT = "Code du travail"  # Alias for CTRAV
    CDEPDLMM = "Code disciplinaire et pénal de la marine marchande"
    CDCEDA = "Code du cinéma et de l'image animée"
    CDDD = "Code du domaine de l'Etat"
    CDDDEDCPAÀLCTDM = "Code du domaine de l'Etat et des collectivités publiques applicable à la collectivité territoriale de Mayotte"
    CDDPFEDLNI = "Code du domaine public fluvial et de la navigation intérieure"
    CDP = "Code du patrimoine"
    CDSN = "Code du service national"
    CDS = "Code du sport"
    CDTM = "Code du travail maritime"
    CF = "Code forestier (nouveau)"
    CGDLFP = "Code général de la fonction publique"
    CGDLPDPP = "Code général de la propriété des personnes publiques"
    CGDCT = "Code général des collectivités territoriales"  # Alias for CGCT
    CGDI = "Code général des impôts"
    CGDAI = "Code général des impôts, annexe IV"
    CM = "Code minier (nouveau)"
    CMEF = "Code monétaire et financier"
    CP = "Code pénitentiaire"
    CR = "Code rural (ancien)"
    CREDLPM = "Code rural et de la pêche maritime"
    CÉ = "Code électoral"
    LDPF = "Livre des procédures fiscales"
    CASF = "Code de l'action sociale et des familles"


# Dictionary mapping code abbreviations to their full names
# This is kept for backward compatibility
CODE_LIST: Dict[str, str] = {
    code.name: code.value
    for code in CodeNom
    if code.name
    in [
        "CCIV",
        "CPRCIV",
        "CCOM",
        "CTRAV",
        "CPI",
        "CPEN",
        "CPP",
        "CASSUR",
        "CCONSO",
        "CSI",
        "CSP",
        "CSS",
        "CESEDA",
        "CGCT",
        "CPCE",
        "CENV",
        "CJA",
    ]
}


class SupplyEnum(str, Enum):
    """
    Enumeration of supply sources for suggestions.
    Used to specify which data sources to query for suggestions.
    """

    ALL = "ALL"
    ALL_SUGGEST = "ALL_SUGGEST"
    LODA_LIST = "LODA_LIST"
    CODE_LIST = "CODE_LIST"
    CODE_RELEASE_DATE = "CODE_RELEASE_DATE"
    CODE_RELEASE_DATE_SUGGEST = "CODE_RELEASE_DATE_SUGGEST"
    CODE_LEGAL_STATUS = "CODE_LEGAL_STATUS"
    LODA_RELEASE_DATE = "LODA_RELEASE_DATE"
    LODA_RELEASE_DATE_SUGGEST = "LODA_RELEASE_DATE_SUGGEST"
    LODA_LEGAL_STATUS = "LODA_LEGAL_STATUS"
    KALI = "KALI"
    KALI_TEXT = "KALI_TEXT"
    CONSTIT = "CONSTIT"
    CETAT = "CETAT"
    JUFI = "JUFI"
    JURI = "JURI"
    JORF = "JORF"
    JORF_SUGGEST = "JORF_SUGGEST"
    CNIL = "CNIL"
    ARTICLE = "ARTICLE"
    CIRC = "CIRC"
    ACCO = "ACCO"
    PDF = "PDF"


class Fonds(str, Enum):
    """
    Enumeration of data sources/collections.
    Used to specify which data sources to query.
    """

    JORF = "JORF"
    CNIL = "CNIL"
    CETAT = "CETAT"
    JURI = "JURI"
    JUFI = "JUFI"
    CONSTIT = "CONSTIT"
    KALI = "KALI"
    CODE_DATE = "CODE_DATE"
    CODE_ETAT = "CODE_ETAT"
    LODA_DATE = "LODA_DATE"
    LODA_ETAT = "LODA_ETAT"
    ALL = "ALL"
    CIRC = "CIRC"
    ACCO = "ACCO"


class Nature(str, Enum):
    """
    Enumeration of document nature types.
    """

    LOI = "LOI"
    ORDONNANCE = "ORDONNANCE"
    DECRET = "DECRET"
    ARRETE = "ARRETE"


class TypeFacettes(str, Enum):
    """
    Enumeration of facet types for filtering.
    """

    NOM_CODE = "NOM_CODE"
    DATE_SIGNATURE = "DATE_SIGNATURE"
    DATE_VERSION = "DATE_VERSION"
    TEXT_LEGAL_STATUS = "TEXT_LEGAL_STATUS"
    ARTICLE_LEGAL_STATUS = "ARTICLE_LEGAL_STATUS"
    NATURE = "NATURE"
    NOR = "NOR"


class TypeRecherche(Enum):
    """
    Enumeration of search types.
    """

    EXACTE = "EXACTE"
    APPROXIMATIVE = "APPROXIMATIVE"
    TOUS_LES_MOTS = "TOUS_LES_MOTS"
    UN_DES_MOTS = "UN_DES_MOTS"
    AUCUN_MOT = "AUCUN_MOT"
    EXPRESSION = "EXPRESSION"
    CHAMP_VIDE = "CHAMP_VIDE"


# List of deprecated routes and their replacements
# Format: (deprecated_route, replacement_route, replacement_params)
# If there are no special parameters needed for the replacement, use None
DEPRECATED_ROUTES: List[Tuple[str, str, Dict[str, str]]] = [
    ("consult/code/tableMatieres", "consult/legi/tableMatieres", {"nature": "CODE"}),
]
