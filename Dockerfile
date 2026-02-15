# 1. Base Image (Python 3.10 is stable for AI)
FROM python:3.10-slim

# 2. Work directory set karo
WORKDIR /app

# 3. System dependencies (OpenCV aur Graphics ke liye)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 4. Saara code copy karo
COPY . .

# 5. Requirements install karo
RUN pip install --no-cache-dir -r requirements.txt

# 6. Streamlit port setup
EXPOSE 7860

# 7. Engine Start!
CMD ["streamlit", "run", "app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]

