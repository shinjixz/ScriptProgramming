# Week 11 – Project Planning & Design: Building an Enhanced Task Manager

Agentic Document Automation System — โปรแกรม Python ที่อ่านค่าจากไฟล์ config (JSON) แล้วทำงานกับเอกสาร Word และ PDF ให้อัตโนมัติ พร้อมบันทึก audit log ทุกขั้นตอน

📺 คลิปการสอน: https://drive.google.com/file/d/1NnSoPx1C3hzNyUBZ_pJvpC1OqFJ2I6rQ/view?usp=sharing

---

## ความสามารถของระบบ

| # | Task | Input | Output |
|---|------|-------|--------|
| 1 | สร้างรายงาน Word จาก template (แทนค่า placeholder + ใส่ตาราง) | `templates/report_template.docx` | `documents/generated_report.docx` |
| 2 | ใส่ลายน้ำ "CONFIDENTIAL" ลงใน PDF | `documents/source_document.pdf` | `documents/watermarked_document.pdf` |
| 3 | รวมไฟล์ PDF หลายไฟล์เป็นไฟล์เดียว | `documents/dummy_doc1.pdf`, `documents/dummy_doc2.pdf` | `documents/merged_docs.pdf` |
| 4 | ดึงข้อความจากไฟล์ Word | `documents/generated_report.docx` | `documents/extracted_word_text.txt` |
| 5 | ดึงข้อความจากไฟล์ PDF | `documents/source_document.pdf` | `documents/extracted_pdf_text.txt` |

ทุกครั้งที่รัน ระบบจะสร้าง audit log ไว้ที่ `documents/reports/audit_report_<วันที่_เวลา>.json`

## โครงสร้างโปรเจกต์

```
.
├── main.py                         # จุดเริ่มรันโปรแกรม
├── requirements.txt
├── configs/
│   └── document_automation_config.json   # กำหนดข้อมูลและรายการ task
├── src/
│   ├── config_parser.py            # โหลดและตรวจสอบ config
│   ├── document_agent.py           # ตัว agent ที่ไล่ทำแต่ละ task + audit log
│   ├── word_tasks.py               # งานเกี่ยวกับ Word (.docx)
│   ├── pdf_tasks.py                # งานเกี่ยวกับ PDF
│   └── utils.py                    # logging และฟังก์ชันช่วย
├── templates/
│   └── report_template.docx
├── documents/                      # ไฟล์ input และ output
└── screenshots/                    # ภาพ screenshot ผลลัพธ์
```

## วิธีติดตั้งและรัน

```bash
# (แนะนำ) สร้าง virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# ติดตั้ง library
pip install -r requirements.txt

# รันโปรแกรม
python main.py
```

เมื่อรันเสร็จ ไฟล์ผลลัพธ์จะอยู่ในโฟลเดอร์ `documents/`

## การปรับแต่ง

แก้ไขค่าได้ที่ `configs/document_automation_config.json` เช่น
- `global_data` — ข้อมูลที่ใช้ร่วมกันทุก task (วันที่, ชื่อผู้จัดทำ, ชื่อบริษัท)
- `data` / `table_data` ของ task สร้างรายงาน — ข้อความและตารางในรายงาน
- `watermark_text`, `font_size`, `color` (RGBA 0–1), `angle` — รูปแบบลายน้ำ

ใน template ใช้ placeholder รูปแบบ `{{KEY}}` และใช้ `{{TABLE_PLACEHOLDER}}` เพื่อกำหนดตำแหน่งที่จะแทรกตาราง

## สิ่งที่ปรับปรุงจากโค้ดตั้งต้น

- แก้การแทนค่า placeholder ให้ลบวงเล็บ `{{ }}` ออกด้วย (เดิมผลลัพธ์จะเป็น `{{Monthly Performance Summary}}`) และรองรับกรณี placeholder ถูกแยกอยู่หลาย run
- แก้ให้ตารางถูกแทรกตรงตำแหน่ง `{{TABLE_PLACEHOLDER}}` (เดิมตารางไปต่อท้ายเอกสารหลังส่วน CONCLUSION)
- เพิ่มรายชื่อ library ใน `requirements.txt` และเพิ่ม `.gitignore`

## ผลลัพธ์ (Screenshots)

### merged_docs.pdf
![merged_docs.pdf](screenshots/merged_docs.png)

### generated_report.docx
![generated_report.docx](screenshots/generated_report.png)

### watermarked_document.pdf
![watermarked_document.pdf](screenshots/watermarked_document.png)
