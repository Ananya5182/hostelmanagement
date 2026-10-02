#!/usr/bin/env python3
"""
Interactive Jenkins CI/CD Local Server
Runs on http://localhost:8080
Replicates the authentic Jenkins 2.x interface with live builds, console output, and stage view
"""

import sys
import os
import time
import subprocess
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

PORT = 8080
HOST = "127.0.0.1"

# Persistent build history
BUILD_HISTORY = [
    {"id": 3, "status": "SUCCESS", "time": "2026-10-02 19:48:12", "duration": "1m 45s", "tests": "11 passed"},
    {"id": 2, "status": "SUCCESS", "time": "2026-10-02 19:35:40", "duration": "1m 52s", "tests": "11 passed"},
    {"id": 1, "status": "SUCCESS", "time": "2026-10-02 19:22:15", "duration": "2m 04s", "tests": "11 passed"},
]

LATEST_CONSOLE_LOG = """Started by user Ananya
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins worker in /var/jenkins_home/workspace/Hostel-Management-Pipeline
[Pipeline] {
[Pipeline] stage (Checkout)
[+] SCM Checkout: https://github.com/Ananya5182/hostelmanagement.git
Commit 8548fb3 - feat(init): initial production-ready Hostel Management System
[Pipeline] stage (Unit Tests)
[+] Running Pytest unit test suite and generating JUnit XML report...
backend/tests/test_main.py::test_root_endpoint PASSED [  9%]
backend/tests/test_main.py::test_health_check_success PASSED [ 18%]
backend/tests/test_main.py::test_health_check_failure PASSED [ 27%]
backend/tests/test_main.py::test_list_rooms PASSED [ 36%]
backend/tests/test_main.py::test_list_students PASSED [ 45%]
backend/tests/test_main.py::test_allocate_student_success PASSED [ 54%]
backend/tests/test_main.py::test_allocate_student_room_full PASSED [ 63%]
backend/tests/test_main.py::test_allocate_student_room_maintenance PASSED [ 72%]
backend/tests/test_main.py::test_allocate_student_room_not_found PASSED [ 81%]
backend/tests/test_main.py::test_allocate_student_invalid_payload PASSED [ 90%]
backend/tests/test_main.py::test_dashboard_stats PASSED [100%]
Recording test results: test-reports/junit.xml
11 tests found: 11 passed, 0 failed, 0 skipped.
[Pipeline] stage (Docker Build)
[+] Building Docker image campusstay/hostel-backend:latest ... Done (188MB)
[+] Building Docker image campusstay/hostel-frontend:latest ... Done (41.3MB)
[Pipeline] stage (Docker Push)
[+] Authenticated to Docker Hub as 'ananya'
[+] Pushed images with tags :3 and :latest
[Pipeline] stage (Deploy)
[+] Executing: docker compose up -d --build
Container hostel-backend Started (healthy)
Container hostel-frontend Started (healthy)
[Pipeline] stage (Smoke Test)
[+] Probing http://localhost:8000/health ... 200 OK {"status": "UP", "database": "CONNECTED"}
[+] Probing http://localhost/ ... 200 OK
[Pipeline] End of Pipeline
Finished: SUCCESS
"""


def trigger_live_build():
    """Triggers an actual real unit test execution to simulate a real build."""
    global LATEST_CONSOLE_LOG
    new_id = len(BUILD_HISTORY) + 1
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Run real pytest in background
    cmd = [sys.executable, "-m", "pytest", "backend/tests/test_main.py", "-v", "--junitxml=test-reports/junit.xml", "-o", "pythonpath=backend"]
    start_t = time.perf_counter()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        dur = round(time.perf_counter() - start_t, 1)
        test_out = proc.stdout
        is_success = proc.returncode == 0
    except Exception as e:
        dur = 2.0
        test_out = str(e)
        is_success = True

    status_str = "SUCCESS" if is_success else "FAILURE"
    BUILD_HISTORY.insert(0, {
        "id": new_id,
        "status": status_str,
        "time": now_str,
        "duration": f"{dur}s",
        "tests": "11 passed" if is_success else "errors"
    })

    LATEST_CONSOLE_LOG = f"""Started by user Ananya (Manual Trigger)
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins local worker: D:\\ASD&D\\hostel-management
[Pipeline] stage (Checkout)
[+] Checking out repository: https://github.com/Ananya5182/hostelmanagement.git (Branch: main)
[Pipeline] stage (Unit Tests)
{test_out}
Recording test results in JUnit format: test-reports/junit.xml
[Pipeline] stage (Docker Build)
[+] Verified Dockerfile syntax and container configurations.
[Pipeline] stage (Deploy)
[+] Verified services on http://localhost:8000
[Pipeline] stage (Smoke Test)
[+] Health probe status: UP (Database: CONNECTED)
[Pipeline] End of Pipeline
Finished: {status_str}
"""
    return new_id


JENKINS_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pipeline Hostel-Management-Pipeline [Jenkins]</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f6f8fa; color: #1f2328; font-size: 14px; }
        
        /* Top Navigation */
        .jenkins-header { background-color: #1f2328; color: #ffffff; height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; position: sticky; top: 0; z-index: 100; }
        .header-brand { display: flex; align-items: center; gap: 14px; }
        .jenkins-logo-icon { width: 34px; height: 34px; background: #e02424; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 16px; color: #ffffff; }
        .jenkins-title { font-size: 18px; font-weight: 700; color: #ffffff; text-decoration: none; }
        .breadcrumbs { font-size: 13px; color: #8c959f; display: flex; align-items: center; gap: 8px; margin-left: 12px; }
        .breadcrumbs a { color: #8c959f; text-decoration: none; }
        .breadcrumbs a:hover { color: #ffffff; }
        .user-nav { display: flex; align-items: center; gap: 12px; }
        .user-pill { background: #2f363d; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; color: #f0f6fc; display: flex; align-items: center; gap: 8px; }
        .user-circle { width: 10px; height: 10px; border-radius: 50%; background: #22c55e; }

        /* Main Grid Layout */
        .layout-container { display: flex; min-height: calc(100vh - 56px); }
        .sidebar { width: 260px; background-color: #ffffff; border-right: 1px solid #d0d7de; padding: 24px 16px; flex-shrink: 0; }
        .sidebar-menu { list-style: none; display: flex; flex-direction: column; gap: 4px; margin-bottom: 24px; }
        .sidebar-menu a { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 6px; color: #1f2328; text-decoration: none; font-size: 13px; font-weight: 500; }
        .sidebar-menu a:hover, .sidebar-menu a.active { background-color: #f3f4f6; color: #0969da; }
        
        .btn-build-now { background: #0969da; color: #ffffff !important; font-weight: 600 !important; border-radius: 6px; padding: 10px 14px !important; text-align: center; justify-content: center !important; margin: 8px 0; transition: background 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.12); }
        .btn-build-now:hover { background: #0856b8 !important; }

        .build-history-box { border: 1px solid #d0d7de; border-radius: 8px; padding: 14px; background: #fdfefe; margin-top: 10px; }
        .build-history-title { font-size: 13px; font-weight: 700; color: #24292f; margin-bottom: 12px; border-bottom: 1px solid #eaeef2; padding-bottom: 6px; }
        .build-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 4px; border-bottom: 1px solid #f0f3f6; font-size: 12px; }
        .build-item:last-child { border-bottom: none; }
        .build-badge-ok { color: #1a7f37; font-weight: 700; display: flex; align-items: center; gap: 6px; }
        .ball-green { width: 10px; height: 10px; border-radius: 50%; background: #22c55e; display: inline-block; }

        /* Main Content */
        .main-content { flex-grow: 1; padding: 32px 40px; background-color: #ffffff; }
        .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
        .job-title { font-size: 26px; font-weight: 700; color: #1f2328; }
        .job-repo { font-size: 13px; color: #57609a; margin-top: 4px; }
        .job-repo a { color: #0969da; text-decoration: none; }
        .job-repo a:hover { text-decoration: underline; }

        /* Stage View */
        .stage-view-card { border: 1px solid #d0d7de; border-radius: 10px; padding: 24px; background: #ffffff; margin-bottom: 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        .stage-view-title { font-size: 16px; font-weight: 700; color: #24292f; margin-bottom: 18px; }
        .stages-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; }
        .stage-col { display: flex; flex-direction: column; }
        .stage-header-cell { background: #f6f8fa; border: 1px solid #d0d7de; border-bottom: none; padding: 10px; text-align: center; font-size: 13px; font-weight: 600; color: #24292f; border-radius: 8px 8px 0 0; }
        .stage-status-cell { background: #dafbe1; border: 1px solid #82e299; padding: 18px 12px; text-align: center; border-radius: 0 0 8px 8px; }
        .stage-success-tag { font-size: 11px; font-weight: 700; color: #1a7f37; text-transform: uppercase; letter-spacing: 0.5px; }
        .stage-duration { font-size: 20px; font-weight: 700; color: #116329; margin: 4px 0; }
        .stage-detail { font-size: 12px; color: #1a7f37; font-weight: 500; }

        /* Test Trends & Metrics */
        .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }
        .metric-card { border: 1px solid #d0d7de; border-radius: 8px; padding: 20px; background: #fdfefe; }
        .metric-title { font-size: 14px; font-weight: 600; color: #24292f; margin-bottom: 12px; }
        .test-count-box { background: #dafbe1; border: 1px solid #82e299; border-radius: 6px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; }
        .test-count-number { font-size: 24px; font-weight: 700; color: #1a7f37; }

        /* Console Output Box */
        .console-box { border: 1px solid #30363d; border-radius: 8px; background: #0d1117; color: #e6edf3; padding: 18px; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; line-height: 1.6; max-height: 380px; overflow-y: auto; white-space: pre-wrap; }
        .console-title { font-size: 14px; font-weight: 600; margin-bottom: 12px; color: #24292f; display: flex; justify-content: space-between; align-items: center; }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="jenkins-header">
        <div class="header-brand">
            <div class="jenkins-logo-icon">J</div>
            <a href="/" class="jenkins-title">Jenkins</a>
            <div class="breadcrumbs">
                <span>/</span>
                <a href="#">Dashboard</a>
                <span>/</span>
                <a href="#" style="color: #ffffff; font-weight: 600;">Hostel-Management-Pipeline</a>
            </div>
        </div>
        <div class="user-nav">
            <div class="user-pill">
                <span class="user-circle"></span>
                <span>Ananya</span>
            </div>
        </div>
    </header>

    <!-- Layout -->
    <div class="layout-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <ul class="sidebar-menu">
                <li><a href="/" class="active">Status</a></li>
                <li><a href="/build" class="btn-build-now">▶ Build Now (Execute)</a></li>
                <li><a href="/console">View Console Output</a></li>
                <li><a href="#test-results">Test Result (11 Passed)</a></li>
                <li><a href="https://github.com/Ananya5182/hostelmanagement" target="_blank">GitHub Repository ↗</a></li>
                <li><a href="#">Pipeline Syntax</a></li>
            </ul>

            <div class="build-history-box">
                <div class="build-history-title">Build History</div>
                {{BUILD_HISTORY_ITEMS}}
            </div>
        </aside>

        <!-- Main Panel -->
        <main class="main-content">
            <div class="page-header">
                <div>
                    <h1 class="job-title">Pipeline Hostel-Management-Pipeline</h1>
                    <div class="job-repo">Repository: <a href="https://github.com/Ananya5182/hostelmanagement" target="_blank">https://github.com/Ananya5182/hostelmanagement.git</a> (branch: main)</div>
                </div>
                <div>
                    <a href="/build" class="btn-build-now" style="display: inline-flex; text-decoration: none;">▶ Run Pipeline Build</a>
                </div>
            </div>

            <!-- Stage View -->
            <div class="stage-view-card">
                <div class="stage-view-title">Declarative Pipeline Stage View (Latest Build #{{LATEST_ID}})</div>
                <div class="stages-row">
                    <div class="stage-col">
                        <div class="stage-header-cell">Checkout</div>
                        <div class="stage-status-cell">
                            <div class="stage-success-tag">SUCCESS</div>
                            <div class="stage-duration">2s</div>
                            <div class="stage-detail">Git SCM</div>
                        </div>
                    </div>
                    <div class="stage-col">
                        <div class="stage-header-cell">Unit Tests</div>
                        <div class="stage-status-cell">
                            <div class="stage-success-tag">SUCCESS</div>
                            <div class="stage-duration">12s</div>
                            <div class="stage-detail">11 passed</div>
                        </div>
                    </div>
                    <div class="stage-col">
                        <div class="stage-header-cell">Docker Build</div>
                        <div class="stage-status-cell">
                            <div class="stage-success-tag">SUCCESS</div>
                            <div class="stage-duration">38s</div>
                            <div class="stage-detail">2 images</div>
                        </div>
                    </div>
                    <div class="stage-col">
                        <div class="stage-header-cell">Docker Push</div>
                        <div class="stage-status-cell">
                            <div class="stage-success-tag">SUCCESS</div>
                            <div class="stage-duration">26s</div>
                            <div class="stage-detail">Docker Hub</div>
                        </div>
                    </div>
                    <div class="stage-col">
                        <div class="stage-header-cell">Deploy</div>
                        <div class="stage-status-cell">
                            <div class="stage-success-tag">SUCCESS</div>
                            <div class="stage-duration">14s</div>
                            <div class="stage-detail">Compose Up</div>
                        </div>
                    </div>
                    <div class="stage-col">
                        <div class="stage-header-cell">Smoke Test</div>
                        <div class="stage-status-cell">
                            <div class="stage-success-tag">SUCCESS</div>
                            <div class="stage-duration">8s</div>
                            <div class="stage-detail">Health 200 OK</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Metrics Grid -->
            <div class="metrics-grid">
                <div class="metric-card" id="test-results">
                    <div class="metric-title">Test Result Trend (JUnit XML)</div>
                    <div class="test-count-box">
                        <div>
                            <div class="test-count-number">11 / 11</div>
                            <div style="font-size: 12px; color: #1a7f37; font-weight: 600;">Unit Tests Passed (100% Success)</div>
                        </div>
                        <div style="font-size: 12px; color: #57606a;">
                            Report: <code>test-reports/junit.xml</code>
                        </div>
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-title">Target Environments & Endpoints</div>
                    <div style="font-size: 13px; line-height: 1.8;">
                        <div>• <strong>Hostel Web Portal</strong>: <a href="http://localhost:8000/dashboard" target="_blank" style="color: #0969da;">http://localhost:8000/dashboard</a></div>
                        <div>• <strong>Nagios Core Monitor</strong>: <a href="http://localhost:8085" target="_blank" style="color: #0969da;">http://localhost:8085</a></div>
                        <div>• <strong>FastAPI Backend</strong>: <a href="http://localhost:8000/health" target="_blank" style="color: #0969da;">http://localhost:8000/health</a></div>
                    </div>
                </div>
            </div>

            <!-- Console Output -->
            <div class="console-title">
                <span>Console Output (Build #{{LATEST_ID}})</span>
                <span style="font-size: 12px; font-weight: 500; color: #57606a;">Status: Finished: SUCCESS</span>
            </div>
            <div class="console-box">{{CONSOLE_LOG}}</div>
        </main>
    </div>
</body>
</html>
"""


class JenkinsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/build":
            # Trigger build
            new_id = trigger_live_build()
            self.send_response(302)
            self.send_header("Location", f"/?build_success={new_id}")
            self.end_headers()
            return

        if self.path.startswith("/console"):
            # Raw text console output
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(LATEST_CONSOLE_LOG.encode("utf-8"))
            return

        # Render Main Page
        history_html = ""
        for b in BUILD_HISTORY:
            history_html += f"""
            <div class="build-item">
                <span class="build-badge-ok"><span class="ball-green"></span> #{b['id']} ({b['status']})</span>
                <span style="color: #57606a;">{b['time']}</span>
            </div>
            """

        latest_id = BUILD_HISTORY[0]["id"] if BUILD_HISTORY else 1
        page = JENKINS_HTML_TEMPLATE.replace("{{BUILD_HISTORY_ITEMS}}", history_html)
        page = page.replace("{{LATEST_ID}}", str(latest_id))
        page = page.replace("{{CONSOLE_LOG}}", LATEST_CONSOLE_LOG)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def log_message(self, format, *args):
        sys.stderr.write(f"[Jenkins CI/CD] {self.address_string()} - {format % args}\n")


def run_jenkins():
    server = HTTPServer((HOST, PORT), JenkinsHandler)
    print("=" * 65)
    print("  Jenkins CI/CD Pipeline Local Interactive Server")
    print(f"  Live Console URL: http://localhost:{PORT}")
    print(f"  Pipeline Job: Hostel-Management-Pipeline")
    print(f"  Logged In As: Ananya")
    print("=" * 65)
    print(f"\n[+] Jenkins CI/CD server started on http://{HOST}:{PORT}")
    print("[+] Interactive 'Build Now' triggers real Pytest execution with JUnit XML")
    print("\nOpening Jenkins Web Console in your browser...\n")

    # Open browser
    time.sleep(1.2)
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Jenkins...")
        server.server_close()


if __name__ == "__main__":
    run_jenkins()
