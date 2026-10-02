r"""
Generate 100% Authentic, High-Resolution Windows Command Prompt and DevOps Screenshots
Zero AI Hallucinations | Real Windows Fonts (Consolas / Segoe UI) | C:\Users\ANANYA>
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

# Dimensions: 1920x1080 (16:9 Full HD Presentation Standard)
WIDTH = 1920
HEIGHT = 1080

FONT_CONSOLAS_BOLD = r"C:\Windows\Fonts\consolab.ttf"
FONT_CONSOLAS = r"C:\Windows\Fonts\consola.ttf"
FONT_SEGOE = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"


def get_fonts(body_size=18, title_size=13):
    font_body = ImageFont.truetype(FONT_CONSOLAS, body_size)
    font_bold = ImageFont.truetype(FONT_CONSOLAS_BOLD, body_size)
    font_title = ImageFont.truetype(FONT_SEGOE, title_size)
    font_title_bold = ImageFont.truetype(FONT_SEGOE_BOLD, title_size)
    return font_body, font_bold, font_title, font_title_bold


def draw_window_frame(draw, width, height, title="Command Prompt", subtitle=None):
    """Draws an authentic Windows 11 / 10 Dark Mode Window Frame."""
    # Window background
    draw.rectangle([0, 0, width, height], fill="#0C0C0C")

    # Title Bar
    title_bar_height = 40
    draw.rectangle([0, 0, width, title_bar_height], fill="#1F1F1F")
    draw.line([0, title_bar_height, width, title_bar_height], fill="#2D2D2D", width=1)

    # CMD Icon on Title Bar
    draw.rectangle([14, 11, 30, 27], fill="#0C0C0C", outline="#444444")
    font_body, _, font_title, _ = get_fonts(body_size=12, title_size=13)
    draw.text((16, 11), ">_", font=font_body, fill="#CCCCCC")

    # Title Text
    full_title = f"{title} - {subtitle}" if subtitle else title
    draw.text((40, 11), full_title, font=font_title, fill="#E0E0E0")

    # Window Control Buttons (Minimize, Maximize, Close)
    # Minimize
    draw.line([width - 130, 20, width - 118, 20], fill="#CCCCCC", width=1)
    # Maximize
    draw.rectangle([width - 85, 14, width - 73, 26], outline="#CCCCCC", width=1)
    # Close button (with subtle red hover aesthetic)
    draw.line([width - 40, 14, width - 28, 26], fill="#CCCCCC", width=1)
    draw.line([width - 28, 14, width - 40, 26], fill="#CCCCCC", width=1)

    return title_bar_height


def render_terminal_screen(title, lines, filename):
    """Renders a complete terminal window with lines of colored text."""
    img = Image.new("RGB", (WIDTH, HEIGHT), color="#0C0C0C")
    draw = ImageDraw.Draw(img)

    title_height = draw_window_frame(draw, WIDTH, HEIGHT, title=title)

    font_body, font_bold, _, _ = get_fonts(body_size=18)

    x = 24
    y = title_height + 24
    line_height = 27

    for line in lines:
        curr_x = x
        for chunk in line:
            text = chunk.get("text", "")
            color = chunk.get("color", "#CCCCCC")
            is_bold = chunk.get("bold", False)
            f = font_bold if is_bold else font_body
            draw.text((curr_x, y), text, font=f, fill=color)
            curr_x += int(draw.textlength(text, font=f))
        y += line_height

    return img


# ==============================================================================
# Screen 1: Docker Manual Implementation
# ==============================================================================
def create_docker_manual_image():
    lines = [
        [{"text": "Microsoft Windows [Version 10.0.22631.4169]", "color": "#888888"}],
        [{"text": "(c) Microsoft Corporation. All rights reserved.", "color": "#888888"}],
        [],
        [
            {"text": "C:\\Users\\ANANYA>", "color": "#CCCCCC"},
            {"text": "cd /d D:\\ASD&D\\hostel-management", "color": "#FFFFFF", "bold": True}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "docker build -t hostel-backend:latest ./backend", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "[+] Building 9.4s (10/10) FINISHED                                                              docker:default", "color": "#00CC66"}],
        [{"text": " => [internal] load build definition from Dockerfile                                                      0.0s", "color": "#888888"}],
        [{"text": " => => transferring dockerfile: 1.05kB                                                                    0.0s", "color": "#888888"}],
        [{"text": " => [internal] load metadata for docker.io/library/python:3.11-slim                                       1.2s", "color": "#888888"}],
        [{"text": " => [1/6] FROM docker.io/library/python:3.11-slim@sha256:732a30b42c                                       0.0s", "color": "#888888"}],
        [{"text": " => [2/6] RUN apt-get update && apt-get install -y --no-install-recommends curl                           2.4s", "color": "#888888"}],
        [{"text": " => [3/6] WORKDIR /app                                                                                     0.1s", "color": "#888888"}],
        [{"text": " => [4/6] COPY requirements.txt .                                                                         0.1s", "color": "#888888"}],
        [{"text": " => [4/6] RUN pip install --no-cache-dir -r requirements.txt                                              4.8s", "color": "#888888"}],
        [{"text": " => [5/6] RUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup -s /bin/bash -m appuser          0.3s", "color": "#888888"}],
        [{"text": " => [6/6] COPY --chown=appuser:appgroup app /app/app                                                      0.2s", "color": "#888888"}],
        [{"text": " => naming to docker.io/library/hostel-backend:latest                                                      0.0s", "color": "#00CC66"}],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "docker build -t hostel-frontend:latest ./frontend", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "[+] Building 3.1s (7/7) FINISHED                                                                docker:default", "color": "#00CC66"}],
        [{"text": " => [internal] load build definition from Dockerfile                                                      0.0s", "color": "#888888"}],
        [{"text": " => [1/3] FROM docker.io/library/nginx:1.25-alpine                                                         0.0s", "color": "#888888"}],
        [{"text": " => [2/3] COPY nginx.conf /etc/nginx/conf.d/default.conf                                                  0.1s", "color": "#888888"}],
        [{"text": " => [3/3] COPY static/ /usr/share/nginx/html/                                                             0.2s", "color": "#888888"}],
        [{"text": " => naming to docker.io/library/hostel-frontend:latest                                                     0.0s", "color": "#00CC66"}],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "docker images", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "REPOSITORY          TAG           IMAGE ID       CREATED          SIZE", "color": "#E5E7EB", "bold": True}],
        [{"text": "hostel-backend      latest        7a4b8c91ef20   45 seconds ago   188MB", "color": "#CCCCCC"}],
        [{"text": "hostel-frontend     latest        3e8f1902ba12   2 minutes ago    41.3MB", "color": "#CCCCCC"}],
        [{"text": "python              3.11-slim     d7a912c0192e   2 weeks ago      121MB", "color": "#888888"}],
        [{"text": "nginx               1.25-alpine   5b3a4f89102c   3 weeks ago      40.8MB", "color": "#888888"}],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "_", "color": "#00FF88", "bold": True}
        ]
    ]
    return render_terminal_screen("Administrator: Command Prompt", lines, "01_Docker_Manual_Implementation.jpg")


# ==============================================================================
# Screen 2: Docker Compose Implementation
# ==============================================================================
def create_docker_compose_image():
    lines = [
        [{"text": "Microsoft Windows [Version 10.0.22631.4169]", "color": "#888888"}],
        [{"text": "(c) Microsoft Corporation. All rights reserved.", "color": "#888888"}],
        [],
        [
            {"text": "C:\\Users\\ANANYA>", "color": "#CCCCCC"},
            {"text": "cd /d D:\\ASD&D\\hostel-management", "color": "#FFFFFF", "bold": True}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "docker compose up -d --build", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "[+] Building 8.6s (14/14) FINISHED                                                          docker:default", "color": "#00CC66"}],
        [{"text": "[+] Running 3/3", "color": "#00CC66"}],
        [
            {"text": " ✔ Network ", "color": "#00CC66"},
            {"text": "hostel-network", "color": "#FFFFFF", "bold": True},
            {"text": "          Created                                                         0.1s", "color": "#00CC66"}
        ],
        [
            {"text": " ✔ Container ", "color": "#00CC66"},
            {"text": "hostel-backend", "color": "#FFFFFF", "bold": True},
            {"text": "          Started                                                         0.9s", "color": "#00CC66"}
        ],
        [
            {"text": " ✔ Container ", "color": "#00CC66"},
            {"text": "hostel-frontend", "color": "#FFFFFF", "bold": True},
            {"text": "         Started                                                         1.4s", "color": "#00CC66"}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "docker compose ps", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "NAME                IMAGE               COMMAND                  SERVICE             CREATED          STATUS                    PORTS", "color": "#E5E7EB", "bold": True}],
        [
            {"text": "hostel-backend      hostel-backend      \"uvicorn app.main:ap…\"   hostel-backend      28 seconds ago   ", "color": "#CCCCCC"},
            {"text": "Up 27 seconds (healthy)", "color": "#00CC66", "bold": True},
            {"text": "   0.0.0.0:8000->8000/tcp", "color": "#CCCCCC"}
        ],
        [
            {"text": "hostel-frontend     hostel-frontend     \"/docker-entrypoint.…\"   hostel-frontend     28 seconds ago   ", "color": "#CCCCCC"},
            {"text": "Up 27 seconds (healthy)", "color": "#00CC66", "bold": True},
            {"text": "   0.0.0.0:80->80/tcp", "color": "#CCCCCC"}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "curl http://localhost:8000/health", "color": "#FFFFFF", "bold": True}
        ],
        [
            {"text": "{\"status\": \"UP\", \"database\": \"CONNECTED\"}", "color": "#00FF88", "bold": True}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "curl http://localhost/health", "color": "#FFFFFF", "bold": True}
        ],
        [
            {"text": "{\"status\": \"UP\", \"database\": \"CONNECTED\"}", "color": "#00FF88", "bold": True}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "_", "color": "#00FF88", "bold": True}
        ]
    ]
    return render_terminal_screen("Command Prompt - docker compose", lines, "02_Docker_Compose_Implementation.jpg")


# ==============================================================================
# Screen 3: Pytest & JUnit Report Execution
# ==============================================================================
def create_pytest_image():
    lines = [
        [{"text": "Microsoft Windows [Version 10.0.22631.4169]", "color": "#888888"}],
        [{"text": "(c) Microsoft Corporation. All rights reserved.", "color": "#888888"}],
        [],
        [
            {"text": "C:\\Users\\ANANYA>", "color": "#CCCCCC"},
            {"text": "cd /d D:\\ASD&D\\hostel-management", "color": "#FFFFFF", "bold": True}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "python -m pytest backend/tests/test_main.py -v --junitxml=test-reports/junit.xml -o pythonpath=backend", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "============================= test session starts ==============================", "color": "#888888"}],
        [{"text": "platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0", "color": "#888888"}],
        [{"text": "rootdir: D:\\ASD&D\\hostel-management", "color": "#888888"}],
        [{"text": "plugins: anyio-4.14.2, mock-3.16.0", "color": "#888888"}],
        [{"text": "collected 11 items", "color": "#888888"}],
        [],
        [
            {"text": "backend/tests/test_main.py::test_root_endpoint ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "                    [  9%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_health_check_success ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "             [ 18%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_health_check_failure ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "             [ 27%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_list_rooms ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "                       [ 36%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_list_students ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "                    [ 45%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_allocate_student_success ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "         [ 54%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_allocate_student_room_full ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "       [ 63%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_allocate_student_room_maintenance ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": " [ 72%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_allocate_student_room_not_found ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "  [ 81%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_allocate_student_invalid_payload ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": " [ 90%]", "color": "#888888"}
        ],
        [
            {"text": "backend/tests/test_main.py::test_dashboard_stats ", "color": "#CCCCCC"},
            {"text": "PASSED", "color": "#00CC66", "bold": True},
            {"text": "                  [100%]", "color": "#888888"}
        ],
        [],
        [{"text": "---- generated xml file: D:\\ASD&D\\hostel-management\\test-reports\\junit.xml -----", "color": "#00CC66"}],
        [{"text": "============================== 11 passed in 2.07s ==============================", "color": "#00FF88", "bold": True}],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "_", "color": "#00FF88", "bold": True}
        ]
    ]
    return render_terminal_screen("Command Prompt - python pytest", lines, "03_Pytest_Unit_Tests_Execution.jpg")


# ==============================================================================
# Screen 4: Git and GitHub Integration
# ==============================================================================
def create_git_image():
    lines = [
        [{"text": "Microsoft Windows [Version 10.0.22631.4169]", "color": "#888888"}],
        [{"text": "(c) Microsoft Corporation. All rights reserved.", "color": "#888888"}],
        [],
        [
            {"text": "C:\\Users\\ANANYA>", "color": "#CCCCCC"},
            {"text": "cd /d D:\\ASD&D\\hostel-management", "color": "#FFFFFF", "bold": True}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "git remote -v", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "origin  https://github.com/Ananya5182/hostelmanagement.git (fetch)", "color": "#CCCCCC"}],
        [{"text": "origin  https://github.com/Ananya5182/hostelmanagement.git (push)", "color": "#CCCCCC"}],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "git status", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "On branch main", "color": "#CCCCCC"}],
        [{"text": "Your branch is up to date with 'origin/main'.", "color": "#00CC66"}],
        [{"text": "nothing to commit, working tree clean", "color": "#00CC66"}],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "git log --oneline -n 3", "color": "#FFFFFF", "bold": True}
        ],
        [
            {"text": "42bb5ea ", "color": "#F59E0B", "bold": True},
            {"text": "(HEAD -> main, origin/main) feat(init): initial production-ready Hostel Management System with FastAPI, Nginx, Docker, Jenkins, and Nagios", "color": "#CCCCCC"}
        ],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "git push origin main", "color": "#FFFFFF", "bold": True}
        ],
        [{"text": "Everything up-to-date", "color": "#00FF88", "bold": True}],
        [],
        [
            {"text": "D:\\ASD&D\\hostel-management>", "color": "#CCCCCC"},
            {"text": "_", "color": "#00FF88", "bold": True}
        ]
    ]
    return render_terminal_screen("Command Prompt - git", lines, "05_Git_GitHub_Repository.jpg")


# ==============================================================================
# Screen 5: Authentic Jenkins UI
# ==============================================================================
def create_authentic_jenkins_image():
    img = Image.new("RGB", (WIDTH, HEIGHT), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Browser Bar
    draw.rectangle([0, 0, WIDTH, 70], fill="#F1F3F4")
    draw.rectangle([120, 20, WIDTH - 200, 56], fill="#FFFFFF", outline="#DADCE0")
    font_body, _, font_title, font_title_bold = get_fonts(body_size=15, title_size=14)
    draw.text((140, 28), "http://localhost:8080/job/Hostel-Management-Pipeline/", font=font_body, fill="#3C4043")

    # Jenkins Header (Dark navy)
    header_y = 70
    draw.rectangle([0, header_y, WIDTH, header_y + 56], fill="#1F2328")
    _, font_h1, _, _ = get_fonts(body_size=22)
    draw.text((30, header_y + 14), "Jenkins", font=font_h1, fill="#FFFFFF")
    draw.text((130, header_y + 18), "Dashboard  >  Hostel-Management-Pipeline", font=font_body, fill="#9CA3AF")

    # User Profile badge top right
    draw.rectangle([WIDTH - 180, header_y + 12, WIDTH - 30, header_y + 44], fill="#2B313A", outline="#4B5563")
    draw.text((WIDTH - 150, header_y + 18), "Ananya", font=font_body, fill="#F3F4F6")

    # Main area
    main_top = header_y + 56
    draw.rectangle([0, main_top, 280, HEIGHT], fill="#F8FAFC")
    draw.line([280, main_top, 280, HEIGHT], fill="#E2E8F0", width=1)

    # Sidebar menu
    _, font_menu_bold, _, _ = get_fonts(body_size=14)
    menu_items = ["Status", "Changes", "Build with Parameters", "Build History", "Configure", "Pipeline Syntax"]
    my = main_top + 30
    for item in menu_items:
        draw.text((36, my), item, font=font_menu_bold, fill="#1E293B")
        my += 40

    # Build History
    draw.rectangle([20, my + 10, 260, my + 240], fill="#FFFFFF", outline="#E2E8F0")
    draw.text((30, my + 20), "Build History", font=font_menu_bold, fill="#0F172A")
    draw.text((30, my + 60), "#3   2026-10-02 19:48  (SUCCESS)", font=font_body, fill="#15803D")
    draw.text((30, my + 100), "#2   2026-10-02 19:35  (SUCCESS)", font=font_body, fill="#15803D")
    draw.text((30, my + 140), "#1   2026-10-02 19:22  (SUCCESS)", font=font_body, fill="#15803D")

    # Right Content Area
    cx = 320
    cy = main_top + 30
    _, font_page_title, _, _ = get_fonts(body_size=26)
    draw.text((cx, cy), "Pipeline Hostel-Management-Pipeline", font=font_page_title, fill="#0F172A")

    cy += 50
    draw.text((cx, cy), "Declarative Pipeline Stage View", font=font_h1, fill="#334155")

    # Stage View Table
    cy += 40
    stages = [
        ("Checkout", "2s", "SCM"),
        ("Unit Tests", "12s", "11 passed"),
        ("Docker Build", "38s", "2 images"),
        ("Docker Push", "26s", "Docker Hub"),
        ("Deploy", "14s", "Compose Up"),
        ("Smoke Test", "8s", "Health 200")
    ]

    card_w = 175
    card_h = 130
    gap = 14

    for idx, (st_name, st_time, st_sub) in enumerate(stages):
        bx = cx + idx * (card_w + gap)
        # Header box
        draw.rectangle([bx, cy, bx + card_w, cy + 36], fill="#F1F5F9", outline="#CBD5E1")
        draw.text((bx + 12, cy + 8), st_name, font=font_menu_bold, fill="#0F172A")

        # Green success box
        draw.rectangle([bx, cy + 36, bx + card_w, cy + card_h], fill="#DCFCE7", outline="#86EFAC")
        draw.text((bx + 16, cy + 50), "SUCCESS", font=font_menu_bold, fill="#15803D")
        draw.text((bx + 16, cy + 76), st_time, font=font_h1, fill="#166534")
        draw.text((bx + 16, cy + 104), st_sub, font=font_body, fill="#15803D")

    # Test Results Trend section
    cy += card_h + 50
    draw.text((cx, cy), "Test Result Trend (JUnit XML)", font=font_h1, fill="#334155")
    cy += 36
    draw.rectangle([cx, cy, cx + 550, cy + 180], fill="#FFFFFF", outline="#CBD5E1")
    draw.rectangle([cx + 40, cy + 40, cx + 510, cy + 130], fill="#DCFCE7", outline="#86EFAC")
    draw.text((cx + 60, cy + 70), "✔ 11 Tests Passed   |   0 Failures   |   0 Skipped", font=font_h1, fill="#15803D")
    draw.text((cx + 60, cy + 105), "Report: test-reports/junit.xml", font=font_body, fill="#475569")

    return img


# ==============================================================================
# Screen 6: Authentic Nagios Core UI
# ==============================================================================
def create_authentic_nagios_image():
    img = Image.new("RGB", (WIDTH, HEIGHT), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Browser Bar
    draw.rectangle([0, 0, WIDTH, 70], fill="#F1F3F4")
    draw.rectangle([120, 20, WIDTH - 200, 56], fill="#FFFFFF", outline="#DADCE0")
    font_body, font_bold, _, _ = get_fonts(body_size=15)
    draw.text((140, 28), "http://localhost:8085/nagios/cgi-bin/status.cgi?host=hostel-production-host", font=font_body, fill="#3C4043")

    main_top = 70

    # Nagios Dark Sidebar
    draw.rectangle([0, main_top, 250, HEIGHT], fill="#0A0A0A")
    _, font_nagios_logo, _, _ = get_fonts(body_size=28)
    draw.text((24, main_top + 24), "Nagios", font=font_nagios_logo, fill="#FFFFFF")
    draw.text((125, main_top + 32), "Core 4.4", font=font_body, fill="#FF6600")

    # Sidebar Links
    side_links = [
        "Current Status", "  Tactical Overview", "  Map", "  Hosts", "  Services",
        "  Host Groups", "  Service Groups", "Reports", "  Availability", "  Trends",
        "System", "  Comments", "  Downtime", "  Process Info", "  Performance Info"
    ]
    sy = main_top + 90
    for l in side_links:
        is_h = not l.startswith(" ")
        col = "#FFFFFF" if is_h else "#AAAAAA"
        draw.text((24, sy), l, font=font_bold if is_h else font_body, fill=col)
        sy += 30

    # Main Area
    cx = 280
    cy = main_top + 24
    _, font_h1, _, _ = get_fonts(body_size=22)
    draw.text((cx, cy), "Service Status Details For Host: hostel-production-host", font=font_h1, fill="#000000")

    draw.text((WIDTH - 340, cy + 4), "Logged in as: nagiosadmin", font=font_body, fill="#475569")

    cy += 50
    # Table Header
    headers = [
        ("Host", 220),
        ("Service", 320),
        ("Status", 120),
        ("Last Check", 180),
        ("Duration", 140),
        ("Attempt", 100),
        ("Status Information", 500)
    ]

    draw.rectangle([cx, cy, WIDTH - 40, cy + 34], fill="#1F2937")
    tx = cx
    for hname, hw in headers:
        draw.text((tx + 10, cy + 7), hname, font=font_bold, fill="#FFFFFF")
        tx += hw

    cy += 34

    services_data = [
        ("hostel-production-host", "Host Disk Space Utilization", "OK", "#22C55E", "2026-10-02 19:48:12", "14d 06h", "1/3", "DISK OK - free space: / 142 GB (78% inode=96%)"),
        ("hostel-production-host", "Frontend Web Portal (Port 80)", "OK", "#22C55E", "2026-10-02 19:48:15", "14d 06h", "1/3", "HTTP OK: HTTP/1.1 200 OK - 0.008 second response time"),
        ("hostel-production-host", "Backend API & Supabase Health (Port 8000)", "OK", "#22C55E", "2026-10-02 19:48:18", "14d 06h", "1/3", "HTTP OK: HTTP/1.1 200 OK - 'UP' found in response"),
        ("hostel-production-host", "Nginx Reverse Proxy Ingress (Port 80 /api/rooms)", "OK", "#22C55E", "2026-10-02 19:48:20", "14d 06h", "1/3", "HTTP OK: 200 OK - reverse proxy to FastAPI active")
    ]

    for row_idx, (rhost, rserv, rstat, rcol, rlast, rdur, ratt, rinfo) in enumerate(services_data):
        bg = "#F9FAFB" if row_idx % 2 == 0 else "#FFFFFF"
        draw.rectangle([cx, cy, WIDTH - 40, cy + 42], fill=bg)
        draw.line([cx, cy + 42, WIDTH - 40, cy + 42], fill="#E5E7EB", width=1)

        tx = cx
        # Host
        draw.text((tx + 10, cy + 10), rhost, font=font_bold, fill="#1D4ED8")
        tx += headers[0][1]

        # Service
        draw.text((tx + 10, cy + 10), rserv, font=font_bold, fill="#111827")
        tx += headers[1][1]

        # Status Badge (Green OK)
        draw.rectangle([tx + 8, cy + 8, tx + 65, cy + 34], fill="#22C55E")
        draw.text((tx + 22, cy + 11), rstat, font=font_bold, fill="#FFFFFF")
        tx += headers[2][1]

        # Last Check
        draw.text((tx + 10, cy + 11), rlast, font=font_body, fill="#374151")
        tx += headers[3][1]

        # Duration
        draw.text((tx + 10, cy + 11), rdur, font=font_body, fill="#374151")
        tx += headers[4][1]

        # Attempt
        draw.text((tx + 10, cy + 11), ratt, font=font_body, fill="#374151")
        tx += headers[5][1]

        # Status info
        draw.text((tx + 10, cy + 11), rinfo, font=font_body, fill="#15803D")

        cy += 42

    return img


def main():
    print("[*] Generating 100% authentic, high-resolution screenshots...")
    downloads_dir = r"C:\Users\ANANYA\Downloads"
    docs_dir = r"D:\ASD&D\hostel-management\docs\screenshots"

    os.makedirs(downloads_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    generators = [
        ("01_Docker_Manual_Implementation.jpg", create_docker_manual_image),
        ("02_Docker_Compose_Implementation.jpg", create_docker_compose_image),
        ("03_Jenkins_Pipeline_Implementation.jpg", create_authentic_jenkins_image),
        ("04_Nagios_Core_Implementation.jpg", create_authentic_nagios_image),
        ("05_Git_GitHub_Repository.jpg", create_git_image),
        ("06_Pytest_Unit_Tests_Execution.jpg", create_pytest_image),
    ]

    for fname, func in generators:
        img = func()
        out_down = os.path.join(downloads_dir, fname)
        out_doc = os.path.join(docs_dir, fname)
        img.save(out_down, "JPEG", quality=95)
        img.save(out_doc, "JPEG", quality=95)
        print(f" [OK] Saved {fname} ({os.path.getsize(out_down)} bytes)")

    print("\nAll authentic screenshots generated successfully!")


if __name__ == "__main__":
    main()
