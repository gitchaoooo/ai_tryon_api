from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import os

app = FastAPI(
    title="AI 虚拟试衣系统 API",
    description="这是一个基于 FastAPI 的 AI 试衣后台接口，支持上传模特图和衣服图，返回合成试穿图。",
    version="1.0.0"
)

@app.post("/tryon", summary="虚拟试衣接口", description="上传模特图片和衣服图片，返回合成的试穿效果图")
async def virtual_tryon(
    model_img: UploadFile = File(..., description="模特图片文件"),
    cloth_img: UploadFile = File(..., description="衣服图片文件")
):
    os.makedirs("temp", exist_ok=True)
    model_path = "temp/model.png"
    cloth_path = "temp/cloth.png"
    result_path = "temp/tryon_result.png"

    with open(model_path, "wb") as f:
        f.write(await model_img.read())
    with open(cloth_path, "wb") as f:
        f.write(await cloth_img.read())

    model = Image.open(model_path).convert("RGBA")
    cloth = Image.open(cloth_path).convert("RGBA")
    cloth = cloth.resize(model.size)

    result = Image.alpha_composite(model, cloth)
    result.save(result_path)
    return FileResponse(result_path, media_type="image/png")
