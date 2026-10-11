import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_parser import ConfigParser
from document_agent import DocumentAgent
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

def check_required_files(config, base_dir):
    # ตรวจสอบไฟล์ Template
    if not os.path.exists(os.path.join(base_dir, config['tasks'][0]['template_path'])): return False
    # ตรวจสอบไฟล์ PDF ต้นฉบับ
    if not os.path.exists(os.path.join(base_dir, config['tasks'][1]['input_pdf'])): return False
    # ตรวจสอบไฟล์ PDF สำหรับ Merge
    for p in config['tasks'][2]['input_pdfs']:
        if not os.path.exists(os.path.join(base_dir, p)): return False
    return True

def main():
    base_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(base_dir, 'configs', 'document_automation_config.json')
    
    ensure_directory_exists(os.path.join(base_dir, 'documents'))
    ensure_directory_exists(os.path.join(base_dir, 'templates'))
    
    config_parser = ConfigParser(config_file_path)
    config = config_parser.load_config()
    
    # แปลง path ใน config ให้เป็น Absolute path
    for key, value in config['output_files'].items():
        config['output_files'][key] = os.path.join(base_dir, value)
    for task in config['tasks']:
        for k in ['template_path', 'input_pdf', 'output_pdf', 'input_docx', 'output_text_file']:
            if k in task: task[k] = os.path.join(base_dir, task[k])
        if 'input_pdfs' in task: task['input_pdfs'] = [os.path.join(base_dir, p) for p in task['input_pdfs']]

    if not check_required_files(config, base_dir):
        logger.critical("Missing required input files! Please check Step 4.")
        return

    agent = DocumentAgent(config)
    agent.run()
    logger.info("Document automation process completed.")

if __name__ == "__main__":
    main()