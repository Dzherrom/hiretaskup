
import re

file_path = r'c:\Users\skrea\Documents\Code\hiretaskup\core\templates\plans\plans.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Markers
marker_part = '<!-- Part-Time Plan -->'
marker_full = '<!-- Full-Time Plan (Highlighted) -->'
marker_team = '<!-- Team Plan -->'
    
# Find indices
idx_part = content.find(marker_part)
idx_full = content.find(marker_full)
idx_team = content.find(marker_team)

if idx_part == -1 or idx_full == -1 or idx_team == -1:
    print("Could not find markers.")
    exit(1)

# Blocks
# Part time block ends where Full Time starts
# Full time block ends where Team starts
# Team block ends where the grid closes.
# We can find the closing divs by searching for the "Satisfaction Guarantee" section start or just identifying the end of the grid logic.

# Actually, the snippet shows:
# </div>
# </div>
# </section>
# <!-- Satisfaction Guarantee -->

# So we can search for <!-- Satisfaction Guarantee --> to find the end of the section
marker_satisfaction = '<!-- Satisfaction Guarantee -->'
idx_satisfaction = content.find(marker_satisfaction)

# The content between idx_team and idx_satisfaction contains the team block + closing grid div + closing container div + closing section tag.
# We need to be careful.
# The grid ends at `</div>` before `</div>` before `</section>`.

# Let's extract blocks by lines or substring more carefully.

# Part Time Block
# Everything from idx_part to idx_full (exclusive)
# But we need to make sure we strip trailing whitespace/newlines effectively to keep formatting clean
part_time_block = content[idx_part:idx_full].rstrip()

# Full Time Block
# Everything from idx_full to idx_team (exclusive)
full_time_block = content[idx_full:idx_team].rstrip()

# Team Block
# This is tricky because we don't have a clear next marker for just the CARD.
# The Team Plan div ends before the closing </div> of the grid.
# The container structure is:
# <div class="grid ...">
#    <div class="bg-white ..."> (Part) </div>
#    <div class="bg-slate-900 ..."> (Full) </div>
#    <div class="bg-white ..."> (Team) </div>
# </div>
# </div>
# </section>

# So we can look for the last </div> before the section close? No, that's brittle.
# Let's count divs? No.
# Let's look for the </div> that matches the indentation of the team block?
# The team block starts with `                <!-- Team Plan -->` (indentation)
# `                <div class="bg-white ...`
# So the closing div should be `                </div>`
# Let's assume the blocks are well formatted.

# Let's try to grab up to the marker_satisfaction and then strip the closing tags from the end?
# The content after Team Plan is the card content + closing grid divs.
remaining = content[idx_team:idx_satisfaction]
# Find the LAST occurrence of `</div>` and back up...
# Actually, simply: Since we are reconstructing the sequence inside the grid, we just need the 3 inner divs.
# The grid wrapper is OUTSIDE these blocks.
# Wait, my previous script tried to replace the whole sequence.
# Let's define the end of Team Block as the position before the string `            </div>\n        </div>\n    </section>` or similar.
# Or simpler: The pattern `            </div>\n        </div>\n    </section>` is at the end of the section.

# Let's use regex again but simpler.
# Start of grid: <div class="grid ... items-start">
# End of grid: </div> ...
grid_start_marker = '<div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto items-start">'
idx_grid_start = content.find(grid_start_marker)

if idx_grid_start == -1:
    print("Grid start not found")
    exit(1)

# The content interesting to us starts after grid_start_marker
content_after_grid = content[idx_grid_start + len(grid_start_marker):]

# Find the end of the section
end_marker = '</section>'
idx_section_end = content_after_grid.find(end_marker)

# Grid content (including the closing divs for grid and container)
grid_content_raw = content_after_grid[:idx_section_end]

# We need to strip the last two </div>s from `grid_content_raw` to get just the cards?
# The structure is:
# \n...cards...\n            </div>\n        </div>\n    
# It seems there are 2 closing divs.

# Let's parse the cards by splitting.
# We can split by the comments!
# This is much safer.

parts = re.split(r'(<!-- .*? Plan.* -->)', grid_content_raw)
# parts[0] = whitespace
# parts[1] = <!-- Part-Time Plan -->
# parts[2] = content of part time
# parts[3] = <!-- Full-Time Plan (Highlighted) -->
# parts[4] = content of full time
# parts[5] = <!-- Team Plan -->
# parts[6] = content of team + closing divs

# Clean up part 6
# Remove the trailing </div>s.
# We can find the last `</div>` and the one before it?
# Or we just assume the formatting provided in previous tool output.
# The closing divs are `            </div>\n        </div>\n    `
# Let's regex replace the closing divs from part 6 temporarily, then add them back at the end.

# Identify the footer of the grid
grid_footer = re.search(r'(\s*</div>\s*</div>\s*)$', parts[6], re.DOTALL)
if not grid_footer:
    print("Could not find grid footer")
    # Backup: maybe the split failed or structure is diff.
    # Let's try to trust the splitting by comment.
    pass

footer_str = grid_footer.group(1) if grid_footer else ""
team_content_clean = parts[6].replace(footer_str, "")

# Now we have:
# Card 1 = parts[1] + parts[2]
# Card 2 = parts[3] + parts[4]
# Card 3 = parts[5] + team_content_clean

card_part_time = parts[1] + parts[2]
card_full_time_raw = parts[3] + parts[4]
card_team = parts[5] + team_content_clean

# Modifying Full Time
card_full_time = card_full_time_raw.replace('$1,199', '$1,499').replace('amount=119900', 'amount=149900')

# Modifying Team Title if needed? User said "La tarjeta de la izquierda tenga una opcion de contactar a ventas".
# Card Team currently has "Enterprise Team" and "Contact Sales".
# So Card Team is the one we want on the left.
# Card Part Time is the one we want on the right.

new_grid_inner = "\n                " + card_team.strip() + "\n\n                " + card_full_time.strip() + "\n\n                " + card_part_time.strip() + "\n\n" + footer_str

# Reconstruct file
new_full_content = content[:idx_grid_start + len(grid_start_marker)] + new_grid_inner + content[idx_grid_start + len(grid_start_marker) + len(grid_content_raw) + len(end_marker):] 
# Wait, len calculation above is tricky.
# Simplified:
prefix = content[:idx_grid_start + len(grid_start_marker)]
suffix = content[idx_grid_start + len(grid_start_marker) + len(grid_content_raw):] # grid_content_raw went up to `</section>` exclusive

new_full_content = prefix + new_grid_inner + suffix

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_full_content)

print(f"Success. Length difference: {len(new_full_content) - len(content)}")
