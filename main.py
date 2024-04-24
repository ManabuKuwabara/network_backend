from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# CORSを設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.jsの開発サーバーのURL
        "https://tech0-gen-5-step4-studentwebapp-11.azurewebsites.net"  # 本番環境のフロントエンドURL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Connection(BaseModel):
    Source: str
    SourceDepartment: str
    Target: str
    TargetDepartment: str
    Weight: int

# 所属リストを読み込んで、名前から部署へのマッピングを作成する関数
def create_name_to_department_map():
    affiliation_path = '所属リスト_v2.csv'
    affiliations = pd.read_csv(affiliation_path, encoding='shift_jis')
    return dict(zip(affiliations['名前'], affiliations['部署']))

# CSVファイルからデータを読み込む関数
def load_data(filepath: str, name_to_department):
    try:
        df = pd.read_csv(filepath)
        df['SourceDepartment'] = df['Source'].map(name_to_department)
        df['TargetDepartment'] = df['Target'].map(name_to_department)
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# グローバル変数として名前から部署へのマップを作成
name_to_department = create_name_to_department_map()

# APIエンドポイントの設定
@app.get("/connections/", response_model=list[Connection])
async def get_connections():
    data = load_data("dummy_connections_v5.csv", name_to_department)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
