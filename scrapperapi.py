import requests as rq
import json, os

BASE = os.getenv("BASE", "http://34.16.163.203:8000/api")


def get(path, params={}):
    res = rq.get(BASE + path, params=params)
    if res.status_code == 200:
        try:
            body = json.loads(res.text)
        except Exception as e:
            body = res.text
        return body
    return ""


def getCompanys():
    return get("/companys")


def getCompanyPosts(companyId):
    return get("/companys/" + (companyId if companyId else ""))


def getInsights(companyId, limit=10, offset=0, newPrompt=None):
    return get(f"/companys/{companyId}/insights", {"limit": limit, "offset": offset})


def getPrompt(id=1):
    return get(f"/prompts/{id}")
