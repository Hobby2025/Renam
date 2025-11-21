# Renam - Dockerfile for GUI Application
# Multi-stage build for optimized image size

FROM python:3.10-slim as base

# 환경 변수 설정
ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:1 \
    VNC_PORT=5901 \
    NOVNC_PORT=6080 \
    VNC_RESOLUTION=1280x720

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python Tkinter
    python3-tk \
    # VNC 서버
    tigervnc-standalone-server \
    tigervnc-common \
    # 경량 윈도우 매니저
    fluxbox \
    # 기타 유틸리티
    xterm \
    wget \
    ca-certificates \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# noVNC 설치 (웹 기반 VNC 클라이언트)
RUN wget -qO- https://github.com/novnc/noVNC/archive/v1.4.0.tar.gz | tar xz -C /opt && \
    mv /opt/noVNC-1.4.0 /opt/novnc && \
    ln -s /opt/novnc/vnc.html /opt/novnc/index.html && \
    wget -qO- https://github.com/novnc/websockify/archive/v0.11.0.tar.gz | tar xz -C /opt && \
    mv /opt/websockify-0.11.0 /opt/novnc/utils/websockify

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# VNC 비밀번호 설정 디렉토리 생성
RUN mkdir -p /root/.vnc

# VNC 비밀번호 설정 (기본값: renam)
RUN echo "renam" | vncpasswd -f > /root/.vnc/passwd && \
    chmod 600 /root/.vnc/passwd

# Fluxbox 설정
RUN mkdir -p /root/.fluxbox && \
    echo "session.screen0.toolbar.visible: false" > /root/.fluxbox/init && \
    echo "xterm &" > /root/.fluxbox/startup && \
    echo "python /app/app.py &" >> /root/.fluxbox/startup && \
    chmod +x /root/.fluxbox/startup

# Supervisor 설정 파일 생성
RUN echo "[supervisord]\n\
nodaemon=true\n\
\n\
[program:xvnc]\n\
command=Xvnc :1 -geometry %(ENV_VNC_RESOLUTION)s -depth 24 -rfbport %(ENV_VNC_PORT)s -SecurityTypes VncAuth -PasswordFile /root/.vnc/passwd\n\
autorestart=true\n\
priority=100\n\
\n\
[program:fluxbox]\n\
command=fluxbox\n\
environment=DISPLAY=\":1\"\n\
autorestart=true\n\
priority=200\n\
\n\
[program:novnc]\n\
command=/opt/novnc/utils/novnc_proxy --vnc localhost:%(ENV_VNC_PORT)s --listen %(ENV_NOVNC_PORT)s\n\
autorestart=true\n\
priority=300\n\
\n\
[program:renam]\n\
command=python /app/app.py\n\
environment=DISPLAY=\":1\"\n\
autorestart=true\n\
priority=400\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
" > /etc/supervisor/conf.d/supervisord.conf

# 포트 노출
EXPOSE 5901 6080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget -q -O - http://localhost:6080 > /dev/null 2>&1 || exit 1

# Supervisor로 모든 서비스 실행
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
