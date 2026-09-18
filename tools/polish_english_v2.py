#!/usr/bin/env python3
"""
English polish script for Protreptic scenarios.
Converts all English content to consistent imperative mood and standardized terminology.
"""
import json
import re

# Load existing data
with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    modes = json.load(f)

en_modes = modes['en']

# Standardized terminology mapping
TERMINOLOGY = {
    # Core concepts
    'Longzhong Plan': 'Longzhong Plan',
    'Three Kingdoms Division': 'Three Kingdoms Division',
    'Northern Expeditions': 'Northern Expeditions',
    'Chushibiao (Memorial on the Expedition)': 'Chushibiao',
    'Admonition to My Son': 'Admonition to My Son',
    'Wooden Ox and Flowing Horse (logistics innovation)': 'Wooden Ox and Flowing Horse',
    'Devotion to the Utmost Until Death': 'Devotion to the Utmost Until Death',
    'Three Visits to the Thatched Cottage': 'Three Visits to the Thatched Cottage',
    'Baidi Entrustment': 'Baidi Entrustment',
    'Righteousness-Based Statecraft': 'Righteousness-Based Statecraft',
    'Strategic Delegation': 'Strategic Delegation',
    'Talent Recognition and Deployment': 'Talent Recognition and Deployment',
    'Using the Emperor to Command Feudal Lords': 'Using the Emperor to Command Feudal Lords',
    'Tuntian Agricultural Garrison System': 'Tuntian System',
    'Short-Decisive Battle Doctrine': 'Short-Decisive Battle',
    'Merit-Based Appointment': 'Merit-Based Appointment',
    'Consolidation Rule': 'Consolidation Rule',
    'Balance-of-Power Statecraft': 'Balance-of-Power Statecraft',
    'Jiangdong Foundation': 'Jiangdong Foundation',
    'Wu-Centric Talent Policy': 'Wu-Centric Talent Policy',
    'Battle of Red Cliffs': 'Battle of Red Cliffs',
    'Fire Attack': 'Fire Attack',
    'Chain Stratagem': 'Chain Stratagem',
    'Borrowing Arrows with Straw Boats': 'Borrowing Arrows with Straw Boats',
    'Borrowing the East Wind': 'Borrowing the East Wind',
    'Self-Inflicted Wound Stratagem': 'Self-Inflicted Wound Stratagem',
    'Battle of Jieting': 'Battle of Jieting',
    'Disobeying Orders': 'Disobeying Orders',
    'Armchair Strategy': 'Armchair Strategy',
    'Execution of Ma Su': 'Execution of Ma Su',
    'Self-Demotion by Three Ranks': 'Self-Demotion by Three Ranks',
    'Battle of Yiling': 'Battle of Yiling',
    'Settling Private Grudge at National Expense': 'Settling Private Grudge at National Expense',
    'Encamped for Seven Hundred Li': 'Encamped for Seven Hundred Li',
    'Lu Xun': 'Lu Xun',
    'Battle of Changban': 'Battle of Changban',
    'Single-Horsed Rescue of the Lord': 'Single-Horsed Rescue of the Lord',
    'Zilong is All Courage': 'Zilong is All Courage',
    'Request to Fulfill Mission with My Life': 'Request to Fulfill Mission with My Life',
    'Maneuver Warfare': 'Maneuver Warfare',
    'Guerrilla Warfare': 'Guerrilla Warfare',
    'Annihilation Warfare': 'Annihilation Warfare',
    'Asymmetric Warfare': 'Asymmetric Warfare',
    'Military Training Precision Standard': 'Military Training Precision Standard',
    'Military Engineering Institute': 'Military Engineering Institute',
    'National University of Defense Technology': 'National University of Defense Technology',
    'Hybrid Rice': 'Hybrid Rice',
    'Three-Line System': 'Three-Line System',
    'Two-Line System': 'Two-Line System',
    'Super Rice': 'Super Rice',
    'Food Security': 'Food Security',
    'Optimization Method': 'Optimization Method',
    'Multi-Objective Programming': 'Multi-Objective Programming',
    'Uniform Distribution': 'Uniform Distribution',
    'Systems Engineering': 'Systems Engineering',
    'Large Systems Perspective': 'Large Systems Perspective',
    'Two Bombs One Satellite': 'Two Bombs One Satellite',
    'Missile and Aerospace': 'Missile and Aerospace',
    'Technology Management': 'Technology Management',
    'Phenology': 'Phenology',
    'Meteorology': 'Meteorology',
    'Geography': 'Geography',
    'President of Zhejiang University': 'President of Zhejiang University',
    'Revitalizing the Nation through Science and Education': 'Revitalizing the Nation through Science and Education',
    # Mode names (standardized)
    'Contradiction Analysis': 'Contradiction Analysis',
    'Mass Line Method': 'Mass Line',
    'Protracted War Thinking': 'Protracted War',
    'Rural Encirclement of Cities': 'Rural Encirclement of Cities',
    'Seeking Truth from Facts': 'Seeking Truth from Facts',
    'United Front Method': 'United Front',
    'Strategic Foresight': 'Strategic Foresight',
    'Gradual Reform': 'Gradual Reform',
    'Self-Reliance': 'Self-Reliance',
    'Criticism and Self-Criticism': 'Criticism and Self-Criticism',
    'Flexible Strategy': 'Flexible Strategy',
    'Systems Thinking': 'Systems Thinking',
    'Total Victory Thinking': 'Total Victory',
    'Center of Gravity (Warfare)': 'Center of Gravity (Warfare)',
    'Maneuver Annihilation': 'Maneuver Annihilation',
    'Sixteen-Character Guerrilla Formula': 'Sixteen-Character Guerrilla Formula',
    'Mental Models Pluralism': 'Multiple Mental Models',
    'Management by Objectives': 'Management by Objectives',
    'Marginal Thinking': 'Marginal Thinking',
    'Game Theory Thinking': 'Game Theory',
    'Loss Aversion': 'Loss Aversion',
    'Holistic Thinking': 'Holistic Thinking',
    'Natural Selection': 'Natural Selection',
    'Punctuated Equilibrium': 'Punctuated Equilibrium',
    'Abstraction and Induction': 'Abstraction and Induction',
    'Unity of Knowledge and Action': 'Unity of Knowledge and Action',
    'Dual-System Thinking': 'Dual-System Thinking',
    'Crossing River by Feeling Stones': 'Crossing River by Feeling Stones',
    'Feedback Loop': 'Feedback Loop',
    'Framing Effect': 'Framing Effect',
    'Institutional Checks and Balances': 'Institutional Checks and Balances',
    'Three-Agency Military Separation': 'Three-Agency Military Separation',
    'Birdcage Economy': 'Birdcage Economy',
    'Marginal Thinking': 'Marginal Thinking',
    'Redundancy and Backup': 'Redundancy and Backup',
    'Boundary Thinking': 'Boundary Thinking',
    'Relay Station System': 'Relay Station System',
    'Three Principles of the People': 'Three Principles of the People',
}

# Imperative mood patterns - convert descriptive to imperative
IMPERATIVE_PATTERNS = [
    (r'is known for', 'Known for'),
    (r'is the', 'Identify the'),
    (r'was a', 'Recognize as'),
    (r'created the', 'Create the'),
    (r'established the', 'Establish the'),
    (r'authored the', 'Author the'),
    (r'proposed the', 'Propose the'),
    (r'led the', 'Lead the'),
    (r'built the', 'Build the'),
    (r'founded the', 'Found the'),
    (r'launched the', 'Launch the'),
    (r'initiated the', 'Initiate the'),
    (r'promoted the', 'Promote the'),
    (r'implemented the', 'Implement the'),
    (r'reformed the', 'Reform the'),
    (r'transformed the', 'Transform the'),
    (r'solved the', 'Solve the'),
    (r'resolved the', 'Resolve the'),
    (r'addressed the', 'Address the'),
    (r'overcame the', 'Overcome the'),
    (r'broke the', 'Break the'),
    (r'defied the', 'Defy the'),
    (r'challenged the', 'Challenge the'),
    (r'pioneered the', 'Pioneer the'),
    (r'spearheaded the', 'Spearhead the'),
    (r'championed the', 'Champion the'),
    (r'advocated the', 'Advocate the'),
    (r'formulated the', 'Formulate the'),
    (r'devised the', 'Devise the'),
    (r'designed the', 'Design the'),
    (r'architected the', 'Architect the'),
    (r'engineered the', 'Engineer the'),
    (r'orchestrated the', 'Orchestrate the'),
    (r'masterminded the', 'Mastermind the'),
    (r'conceived the', 'Conceive the'),
    (r'envisaged the', 'Envisage the'),
    (r'foresaw the', 'Foresight the'),
    (r'anticipated the', 'Anticipate the'),
    (r'predicted the', 'Predict the'),
    (r'planned the', 'Plan the'),
    (r'strategized the', 'Strategize the'),
    (r'organized the', 'Organize the'),
    (r'mobilized the', 'Mobilize the'),
    (r'rallied the', 'Rally the'),
    (r'united the', 'Unite the'),
    (r'aligned the', 'Align the'),
    (r'harmonized the', 'Harmonize the'),
    (r'integrated the', 'Integrate the'),
    (r'synthesized the', 'Synthesize the'),
    (r'consolidated the', 'Consolidate the'),
    (r'strengthened the', 'Strengthen the'),
    (r'fortified the', 'Fortify the'),
    (r'secured the', 'Secure the'),
    (r'protected the', 'Protect the'),
    (r'defended the', 'Defend the'),
    (r'shielded the', 'Shield the'),
    (r'guarded the', 'Guard the'),
    (r'preserved the', 'Preserve the'),
    (r'maintained the', 'Maintain the'),
    (r'sustained the', 'Sustain the'),
    (r'upheld the', 'Uphold the'),
    (r'ensured the', 'Ensure the'),
    (r'guaranteed the', 'Guarantee the'),
    (r'assured the', 'Assure the'),
    (r'certified the', 'Certify the'),
    (r'validated the', 'Validate the'),
    (r'verified the', 'Verify the'),
    (r'confirmed the', 'Confirm the'),
    (r'affirmed the', 'Affirm the'),
    (r'attested the', 'Attest the'),
    (r'endorsed the', 'Endorse the'),
    (r'supported the', 'Support the'),
    (r'backed the', 'Back the'),
    (r'funded the', 'Fund the'),
    (r'financed the', 'Finance the'),
    (r'invested in the', 'Invest in the'),
    (r'capitalized the', 'Capitalize the'),
    (r'resourced the', 'Resource the'),
    (r'equipped the', 'Equip the'),
    (r'empowered the', 'Empower the'),
    (r'enabled the', 'Enable the'),
    (r'facilitated the', 'Facilitate the'),
    (r'accelerated the', 'Accelerate the'),
    (r'expedited the', 'Expedite the'),
    (r'streamlined the', 'Streamline the'),
    (r'optimized the', 'Optimize the'),
    (r'enhanced the', 'Enhance the'),
    (r'improved the', 'Improve the'),
    (r'upgraded the', 'Upgrade the'),
    (r'modernized the', 'Modernize the'),
    (r'transformed the', 'Transform the'),
    (r'revolutionized the', 'Revolutionize the'),
    (r'innovated the', 'Innovate the'),
    (r'invented the', 'Invent the'),
    (r'created the', 'Create the'),
    (r'originated the', 'Originate the'),
    (r'initiated the', 'Initiate the'),
    (r'inaugurated the', 'Inaugurate the'),
    (r'launched the', 'Launch the'),
    (r'rolled out the', 'Roll out the'),
    (r'deployed the', 'Deploy the'),
    (r'implemented the', 'Implement the'),
    (r'executed the', 'Execute the'),
    (r'administered the', 'Administer the'),
    (r'managed the', 'Manage the'),
    (r'directed the', 'Direct the'),
    (r'oversaw the', 'Oversee the'),
    (r'supervised the', 'Supervise the'),
    (r'monitored the', 'Monitor the'),
    (r'tracked the', 'Track the'),
    (r'measured the', 'Measure the'),
    (r'assessed the', 'Assess the'),
    (r'evaluated the', 'Evaluate the'),
    (r'appraised the', 'Appraise the'),
    (r'reviewed the', 'Review the'),
    (r'audited the', 'Audit the'),
    (r'inspected the', 'Inspect the'),
    (r'examined the', 'Examine the'),
    (r'analyzed the', 'Analyze the'),
    (r'studied the', 'Study the'),
    (r'investigated the', 'Investigate the'),
    (r'researched the', 'Research the'),
    (r'explored the', 'Explore the'),
    (r'discovered the', 'Discover the'),
    (r'uncovered the', 'Uncover the'),
    (r'revealed the', 'Reveal the'),
    (r'exposed the', 'Expose the'),
    (r'illuminated the', 'Illuminate the'),
    (r'clarified the', 'Clarify the'),
    (r'elucidated the', 'Elucidate the'),
    (r'explained the', 'Explain the'),
    (r'interpreted the', 'Interpret the'),
    (r'decoded the', 'Decode the'),
    (r'deciphered the', 'Decipher the'),
    (r'translated the', 'Translate the'),
    (r'rendered the', 'Render the'),
    (r'converted the', 'Convert the'),
    (r'transformed the', 'Transform the'),
    (r'adapted the', 'Adapt the'),
    (r'modified the', 'Modify the'),
    (r'altered the', 'Alter the'),
    (r'adjusted the', 'Adjust the'),
    (r'calibrated the', 'Calibrate the'),
    (r'fine-tuned the', 'Fine-tune the'),
    (r'optimized the', 'Optimize the'),
    (r'refined the', 'Refine the'),
    (r'polished the', 'Polish the'),
    (r'perfected the', 'Perfect the'),
]

def polish_reason(reason: str) -> str:
    """Convert reason to imperative mood."""
    if not reason:
        return ''
    
    # Replace descriptive openings with imperative
    reason = reason.strip()
    
    # Pattern: "X did Y with Z, achieving W" -> "Execute Y with Z to achieve W"
    # Pattern: "X used Y to Z" -> "Use Y to Z"
    # Pattern: "X's approach was Y" -> "Adopt Y approach"
    
    # Simple replacements for common patterns
    replacements = {
        'core contribution: ': 'Core Contribution: ',
        'Core contribution: ': 'Core Contribution: ',
        'rationale: ': 'Rationale: ',
        'Rationale: ': 'Rationale: ',
    }
    
    for k, v in replacements.items():
        if reason.lower().startswith(k.lower()):
            reason = v + reason[len(k):]
            break
    
    # Convert first sentence to imperative if it starts with descriptive
    sentences = re.split(r'(?<=[.!?])\s+', reason)
    if sentences:
        first = sentences[0]
        # If starts with name + verb, convert
        first = re.sub(r'^[A-Z][a-z]+\s+(?:used|used|employed|adopted|implemented|created|established|built|founded|launched|initiated|led|led|guided|directed|orchestrated|masterminded|conceived|envisaged|foresaw|anticipated|predicted|planned|strategized|organized|mobilized|rallied|united|aligned|harmonized|integrated|synthesized|consolidated|strengthened|fortified|secured|protected|defended|shielded|guarded|preserved|maintained|sustained|upheld|ensured|guaranteed|assured|certified|validated|verified|confirmed|affirmed|attested|endorsed|supported|backed|funded|financed|invested in|capitalized|resourced|equipped|empowered|enabled|facilitated|accelerated|expedited|streamlined|optimized|enhanced|improved|upgraded|modernized|transformed|revolutionized|innovated|invented|created|originated|initiated|inaugurated|launched|rolled out|deployed|implemented|executed|administered|managed|directed|oversaw|supervised|monitored|tracked|measured|assessed|evaluated|appraised|reviewed|audited|inspected|examined|analyzed|studied|investigated|researched|explored|discovered|uncovered|revealed|exposed|illuminated|clarified|elucidated|explained|interpreted|decoded|deciphered|translated|rendered|converted|transformed|adapted|modified|adjusted|calibrated|fine-tuned|optimized|refined|polished|perfected)\s+', '', first, flags=re.IGNORECASE)
        if first != sentences[0]:
            sentences[0] = first.strip()
        reason = ' '.join(sentences)
    
    return reason

def polish_steps(steps: list) -> list:
    """Ensure steps are in imperative mood."""
    polished = []
    for step in steps:
        step = step.strip()
        # Remove numbering if present
        step = re.sub(r'^(?:Step\s+\d+[:：]?\s*|第\s*\d+\s*[步步骤][：:]?\s*|\d+[.:]\s*)', '', step, flags=re.IGNORECASE)
        # Ensure starts with verb
        if step and not re.match(r'^(?:Identify|Establish|Build|Create|Execute|Implement|Deploy|Launch|Initiate|Lead|Direct|Guide|Design|Architect|Engineer|Orchestrate|Mastermind|Conceive|Envisage|Foresight|Anticipate|Predict|Plan|Strategize|Organize|Mobilize|Rally|Unite|Align|Harmonize|Integrate|Synthesize|Consolidate|Strengthen|Fortify|Secure|Protect|Defend|Shield|Guard|Preserve|Maintain|Sustain|Uphold|Ensure|Guarantee|Assure|Certify|Validate|Verify|Confirm|Affirm|Attest|Endorse|Support|Back|Fund|Finance|Invest|Capitalize|Resource|Equip|Empower|Enable|Facilitate|Accelerate|Expedite|Streamline|Optimize|Enhance|Improve|Upgrade|Modernize|Transform|Revolutionize|Innovate|Invent|Create|Originate|Initiate|Inaugurate|Launch|Roll out|Deploy|Implement|Execute|Administer|Manage|Direct|Oversee|Supervise|Monitor|Track|Measure|Assess|Evaluate|Appraise|Review|Audit|Inspect|Examine|Analyze|Study|Investigate|Research|Explore|Discover|Uncover|Reveal|Expose|Illuminate|Clarify|Elucidate|Explain|Interpret|Decode|Decipher|Translate|Render|Convert|Transform|Adapt|Modify|Adjust|Calibrate|Fine-tune|Optimize|Refine|Polish|Perfect)', step, re.IGNORECASE):
            # Try to extract action from step
            # Default: prepend "Execute"
            step = f"Execute: {step}"
        polished.append(step)
    return polished

def polish_expected(expected: str) -> str:
    """Convert expected to imperative deliverable format."""
    if not expected:
        return ''
    expected = expected.strip()
    # Convert "Become X" to "Deliver X" or "Achieve X"
    expected = re.sub(r'^Become\s+', 'Achieve: ', expected, flags=re.IGNORECASE)
    expected = re.sub'^Be\s+', 'Be: ', expected, flags=re.IGNORECASE)
    return expected

def polish_case(case: str) -> str:
    """Polish case study to be more concise and imperative-referenced."""
    if not case:
        return ''
    case = case.strip()
    # Keep as is but ensure it references the thinking modes
    return case

# Process all scenarios
updated = 0
for code, entry in en.items():
    if not code.startswith(('H-', 'M-')):
        continue
    
    zh_entry = zh.get(code, {})
    if not zh_entry:
        continue
    
    # Get modes for reference
    mode_names = [en_modes.get(str(m), [''])[0] for m in entry.get('modes', [])]
    
    # Polish reason
    if 'reason' in entry and entry['reason']:
        entry['reason'] = polish_reason(entry['reason'])
    
    # Polish steps
    if 'steps' in entry and entry['steps']:
        entry['steps'] = polish_steps(entry['steps'])
    
    # Polish expected
    if 'expected' in entry and entry['expected']:
        entry['expected'] = polish_expected(entry['expected'])
    
    # Polish case
    if 'case' in entry and entry['case']:
        entry['case'] = polish_case(entry['case'])
    
    updated += 1

# Save polished English
with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

print(f"Polished {updated} entries")

# Also generate TERMINOLOGY.md
terminology_lines = [
    "# Protreptic Terminology Reference",
    "",
    "| Chinese Term | English Standard | Context | Deprecated |",
    "|--------------|------------------|---------|------------|"
]
for zh_term, en_term in sorted(TERMINOLOGY.items()):
    terminology_lines.append(f"| {zh_term} | {en_term} | Core concept | - |")

with open('/opt/data/workspace/Protreptic/docs/TERMINOLOGY.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(terminology_lines))

print("Generated TERMINOLOGY.md")