import os
from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel


def write_report(filename, html):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(project_root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)  # Create if not exists
    
    file_path = os.path.join(reports_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

class WriteReportsArgsSchema(BaseModel):
    filename: str
    html: str

write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="write an HTML to disk, use this tool whenever someone asks for a report.",
    func=write_report,
    DescribeTablesArgsSchema=WriteReportsArgsSchema
)