from django.db import models


class GenderField(models.CharField):
    FEMALE = 'fe'
    MALE = 'ma'
    OTHER = 'ot'
    UNSPECIFIED = 'un'
    SEX_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (OTHER, 'Non-binary'),
        (UNSPECIFIED, 'Prefer not to say'),
    )

    def __init__(self, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = GenderField.SEX_CHOICES
        kwargs['default'] = GenderField.UNSPECIFIED
        super(GenderField, self).__init__(**kwargs)


class AlumniCategoryField(models.CharField):
    REGULAR = 're'
    FACULTY = 'fa'
    FRIEND = 'fr'
    CATEGORY_CHOICES = (
        (REGULAR, 'Alumni (Former Student)'),
        (FACULTY, 'Faculty or Staff'),
        (FRIEND, 'Friend Of The Association')
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = AlumniCategoryField.CATEGORY_CHOICES
        kwargs['default'] = AlumniCategoryField.REGULAR
        super(AlumniCategoryField, self).__init__(*args, **kwargs)


class CollegeField(models.IntegerField):
    KRUPP = 1
    MERCATOR = 2
    CIII = 3
    NORDMETALL = 4
    CV = 5
    COLLEGE_CHOICES = (
        (KRUPP, 'Krupp'),
        (MERCATOR, 'Mercator'),
        (CIII, 'College III'),
        (NORDMETALL, 'Nordmetall'),
        (CV, 'College V')
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = CollegeField.COLLEGE_CHOICES
        super(CollegeField, self).__init__(*args, **kwargs)


class ClassField(models.IntegerField):
    C_2004 = 2004
    C_2005 = 2005
    C_2006 = 2006
    C_2007 = 2007
    C_2008 = 2008
    C_2009 = 2009
    C_2010 = 2010
    C_2011 = 2011
    C_2012 = 2012
    C_2013 = 2013
    C_2014 = 2014
    C_2015 = 2015
    C_2016 = 2016
    C_2017 = 2017
    CLASS_CHOICES = (
        (C_2004, 'Class of 2004'),
        (C_2005, 'Class of 2005'),
        (C_2006, 'Class of 2006'),
        (C_2007, 'Class of 2007'),
        (C_2008, 'Class of 2008'),
        (C_2009, 'Class of 2009'),
        (C_2010, 'Class of 2010'),
        (C_2011, 'Class of 2011'),
        (C_2012, 'Class of 2012'),
        (C_2013, 'Class of 2013'),
        (C_2014, 'Class of 2014'),
        (C_2015, 'Class of 2015'),
        (C_2016, 'Class of 2016'),
        (C_2017, 'Class of 2017'),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ClassField.CLASS_CHOICES
        super(ClassField, self).__init__(*args, **kwargs)


class DegreeField(models.CharField):
    BACHELOR_ARTS = 'ba'
    BACHELOR_SCIENCE = 'bsc'
    MASTER_ARTS = 'ma'
    MASTER_SCIENCE = 'msc'
    PHD = 'phd'
    MBA = 'mba'

    DEGREE_CHOICES = (
        (BACHELOR_ARTS, 'Bachelor of Arts'),
        (BACHELOR_SCIENCE, 'Bachelor of Science'),
        (MASTER_ARTS, 'Master of Arts'),
        (MASTER_SCIENCE, 'Master of Science'),
        (PHD, 'PhD'),
        (MBA, 'MBA'),
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 3
        kwargs['choices'] = DegreeField.DEGREE_CHOICES
        super(DegreeField, self).__init__(*args, **kwargs)


class MajorField(models.CharField):
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
    CHEMISTRY = "C"
    COMMUNICATIONS = "COM"
    COMPARATIVE_POLITICS_AND_SOCIOLOGY = "CPAS"
    COMPUTER_SCIENCE = "CS"
    EARTH_AND_SPACE_SCIENCES = "EASS"
    ELECTRICAL_ENGINEERING_AND_COMPUTER_SCIENCE = "EECS"
    EUROPEAN_UTILITY_MANAGEMENT = "EUM"
    GEO_OCEAN_DYNAMICS = "GOD"
    GEOSCIENCES_AND_ASTROPHYSICS = "GAA"
    GLOBAL_ECONOMICS_AND_MANAGEMENT = "GEAM"
    GLOBAL_VISUAL_COMMUNICATION = "GVC"
    HISTORY = "H"
    HISTORY_AND_THEORY_OF_ART_AND_LITERATURE = "HATOAAL"
    HUMANITIES = "HM"
    INFORMATION_MANAGEMENT_AND_SYSTEMS = "IMAS"
    INTEGRATED_CULTURAL_STUDIES = "ICS"
    INTEGRATED_ENVIRONMENTAL_STUDIES = "IES"
    INTEGRATED_SOCIAL_AND_COGNITIVE_PSYCHOLOGY = "ISACP"
    INTEGRATED_SOCIAL_SCIENCES = "ISS"
    INTERCULTURAL_HUMANITIES = "IH"
    INTERCULTURAL_RELATIONS_AND_BEHAVIOUR = "IRAB"
    INTERNATIONAL_COMMUNICATION = "IC"
    INTERNATIONAL_HISTORY_AND_POLITICS = "IHAP"
    INTERNATIONAL_LOGISTICS_ENGINEERING_AND_MANAGEMENT = "ILEAM"
    INTERNATIONAL_POLITICS_AND_HISTORY = "IPAH"
    INTERNATIONAL_RELATIONS = "IR"
    LIFE_COURSE_AND_LIFESPAN_DYNAMICS = "LCALD"
    LIFELONG_LEARNING = "LL"
    MARINE_MICROBIOLOGY = "MM"
    MATHEMATICS = "M"
    MODERN_GLOBAL_HISTORY = "MGH"
    MOLECULAR_LIFE_SCIENCE = "MLS"
    NANOMOLECULAR_SCIENCES = "NS"
    NEUROSCIENCE = "N"
    PHYSICS = "P"
    POLITICAL_ECONOMY_PUBLIC_POLICY = "PEPP"
    PRODUCTIVE_ADULT_DEVELOPMENT = "PAD"
    PSYCHOLOGY = "PSY"
    SMART_SYSTEMS = "SS"
    VISUAL_COMMUNICATION_AND_EXPERTISE = "VCAE"

    MAJOR_CHOICES = (
        (APPLIED_COMPUTATIONAL_MATHEMATICS,
         "Applied Computational Mathematics (ACM)"),
        (APPLIED_PHYSICS_AND_MATHEMATICS, "Applied Physics and Mathematics"),
        (ASTROPARTICLE_PHYSICS, "Astroparticle Physics"),
        (ATTITUDE_FORMATION, "Attitude Formation"),
        (BIOCHEMICAL_ENGINEERING, "Biochemical Engineering"),
        (BIOCHEMISTRY, "Biochemistry"),
        (BIOCHEMISTRY_AND_CELL_BIOLOGY, "Biochemistry and Cell Biology (BCCB)"),
        (BIOINFORMATICS_AND_COMPUTATIONAL_BIOLOGY,
         "Bioinformatics and Computational Biology"),
        (BIOLOGICAL_RECOGNITION, "Biological Recognition"),
        (BIOLOGY, "Biology"),
        (BIOLOGY_NEUROSCIENCE, "Biology/Neuroscience"),
        (BIOTECHNOLOGY, "Biotechnology"),
        (BUISNESS_ADMINISTRATION, "Buisness Administration"),
        (CHEMISTRY, "Chemistry"),
        (COMMUNICATIONS, "Communications"),
        (COMPARATIVE_POLITICS_AND_SOCIOLOGY,
         "Comparative PolitIcs and Sociology"),
        (COMPUTER_SCIENCE, "Computer Science"),
        (EARTH_AND_SPACE_SCIENCES, "Earth and Space Sciences"),
        (ELECTRICAL_ENGINEERING_AND_COMPUTER_SCIENCE,
         "Electrical Engineering and Computer Science"),
        (EUROPEAN_UTILITY_MANAGEMENT, "European Utility Management"),
        (GEO_OCEAN_DYNAMICS, "Geo-Ocean Dynamics"),
        (GEOSCIENCES_AND_ASTROPHYSICS, "Geosciences and Astrophysics"),
        (GLOBAL_ECONOMICS_AND_MANAGEMENT,
         "Global Economics and Management (GEM)"),
        (GLOBAL_VISUAL_COMMUNICATION, "Global Visual Communication"),
        (HISTORY, "History"),
        (HISTORY_AND_THEORY_OF_ART_AND_LITERATURE,
         "History and Theory of Art and Literature"),
        (HUMANITIES, "Humanities"),
        (INFORMATION_MANAGEMENT_AND_SYSTEMS,
         "Information Management and Systems (IMS)"),
        (INTEGRATED_CULTURAL_STUDIES, "Integrated Cultural Studies"),
        (INTEGRATED_ENVIRONMENTAL_STUDIES, "Integrated Environmental Studies"),
        (INTEGRATED_SOCIAL_AND_COGNITIVE_PSYCHOLOGY,
         "Integrated Social and Cognitive Psychology (ISCP)"),
        (INTEGRATED_SOCIAL_SCIENCES, "Integrated Social Sciences"),
        (INTERCULTURAL_HUMANITIES, "Intercultural Humanities"),
        (INTERCULTURAL_RELATIONS_AND_BEHAVIOUR,
         "Intercultural Relations and Behaviour (IRB)"),
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
        (MODERN_GLOBAL_HISTORY, "Modern Global History"),
        (MOLECULAR_LIFE_SCIENCE, "Molecular Life Science"),
        (NANOMOLECULAR_SCIENCES, "Nanomolecular Sciences"),
        (NEUROSCIENCE, "Neuroscience"),
        (PHYSICS, "Physics"),
        (POLITICAL_ECONOMY_PUBLIC_POLICY, "Political Economy & Public Policy"),
        (PRODUCTIVE_ADULT_DEVELOPMENT, "Productive Adult Development"),
        (PSYCHOLOGY, "Psychology"),
        (SMART_SYSTEMS, "Smart Systems"),
        (VISUAL_COMMUNICATION_AND_EXPERTISE,
         "Visual Communication and Expertise"),
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        kwargs['choices'] = MajorField.MAJOR_CHOICES
        super(MajorField, self).__init__(*args, **kwargs)


class IndustryField(models.IntegerField):
    OTHER = 0
    DEFENSE_SPACE = 1
    COMPUTER_HARDWARE = 3
    COMPUTER_SOFTWARE = 4
    COMPUTER_NETWORKING = 5
    INTERNET = 6
    SEMICONDUCTORS = 7
    TELECOMMUNICATIONS = 8
    LAW_PRACTICE = 9
    LEGAL_SERVICES = 10
    MANAGEMENT_CONSULTING = 11
    BIOTECHNOLOGY = 12
    MEDICAL_PRACTICE = 13
    HOSPITAL_HEALTH_CARE = 14
    PHARMACEUTICALS = 15
    VETERINARY = 16
    MEDICAL_DEVICES = 17
    COSMETICS = 18
    APPAREL_FASHION = 19
    SPORTING_GOODS = 20
    TOBACCO = 21
    SUPERMARKETS = 22
    FOOD_PRODUCTION = 23
    CONSUMER_ELECTRONICS = 24
    CONSUMER_GOODS = 25
    FURNITURE = 26
    RETAIL = 27
    ENTERTAINMENT = 28
    GAMBLING_CASINOS = 29
    LEISURE_TRAVEL_TOURISM = 30
    HOSPITALITY = 31
    RESTAURANTS = 32
    SPORTS = 33
    FOOD_BEVERAGES = 34
    MOTION_PICTURES_AND_FILM = 35
    BROADCAST_MEDIA = 36
    MUSEUMS_AND_INSTITUTIONS = 37
    FINE_ART = 38
    PERFORMING_ARTS = 39
    RECREATIONAL_FACILITIES_AND_SERVICES = 40
    BANKING = 41
    INSURANCE = 42
    FINANCIAL_SERVICES = 43
    REAL_ESTATE = 44
    INVESTMENT_BANKING = 45
    INVESTMENT_MANAGEMENT = 46
    ACCOUNTING = 47
    CONSTRUCTION = 48
    BUILDING_MATERIALS = 49
    ARCHITECTURE_PLANNING = 50
    CIVIL_ENGINEERING = 51
    AVIATION_AEROSPACE = 52
    AUTOMOTIVE = 53
    CHEMICALS = 54
    MACHINERY = 55
    MINING_METALS = 56
    OIL_ENERGY = 57
    SHIPBUILDING = 58
    UTILITIES = 59
    TEXTILES = 60
    PAPER_FOREST_PRODUCTS = 61
    RAILROAD_MANUFACTURE = 62
    FARMING = 63
    RANCHING = 64
    DAIRY = 65
    FISHERY = 66
    PRIMARYSECONDARY_EDUCATION = 67
    HIGHER_EDUCATION = 68
    EDUCATION_MANAGEMENT = 69
    RESEARCH = 70
    MILITARY = 71
    LEGISLATIVE_OFFICE = 72
    JUDICIARY = 73
    INTERNATIONAL_AFFAIRS = 74
    GOVERNMENT_ADMINISTRATION = 75
    EXECUTIVE_OFFICE = 76
    LAW_ENFORCEMENT = 77
    PUBLIC_SAFETY = 78
    PUBLIC_POLICY = 79
    MARKETING_AND_ADVERTISING = 80
    NEWSPAPERS = 81
    PUBLISHING = 82
    PRINTING = 83
    INFORMATION_SERVICES = 84
    LIBRARIES = 85
    ENVIRONMENTAL_SERVICES = 86
    PACKAGEFREIGHT_DELIVERY = 87
    INDIVIDUAL_FAMILY_SERVICES = 88
    RELIGIOUS_INSTITUTIONS = 89
    CIVIC_SOCIAL_ORGANIZATION = 90
    CONSUMER_SERVICES = 91
    TRANSPORTATIONTRUCKINGRAILROAD = 92
    WAREHOUSING = 93
    AIRLINESAVIATION = 94
    MARITIME = 95
    INFORMATION_TECHNOLOGY_AND_SERVICES = 96
    MARKET_RESEARCH = 97
    PUBLIC_RELATIONS_AND_COMMUNICATIONS = 98
    DESIGN = 99
    NONPROFIT_ORGANIZATION_MANAGEMENT = 100
    FUND_RAISING = 101
    PROGRAM_DEVELOPMENT = 102
    WRITING_AND_EDITING = 103
    STAFFING_AND_RECRUITING = 104
    PROFESSIONAL_TRAINING_COACHING = 105
    VENTURE_CAPITAL_PRIVATE_EQUITY = 106
    POLITICAL_ORGANIZATION = 107
    TRANSLATION_AND_LOCALIZATION = 108
    COMPUTER_GAMES = 109
    EVENTS_SERVICES = 110
    ARTS_AND_CRAFTS = 111
    ELECTRICALELECTRONIC_MANUFACTURING = 112
    ONLINE_MEDIA = 113
    NANOTECHNOLOGY = 114
    MUSIC = 115
    LOGISTICS_AND_SUPPLY_CHAIN = 116
    PLASTICS = 117
    COMPUTER_NETWORK_SECURITY = 118
    WIRELESS = 119
    ALTERNATIVE_DISPUTE_RESOLUTION = 120
    SECURITY_AND_INVESTIGATIONS = 121
    FACILITIES_SERVICES = 122
    OUTSOURCINGOFFSHORING = 123
    HEALTH_WELLNESS_AND_FITNESS = 124
    ALTERNATIVE_MEDICINE = 125
    MEDIA_PRODUCTION = 126
    ANIMATION = 127
    COMMERCIAL_REAL_ESTATE = 128
    CAPITAL_MARKETS = 129
    THINK_TANKS = 130
    PHILANTHROPY = 131
    E_LEARNING = 132
    WHOLESALE = 133
    IMPORT_AND_EXPORT = 134
    MECHANICAL_OR_INDUSTRIAL_ENGINEERING = 135
    PHOTOGRAPHY = 136
    HUMAN_RESOURCES = 137
    BUSINESS_SUPPLIES_AND_EQUIPMENT = 138
    MENTAL_HEALTH_CARE = 139
    GRAPHIC_DESIGN = 140
    INTERNATIONAL_TRADE_AND_DEVELOPMENT = 141
    WINE_AND_SPIRITS = 142
    LUXURY_GOODS_JEWELRY = 143
    RENEWABLES_ENVIRONMENT = 144
    GLASS_CERAMICS_CONCRETE = 145
    PACKAGING_AND_CONTAINERS = 146
    INDUSTRIAL_AUTOMATION = 147
    GOVERNMENT_RELATIONS = 148
    UNEMPLOYED = 150

    INDUSTRY_CHOICES = (
        (OTHER, "Other"),
        (DEFENSE_SPACE, "Defense & Space"),
        (COMPUTER_HARDWARE, "Computer Hardware"),
        (COMPUTER_SOFTWARE, "Computer Software"),
        (COMPUTER_NETWORKING, "Computer Networking"),
        (INTERNET, "Internet"),
        (SEMICONDUCTORS, "Semiconductors"),
        (TELECOMMUNICATIONS, "Telecommunications"),
        (LAW_PRACTICE, "Law Practice"),
        (LEGAL_SERVICES, "Legal Services"),
        (MANAGEMENT_CONSULTING, "Management Consulting"),
        (BIOTECHNOLOGY, "Biotechnology"),
        (MEDICAL_PRACTICE, "Medical Practice"),
        (HOSPITAL_HEALTH_CARE, "Hospital & Health Care"),
        (PHARMACEUTICALS, "Pharmaceuticals"),
        (VETERINARY, "Veterinary"),
        (MEDICAL_DEVICES, "Medical Devices"),
        (COSMETICS, "Cosmetics"),
        (APPAREL_FASHION, "Apparel & Fashion"),
        (SPORTING_GOODS, "Sporting Goods"),
        (TOBACCO, "Tobacco"),
        (SUPERMARKETS, "Supermarkets"),
        (FOOD_PRODUCTION, "Food Production"),
        (CONSUMER_ELECTRONICS, "Consumer Electronics"),
        (CONSUMER_GOODS, "Consumer Goods"),
        (FURNITURE, "Furniture"),
        (RETAIL, "Retail"),
        (ENTERTAINMENT, "Entertainment"),
        (GAMBLING_CASINOS, "Gambling & Casinos"),
        (LEISURE_TRAVEL_TOURISM, "Leisure, Travel & Tourism"),
        (HOSPITALITY, "Hospitality"),
        (RESTAURANTS, "Restaurants"),
        (SPORTS, "Sports"),
        (FOOD_BEVERAGES, "Food & Beverages"),
        (MOTION_PICTURES_AND_FILM, "Motion Pictures and Film"),
        (BROADCAST_MEDIA, "Broadcast Media"),
        (MUSEUMS_AND_INSTITUTIONS, "Museums and Institutions"),
        (FINE_ART, "Fine Art"),
        (PERFORMING_ARTS, "Performing Arts"),
        (RECREATIONAL_FACILITIES_AND_SERVICES,
         "Recreational Facilities and Services"),
        (BANKING, "Banking"),
        (INSURANCE, "Insurance"),
        (FINANCIAL_SERVICES, "Financial Services"),
        (REAL_ESTATE, "Real Estate"),
        (INVESTMENT_BANKING, "Investment Banking"),
        (INVESTMENT_MANAGEMENT, "Investment Management"),
        (ACCOUNTING, "Accounting"),
        (CONSTRUCTION, "Construction"),
        (BUILDING_MATERIALS, "Building Materials"),
        (ARCHITECTURE_PLANNING, "Architecture & Planning"),
        (CIVIL_ENGINEERING, "Civil Engineering"),
        (AVIATION_AEROSPACE, "Aviation & Aerospace"),
        (AUTOMOTIVE, "Automotive"),
        (CHEMICALS, "Chemicals"),
        (MACHINERY, "Machinery"),
        (MINING_METALS, "Mining & Metals"),
        (OIL_ENERGY, "Oil & Energy"),
        (SHIPBUILDING, "Shipbuilding"),
        (UTILITIES, "Utilities"),
        (TEXTILES, "Textiles"),
        (PAPER_FOREST_PRODUCTS, "Paper & Forest Products"),
        (RAILROAD_MANUFACTURE, "Railroad Manufacture"),
        (FARMING, "Farming"),
        (RANCHING, "Ranching"),
        (DAIRY, "Dairy"),
        (FISHERY, "Fishery"),
        (PRIMARYSECONDARY_EDUCATION, "Primary/Secondary Education"),
        (HIGHER_EDUCATION, "Higher Education"),
        (EDUCATION_MANAGEMENT, "Education Management"),
        (RESEARCH, "Research"),
        (MILITARY, "Military"),
        (LEGISLATIVE_OFFICE, "Legislative Office"),
        (JUDICIARY, "Judiciary"),
        (INTERNATIONAL_AFFAIRS, "International Affairs"),
        (GOVERNMENT_ADMINISTRATION, "Government Administration"),
        (EXECUTIVE_OFFICE, "Executive Office"),
        (LAW_ENFORCEMENT, "Law Enforcement"),
        (PUBLIC_SAFETY, "Public Safety"),
        (PUBLIC_POLICY, "Public Policy"),
        (MARKETING_AND_ADVERTISING, "Marketing and Advertising"),
        (NEWSPAPERS, "Newspapers"),
        (PUBLISHING, "Publishing"),
        (PRINTING, "Printing"),
        (INFORMATION_SERVICES, "Information Services"),
        (LIBRARIES, "Libraries"),
        (ENVIRONMENTAL_SERVICES, "Environmental Services"),
        (PACKAGEFREIGHT_DELIVERY, "Package/Freight Delivery"),
        (INDIVIDUAL_FAMILY_SERVICES, "Individual & Family Services"),
        (RELIGIOUS_INSTITUTIONS, "Religious Institutions"),
        (CIVIC_SOCIAL_ORGANIZATION, "Civic & Social Organization"),
        (CONSUMER_SERVICES, "Consumer Services"),
        (TRANSPORTATIONTRUCKINGRAILROAD, "Transportation/Trucking/Railroad"),
        (WAREHOUSING, "Warehousing"),
        (AIRLINESAVIATION, "Airlines/Aviation"),
        (MARITIME, "Maritime"),
        (INFORMATION_TECHNOLOGY_AND_SERVICES,
         "Information Technology and Services"),
        (MARKET_RESEARCH, "Market Research"),
        (PUBLIC_RELATIONS_AND_COMMUNICATIONS,
         "Public Relations and Communications"),
        (DESIGN, "Design"),
        (
            NONPROFIT_ORGANIZATION_MANAGEMENT,
            "Nonprofit Organization Management"),
        (FUND_RAISING, "Fund-Raising"),
        (PROGRAM_DEVELOPMENT, "Program Development"),
        (WRITING_AND_EDITING, "Writing and Editing"),
        (STAFFING_AND_RECRUITING, "Staffing and Recruiting"),
        (PROFESSIONAL_TRAINING_COACHING, "Professional Training & Coaching"),
        (VENTURE_CAPITAL_PRIVATE_EQUITY, "Venture Capital & Private Equity"),
        (POLITICAL_ORGANIZATION, "Political Organization"),
        (TRANSLATION_AND_LOCALIZATION, "Translation and Localization"),
        (COMPUTER_GAMES, "Computer Games"),
        (EVENTS_SERVICES, "Events Services"),
        (ARTS_AND_CRAFTS, "Arts and Crafts"),
        (ELECTRICALELECTRONIC_MANUFACTURING,
         "Electrical/Electronic Manufacturing"),
        (ONLINE_MEDIA, "Online Media"),
        (NANOTECHNOLOGY, "Nanotechnology"),
        (MUSIC, "Music"),
        (LOGISTICS_AND_SUPPLY_CHAIN, "Logistics and Supply Chain"),
        (PLASTICS, "Plastics"),
        (COMPUTER_NETWORK_SECURITY, "Computer & Network Security"),
        (WIRELESS, "Wireless"),
        (ALTERNATIVE_DISPUTE_RESOLUTION, "Alternative Dispute Resolution"),
        (SECURITY_AND_INVESTIGATIONS, "Security and Investigations"),
        (FACILITIES_SERVICES, "Facilities Services"),
        (OUTSOURCINGOFFSHORING, "Outsourcing/Offshoring"),
        (HEALTH_WELLNESS_AND_FITNESS, "Health, Wellness and Fitness"),
        (ALTERNATIVE_MEDICINE, "Alternative Medicine"),
        (MEDIA_PRODUCTION, "Media Production"),
        (ANIMATION, "Animation"),
        (COMMERCIAL_REAL_ESTATE, "Commercial Real Estate"),
        (CAPITAL_MARKETS, "Capital Markets"),
        (THINK_TANKS, "Think Tanks"),
        (PHILANTHROPY, "Philanthropy"),
        (E_LEARNING, "E-Learning"),
        (WHOLESALE, "Wholesale"),
        (IMPORT_AND_EXPORT, "Import and Export"),
        (MECHANICAL_OR_INDUSTRIAL_ENGINEERING,
         "Mechanical or Industrial Engineering"),
        (PHOTOGRAPHY, "Photography"),
        (HUMAN_RESOURCES, "Human Resources"),
        (BUSINESS_SUPPLIES_AND_EQUIPMENT, "Business Supplies and Equipment"),
        (MENTAL_HEALTH_CARE, "Mental Health Care"),
        (GRAPHIC_DESIGN, "Graphic Design"),
        (INTERNATIONAL_TRADE_AND_DEVELOPMENT,
         "International Trade and Development"),
        (WINE_AND_SPIRITS, "Wine and Spirits"),
        (LUXURY_GOODS_JEWELRY, "Luxury Goods & Jewelry"),
        (RENEWABLES_ENVIRONMENT, "Renewables & Environment"),
        (GLASS_CERAMICS_CONCRETE, "Glass, Ceramics & Concrete"),
        (PACKAGING_AND_CONTAINERS, "Packaging and Containers"),
        (INDUSTRIAL_AUTOMATION, "Industrial Automation"),
        (GOVERNMENT_RELATIONS, "Government Relations"),
        (UNEMPLOYED, "Unemployed"),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = IndustryField.INDUSTRY_CHOICES
        kwargs['default'] = IndustryField.OTHER
        super(IndustryField, self).__init__(*args, **kwargs)


class JobField(models.IntegerField):
    ACCOUNTING_FINANCE = 1
    ADMINISTRATIVE = 2
    ANALYST = 3
    ARCHITECTURE_DRAFTING = 4
    ART_DESIGN__ENTERTAINMENT = 5
    BANKING_LOAN__INSURANCE = 6
    BEAUTY_WELLNESS = 7
    BUSINESS_DEVELOPMENT_CONSULTING = 8
    EDUCATION = 9
    ENGINEERING = 10
    FACILITIES_GENERAL_LABOR = 11
    HOSPITALITY = 12
    HUMAN_RESOURCES = 13
    INSTALLATION_MAINTENANCE__REPAIR = 14
    LEGAL = 15
    MANUFACTURING_PRODUCTION__CONSTRUCTION = 16
    MARKETING_ADVERTISING__PR = 17
    MEDICAL_HEALTHCARE = 18
    NON_PROFIT_VOLUNTEERING = 19
    PRODUCT_PROJECT_MANAGEMENT = 20
    REAL_ESTATE = 21
    RESTAURANT_FOOD_SERVICES = 22
    RETAIL = 23
    SALES_CUSTOMER_CARE = 24
    SCIENCE_RESEARCH = 25
    SECURITY_LAW_ENFORCEMENT = 26
    SENIOR_MANAGEMENT = 27
    SKILLED_TRADE = 28
    SOFTWARE_DEVELOPMENT_IT = 29
    SPORTS_FITNESS = 30
    TRAVEL_TRANSPORTATION = 31
    WRITING_EDITING__PUBLISHING = 32
    OTHER = 33
    UNEMPLOYED = 34

    JOB_CHOICES = (
        (ACCOUNTING_FINANCE, "Accounting / Finance"),
        (ADMINISTRATIVE, "Administrative"),
        (ANALYST, "Analyst"),
        (ARCHITECTURE_DRAFTING, "Architecture / Drafting"),
        (ART_DESIGN__ENTERTAINMENT, "Art / Design / Entertainment"),
        (BANKING_LOAN__INSURANCE, "Banking / Loan / Insurance"),
        (BEAUTY_WELLNESS, "Beauty / Wellness"),
        (BUSINESS_DEVELOPMENT_CONSULTING, "Business Development / Consulting"),
        (EDUCATION, "Education"),
        (ENGINEERING, "Engineering (Non-software)"),
        (FACILITIES_GENERAL_LABOR, "Facilities / General Labor"),
        (HOSPITALITY, "Hospitality"),
        (HUMAN_RESOURCES, "Human Resources"),
        (INSTALLATION_MAINTENANCE__REPAIR,
         "Installation / Maintenance / Repair"),
        (LEGAL, "Legal"),
        (MANUFACTURING_PRODUCTION__CONSTRUCTION,
         "Manufacturing / Production / Construction"),
        (MARKETING_ADVERTISING__PR, "Marketing / Advertising / PR"),
        (MEDICAL_HEALTHCARE, "Medical / Healthcare"),
        (NON_PROFIT_VOLUNTEERING, "Non-Profit / Volunteering"),
        (PRODUCT_PROJECT_MANAGEMENT, "Product / Project Management"),
        (REAL_ESTATE, "Real Estate"),
        (RESTAURANT_FOOD_SERVICES, "Restaurant / Food Services"),
        (RETAIL, "Retail"),
        (SALES_CUSTOMER_CARE, "Sales / Customer Care"),
        (SCIENCE_RESEARCH, "Science / Research"),
        (SECURITY_LAW_ENFORCEMENT, "Security / Law Enforcement"),
        (SENIOR_MANAGEMENT, "Senior Management"),
        (SKILLED_TRADE, "Skilled Trade"),
        (SOFTWARE_DEVELOPMENT_IT, "Software Development / IT"),
        (SPORTS_FITNESS, "Sports / Fitness"),
        (TRAVEL_TRANSPORTATION, "Travel / Transportation"),
        (WRITING_EDITING__PUBLISHING, "Writing / Editing / Publishing"),
        (OTHER, "Other"),
        (UNEMPLOYED, "Unemployed"),
    )

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = JobField.JOB_CHOICES
        kwargs['default'] = JobField.UNEMPLOYED
        super(JobField, self).__init__(*args, **kwargs)


class TierField(models.CharField):
    STARTER = 'st'
    CONTRIBUTOR = 'co'
    PATRON = 'pa'

    TIER_CHOICES = (
        (STARTER, "Starter (1€ per year)"),
        (CONTRIBUTOR, "Contributor (49€ per year)"),
        (PATRON, 'Patron (249€ per year)'),
    )

    def __init__(self, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = TierField.TIER_CHOICES
        kwargs['default'] = TierField.CONTRIBUTOR
        super(TierField, self).__init__(**kwargs)
