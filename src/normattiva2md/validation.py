import re
import datetime
import json
from .constants import AKN_NAMESPACE

class MarkdownValidator:
    """
    Validates Markdown generated from Normattiva XML.
    """

    REQUIRED_METADATA = ["url", "dataGU", "codiceRedaz", "dataVigenza"]

    def validate(self, markdown_text):
        markdown_text = markdown_text.lstrip()
        errors = []
        checks = []

        # 1. Front Matter Check
        fm_check = self._check_front_matter(markdown_text)
        checks.append(fm_check)
        if fm_check["status"] != "PASS":
            errors.append({"type": "FRONT_MATTER", "message": fm_check["message"]})

        # 2. Header Structure Check
        if fm_check["status"] == "PASS":
            hh_check = self._check_header_structure(markdown_text)
            checks.append(hh_check)
            if hh_check["status"] != "PASS":
                errors.append({"type": "HEADER_STRUCTURE", "message": hh_check["message"]})
        else:
            checks.append({"check_name": "Header Structure", "status": "FAIL", "message": "Skipped due to missing front matter"})

        status = "PASS"
        if any(c["status"] == "FAIL" for c in checks):
            status = "FAIL"
        elif any(c["status"] == "WARNING" for c in checks):
            status = "WARNING"

        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "status": status,
            "checks": checks,
            "errors": errors
        }

    def _check_front_matter(self, text):
        if not text.startswith("---"):
            return {"check_name": "Front Matter", "status": "FAIL", "message": "Missing front matter start delimiter (---)"}
        
        parts = text.split("---", 2)
        if len(parts) < 3:
            return {"check_name": "Front Matter", "status": "FAIL", "message": "Missing front matter end delimiter (---)"}
        
        fm_content = parts[1]
        metadata = {}
        for line in fm_content.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        missing = [key for key in self.REQUIRED_METADATA if key not in metadata]
        if missing:
            return {
                "check_name": "Front Matter", 
                "status": "FAIL", 
                "message": f"Missing required metadata fields: {', '.join(missing)}"
            }

        return {"check_name": "Front Matter", "status": "PASS", "message": "Front matter is present and valid"}

    def _check_header_structure(self, text):
        headers = re.findall(r"^(#+)\s", text, re.MULTILINE)
        if not headers:
            return {"check_name": "Header Structure", "status": "PASS", "message": "No headers found"}

        # Check 1: Only H1, H2, H3, H4 allowed
        for h in headers:
            if len(h) > 4:
                return {
                    "check_name": "Header Structure", 
                    "status": "FAIL", 
                    "message": f"Invalid header level: H{len(h)}. Only H1-H4 are allowed."
                }
        
        # Check 2: Exactly one H1
        h1_count = len([h for h in headers if len(h) == 1])
        if h1_count == 0:
             return {
                "check_name": "Header Structure", 
                "status": "FAIL", 
                "message": "Missing document title (H1)."
            }
        if h1_count > 1:
             return {
                "check_name": "Header Structure", 
                "status": "FAIL", 
                "message": f"Multiple document titles (H1) found: {h1_count}."
            }

        return {"check_name": "Header Structure", "status": "PASS", "message": "Header structure is valid"}


class StructureComparer:
    """
    Compares the structure of the source XML with the generated Markdown.
    """
    
    def compare(self, xml_root, markdown_text):
        # XML counting
        # Try finding with namespace
        articles_xml = xml_root.findall(".//akn:article", AKN_NAMESPACE)
        if not articles_xml:
             # Try without namespace (test data or older XML)
             articles_xml = xml_root.findall(".//article")
        
        if not articles_xml:
             # Try 'art' tag (NIR or test data)
             articles_xml = xml_root.findall(".//akn:art", AKN_NAMESPACE)
             if not articles_xml:
                 articles_xml = xml_root.findall(".//art")
        
        xml_count = len(articles_xml)

        # Markdown counting
        # Count lines starting with "#### Art."
        md_count = len(re.findall(r"^#### Art.", markdown_text, re.MULTILINE))

        if xml_count == md_count:
            return {
                "check_name": "Structure Comparison",
                "status": "PASS",
                "message": f"Article count matches: {xml_count}",
                "details": {"xml_count": xml_count, "md_count": md_count}
            }
        else:
            return {
                "check_name": "Structure Comparison",
                "status": "FAIL",
                "message": f"Article count mismatch: XML={xml_count}, MD={md_count}",
                "details": {"xml_count": xml_count, "md_count": md_count}
            }


class ReportGenerator:
    """
    Generates summary reports for conversion quality.
    """
    
    def generate_json(self, v_report, c_report, source_path):
        """
        Generate a comprehensive JSON report.
        """
        report = {
            "source": source_path,
            "timestamp": datetime.datetime.now().isoformat(),
            "overall_status": "PASS" if v_report["status"] == "PASS" and c_report["status"] == "PASS" else "FAIL",
            "markdown_validation": v_report,
            "structure_comparison": c_report
        }
        return json.dumps(report, indent=2)