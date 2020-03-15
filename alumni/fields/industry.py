from __future__ import annotations

from .custom import CustomIntegerChoiceField

__all__ = ['IndustryField']


class IndustryField(CustomIntegerChoiceField):
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

    CHOICES = (
        (ACCOUNTING, "Accounting"),
        (AIRLINESAVIATION, "Airlines/Aviation"),
        (ALTERNATIVE_DISPUTE_RESOLUTION, "Alternative Dispute Resolution"),
        (ALTERNATIVE_MEDICINE, "Alternative Medicine"),
        (ANIMATION, "Animation"),
        (APPAREL_FASHION, "Apparel & Fashion"),
        (ARCHITECTURE_PLANNING, "Architecture & Planning"),
        (ARTS_AND_CRAFTS, "Arts and Crafts"),
        (AUTOMOTIVE, "Automotive"),
        (AVIATION_AEROSPACE, "Aviation & Aerospace"),
        (BANKING, "Banking"),
        (BIOTECHNOLOGY, "Biotechnology"),
        (BROADCAST_MEDIA, "Broadcast Media"),
        (BUILDING_MATERIALS, "Building Materials"),
        (BUSINESS_SUPPLIES_AND_EQUIPMENT, "Business Supplies and Equipment"),
        (CAPITAL_MARKETS, "Capital Markets"),
        (CHEMICALS, "Chemicals"),
        (CIVIC_SOCIAL_ORGANIZATION, "Civic & Social Organization"),
        (CIVIL_ENGINEERING, "Civil Engineering"),
        (COMMERCIAL_REAL_ESTATE, "Commercial Real Estate"),
        (COMPUTER_GAMES, "Computer Games"),
        (COMPUTER_HARDWARE, "Computer Hardware"),
        (COMPUTER_NETWORK_SECURITY, "Computer & Network Security"),
        (COMPUTER_NETWORKING, "Computer Networking"),
        (COMPUTER_SOFTWARE, "Computer Software"),
        (CONSTRUCTION, "Construction"),
        (CONSUMER_ELECTRONICS, "Consumer Electronics"),
        (CONSUMER_GOODS, "Consumer Goods"),
        (CONSUMER_SERVICES, "Consumer Services"),
        (COSMETICS, "Cosmetics"),
        (DAIRY, "Dairy"),
        (DEFENSE_SPACE, "Defense & Space"),
        (DESIGN, "Design"),
        (E_LEARNING, "E-Learning"),
        (EDUCATION_MANAGEMENT, "Education Management"),
        (ELECTRICALELECTRONIC_MANUFACTURING,
         "Electrical/Electronic Manufacturing"),
        (ENTERTAINMENT, "Entertainment"),
        (ENVIRONMENTAL_SERVICES, "Environmental Services"),
        (EVENTS_SERVICES, "Events Services"),
        (EXECUTIVE_OFFICE, "Executive Office"),
        (FACILITIES_SERVICES, "Facilities Services"),
        (FARMING, "Farming"),
        (FINANCIAL_SERVICES, "Financial Services"),
        (FINE_ART, "Fine Art"),
        (FISHERY, "Fishery"),
        (FOOD_BEVERAGES, "Food & Beverages"),
        (FOOD_PRODUCTION, "Food Production"),
        (FUND_RAISING, "Fund-Raising"),
        (FURNITURE, "Furniture"),
        (GAMBLING_CASINOS, "Gambling & Casinos"),
        (GLASS_CERAMICS_CONCRETE, "Glass, Ceramics & Concrete"),
        (GOVERNMENT_ADMINISTRATION, "Government Administration"),
        (GOVERNMENT_RELATIONS, "Government Relations"),
        (GRAPHIC_DESIGN, "Graphic Design"),
        (HEALTH_WELLNESS_AND_FITNESS, "Health, Wellness and Fitness"),
        (HIGHER_EDUCATION, "Higher Education"),
        (HOSPITAL_HEALTH_CARE, "Hospital & Health Care"),
        (HOSPITALITY, "Hospitality"),
        (HUMAN_RESOURCES, "Human Resources"),
        (IMPORT_AND_EXPORT, "Import and Export"),
        (INDIVIDUAL_FAMILY_SERVICES, "Individual & Family Services"),
        (INDUSTRIAL_AUTOMATION, "Industrial Automation"),
        (INFORMATION_SERVICES, "Information Services"),
        (INFORMATION_TECHNOLOGY_AND_SERVICES,
         "Information Technology and Services"),
        (INSURANCE, "Insurance"),
        (INTERNATIONAL_AFFAIRS, "International Affairs"),
        (INTERNATIONAL_TRADE_AND_DEVELOPMENT,
         "International Trade and Development"),
        (INTERNET, "Internet"),
        (INVESTMENT_BANKING, "Investment Banking"),
        (INVESTMENT_MANAGEMENT, "Investment Management"),
        (JUDICIARY, "Judiciary"),
        (LAW_ENFORCEMENT, "Law Enforcement"),
        (LAW_PRACTICE, "Law Practice"),
        (LEGAL_SERVICES, "Legal Services"),
        (LEGISLATIVE_OFFICE, "Legislative Office"),
        (LEISURE_TRAVEL_TOURISM, "Leisure, Travel & Tourism"),
        (LIBRARIES, "Libraries"),
        (LOGISTICS_AND_SUPPLY_CHAIN, "Logistics and Supply Chain"),
        (LUXURY_GOODS_JEWELRY, "Luxury Goods & Jewelry"),
        (MACHINERY, "Machinery"),
        (MANAGEMENT_CONSULTING, "Management Consulting"),
        (MARITIME, "Maritime"),
        (MARKET_RESEARCH, "Market Research"),
        (MARKETING_AND_ADVERTISING, "Marketing and Advertising"),
        (MECHANICAL_OR_INDUSTRIAL_ENGINEERING,
         "Mechanical or Industrial Engineering"),
        (MEDIA_PRODUCTION, "Media Production"),
        (MEDICAL_DEVICES, "Medical Devices"),
        (MEDICAL_PRACTICE, "Medical Practice"),
        (MENTAL_HEALTH_CARE, "Mental Health Care"),
        (MILITARY, "Military"),
        (MINING_METALS, "Mining & Metals"),
        (MOTION_PICTURES_AND_FILM, "Motion Pictures and Film"),
        (MUSEUMS_AND_INSTITUTIONS, "Museums and Institutions"),
        (MUSIC, "Music"),
        (NANOTECHNOLOGY, "Nanotechnology"),
        (NEWSPAPERS, "Newspapers"),
        (
            NONPROFIT_ORGANIZATION_MANAGEMENT,
            "Nonprofit Organization Management"),
        (OIL_ENERGY, "Oil & Energy"),
        (ONLINE_MEDIA, "Online Media"),
        (OTHER, "Other"),
        (OUTSOURCINGOFFSHORING, "Outsourcing/Offshoring"),
        (PACKAGEFREIGHT_DELIVERY, "Package/Freight Delivery"),
        (PACKAGING_AND_CONTAINERS, "Packaging and Containers"),
        (PAPER_FOREST_PRODUCTS, "Paper & Forest Products"),
        (PERFORMING_ARTS, "Performing Arts"),
        (PHARMACEUTICALS, "Pharmaceuticals"),
        (PHILANTHROPY, "Philanthropy"),
        (PHOTOGRAPHY, "Photography"),
        (PLASTICS, "Plastics"),
        (POLITICAL_ORGANIZATION, "Political Organization"),
        (PRIMARYSECONDARY_EDUCATION, "Primary/Secondary Education"),
        (PRINTING, "Printing"),
        (PROFESSIONAL_TRAINING_COACHING, "Professional Training & Coaching"),
        (PROGRAM_DEVELOPMENT, "Program Development"),
        (PUBLIC_POLICY, "Public Policy"),
        (PUBLIC_RELATIONS_AND_COMMUNICATIONS,
         "Public Relations and Communications"),
        (PUBLIC_SAFETY, "Public Safety"),
        (PUBLISHING, "Publishing"),
        (RAILROAD_MANUFACTURE, "Railroad Manufacture"),
        (RANCHING, "Ranching"),
        (REAL_ESTATE, "Real Estate"),
        (RECREATIONAL_FACILITIES_AND_SERVICES,
         "Recreational Facilities and Services"),
        (RELIGIOUS_INSTITUTIONS, "Religious Institutions"),
        (RENEWABLES_ENVIRONMENT, "Renewables & Environment"),
        (RESEARCH, "Research"),
        (RESTAURANTS, "Restaurants"),
        (RETAIL, "Retail"),
        (SECURITY_AND_INVESTIGATIONS, "Security and Investigations"),
        (SEMICONDUCTORS, "Semiconductors"),
        (SHIPBUILDING, "Shipbuilding"),
        (SPORTING_GOODS, "Sporting Goods"),
        (SPORTS, "Sports"),
        (STAFFING_AND_RECRUITING, "Staffing and Recruiting"),
        (SUPERMARKETS, "Supermarkets"),
        (TELECOMMUNICATIONS, "Telecommunications"),
        (TEXTILES, "Textiles"),
        (THINK_TANKS, "Think Tanks"),
        (TOBACCO, "Tobacco"),
        (TRANSLATION_AND_LOCALIZATION, "Translation and Localization"),
        (TRANSPORTATIONTRUCKINGRAILROAD, "Transportation/Trucking/Railroad"),
        (UNEMPLOYED, "Unemployed"),
        (UTILITIES, "Utilities"),
        (VENTURE_CAPITAL_PRIVATE_EQUITY, "Venture Capital & Private Equity"),
        (VETERINARY, "Veterinary"),
        (WAREHOUSING, "Warehousing"),
        (WHOLESALE, "Wholesale"),
        (WINE_AND_SPIRITS, "Wine and Spirits"),
        (WIRELESS, "Wireless"),
        (WRITING_AND_EDITING, "Writing and Editing"),
    )

    DEFAULT_CHOICE = OTHER
