import io
import time
from pathlib import Path

import fitz
import streamlit as st
from PIL import Image

from converter import Transform
from evaluator import Validate
from metrics import SimilarityMetrics
from preprocessor import XMLPreProcessor
from readers import PDFParser

st.set_page_config(page_title="RAG SDK Viewer", layout="wide")
st.title("📘 Project AIXtract Demo ")

# 初始化 session state
if "reader_data" not in st.session_state:
    st.session_state.reader_data = {}
    st.session_state.preprocessor_data = {}
    st.session_state.converter_data = {}
    st.session_state.evaluator_data = {}

if "pdf_path" not in st.session_state:
    st.session_state["pdf_path"] = "./data/EMPU_3401_Datasheet.pdf"

if st.button("📂 顯示當前資料夾所有 PDF 檔案"):
    current_dir = Path("./data")
    pdf_files = list(current_dir.glob("*.pdf"))
    if pdf_files:
        st.write("找到以下 PDF 檔案：")
        for f in pdf_files:
            st.write(f.name)
    else:
        st.info("目前資料夾中沒有 PDF 檔案。")
# 輸入參數
with st.form(key="pdf_form"):
    path = st.text_input("請輸入 PDF 路徑：", st.session_state["pdf_path"])
    submitted = st.form_submit_button("📂 重新載入 PDF")
    if submitted:
        st.session_state["pdf_path"] = path

model_name = st.text_input("請輸入 model name：", "llama3.2:1b")
model_url = st.text_input("請輸入 model url：", "http://127.0.0.1:6589/model_server/")
prompt = st.text_area(
    "請輸入 prompt：",
    """The following XML content was converted from a PDF using `pdf2xml`. Your task is to extract structured information from this XML based on the `<text>` tags, focusing on the actual text content and its positions (`top`, `left`).

```xml
{{xml_content}}
```

Please convert the extracted information into a well-structured JSON format, organized by section headers and their corresponding key-value pairs. Do not include any attribute metadata in the JSON. Ensure that the JSON syntax is valid, with proper indentation, brackets, and quotation marks.
Output only the JSON.""",
    height=200,
)

if st.button("🚀 開始處理"):
    with st.spinner("🔄 AIXtract 正在進行轉換中，請稍候..."):
        start_t = time.time()

        parser = PDFParser()
        xml_data = parser.process(path)
        st.session_state.reader_data = xml_data

        start_p = time.time()
        preprocessor = XMLPreProcessor()
        st.session_state.preprocessor_data = preprocessor.process(xml_data)

        start_c = time.time()
        transformer = Transform(model_name=model_name, model_url=model_url)
        st.session_state.converter_data = transformer.process(
            st.session_state.preprocessor_data, format="dict", prompt=prompt
        )
        start_e = time.time()
        metric, _ = SimilarityMetrics.get("str_similarity")
        validator = Validate(metrics=metric)
        st.session_state.evaluator_data = validator.process(
            gt_data=xml_data, data=st.session_state.converter_data
        )

    st.subheader("⏱️ 執行時間統計")
    st.text(f"總時間: {time.time() - start_t:.2f} 秒")
    st.text(f"前處理: {start_c - start_p:.2f} 秒")
    st.text(f"轉換: {start_e - start_c:.2f} 秒")
    st.text(f"評估: {time.time() - start_e:.2f} 秒")

converter_data = st.session_state.converter_data
preprocessor_data = st.session_state.preprocessor_data
reader_data = st.session_state.reader_data
evaluator_data = st.session_state.evaluator_data


if converter_data:
    page_id = st.selectbox("選擇頁面 Page", sorted(converter_data.keys()))

    score = evaluator_data.get(page_id)
    if score is not None:
        st.metric("📊 相似度評估分數", f"{score:.2f}")
    elif isinstance(score, str):
        st.metric("📊 相似度評估分數", score)
    else:
        st.warning("此頁尚無評分結果")

    st.markdown("### 📄 PDF 原始頁面預覽")
    if page_id == 0:
        try:
            image = Image.open("/mnt/data/848f0e51-65a7-4c69-ac22-7924054ae86d.png")
            st.image(image, caption="PDF 頁面 0 預覽", use_column_width=True)
        except Exception as e:
            st.error(f"無法載入圖片：{e}")
    else:
        st.info("目前僅提供第 0 頁預覽。")

    col1, col2 = st.columns(2)

    with col1:
        st.header("左欄模組")
        left_module = st.selectbox(
            "選擇左欄模組", ["Reader", "Preprocessor", "Converter"], key="left_mod"
        )

        if left_module == "Reader":
            st.json(reader_data.get(page_id, []))
        elif left_module == "Preprocessor":
            pre_data = preprocessor_data.get(page_id, {})
            if isinstance(pre_data, dict):
                subpage = st.radio(
                    "上下頁", ["0", "1"], key="left_pre", horizontal=True
                )
                content = pre_data.get(int(subpage), [])
                if isinstance(content, list):
                    if content:
                        st.json(content)
                    else:
                        st.write("⚠️ 無資料")
                else:
                    st.write("⚠️ 非預期的資料型別")
            elif isinstance(pre_data, list):
                if pre_data:
                    st.json(pre_data)
                else:
                    st.write("⚠️ 無資料")
            else:
                st.write("⚠️ 非預期的資料型別")
        elif left_module == "Converter":
            subpage = st.radio("上下頁", ["0", "1"], key="left_conv", horizontal=True)
            st.json(converter_data.get(page_id, {}).get(int(subpage), "無資料"))

    with col2:
        st.header("右欄模組")
        right_module = st.selectbox(
            "選擇右欄模組", ["Reader", "Preprocessor", "Converter"], key="right_mod"
        )

        if right_module == "Reader":
            st.json(reader_data.get(page_id, []))
        elif right_module == "Preprocessor":
            pre_data = preprocessor_data.get(page_id, {})
            if isinstance(pre_data, dict):
                subpage = st.radio(
                    "上下頁", ["0", "1"], key="right_pre", horizontal=True
                )
                content = pre_data.get(int(subpage), [])
                if isinstance(content, list):
                    if content:
                        st.json(content)
                    else:
                        st.write("⚠️ 無資料")
                else:
                    st.write("⚠️ 非預期的資料型別")
            elif isinstance(pre_data, list):
                if pre_data:
                    st.json(pre_data)
                else:
                    st.write("⚠️ 無資料")
            else:
                st.write("⚠️ 非預期的資料型別")
        elif right_module == "Converter":
            subpage = st.radio("上下頁", ["0", "1"], key="right_conv", horizontal=True)
            st.json(converter_data.get(page_id, {}).get(int(subpage), "無資料"))
else:
    st.info("請先執行處理以顯示資料。")

st.subheader("📑 PDF 原始頁面顯示（可選頁）")
pdf_file = Path(path)
if pdf_file.exists() and pdf_file.suffix == ".pdf":
    doc = fitz.open(pdf_file)
    total_pages = len(doc)
    if total_pages > 1:
        selected_pdf_page = st.slider("選擇要顯示的 PDF 頁面", 1, total_pages, 1)
    else:
        selected_pdf_page = 1
        st.info("📄 PDF 僅有 1 頁")

    page = doc[selected_pdf_page - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    st.image(img, caption=f"PDF Page {selected_pdf_page}", use_column_width=True)
else:
    st.warning("PDF 檔案不存在或副檔名錯誤")
