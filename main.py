
import torch
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from torchvision import transforms
import base64
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression


# インスタンス化
app = FastAPI()

# モデルを読み込む
path = 'best.pt' # best.ptのパスを指定
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = attempt_load(path, device=device)  # CUDAを使用する場合

# 入力するデータの型の定義
class TagImage(BaseModel):
    file: str

# トップページ
@app.get('/')
def index():
    return {'tag': 'tag_prediction'}

@app.post('/predict')
async def make_prediction(image: TagImage):
    try:
        # 画像をテンソルに変換する処理
        transform = transforms.Compose([
            transforms.Resize((640, 640)),  # YOLOv5の入力サイズに合わせてリサイズ
            transforms.ToTensor(),  # テンソルに変換
        ])

        # 画像データの読み込み
        file_data = base64.b64decode(image.file)
        image = Image.open(io.BytesIO(file_data))
        image = transform(image).unsqueeze(0)
        
        # 推論
        result = model(image)
        result = non_max_suppression(result)

        # クラスラベルのみを取得
        class_labels = [int(det[5]) for det in result[0] if det[4] >= 0.5]
        return {'prediction': class_labels}
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)


    