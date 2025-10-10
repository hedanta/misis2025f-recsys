import os
import streamlit as st
from dotenv import load_dotenv

from service.api_clients import KiraAPIClient, OdlicaAPIClient
from service.metrics import compare_tags

load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
API1_HOST = os.getenv("API1_HOST")
API2_HOST = os.getenv("API2_HOST")

client1 = KiraAPIClient(f"https://{API1_HOST}/api/tag", API_KEY, API1_HOST)
client2 = OdlicaAPIClient(f"https://{API2_HOST}/analyze", API_KEY, API2_HOST)

# ui
st.title("Получение тегов изображений")

image_url = st.text_input("Вставьте публичный URL изображения")
if not image_url:
    st.stop()

st.image(image_url, caption="Исходное изображение", width="stretch")

col1, col2, col3 = st.columns([1, 2, 1])

def format_tags(tags: list[str]) -> str:
    return "_Нет тегов_" if not tags else "  \n".join(f"- **{t}**" for t in tags)

if col2.button("Запустить теггинг", width="stretch"):
    tags1 = client1.get_tags(image_url)
    tags2 = client2.get_tags(image_url)

    col1.markdown("### API1")
    col1.write(tags1)

    col3.markdown("### API2")
    col3.write(tags2)

    metrics = compare_tags(tags1, tags2)
    st.subheader("Сравнение результатов")
    st.write("Пересечения:")
    st.markdown(format_tags(metrics["overlap"]))
    st.write("Уникальные у API1:", metrics["unique_api1"])
    st.write("Уникальные у API2:", metrics["unique_api2"])
