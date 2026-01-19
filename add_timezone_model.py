import os

path = r"c:\Users\skrea\Documents\Code\hiretaskup\core\models.py"

old_code = r"""    company_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of company/industry")
    va_tasks = models.TextField(blank=True, null=True, help_text="Tasks you want the VA to perform")
    
    def __str__(self):"""

new_code = r"""    company_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of company/industry")
    va_tasks = models.TextField(blank=True, null=True, help_text="Tasks you want the VA to perform")
    time_zone = models.CharField(max_length=100, blank=True, null=True, help_text="Preferred Time Zone")
    
    def __str__(self):"""

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("models.py updated")
else:
    print("models.py match failed")
