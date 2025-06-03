import json
import openai
import csv

# Set your OpenAI API key
openai.api_key = "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"  # Replace with your actual key

# Set the path to your CSV file
csv_file = "AI_Uses_Risks_Mitigations.csv"

# Use a set to avoid repetitions
ai_uses_keywords = set()
ai_risks_keywords = set()
ai_mitigations_keywords = set()

# Read and parse the CSV
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tech = row['Technology'].strip()
        use = row['Use'].strip()
        risks = row['Risks'].strip()
        mitigations = row['Possible Mitigations'].strip()
        if tech and use:
            ai_uses_keywords.add(f"{tech} {use}")
            ai_risks_keywords.add(f"{tech} {use} {risks}")
        if risks and mitigations:
            ai_mitigations_keywords.add(f"{risks} {mitigations}")

# Convert set to sorted list for readability
sorted_ai_uses_keywords = sorted(ai_uses_keywords)
sorted_ai_risks_keywords = sorted(ai_risks_keywords)
sorted_ai_mitigations_keywords = sorted(ai_mitigations_keywords)

# Load the JSON file
with open("Clean_SouthSudan_problems_20250504_150058.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Build a formatted string with all problems
problems_str = ""
for i, item in enumerate(data, start=1):
    problem = item.get("problem", "N/A")
    description = item.get("description", "N/A")
    link = item.get("link", "N/A")
    problems_str += f"{i}. Problem: {problem}\n   Description: {description}\n   Source: {link}\n\n"

# Prompt 1: Research assistant prompt
prompt1 = f"""
You are a research assistant specialized in geopolitical conflict analysis.
Based on the following information about a past conflict, research the **specific post-war consequences** it caused. Focus on factual findings from trusted, verifiable sources.

Conflict_type: civil war,
Timeline: 2013,
Regions: [Juba, South Sudan, Bor, Uganda, Equatoria],
Actors: [Dinka, SPLA, Nuer, Shilluk, SPLM],
Issues:
{problems_str}

Focus your research on the **post-conflict consequences** that were directly caused or worsened by this war, including:
- Humanitarian issues (displacement, health, poverty)
- Infrastructural damage (roads, hospitals, schools)
- Cultural impact (disrupted traditions, community divisions)
- Logistical and operational challenges (aid delivery, mobility)
- Political instability (governance, peace processes)

Rules:
- Only use reliable sources: UN, ICRC, Human Rights Watch, Amnesty International, Al Jazeera, Reuters, BBC, SIPRI, academic publications.
- Return only **factual bullet points** with dates or figures if available.
- Keep each point brief and avoid speculation.
- Do not copy directly from Wikipedia; use it only for context.
"""

# === Send Prompt 1 ===
response1 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt1}],
    temperature=0.3
)
output_prompt1 = response1.choices[0].message.content

# Prompt 2: Validation prompt
prompt2 = f"""
You are a senior geopolitical analyst tasked with **validating the factual accuracy** of a post-conflict report.

Below is a summary of post-war consequences related to:

Conflict_type: civil war,
Timeline: 2013,
Regions: [Juba, South Sudan, Bor, Uganda, Equatoria],
Actors: [Dinka, SPLA, Nuer, Shilluk, SPLM],

Your task is to:

* Identify any **statements that appear vague, speculative, or potentially hallucinated**.
* Cross-check the facts using only **reliable sources**: UN, ICRC, Amnesty International, Human Rights Watch, Al Jazeera, BBC, Reuters, SIPRI, or peer-reviewed academic sources.
* Remove or correct any incorrect, biased, or unverifiable information.
* Keep only **verifiable, well-supported bullet points and related to the Conflict_type and Regions**.
* If a statement cannot be verified, remove it entirely.

Original Findings:

{output_prompt1}

Return only the **cleaned and verified bullet points**, in the same format.
Do not add any extra text.
Do not justify your changes.
"""

# === Send Prompt 2 ===
response2 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt2}],
    temperature=0.3
)
output_prompt2 = response2.choices[0].message.content

# Prompt 3: Extract core post-conflict problems
prompt3 = f""" 
You are a humanitarian impact analyst.

Below is a verified summary of post-conflict consequences.

Your task is to extract and list the **key post-war problems** that were identified. Focus only on **concrete, factual problems** related to:
- Humanitarian conditions
- Logistical or operational challenges
- Political or infrastructural issues

Format:
- Use bullet points.
- Be specific and concise.
- Do not rephrase or generalize—quote the core problems directly from the summary.

Verified Post-Conflict Summary:
{output_prompt2} 
"""

# === Send Prompt 3 ===
response3 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt3}],
    temperature=0.3
)
output_prompt3 = response3.choices[0].message.content

# Prompt 4: AI application to real-world conflict problems

prompt4 = f"""
You are an AI policy analyst.

Given the list of real-world problems from a conflict and a list of AI-related technologies or methods, associate each AI use with a relevant problem, and describe in 1–2 sentences how it could help. Only use logical, evidence-based connections. Do not invent or speculate. Omit any AI uses that are not clearly applicable.

Conflict problems:
{output_prompt3}

AI use keywords:{sorted_ai_uses_keywords}

Return results as a list in this format:

- **[AI Keyword]**: [One-sentence explanation of how it can address a listed problem]
"""

# === Send Prompt 4 ===
response4 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt4}],
    temperature=0.3
)
output_prompt4 = response4.choices[0].message.content

# Prompt 5: AI application to real-world conflict problems

prompt5 = f"""
You are an AI ethics analyst reviewing technology in conflict zones.

Given the use cases below (AI uses and their applications in a specific conflict), and the generic AI-related risks listed after, analyze which risks are realistically applicable to each AI use case, based on the conflict context.

Only include risks that are relevant given the description. Be specific about how the risk could appear in that situation. Do not list risks if no clear, context-specific threat can be explained.

—
**Specific conflict**:
{output_prompt4}


**List of AI Use Cases and Risks**:
{sorted_ai_risks_keywords}

---

Return the result as:

- **[AI Use Name]**
  - *Use*: [Short description provided]
  - *Risks*:
    - [Risk name]: [Explain how the risk applies in this context]
"""

# === Send Prompt 5 ===
response5 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt5}],
    temperature=0.3
)
output_prompt5 = response5.choices[0].message.content

# Prompt 6: AI application to real-world conflict problems

prompt6 = f"""
You are an AI ethics analyst tasked with proposing mitigations for the risks identified in AI systems deployed in conflict zones.

Below are the AI use cases, the associated risks for each, and a list of potential generic AI risk mitigations:

**AI Use Cases and Risks**:
{output_prompt5}

**AI Risk Mitigations**:
{sorted_ai_mitigations_keywords}

---

For each AI tool and risk, propose **specific mitigations** based on the conflict scenario, considering the constraints and operational realities. Be as practical and context-relevant as possible. If no mitigation can be applied, leave that risk out.

Return the output as follows (without any other text content):

- **[AI Tool Name]**
  - *Use*: [Description provided]
  - *Risks and Mitigations*:
    - [Risk name]: [Description provided] + [Mitigation strategy]

"""

# === Send Prompt 6 ===
response6 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt6}],
    temperature=0.3
)
output_prompt6 = response6.choices[0].message.content


# Prompt 7: AI application to real-world conflict problems

prompt7 = f"""
You are an AI ethics analyst working in the context of conflict zones and post-war recovery.

Below is a list of AI tools, their intended uses, associated risks, and a generic list of risk mitigation strategies.

**AI Use Cases, Risks, and Mitigations**:
{output_prompt6}


---

Your task is to enhance this evaluation by also highlighting the **key benefits** of each AI tool in relation to the specific conflict or post-conflict challenges.

Instructions:
- For each AI tool:
  - Include a *brief explanation of its use* in this context.
  - Identify **major benefits** of that use—especially humanitarian, logistical, or peace-building benefits.
  - Then list each **identified risk** followed by a **practical, context-specific mitigation strategy** from the mitigation list.
  - Focus on the operational realities of conflict zones (e.g., resource scarcity, infrastructure damage, lack of trust).
  - If a risk has no viable mitigation, skip it.

Format:
- **[AI Tool Name]**
  - *Use*: [Short description]
  - *Benefits*:
    - [Short bullet point describing a benefit]
    - [Second benefit, if applicable]
  - *Risks and Mitigations*:
    - [Risk name]: [Risk description] + [Mitigation strategy]

Be concise, fact-based, and relevant to conflict-zone conditions. Do not speculate beyond the data provided.Do not write any other text not requested.
"""

# === Send Prompt 7 ===
response7 = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt7}],
    temperature=0.3
)
output_prompt7 = response7.choices[0].message.content


# === Final Output Variables ===
print("\n=== Prompt 1 Output ===\n")
print(output_prompt1)

print("\n=== Prompt 2 Output ===\n")
print(output_prompt2)

print("\n=== Prompt 3 Output ===\n")
print(output_prompt3)

print("\n=== Prompt 4 Output ===\n")
print(output_prompt4)

print("\n=== Prompt 5 Output ===\n")
print(output_prompt5)

print("\n=== Prompt 6 Output ===\n")
print(output_prompt6)

print("\n=== Prompt 7 Output ===\n")
print(output_prompt7)
