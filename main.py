from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "欢迎使用 AI 虚拟试衣系统"}

@app.post("/tryon/")
async def virtual_tryon(model_img: UploadFile = File(...), cloth_img: UploadFile = File(...)):
    try:
        # 读取上传的模特图片
        model_bytes = await model_img.read()
        model = Image.open(io.BytesIO(model_bytes)).convert("RGBA")

        # 读取上传的服装图片
        cloth_bytes = await cloth_img.read()
        cloth = Image.open(io.BytesIO(cloth_bytes)).convert("RGBA")

        # 这里是简单示范，直接将服装叠加到模特图片中心（请替换为你的AI试衣逻辑）
        model.paste(cloth, (int((model.width - cloth.width)/2), int((model.height - cloth.height)/2)), cloth)

        # 保存结果到内存
        buf = io.BytesIO()
        model.save(buf, format="PNG")
        buf.seek(0)

        # 返回图片二进制（base64编码或者直接返回文件流根据需要调整）
        return JSONResponse(content={"result": "试穿图片生成成功，示例不返回图片，请用实际接口返回图片二进制或URL"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
