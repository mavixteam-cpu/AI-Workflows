import json
import random
import re

# =======================================================
# 1. GET INPUTS (Matches your n8n Input Data)
# =======================================================
# We use .get() with defaults so the script never crashes even if data is missing
company_name = input_data.get('Company', 'your company').strip()
niche = input_data.get('Niche', 'Business').strip()
context_text = input_data.get('data', '') # This is the website text

# Clean up context text (remove weird spacing)
clean_context = " ".join(context_text.split())

# =======================================================
# 2. LOGIC: THE SUBJECT LINE (Randomized)
# =======================================================
subject_options = [
    f"Quick thought re: {company_name}",
    f"Question about your {niche} workflow",
    f"Automation idea for {company_name}"
]
selected_subject = random.choice(subject_options)

# =======================================================
# 3. LOGIC: THE COMPLIMENT (The "Smart" Part)
# =======================================================
# Since we aren't using an LLM, we use Python to hunt for specific clues.

compliment = ""

# Strategy A: Look for location (e.g., "based in London")
# We scan for the phrase "based in" followed by a word starting with a capital letter
location_match = re.search(r"based in ([A-Z][a-z]+)", clean_context)

# Strategy B: Look for specific service keywords based on Niche
service_keywords = {
    "Real Estate": ["property management", "residential", "commercial", "listings"],
    "Dental": ["orthodontics", "implants", "family dentistry", "cosmetic"],
    "Marketing": ["SEO", "paid media", "content creation", "branding"]
}

found_service = None
if niche in service_keywords:
    for service in service_keywords[niche]:
        if service in clean_context.lower():
            found_service = service
            break

# DECISION TIME: Which compliment do we use?
if location_match:
    city = location_match.group(1)
    compliment = f"We saw you have operations based in {city} and wanted to reach out."
elif found_service:
    compliment = f"We were looking at your site and noticed your focus on {found_service}."
elif len(clean_context) > 50:
    # If we have text but no specific match, we reference the site generally
    compliment = f"We’ve been following your growth in the {niche} space and like what we see."
else:
    # Fallback if website data is empty
    compliment = f"We’ve been following your growth in the {niche} space."

# =======================================================
# 4. LOGIC: THE PAIN POINT (Dynamic based on Niche)
# =======================================================
# This maps the "Niche" from your sheet to a specific problem they have.
pain_point_map = {
    "Real Estate": "chasing documents and scheduling viewings",
    "Dental": "managing patient bookings and follow-ups",
    "Marketing": "generating reports and qualifying leads",
    "Law": "processing client intake forms",
    "General": "repetitive manual data entry"
}

# Get the specific pain point, or default to 'General' if niche isn't found
selected_pain_point = pain_point_map.get(niche, pain_point_map["General"])

# =======================================================
# 5. ASSEMBLE THE EMAIL (HTML Format)
# =======================================================
email_body = f"""<p>Hi there,</p>

<p>{compliment}</p>

<p>That said, managing that kind of volume usually means the team gets buried in <b>{selected_pain_point}</b>.</p>

<p>At Mavix, we build custom AI agents to handle exactly that.</p>

<p>We actually have a <b>live demo</b> ready that shows how this would work for {company_name}.</p>

<p>If you're open to it, we'd love to send over the demo link.</p>

<p>Best,<br>
The Mavix Team<br><br>
<span style='font-size:12px; color: #666;'>Mavix AI Engineering | <a href='https://mavix-ks.com/'>Website</a> | <a href='https://www.instagram.com/mavix.ks/'>Instagram</a></span></p>
"""

# =======================================================
# 6. OUTPUT (Strict JSON)
# =======================================================
output_data = {
    "subject": selected_subject,
    "body": email_body,
    "debug_compliment_type": "Location" if location_match else ("Service" if found_service else "Fallback")
}