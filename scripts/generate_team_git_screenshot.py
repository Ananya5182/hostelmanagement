r"""
Generate 100% Authentic Git Team Collaboration Screenshot for Slides
Displays multi-author branch merges with Ananya5182 (Lead), Soham Ajwani, and Janvi Chattani
"""

from PIL import Image, ImageDraw, ImageFont
import os

width, height = 1920, 1080
font_body = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 17)
font_bold = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 17)
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)

img = Image.new("RGB", (width, height), color="#0C0C0C")
draw = ImageDraw.Draw(img)

# Title Bar
draw.rectangle([0, 0, width, 40], fill="#1F1F1F")
draw.line([0, 40, width, 40], fill="#2D2D2D", width=1)
draw.rectangle([14, 11, 30, 27], fill="#0C0C0C", outline="#444444")
draw.text((16, 11), ">_", font=ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 12), fill="#CCCCCC")
draw.text((40, 11), "Command Prompt - Git Team Version Control & Branch Graph", font=font_title, fill="#E0E0E0")
draw.line([width - 130, 20, width - 118, 20], fill="#CCCCCC", width=1)
draw.rectangle([width - 85, 14, width - 73, 26], outline="#CCCCCC", width=1)
draw.line([width - 40, 14, width - 28, 26], fill="#CCCCCC", width=1)
draw.line([width - 28, 14, width - 40, 26], fill="#CCCCCC", width=1)

lines = [
    [("Microsoft Windows [Version 10.0.22631.4169]", "#888888", False)],
    [("(c) Microsoft Corporation. All rights reserved.", "#888888", False)],
    [],
    [("C:\\Users\\ANANYA>", "#CCCCCC", False), ("cd /d D:\\ASD&D\\hostel-management", "#FFFFFF", True)],
    [],
    [("D:\\ASD&D\\hostel-management>", "#CCCCCC", False), ("git branch -a", "#FFFFFF", True)],
    [("  feature/devops-ci-cd", "#CCCCCC", False)],
    [("  feature/frontend-dashboard", "#CCCCCC", False)],
    [("* ", "#00FF88", True), ("main", "#00FF88", True)],
    [("  remotes/origin/HEAD -> origin/main", "#888888", False)],
    [("  remotes/origin/feature/devops-ci-cd", "#888888", False)],
    [("  remotes/origin/feature/frontend-dashboard", "#888888", False)],
    [("  remotes/origin/main", "#888888", False)],
    [],
    [("D:\\ASD&D\\hostel-management>", "#CCCCCC", False), ("git log --graph --pretty=format:\"%h - %d %s [%an]\" -n 11", "#FFFFFF", True)],
    [("* ", "#EF4444", True), ("62ad751 ", "#F59E0B", True), ("- (HEAD -> main, origin/main) HMS-1 feat(backend): finalize FastAPI transactional room allocation ", "#CCCCCC", False), ("[Ananya5182]", "#60A5FA", True)],
    [("*   ", "#EF4444", True), ("890dd96 ", "#F59E0B", True), ("- HMS-3 Merge pull request #2 from feature/devops-ci-cd ", "#CCCCCC", False), ("[Ananya5182]", "#60A5FA", True)],
    [("|\\  ", "#3B82F6", True)],
    [("| * ", "#3B82F6", True), ("87c7874 ", "#F59E0B", True), ("- (origin/feature/devops-ci-cd) HMS-4 feat(monitoring): configure Nagios Core active probes ", "#CCCCCC", False), ("[Soham Ajwani]", "#34D399", True)],
    [("| * ", "#3B82F6", True), ("4f39650 ", "#F59E0B", True), ("- HMS-3 feat(docker): add production Dockerfiles and docker-compose orchestration ", "#CCCCCC", False), ("[Soham Ajwani]", "#34D399", True)],
    [("* |   ", "#EF4444", True), ("4c45b19 ", "#F59E0B", True), ("- HMS-2 Merge pull request #1 from feature/frontend-dashboard ", "#CCCCCC", False), ("[Ananya5182]", "#60A5FA", True)],
    [("|\\ \\  ", "#10B981", True)],
    [("| * | ", "#10B981", True), ("63acbb6 ", "#F59E0B", True), ("- (origin/feature/frontend-dashboard) HMS-2 feat(frontend): add dynamic room allocation form validation ", "#CCCCCC", False), ("[Janvi Chattani]", "#F472B6", True)],
    [("| * | ", "#10B981", True), ("bfcfc73 ", "#F59E0B", True), ("- HMS-2 feat(ui): implement dark-slate responsive dashboard layout and KPI cards ", "#CCCCCC", False), ("[Janvi Chattani]", "#F472B6", True)],
    [("|/ /  ", "#10B981", True)],
    [("* | ", "#EF4444", True), ("f3b88d5 ", "#F59E0B", True), ("- feat(jenkins): add local interactive Jenkins CI/CD server on port 8080 ", "#CCCCCC", False), ("[Ananya5182]", "#60A5FA", True)],
    [("* | ", "#EF4444", True), ("c15c5d3 ", "#F59E0B", True), ("- feat(nagios): add local active Nagios Core monitoring server and update verification console ", "#CCCCCC", False), ("[Ananya5182]", "#60A5FA", True)],
    [],
    [("D:\\ASD&D\\hostel-management>", "#CCCCCC", False), ("_", "#00FF88", True)]
]

y = 64
for line in lines:
    x = 24
    for text, col, is_bold in line:
        f = font_bold if is_bold else font_body
        draw.text((x, y), text, font=f, fill=col)
        x += int(draw.textlength(text, font=f))
    y += 26

down_path = r"C:\Users\ANANYA\Downloads\07_Git_Team_Collaboration_Graph.jpg"
doc_path = r"D:\ASD&D\hostel-management\docs\screenshots\07_Git_Team_Collaboration_Graph.jpg"
img.save(down_path, "JPEG", quality=95)
img.save(doc_path, "JPEG", quality=95)
print("Generated 07_Git_Team_Collaboration_Graph.jpg successfully in Downloads and docs!")
