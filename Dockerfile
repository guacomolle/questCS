# Квест: Команда Безопасика — образ для запуска на Ubuntu-сервере
FROM python:3.12-slim

WORKDIR /app

# Зависимости ставим отдельным слоем, чтобы кэш Docker не сбрасывался
# при изменении кода приложения.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код приложения и картинки, которые он использует (маскот и сертификат).
COPY app.py mascot.png certificate.png ./

# Отключаем сбор телеметрии и разовый запрос email при первом запуске Streamlit,
# включаем headless-режим и слушаем на всех интерфейсах контейнера.
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app.py"]
