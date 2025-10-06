import os
import streamlit as st
from dotenv import load_dotenv

from service.api_clients import KiraAPIClient, OdlicaAPIClient
from service.metrics import compare_tags

load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
API1_HOST = os.getenv("API1_HOST")
API2_HOST = os.getenv("API2_HOST")

API1_URL = f"https://{API1_HOST}/api/tag"
API2_URL = f"https://{API2_HOST}/analyze"

client1 = KiraAPIClient(API1_URL, API_KEY, API1_HOST)
client2 = OdlicaAPIClient(API2_URL, API_KEY, API2_HOST)

# ui
st.title("Получение тегов изображений")

image_url = st.text_input("Вставьте публичный URL изображения")

if image_url:
    st.image(image_url, caption="Исходное изображение", width="stretch")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:

        if st.button("Запустить теггинг", width="stretch"):
            tags1 = client1.get_tags(image_url)
            tags2 = client2.get_tags(image_url)

            def format_tags(tags: list[str]) -> str:
                if not tags:
                    return "_Нет тегов_"
                return "  \n".join(f"- **{t}**" for t in tags)

            with col1:
                st.markdown("### API1")
                st.write(tags1)

            with col3:
                st.markdown("### API2")
                st.write(tags2)

            metrics = compare_tags(tags1, tags2)
            st.subheader("Сравнение результатов")
            st.write("Пересечения:")
            st.markdown(format_tags(metrics["overlap"]))
            st.write("Уникальные у API1:", metrics["unique_api1"])
            st.write("Уникальные у API2:", metrics["unique_api2"])
