from __future__ import annotations

from .custom import CustomTextChoiceField

__all__ = ['MajorField']


class MajorField(CustomTextChoiceField):
    APPLIED_COMPUTATIONAL_MATHEMATICS = "ACM"
    APPLIED_PHYSICS_AND_MATHEMATICS = "APAM"
    ASTROPARTICLE_PHYSICS = "AP"
    ATTITUDE_FORMATION = "AF"
    BIOCHEMICAL_ENGINEERING = "BE"
    BIOCHEMISTRY = "BC"
    BIOCHEMISTRY_AND_CELL_BIOLOGY = "BACB"
    BIOINFORMATICS_AND_COMPUTATIONAL_BIOLOGY = "BCCB"
    BIOLOGICAL_RECOGNITION = "BR"
    BIOLOGY = "B"
    BIOLOGY_NEUROSCIENCE = "BNEO"
    BIOTECHNOLOGY = "BT"
    BUISNESS_ADMINISTRATION = "BA"
    CHANGING_LIVES_IN_CHANGING_SOCIOCULTURAL_CONTEXTS = "CLICSC"
    CHEMISTRY = "C"
    COMMUNICATIONS = "COM"
    COMPARATIVE_POLITICS_AND_SOCIOLOGY = "CPAS"
    COMPUTATIONAL_LIFE_SCIENCE = "CLS"
    COMPUTER_SCIENCE = "CS"
    DATA_ENGINEERING = "DE"
    EARTH_AND_ENVIRONMENTAL_SCIENCES = "EAES"
    EARTH_AND_SPACE_SCIENCES = "EASS"
    ELECTRICAL_AND_COMPUTER_ENGINEERING = "EACE"
    ELECTRICAL_ENGINEERING_AND_COMPUTER_SCIENCE = "EECS"
    EUROPEAN_UTILITY_MANAGEMENT = "EUM"
    GEO_OCEAN_DYNAMICS = "GOD"
    GEOSCIENCES_AND_ASTROPHYSICS = "GAA"
    GLOBAL_ECONOMICS_AND_MANAGEMENT = "GEAM"
    GLOBAL_GOVERNANCE_AND_REGIONAL_INTEGRATION = "GGARI"
    GLOBAL_VISUAL_COMMUNICATION = "GVC"
    HISTORY = "H"
    HISTORY_AND_THEORY_OF_ART_AND_LITERATURE = "HATOAAL"
    HUMANITIES = "HM"
    INDUSTRIAL_ENGINEERING_AND_MANAGEMENT = "IEAM"
    INFORMATION_MANAGEMENT_AND_SYSTEMS = "IMAS"
    INTEGRATED_CULTURAL_STUDIES = "ICS"
    INTEGRATED_ENVIRONMENTAL_STUDIES = "IES"
    INTEGRATED_SOCIAL_AND_COGNITIVE_PSYCHOLOGY = "ISACP"
    INTEGRATED_SOCIAL_SCIENCES = "ISS"
    INTELLIGENT_MOBILE_SYSTEMS = "IMS"
    INTERCULTURAL_HUMANITIES = "IH"
    INTERCULTURAL_RELATIONS_AND_BEHAVIOUR = "IRAB"
    INTERNATIONAL_RELATIONS_GLOBAL_GOVERNANCE_AND_SOCIAL_THEORY = "IRGGAST"
    INTERNATIONAL_BUSINESS_ADMINISTRATION = 'IBA'
    INTERNATIONAL_COMMUNICATION = "IC"
    INTERNATIONAL_HISTORY_AND_POLITICS = "IHAP"
    INTERNATIONAL_LOGISTICS_ENGINEERING_AND_MANAGEMENT = "ILEAM"
    INTERNATIONAL_POLITICS_AND_HISTORY = "IPAH"
    INTERNATIONAL_RELATIONS = "IR"
    LIFE_COURSE_AND_LIFESPAN_DYNAMICS = "LCALD"
    LIFELONG_LEARNING = "LL"
    MARINE_MICROBIOLOGY = "MM"
    MATHEMATICS = "M"
    MEDICAL_CHEMISTRY_AND_CHEMICAL_BIOLOGY = "MCACB"
    MEDICAL_NATURAL_SCIENCES = "MNS"
    MODERN_GLOBAL_HISTORY = "MGH"
    MOLECULAR_LIFE_SCIENCE = "MLS"
    NANOMOLECULAR_SCIENCES = "NS"
    NEUROSCIENCE = "N"
    PHYSICS = "P"
    POLITICAL_ECONOMY_PUBLIC_POLICY = "PEPP"
    PRODUCTIVE_ADULT_DEVELOPMENT = "PAD"
    PSYCHOLOGY = "PSY"
    SMART_SYSTEMS = "SS"
    SUPPLY_CHAIN_ENGINEERING_AND_MANAGEMENT = "SCEAM"
    VISUAL_COMMUNICATION_AND_EXPERTISE = "VCAE"
    WELFARE_STATE_INEQUALITY_AND_QUALITY_OF_LIFE = "WSIAQOL"
    OTHER = "OTHER"

    CHOICES = (
        (APPLIED_COMPUTATIONAL_MATHEMATICS,
         "Applied Computational Mathematics (ACM)"),
        (APPLIED_PHYSICS_AND_MATHEMATICS, "Applied Physics and Mathematics"),
        (ASTROPARTICLE_PHYSICS, "Astroparticle Physics"),
        (ATTITUDE_FORMATION, "Attitude Formation"),
        (BIOCHEMICAL_ENGINEERING, "Biochemical Engineering"),
        (BIOCHEMISTRY, "Biochemistry"),
        (
            BIOCHEMISTRY_AND_CELL_BIOLOGY,
            "Biochemistry and Cell Biology (BCCB)"),
        (BIOINFORMATICS_AND_COMPUTATIONAL_BIOLOGY,
         "Bioinformatics and Computational Biology"),
        (BIOLOGICAL_RECOGNITION, "Biological Recognition"),
        (BIOLOGY, "Biology"),
        (BIOLOGY_NEUROSCIENCE, "Biology/Neuroscience"),
        (BIOTECHNOLOGY, "Biotechnology"),
        (BUISNESS_ADMINISTRATION, "Buisness Administration"),
        (CHANGING_LIVES_IN_CHANGING_SOCIOCULTURAL_CONTEXTS,
         "Changing Lives in Changing Socio-Cultural Contexts"),
        (CHEMISTRY, "Chemistry"),
        (COMMUNICATIONS, "Communications"),
        (COMPARATIVE_POLITICS_AND_SOCIOLOGY,
         "Comparative PolitIcs and Sociology"),
        (COMPUTATIONAL_LIFE_SCIENCE, 'Computational Life Science'),
        (COMPUTER_SCIENCE, "Computer Science"),
        (DATA_ENGINEERING, "Data Engineering"),
        (EARTH_AND_ENVIRONMENTAL_SCIENCES, "Earth and Environmental Sciences"),
        (EARTH_AND_SPACE_SCIENCES, "Earth and Space Sciences"),
        (ELECTRICAL_AND_COMPUTER_ENGINEERING,
         "Electrical and Computer Engineering"),
        (ELECTRICAL_ENGINEERING_AND_COMPUTER_SCIENCE,
         "Electrical Engineering and Computer Science"),
        (EUROPEAN_UTILITY_MANAGEMENT, "European Utility Management"),
        (GEO_OCEAN_DYNAMICS, "Geo-Ocean Dynamics"),
        (GEOSCIENCES_AND_ASTROPHYSICS, "Geosciences and Astrophysics"),
        (GLOBAL_ECONOMICS_AND_MANAGEMENT,
         "Global Economics and Management (GEM)"),
        (GLOBAL_GOVERNANCE_AND_REGIONAL_INTEGRATION,
         "Global Governance and Regional Integration"),
        (GLOBAL_VISUAL_COMMUNICATION, "Global Visual Communication"),
        (HISTORY, "History"),
        (HISTORY_AND_THEORY_OF_ART_AND_LITERATURE,
         "History and Theory of Art and Literature"),
        (HUMANITIES, "Humanities"),
        (INDUSTRIAL_ENGINEERING_AND_MANAGEMENT,
         "Industrial Engineering and Management"),
        (INFORMATION_MANAGEMENT_AND_SYSTEMS,
         "Information Management and Systems (IMS)"),
        (INTEGRATED_CULTURAL_STUDIES, "Integrated Cultural Studies"),
        (INTEGRATED_ENVIRONMENTAL_STUDIES, "Integrated Environmental Studies"),
        (INTEGRATED_SOCIAL_AND_COGNITIVE_PSYCHOLOGY,
         "Integrated Social and Cognitive Psychology (ISCP)"),
        (INTEGRATED_SOCIAL_SCIENCES, "Integrated Social Sciences"),
        (INTELLIGENT_MOBILE_SYSTEMS, "Intelligent Mobile Systems"),
        (INTERCULTURAL_HUMANITIES, "Intercultural Humanities"),
        (INTERCULTURAL_RELATIONS_AND_BEHAVIOUR,
         "Intercultural Relations and Behaviour (IRB)"),
        (INTERNATIONAL_RELATIONS_GLOBAL_GOVERNANCE_AND_SOCIAL_THEORY, "International Relations: Global Governance and Social Theory"),
        (INTERNATIONAL_BUSINESS_ADMINISTRATION,
         "International Business Administration"),
        (INTERNATIONAL_COMMUNICATION, "International Communication"),
        (INTERNATIONAL_HISTORY_AND_POLITICS,
         "International History and Politics"),
        (INTERNATIONAL_LOGISTICS_ENGINEERING_AND_MANAGEMENT,
         "International Logistics Engineering and Management (ILME)"),
        (INTERNATIONAL_POLITICS_AND_HISTORY,
         "International Politics and History (IPH)"),
        (INTERNATIONAL_RELATIONS, "International Relations"),
        (
            LIFE_COURSE_AND_LIFESPAN_DYNAMICS,
            "Life-Course and Lifespan Dynamics"),
        (LIFELONG_LEARNING, "Lifelong Learning"),
        (MARINE_MICROBIOLOGY, "Marine Microbiology"),
        (MATHEMATICS, "Mathematics"),
        (MEDICAL_CHEMISTRY_AND_CHEMICAL_BIOLOGY,
         "Medical Chemistry and Chemical Biology"),
        (MEDICAL_NATURAL_SCIENCES, "Medical Natural Sciences"),
        (MODERN_GLOBAL_HISTORY, "Modern Global History"),
        (MOLECULAR_LIFE_SCIENCE, "Molecular Life Science"),
        (NANOMOLECULAR_SCIENCES, "Nanomolecular Sciences"),
        (NEUROSCIENCE, "Neuroscience"),
        (PHYSICS, "Physics"),
        (POLITICAL_ECONOMY_PUBLIC_POLICY, "Political Economy & Public Policy"),
        (PRODUCTIVE_ADULT_DEVELOPMENT, "Productive Adult Development"),
        (PSYCHOLOGY, "Psychology"),
        (SMART_SYSTEMS, "Smart Systems"),
        (SUPPLY_CHAIN_ENGINEERING_AND_MANAGEMENT,
         "Supply Chain Engineering and Management"),
        (VISUAL_COMMUNICATION_AND_EXPERTISE,
         "Visual Communication and Expertise"),
        (WELFARE_STATE_INEQUALITY_AND_QUALITY_OF_LIFE,
         "Welfare State, Inequality and Quality of Life"),
        (OTHER, "Other (Please specify in comments)"),
    )

    DEFAULT_CHOICE = OTHER
