from streamlit.delta_generator import DeltaGenerator
from models import Company
from scrapperapi import getCompanys


def companyList(dg: DeltaGenerator):
    companies = [Company(**c) for c in getCompanys()]
    options = list(map(lambda c: c.Name, companies))
    selected = dg.selectbox("Select Company", options=options)
    selected = next(filter(lambda c: c.Name == selected, companies))
    return selected
