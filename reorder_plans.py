
import re

file_path = r'c:\Users\skrea\Documents\Code\hiretaskup\core\templates\plans\plans.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Regex to extract the three cards
# Relies on the comments I added/saw in the file
# 1. Part-Time
part_time_pattern = r'(<!-- Part-Time Plan -->.*?)(?=<!-- Full-Time Plan \(Highlighted\) -->)'
# 2. Full-Time
full_time_pattern = r'(<!-- Full-Time Plan \(Highlighted\) -->.*?)(?=<!-- Team Plan -->)'
# 3. Team
team_pattern = r'(<!-- Team Plan -->.*?)(?=\s*</div>\s*</div>\s*</section>)'

part_time_match = re.search(part_time_pattern, content, re.DOTALL)
full_time_match = re.search(full_time_pattern, content, re.DOTALL)
team_match = re.search(team_pattern, content, re.DOTALL)

if not (part_time_match and full_time_match and team_match):
    print("Could not find all plan sections. Aborting.")
    exit(1)

part_time_block = part_time_match.group(1)
full_time_block = full_time_match.group(1)
team_block = team_match.group(1)

# Update Full Time Price
# $1,199 -> $1,499
# amount=119900 -> amount=149900
full_time_block = full_time_block.replace('$1,199', '$1,499')
full_time_block = full_time_block.replace('amount=119900', 'amount=149900')

# Construct new content by replacing the original sequence with the new sequence
# Structure in file is: [Part Time] [Full Time] [Team]
# New Structure: [Team] [Full Time] [Part Time]

original_sequence_pattern = r'<!-- Part-Time Plan -->.*?<!-- Team Plan -->.*?</div>\s*(?=\s*</div>\s*</section>)'
# We need to capture from start of Part time to end of Team plan div. The team plan regex stopped before the closing divs.
# Let's just reconstruct the whole block using the start and end of the matches found.

start_index = part_time_match.start()
end_index = team_match.end()

new_sequence = team_block + "\n\n                " + full_time_block + "\n\n                " + part_time_block

new_content = content[:start_index] + new_sequence + content[end_index:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully rearranged plans.")
