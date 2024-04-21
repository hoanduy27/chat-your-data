FROM python:3.9-slim

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-venv && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    rm -rf /root/.cache/pip

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app_st.py", "--server.port=8501", "--server.address=0.0.0.0"]