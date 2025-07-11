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

# Initialize session state
if "reader_data" not in st.session_state:
    st.session_state.reader_data = None
    st.session_state.preprocessor_data = None
    st.session_state.converter_data = None
    st.session_state.evaluator_data = None

if st.button("📂 顯示當前資料夾所有 PDF 檔案"):
    current_dir = Path("./data")
    pdf_files = list(current_dir.glob("*.pdf"))
    if pdf_files:
        st.write("找到以下 PDF 檔案：")
        for f in pdf_files:
            st.write(f.name)
    else:
        st.info("目前資料夾中沒有 PDF 檔案。")

if "pdf_path" not in st.session_state:
    st.session_state["pdf_path"] = "./example/data/EMPU_3401_Datasheet.pdf"

# Input parameters
with st.form(key="pdf_form"):
    path = st.text_input("請輸入 PDF 路徑：", st.session_state["pdf_path"])
    submitted = st.form_submit_button("📂 重新載入 PDF")
    if submitted:
        st.session_state["pdf_path"] = path


model_name = st.text_input("請輸入 model name：", "mistral-small3.1:24b")
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
        st.session_state.reader_data = parser.process(path)

        start_p = time.time()
        preprocessor = XMLPreProcessor()
        st.session_state.preprocessor_data = preprocessor.process(
            st.session_state.reader_data
        )

        start_c = time.time()
        transformer = Transform(model_name=model_name, model_url=model_url)
        st.session_state.converter_data = transformer.process(
            st.session_state.preprocessor_data, format="dict", prompt=prompt
        )
        start_e = time.time()
        metric, _ = SimilarityMetrics.get("str_similarity")
        validator = Validate(metrics=metric)
        st.session_state.evaluator_data = validator.process(
            gt_data=st.session_state.reader_data, data=st.session_state.converter_data
        )
        end_t = time.time()

    st.subheader("⏱️ 執行時間統計")
    st.text(f"總時間: {end_t - start_t:.2f} 秒")
    st.text(f"前處理: {start_c - start_p:.2f} 秒")
    st.text(f"轉換: {start_e - start_c:.2f} 秒")
    st.text(f"評估: {end_t - start_e:.2f} 秒")

# --- Main Display Area ---
converter_data = st.session_state.converter_data
preprocessor_data = st.session_state.preprocessor_data
reader_data = st.session_state.reader_data
evaluator_data = st.session_state.evaluator_data

if converter_data and hasattr(converter_data, "pages"):
    page_keys = sorted(converter_data.pages.keys())
    if not page_keys:
        st.warning("No pages processed.")
    else:
        page_id = st.selectbox("選擇頁面 Page", page_keys)

        score = None
        if evaluator_data and hasattr(evaluator_data, "pages"):
            score = evaluator_data.pages.get(page_id)

        if score is not None:
            st.metric("📊 相似度評估分數", f"{score:.2f}")
        else:
            st.warning("此頁尚無評分結果")

        col1, col2 = st.columns(2)

        # --- Column Logic ---
        for i, col in enumerate([col1, col2]):
            with col:
                key_prefix = "left" if i == 0 else "right"
                default_module = "Converter" if i == 1 else "Reader"

                st.header(f"{'右' if i == 1 else '左'}欄模組")
                module = st.selectbox(
                    f"選擇{key_prefix}欄模組",
                    ["Reader", "Preprocessor", "Converter"],
                    key=f"{key_prefix}_mod",
                    index=["Reader", "Preprocessor", "Converter"].index(default_module),
                )

                if module == "Reader":
                    if (
                        reader_data
                        and hasattr(reader_data, "pages")
                        and page_id in reader_data.pages
                    ):
                        st.json(reader_data.pages[page_id].model_dump())
                    else:
                        st.warning("⚠️ 無資料")

                elif module == "Preprocessor":
                    if (
                        preprocessor_data
                        and hasattr(preprocessor_data, "pages")
                        and page_id in preprocessor_data.pages
                    ):
                        page_data = preprocessor_data.pages[page_id]
                        display_data = page_data.model_dump()

                        if "data" in display_data and isinstance(
                            display_data["data"], dict
                        ):
                            subpage_keys = sorted(display_data["data"].keys(), key=int)
                            if subpage_keys:
                                subpage = st.radio(
                                    "Sub-page",
                                    subpage_keys,
                                    key=f"{key_prefix}_pre",
                                    horizontal=True,
                                )
                                content = display_data["data"].get(subpage, [])
                                st.code("\n".join(content), language="xml")
                            else:
                                st.warning("⚠️ 無 sub-page 資料")
                        else:
                            st.json(display_data)  # Fallback
                    else:
                        st.warning("⚠️ 無資料")

                elif module == "Converter":
                    if (
                        converter_data
                        and hasattr(converter_data, "pages")
                        and page_id in converter_data.pages
                    ):
                        page_data = converter_data.pages[page_id]
                        display_data = page_data.model_dump()

                        if "data" in display_data and isinstance(
                            display_data["data"], dict
                        ):
                            subpage_keys = sorted(display_data["data"].keys(), key=int)
                            if subpage_keys:
                                subpage = st.radio(
                                    "Sub-page",
                                    subpage_keys,
                                    key=f"{key_prefix}_conv",
                                    horizontal=True,
                                )
                                content = display_data["data"].get(subpage)
                                if isinstance(content, (dict, list)):
                                    st.json(content)
                                else:
                                    st.code(str(content), language="json")
                            else:
                                st.warning("⚠️ 無 sub-page 資料")
                        else:
                            st.json(display_data)  # Fallback
                    else:
                        st.warning("⚠️ 無資料")
else:
    st.info("請先執行處理以顯示資料。")

st.subheader("📑 PDF 原始頁面顯示（可選頁）")
pdf_file = Path(path)
if pdf_file.exists() and pdf_file.suffix == ".pdf":
    doc = fitz.open(pdf_file)
    total_pages = len(doc)

    # Use the page_id from the selectbox if available, otherwise default to 1
    selected_page_index = page_id if "page_id" in locals() else 0

    if total_pages > 1:
        # The slider now controls the viewer, and its default is the selected page
        selected_page_number = st.slider(
            "選擇要顯示的 PDF 頁面", 1, total_pages, selected_page_index + 1
        )
    else:
        selected_page_number = 1
        st.info("📄 PDF 僅有 1 頁")

    page = doc[selected_page_number - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    st.image(img, caption=f"PDF Page {selected_page_number}", use_column_width=True)
else:
    st.warning("PDF 檔案不存在或副檔名錯誤")
