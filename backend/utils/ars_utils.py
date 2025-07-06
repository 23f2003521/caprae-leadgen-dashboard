def calculate_ars(row, weights):
    import pandas as pd
    try:
        company_age = min(2025 - int(row['Year Founded']), 20) / 20 if row['Year Founded'] else 0
    except:
        company_age = 0

    website_score = 1 if pd.notna(row['Website']) and row['Website'] else 0
    linkedin_score = 1 if pd.notna(row['Company LinkedIn']) and row['Company LinkedIn'] else 0
    owner_contact_info = 0  # Placeholder for future implementation
    address_completeness = 1 if pd.notna(row['City']) and pd.notna(row['State']) else 0
    bbb_rating_map = {'A+': 1.0, 'A': 0.9, 'B': 0.6}
    bbb_score = bbb_rating_map.get(row['BBB Rating'], 0.5)

    attractive_industries = ['SaaS', 'FinTech', 'B2B']
    industry_score = 1.0 if any(ind in str(row['Industry']) for ind in attractive_industries) else 0.6

    try:
        emp = int(row['Employees Count'])
        revenue_employees_score = 1 if emp > 50 else 0.7 if emp > 10 else 0.5
    except:
        revenue_employees_score = 0.5

    ars = (
        company_age * weights["age"] +
        website_score * weights["website"] +
        linkedin_score * weights["linkedin"] +
        owner_contact_info * weights["owner"] +
        address_completeness * weights["address"] +
        bbb_score * weights["bbb"] +
        industry_score * weights["industry"] +
        revenue_employees_score * weights["team"]
    ) * 100

    return round(ars, 2)


def color_score(score):
    if score >= 60:
        return '🟢 High'
    elif score >= 30:
        return '🟡 Medium'
    else:
        return '🔴 Low'

