from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from ner import ner
from sentiment import sentiment
from tag_prediction import get_tag
from summarization import summarize

app = FastAPI()

class InputText(BaseModel):
    text: str

class NLPResult(BaseModel):
    tag: str
    summarization: str
    sentiment_result: str
    person: list
    location: list
    organization: list


@app.post("/analyze/", response_model=NLPResult)
async def analyze_text(input_text: InputText):
    text = input_text.text
    tag = get_tag(text)
    summarization = summarize(text, n_words=10)  
    sentiment_result = sentiment(text)
    ner_results = ner(text)
    
    PER = set([res.title() for res in ner_results['PER']])
    LOC = set([res.title() for res in ner_results['LOC']])
    ORG = set([res.upper() for res in ner_results['ORG']])

    return {'tag': tag,
            'summarization': summarization,
            'sentiment_result': sentiment_result,
            'person': PER,
            'location': LOC,
            'organization': ORG}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/docs/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation", oauth2_redirect_url="/docs")


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    return app.openapi()
