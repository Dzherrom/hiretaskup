import os

path = r"c:\Users\skrea\Documents\Code\hiretaskup\core\templates\onboarding\checkout.html"

# 1. Insert HTML for Time Zone
# Let's insert it after Company Type and before Client Needs
match_html = r"""                    <!-- Extra Info -->
                    <div>
                         <label class="block text-sm font-semibold text-slate-700 mb-2">Type of Company</label>
                         <input type="text" id="company_type" name="company_type" placeholder="e.g. Real Estate, E-commerce..." class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow">
                    </div>"""

new_html = r"""                    <!-- Extra Info -->
                    <div>
                         <label class="block text-sm font-semibold text-slate-700 mb-2">Type of Company</label>
                         <input type="text" id="company_type" name="company_type" placeholder="e.g. Real Estate, E-commerce..." class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow">
                    </div>
                    <div>
                         <label class="block text-sm font-semibold text-slate-700 mb-2">Preferred Time Zone</label>
                         <input type="text" id="time_zone" name="time_zone" placeholder="e.g. EST (New York), GMT (London), or UTC-5" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow">
                    </div>"""

# 2. Update JS formData
match_js = r"""            company_type: document.getElementById('company_type').value,
            client_needs: document.getElementById('client_needs').value,"""

new_js = r"""            company_type: document.getElementById('company_type').value,
            time_zone: document.getElementById('time_zone').value,
            client_needs: document.getElementById('client_needs').value,"""


with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if match_html in content:
    content = content.replace(match_html, new_html)
else:
    print("HTML match failed")

if match_js in content:
    content = content.replace(match_js, new_js)
else:
    print("JS match failed")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("checkout.html updated")
