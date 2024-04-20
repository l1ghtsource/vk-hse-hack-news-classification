from fastapi import FastAPI
from pydantic import BaseModel
from ner import ner
from sentiment import sentiment
from tag_prediction import get_tag

app = FastAPI()

class InputText(BaseModel):
    text: str

class NLPResult(BaseModel):
    tag: str
    keywords: str
    sentiment_result: str
    person: list
    location: list
    organization: list

@app.post("/analyze/", response_model=NLPResult)
async def analyze_text(input_text: InputText):
    text = input_text.text
    tag = get_tag(text)
    keywords = 'слова, слова, слова'
    sentiment_result = sentiment(text)
    ner_results = ner(text)
    
    PER = ner_results['PER']
    LOC = ner_results['LOC']
    ORG = ner_results['ORG']

    return {'tag': tag,
            'keywords': keywords,
            'sentiment_result': sentiment_result,
            'person': PER,
            'location': LOC,
            'organization': ORG}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation", oauth2_redirect_url="/docs")

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    return app.openapi()
