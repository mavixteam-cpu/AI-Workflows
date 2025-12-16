import re

# =======================================================
# 1. SETUP & INPUTS
# =======================================================
lead_name = input_data.get('Name', 'there').strip()
website_text = input_data.get('data', '') # 'data' from HTML to Text node

# Clean up the text (remove extra spaces/newlines for better analysis)
clean_text = " ".join(website_text.split())

# =======================================================
# 2. THE ANALYST (Industry Detection)
# =======================================================
# We define "fingerprints" for different industries to make the email specific.
industries = {
    "Real Estate": ["realtor", "property", "listings", "home buying", "tenants", "estate agent"],
    "E-commerce": ["shop now", "cart", "checkout", "shipping", "store", "products"],
    "Medical/Health": ["patient", "clinic", "care", "health", "treatment", "book appointment"],
    "B2B Services": ["consulting", "agency", "solutions", "strategy", "clients", "growth"]
}

detected_industry = "General Business"
industry_hook = "streamline your operations"

# Loop through our dictionary to find a match
for industry, keywords in industries.items():
    # Check if any of the keywords exist in their website text
    if any(keyword in clean_text.lower() for keyword in keywords):
        detected_industry = industry
        break

# =======================================================
# 3. THE RESEARCHER (Finding a specific quote)
# =======================================================
# This logic tries to find their "Mission Statement" or a "We help" sentence.
# It looks for sentences starting with "We help", "We provide", or "Our mission".

research_snippet = ""
sentences = re.split(r'[.!?]', clean_text) # Split text into sentences

for sentence in sentences:
    lower_s = sentence.lower().strip()
    if lower_s.startswith("we help") or lower_s.startswith("we provide") or "mission is" in lower_s:
        # Keep it reasonable length (under 150 chars) so the email isn't huge
        if len(sentence) < 150 and len(sentence) > 20:
            research_snippet = sentence.strip()
            break

# If we found a snippet, we quote it. If not, we use a fallback.
if research_snippet:
    research_proof = f"I was reading through your site and loved how you mentioned that '{research_snippet}'."
else:
    research_proof = f"I spent some time analyzing your website and was impressed by your clear focus in the {detected_industry} space."

# =======================================================
# 4. THE STRATEGIST (Dynamic Offer)
# =======================================================
# Custom pain points based on what we found
pain_points = {
    "Real Estate": "managing client inquiries and scheduling viewings 24/7",
    "E-commerce": "recovering abandoned carts and handling customer support tickets",
    "Medical/Health": "automating patient intake forms and appointment reminders",
    "B2B Services": "qualifying leads before they even reach your sales team",
    "General Business": "automating repetitive tasks to save your team hours every week"
}

specific_problem = pain_points.get(detected_industry, pain_points["General Business"])

# =======================================================
# 5. ASSEMBLE THE EMAIL
# =======================================================
email_body = f"""
Hi {lead_name},

{research_proof}

Working with other companies in {detected_industry}, we've noticed that {specific_problem} is often a massive time-sink.

At Mavix, we build AI agents that handle exactly that. We don't just offer "tools" — we build systems that do the work for you.

Are you open to a 10-minute demo to see how an AI agent could run your {specific_problem} on autopilot?

Best,

Mavix Team
"""

# =======================================================
# 6. OUTPUT RESULTS
# =======================================================
output_data = {
    "industry_detected": detected_industry,
    "research_snippet": research_snippet,
    "generated_email": email_body,
    "lead_score": 80 if research_snippet else 40
}