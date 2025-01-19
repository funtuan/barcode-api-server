from flask import Flask, request, jsonify
import cv2
import json
import requests
import numpy as np
import re
import logging
from daisykit import BarcodeScannerFlow

# 初始化 Flask 应用
app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置 DaisyKit BarcodeScannerFlow
config = {
    "try_harder": True,
    "try_rotate": True
}
barcode_scanner_flow = BarcodeScannerFlow(json.dumps(config))

# 条码解析的正则表达式
barcode_pattern = r'([\w-]+)\s"(\d+)"'

@app.route('/scan-barcode', methods=['POST'])
def scan_barcode():
    try:
        logger.info("Received request to /scan-barcode")
        
        # 获取 JSON 请求中的 imageUrl
        data = request.json
        image_url = data.get('imageUrl')
        if not image_url:
            logger.error("Missing imageUrl in request")
            return jsonify({"error": "Missing imageUrl"}), 400

        logger.info(f"Fetching image from URL: {image_url}")
        
        # 下载图像
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            logger.error(f"Failed to fetch image, status code: {response.status_code}")
            return jsonify({"error": "Failed to fetch image"}), 400

        # 将图像数据转换为 NumPy 数组
        image_data = np.frombuffer(response.content, np.uint8)
        frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        # 转换颜色以适配 DaisyKit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        logger.info("Processing image with DaisyKit BarcodeScannerFlow")
        
        # 使用 DaisyKit 扫描条码
        result = barcode_scanner_flow.Process(frame_rgb, draw=False)

        logger.info(f"BarcodeScannerFlow result: {result}")

        data = re.findall(barcode_pattern, result)


        barcodes = []
        # 顯示結果
        print("解析出的條碼:")
        for barcode_type, barcode_value in data:
            print(f"類型: {barcode_type}, 條碼: {barcode_value}")
            barcodes.append({"type": barcode_type, "value": barcode_value})

        logger.info(f"Barcodes found: {barcodes}")
        
        # 返回结果
        return jsonify({"barcodes": barcodes})
    except Exception as e:
        logger.exception("An error occurred while processing the request", exc_info=e)
        return jsonify({"error": str(e)}), 500

# 启动服务器
if __name__ == '__main__':
    logger.info("Starting server")
    app.run(host='0.0.0.0', port=5005)
