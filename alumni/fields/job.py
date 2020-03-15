from __future__ import annotations

from .custom import CustomIntegerChoiceField

__all__ = ['JobField']


class JobField(CustomIntegerChoiceField):
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

    CHOICES = (
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

    DEFAULT_CHOICE = OTHER
