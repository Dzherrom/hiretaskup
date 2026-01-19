import os

path = r"c:\Users\skrea\Documents\Code\hiretaskup\core\templates\onboarding\checkout.html"

# 1. Insert HTML Fields
# Match the end of the website input block
match_str = r"""                                    placeholder="https://example.com"
                                    class="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow"
                                >
                            </div>
                        </div>
                    </div>"""

# New HTML block
new_html = r"""                                    placeholder="https://example.com"
                                    class="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow"
                                >
                            </div>
                        </div>
                    </div>

                    <!-- Extra Info -->
                    <div>
                         <label class="block text-sm font-semibold text-slate-700 mb-2">Type of Company</label>
                         <input type="text" id="company_type" name="company_type" placeholder="e.g. Real Estate, E-commerce..." class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">What are your main needs?</label>
                        <textarea id="client_needs" name="client_needs" rows="2" placeholder="Briefly describe what you need help with..." class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow"></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Tasks for the VA</label>
                        <textarea id="va_tasks" name="va_tasks" rows="3" placeholder="- Email Management\n- Scheduling\n- Data Entry" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white transition-all input-glow"></textarea>
                    </div>"""

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if match_str in content:
    content = content.replace(match_str, new_html)
else:
    print("HTML match failed")

# 2. Update JS formData
js_match = r"""            phone: phoneInput.value,
            website: document.getElementById('website').value
        };"""

js_replace = r"""            phone: phoneInput.value,
            website: document.getElementById('website').value,
            company_type: document.getElementById('company_type').value,
            client_needs: document.getElementById('client_needs').value,
            va_tasks: document.getElementById('va_tasks').value
        };"""

if js_match in content:
    content = content.replace(js_match, js_replace)
    # Write back
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("checkout.html updated successfully")
else:
    print("JS match failed")
