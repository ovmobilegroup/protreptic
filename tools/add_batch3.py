#!/usr/bin/env python3
"""
Add Batch 3 (10 figures) to Protreptic data files
"""
import json

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # Load batch3 candidates
    with open('batch3_candidates.json', 'r') as f:
        candidates = json.load(f)
    
    print(f"Loading {len(candidates)} Batch 3 candidates...")
    
    # Load existing data files
    scenarios_zh = load_json('scenarios_zh.json')
    scenarios_en = load_json('scenarios_en.json')
    code_maps = load_json('code_maps.json')
    scenario_tags = load_json('scenario_tags.json')
    
    # English translations for each candidate
    en_data = {
        "H-KS-352": {
            "name": "Kang Sheng: Intelligence United Front and Discipline Construction Dual Architect - Three Disciplines Eight Points Ultimate Implementation in Intelligence System",
            "description": "Intelligence United Front, Discipline Construction, Organizational Purification",
            "reason": "Kang Sheng built intelligence united front network with United Front (Mode 10) as strategy, infiltrating enemy systems. Three Disciplines Eight Points (Mode 42) absolutized in intelligence system: confidentiality, discipline, work style zero tolerance. Mass Line (Mode 6) applied in intelligence work: go deep into masses, rely on masses. Criticism & Self-Criticism (Mode 2) as internal purification mechanism: regular rectification, eliminate aliens, maintain team purity. Intelligence feedback decision-making: intelligence results directly serve top decision-making, forming 'intelligence-decision-execution' closed loop. Experience institutionalization: intelligence work regulations, confidentiality regulations, discipline regulations.",
            "steps": [
                "Step 1: Establish intelligence united front network - United Front (Mode 10) as strategy, infiltrate enemy systems internally",
                "Step 2: Three Disciplines Eight Points (Mode 42) absolutized in intelligence system - confidentiality, discipline, work style zero tolerance",
                "Step 3: Mass Line (Mode 6) applied in intelligence work - go deep into masses, rely on masses, from masses to masses",
                "Step 4: Criticism & Self-Criticism (Mode 2) as internal purification mechanism - regular rectification, eliminate aliens, maintain team purity",
                "Step 5: Intelligence feedback decision-making - intelligence results directly serve top decision-making, forming intelligence-decision-execution closed loop",
                "Step 6: Experience institutionalization - form inheritable intelligence work regulations, confidentiality regulations, discipline regulations"
            ],
            "expected": [
                "Build intelligence system with united front strategy",
                "Achieve absolute discipline in intelligence work",
                "Form intelligence-decision closed loop"
            ],
            "case": "Kang Sheng led CCP intelligence work: united front infiltrated KMT, Three Disciplines Eight Points as absolute discipline in intelligence system. Mass line: intelligence from masses, to masses. Criticism/self-criticism: Yan'an Rectification, purge aliens. Modern applications: intelligence system building, united front work, discipline construction, organizational purification."
        },
        "H-LRQ-353": {
            "name": "Luo Ruiqing: Army Building Systematization / Three Disciplines Eight Points Legalization / Public Security Intelligence Integration",
            "description": "Army Building, Legal System Construction, Public Security Intelligence",
            "reason": "Luo Ruiqing systematized army building. Three Disciplines Eight Points (Mode 42) legalized: discipline regulation, enforcement procedure, violation accountability. Four great treasures: Military Service Law, Military Rank System, Military Training Outline, Political Work Regulations. United Front (Mode 10) in army building: unite all unitable forces, isolate few opposition. Strategic Foresight (Mode 1) guides armament: nuclear missile satellite 'Two Bombs One Satellite' support, conventional equipment independent R&D. Public security intelligence integration: public security intelligence network nationwide, social security prevention system. Military diplomacy expansion: military delegation exchanges, military aid, international military cooperation framework.",
            "steps": [
                "Step 1: Three Disciplines Eight Points (Mode 42) legalization - discipline regulation, enforcement procedure, violation accountability system",
                "Step 2: Army building systematization - Military Service Law, Military Rank System, Military Training Outline, Political Work Regulations four great treasures",
                "Step 3: United Front (Mode 10) applied in army building - unite all unitable forces, isolate few opposition",
                "Step 4: Strategic Foresight (Mode 1) guides armament building - nuclear missile satellite Two Bombs One Satellite support, conventional equipment independent R&D",
                "Step 5: Public security intelligence integration - public security intelligence network nationwide, social security prevention system construction",
                "Step 6: Military diplomacy expansion - military delegation exchanges, military aid, international military cooperation framework"
            ],
            "expected": [
                "Build systematized people's army",
                "Form army legal system",
                "Establish public security intelligence prevention system"
            ],
            "case": "Luo Ruiqing as Chief of General Staff and Public Security Minister: Three Disciplines Eight Points legalized into regulations. Four great treasures formed army legal foundation. Public security intelligence network covered nation. Modern applications: army building, legal construction, public security intelligence, military diplomacy."
        },
        "H-XFZ-354": {
            "name": "Xie Fuzhi: Public Security Minister and Military General Dual Roles - Three Disciplines Eight Points Ultimate Implementation in Public Security System",
            "description": "Public Security Construction, Social Security Prevention, United Front Work",
            "reason": "Xie Fuzhi as Public Security Minister and military general dual roles. United Front (Mode 10) in政法work: unite all unitable forces, strike few hostile elements. Three Disciplines Eight Points (Mode 42) in public security team: absolute loyalty, absolute purity, absolute reliability. Mass Line (Mode 6) in social security prevention: professional-mass combination, mass prevention mass governance, mobilize masses participate security management. Criticism & Self-Criticism (Mode 2) as team rectification core means: rectification style discipline, purge poison, scrape bone cure poison. Military-police-civil three-in-one: militia, public security, PLA trinity stability maintenance system. Experience institutionalization: public security regulations, household registration system, security management regulations, labor reform system.",
            "steps": [
                "Step 1: United Front (Mode 10) applied in政法work - unite all unitable forces, strike few hostile elements",
                "Step 2: Three Disciplines Eight Points (Mode 42) in public security team - absolute loyalty, absolute purity, absolute reliability",
                "Step 3: Mass Line (Mode 6) in social security prevention - professional-mass combination, mass prevention mass governance, mobilize masses participate security management",
                "Step 4: Criticism & Self-Criticism (Mode 2) as team rectification core means - rectification style discipline, purge poison, scrape bone cure poison",
                "Step 5: Military-police-civil three-in-one - militia, public security, PLA trinity stability maintenance system",
                "Step 6: Experience institutionalization - public security regulations, household registration system, security management regulations, labor reform system"
            ],
            "expected": [
                "Build highly disciplined public security force",
                "Form social security prevention system",
                "Establish military-police-civil trinity stability maintenance system"
            ],
            "case": "Xie Fuzhi dual role Public Security Minister and General: United Front in政法, Three Disciplines Eight Points absolute in police. Mass line: professional-mass combination prevention. Criticism/self-criticism: team rectification core. Modern applications: public security construction, social security prevention, united front work, discipline construction."
        },
        "H-WZ-355": {
            "name": "Wang Zhen: Reclamation and Border Defense / Three Disciplines Eight Points Practice in Production Construction Corps / Crossing River by Feeling Stones Develop Great Northwest",
            "description": "Border Development, Production Construction Corps, Ethnic Unity",
            "reason": "Wang Zhen led Xinjiang Production Construction Corps construction. Three Disciplines Eight Points (Mode 42) in corps construction: militarized management, strict discipline, orders obeyed. Gradual Reform (Mode 8) develop Great Northwest: small steps pilot, not seeking large and complete, adapt to local conditions. Crossing River by Feeling Stones (Mode 38): Three Favorables evaluation, pilot success then expand, no rash advance. United Front (Mode 10) unite multi-ethnic cadres masses: ethnic policy implementation, religious policy execution, Han-Uighur unity. Reclamation border defense model: corps 'one whip law', military-political-civil three-in-one, production self-sufficiency. Experience inheritance: corps spirit, reclamation spirit, veteran spirit generation to generation.",
            "steps": [
                "Step 1: Three Disciplines Eight Points (Mode 42) in corps construction - militarized management, strict discipline, orders obeyed",
                "Step 2: Gradual Reform (Mode 8) develop Great Northwest - small step pilots, not seeking large and complete, adapt to local conditions",
                "Step 3: Crossing River by Feeling Stones (Mode 38) - Three Favorables evaluation, pilot success then expand, no rash advance",
                "Step 4: United Front (Mode 10) unite multi-ethnic cadres masses - ethnic policy implementation, religious policy execution, Han-Uighur unity",
                "Step 5: Reclamation border defense model - corps one whip law, military-political-civil three-in-one, production self-sufficiency",
                "Step 6: Experience inheritance - corps spirit, reclamation spirit, veteran spirit generation to generation"
            ],
            "expected": [
                "Build Xinjiang Production Construction Corps",
                "Achieve Great Northwest development",
                "Form military-political-civil trinity border defense model"
            ],
            "case": "Wang Zhen led Xinjiang Production Construction Corps: Three Disciplines Eight Points as corps discipline. Gradual reform: pilot first, expand after success. Three Favorables evaluation. United Front: ethnic unity, religious policy. Corps 'one whip law': military-political-civil trinity. Modern applications: border development, production construction corps, ethnic unity, military-civil fusion."
        },
        "H-CBD-356": {
            "name": "Chen Boda: Theoretical Authority / Cultural Revolution Theory Construction / Three Disciplines Eight Points Defense in Theoretical Position / Dialectic of Seek Truth from Facts and Dogmatism",
            "description": "Theoretical Construction, Ideological Political Work, Theoretical Critique",
            "reason": "Chen Boda as theoretical authority built Cultural Revolution theoretical framework. United Front (Mode 10) in theoretical circles: unite all unitable theoretical workers, establish theoretical authority. Three Disciplines Eight Points (Mode 42) in theoretical creation: political discipline, organizational discipline, confidentiality discipline. Criticism & Self-Criticism (Mode 2) as theoretical correction mechanism: dare self-negate, correct theoretical deviations. Seek Truth from Facts (Mode 7) dialectic with dogmatism: theory link practice, oppose book worship. Theoretical results convert to material force: theory arm teams, guide practice, serve decision-making. Theoretical legacy critical inheritance: affirm contributions, reveal limitations, absorb lessons.",
            "steps": [
                "Step 1: United Front (Mode 10) in theoretical circles - unite all unitable theoretical workers, establish theoretical authority",
                "Step 2: Three Disciplines Eight Points (Mode 42) in theoretical creation - political discipline, organizational discipline, confidentiality discipline",
                "Step 3: Criticism & Self-Criticism (Mode 2) as theoretical correction mechanism - dare self-negate, correct theoretical deviations",
                "Step 4: Seek Truth from Facts (Mode 7) dialectic with dogmatism - theory link practice, oppose book worship",
                "Step 5: Theoretical results convert to material force - theory arm teams, guide practice, serve decision-making",
                "Step 6: Theoretical legacy critical inheritance - affirm contributions, reveal limitations, absorb lessons"
            ],
            "expected": [
                "Build theoretical authority system",
                "Form theoretical critique methodology",
                "Absorb theoretical construction lessons"
            ],
            "case": "Chen Boda as Mao's theoretical secretary: built Cultural Revolution theory. United Front: unite theoretical workers. Three Disciplines Eight Points: theory discipline. Criticism/self-criticism: theory correction. Seek Truth from Facts: theory-practice link. Modern applications: theoretical construction, ideological political work, theoretical critique, decision consulting."
        },
        "H-YWY-357": {
            "name": "Yao Wenyuan: Literary Criticism / Three Disciplines Eight Points Execution in Literary Front / Abstract Induction Extract Class Struggle Program",
            "description": "Literary Criticism, Cultural Policy, Theory Extraction",
            "reason": "Yao Wenyuan as Cultural Revolution literary critic. United Front (Mode 10) in literary circles: unite revolutionary literary workers, isolate bourgeois literary black line. Three Disciplines Eight Points (Mode 42) in literary creation: politics in command, content king, form serves content. Criticism & Self-Criticism (Mode 2) as literary criticism core method: criticize old literature, build new literature. Abstract Induction (Mode 25) extract class struggle program: from specific works rise to line struggle height. Literary criticism as class struggle tool: pen as gun, public opinion position contention. Literary theory institutionalization: model opera system, literary creation regulations, literary criticism norms.",
            "steps": [
                "Step 1: United Front (Mode 10) in literary circles - unite revolutionary literary workers, isolate bourgeois literary black line",
                "Step 2: Three Disciplines Eight Points (Mode 42) in literary creation - politics in command, content king, form serves content",
                "Step 3: Criticism & Self-Criticism (Mode 2) as literary criticism core method - criticize old literature, build new literature",
                "Step 4: Abstract Induction (Mode 25) extract class struggle program - from specific works rise to line struggle height",
                "Step 5: Literary criticism as class struggle tool - pen as gun, public opinion position contention",
                "Step 6: Literary theory institutionalization - model opera system, literary creation regulations, literary criticism norms"
            ],
            "expected": [
                "Build revolutionary literary criticism system",
                "Form model opera institutional system",
                "Extract class struggle theoretical program"
            ],
            "case": "Yao Wenyuan wrote 'On the New Historical Drama Hai Rui Dismissed from Office' triggering Cultural Revolution. United Front: unite revolutionary writers. Three Disciplines Eight Points: literary discipline. Criticism/self-criticism: criticism method. Abstract induction: from play to line. Modern applications: literary criticism, cultural policy, public opinion guidance, theory extraction."
        },
        "H-KKQ-358": {
            "name": "Kang Keqing: Female General / Three Disciplines Eight Points Practice in Women's Work / United Front Unite Women's Forces",
            "description": "Women's Work, United Front Work, Discipline Construction, Family Tradition Inheritance",
            "reason": "Kang Keqing as female general practiced Three Disciplines Eight Points (Mode 42) as life creed: integrity, strict self-discipline, exemplary practice. United Front (Mode 10) unite women of all circles: regardless class, ethnicity, belief, widely unite. Mass Line (Mode 6) deep into women masses: investigation research, listen to voices, solve practical difficulties. Criticism & Self-Criticism (Mode 2) in women organizational life: democratic life meetings, mutual criticism, common improvement. Women liberation and national construction synchronized: Marriage Law implementation, employment equality, political participation, family virtue. Family tradition inheritance: Zhu De Kang Keqing family tradition: hard struggle, integrity, care for next generation.",
            "steps": [
                "Step 1: Three Disciplines Eight Points (Mode 42) as life creed - integrity public service, strict self-discipline, exemplary practice",
                "Step 2: United Front (Mode 10) unite all circles women - regardless class, ethnicity, belief, widely unite",
                "Step 3: Mass Line (Mode 6) deep into women masses - investigation research, listen to voices, solve practical difficulties",
                "Step 4: Criticism & Self-Criticism (Mode 2) in women organizational life - democratic life meetings, mutual criticism, common improvement",
                "Step 5: Women liberation and national construction synchronized - Marriage Law implementation, employment equality, political participation, family virtue",
                "Step 6: Family tradition inheritance - Zhu De Kang Keqing family tradition: hard struggle, integrity, care for next generation"
            ],
            "expected": [
                "Promote women's rights legislation",
                "Participate in international women's movement",
                "Establish integrity family tradition benchmark"
            ],
            "case": "Kang Keqing promoted Marriage Law, women political participation. Accompanied Zhu De diplomatic visits. Democratic life meetings, criticism/self-criticism. Modern applications: women's rights, united front work, discipline construction, family tradition inheritance."
        },
        "H-YJY-359": {
            "name": "Ye Jianying: Strategic Decision / Relay Station Intelligence Network / Military Diplomacy / Triple-Integration National Construction",
            "description": "Strategic Decision, Military Diplomacy, Intelligence Work, Cadre Management",
            "reason": "Ye Jianying as Marshal and state leader. Relay Station (Mode 41) established military intelligence network: intelligence station layout, intelligence transmission timeliness, multi-source cross-verification. United Front (Mode 10) in military diplomacy: unite all unitable international forces, military aid abroad. Mass Line (Mode 6) in troop construction: officer-soldier unity, military-civilian unity, disintegrate enemy. Strategic Delegation (Mode 33) identify talent, set strategy, share rewards, safety nets: establish army cadre echelons, authorize in place, fault tolerance correction. Strategic decision support national construction: national defense construction, national economy, diplomatic strategy triple integration. Experience institutionalization: military diplomacy regulations, intelligence work regulations, cadre management regulations.",
            "steps": [
                "Step 1: Relay Station (Mode 41) establish military intelligence network - intelligence station layout, intelligence transmission timeliness, multi-source cross-verification",
                "Step 2: United Front (Mode 10) in military diplomacy - unite all unitable international forces, military aid abroad",
                "Step 3: Mass Line (Mode 6) in troop construction - officer-soldier unity, military-civilian unity, disintegrate enemy",
                "Step 4: Strategic Delegation (Mode 33) identify talent, set strategy, share rewards, safety nets - establish army cadre echelons, authorize in place, fault tolerance correction",
                "Step 5: Strategic decision support national construction - national defense construction, national economy, diplomatic strategy triple integration",
                "Step 6: Experience institutionalization - military diplomacy regulations, intelligence work regulations, cadre management regulations"
            ],
            "expected": [
                "Build military intelligence network system",
                "Expand military diplomatic strategic space",
                "Form army cadre echelon construction system"
            ],
            "case": "Ye Jianying as Vice Chairman Military Commission: intelligence network three-level linkage. Military diplomacy: unite international forces, military aid. Mass line: officer-soldier unity. Strategic delegation: cadre echelons. Modern applications: strategic decision, military diplomacy, intelligence work, cadre management."
        },
        "H-LWH-360": {
            "name": "Li Weihan: United Front Minister / Multi-Mental Models Build United Front Theory System / Three Disciplines Eight Points Norm in United Front Work",
            "description": "United Front Work, Multi-Party Cooperation, Ethnic Religious Work, Cadre Team Building",
            "reason": "Li Weihan as United Front Minister built united front theory system. United Front (Mode 10) theorized: united front object layers, united front strategy principles, united front work methods. Multi-Mental Models (Mode 17) build united front work framework: politics+economy+culture+society+religion multi-dimensional fusion. Three Disciplines Eight Points (Mode 42) in united front cadre team: politically firm, democratic style, clean self-discipline. Criticism & Self-Criticism (Mode 2) as united front work correction mechanism: regular summary, correct deviations, keep pace with times. United Front work legalization: united front regulations, party regulations, ethnic regulations, religious regulations system construction. United Front experience inheritance: united front history compilation, united front theory textbooks, united front cadre training system.",
            "steps": [
                "Step 1: United Front (Mode 10) theory systematization - united front object layers, united front strategy principles, united front work methods",
                "Step 2: Multi-Mental Models (Mode 17) build united front work framework - politics+economy+culture+society+religion multi-dimensional fusion",
                "Step 3: Three Disciplines Eight Points (Mode 42) in united front cadre team - politically firm, democratic style, clean self-discipline",
                "Step 4: Criticism & Self-Criticism (Mode 2) as united front work correction mechanism - regular summary, correct deviations, keep pace with times",
                "Step 5: United Front work legalization - united front regulations, party regulations, ethnic regulations, religious regulations system construction",
                "Step 6: United Front experience inheritance - united front history compilation, united front theory textbooks, united front cadre training system"
            ],
            "expected": [
                "Build united front theory system",
                "Form multi-party cooperation institutional system",
                "Establish united front cadre training system"
            ],
            "case": "Li Weihan as United Front Minister: united front theory system. Multi-mental models: politics+economy+culture+society+religion. Three Disciplines Eight Points: united front cadre norms. Criticism/self-criticism: work correction. Modern applications: united front work, multi-party cooperation, ethnic religious work, cadre team building."
        },
        "H-YSK-361": {
            "name": "Yang Shangkun: State Chairman / Military Commission Vice Chairman / Relay Station Intelligence Command / Gradual Reform Push Army Modernization / Procedural Justice Build Rule of Law Army",
            "description": "Army Building, Army Reform, Intelligence Command, Rule of Law Construction",
            "reason": "Yang Shangkun as State Chairman and Military Commission Vice Chairman. Relay Station (Mode 41) commanded army intelligence system: Military Commission intelligence department, General Staff intelligence department, military region intelligence networks three-level linkage. Gradual Reform (Mode 8) push army modernization: reduce million troops, service arms synthesis, equipment update, military training legalization. Crossing River by Feeling Stones (Mode 38) army reform pilots: streamline reorganization pilots, military rank system pilots, military court pilots. Procedural Justice (Mode 32) build rule of law army: military legislation, military justice, military procuratorate, military enforcement four-in-one. Army regularization, modernization, legalization 'three modernizations' synchronous push. Experience inheritance: 'Yang Shangkun Military Works', army construction experience summary, army reform experience lessons.",
            "steps": [
                "Step 1: Relay Station (Mode 41) command army intelligence system - Military Commission intelligence dept, General Staff intelligence dept, military region intelligence networks three-level linkage",
                "Step 2: Gradual Reform (Mode 8) push army modernization - reduce million troops, service arms synthesis, equipment update, military training legalization",
                "Step 3: Crossing River by Feeling Stones (Mode 38) army reform pilots - streamline reorganization pilots, military rank system pilots, military court pilots",
                "Step 4: Procedural Justice (Mode 32) build rule of law army - military legislation, military justice, military procuratorate, military enforcement four-in-one",
                "Step 5: Army regularization, modernization, legalization 'three modernizations' synchronous push",
                "Step 6: Experience inheritance - 'Yang Shangkun Military Works', army construction experience summary, army reform experience lessons"
            ],
            "expected": [
                "Achieve army million-troop reduction and synthesis",
                "Build army intelligence command system",
                "Establish rule of law army legal system"
            ],
            "case": "Yang Shangkun as Military Commission Vice Chairman: million troop reduction. Relay Station intelligence three-level linkage. Gradual reform: pilots first. Procedural justice: military legislation/justice/procuratorate/enforcement. Modern applications: army building, army reform, intelligence command, rule of law construction."
        }
    }
    
    # Add each candidate
    for c in candidates:
        code = c['code']
        
        # Chinese version
        desc_zh = c.get('unique_thinking', '')
        reason_zh = f"{c['name_zh']}的核心思维贡献：{c.get('unique_thinking', '')}。结合相关思维模式框架，分析其在相关领域的卓越贡献和思想方法。"
        steps_zh = c.get('proposed_steps', [])
        expected_zh = c.get('applications', [])
        case_zh = f"{c['name_zh']}的核心实践：{'；'.join(c.get('applications', []))}"
        era = c.get('era', 'Modern')
        
        scenarios_zh[code] = {
            "name": f"{c['name_zh']}：{c.get('unique_thinking', '')}",
            "description": desc_zh,
            "modes": c['core_modes'],
            "reason": reason_zh,
            "steps": steps_zh,
            "expected": expected_zh,
            "case": case_zh,
            "era": era
        }
        
        # English version
        en = en_data.get(code, {})
        if en:
            scenarios_en[code] = {
                "name": en['name'],
                "description": en['description'],
                "modes": c['core_modes'],
                "reason": en['reason'],
                "steps": en['steps'],
                "expected": en['expected'],
                "case": en['case'],
                "era": era
            }
        else:
            scenarios_en[code] = {
                "name": f"{c['name_en']}: {c.get('unique_thinking', '')}",
                "description": c.get('unique_thinking', ''),
                "modes": c['core_modes'],
                "reason": f"{c['name_en']}'s core thinking contribution: {c.get('unique_thinking', '')}. Combined with relevant thinking mode framework, analyzing their outstanding contributions and thinking methods in related fields.",
                "steps": [s.replace('第', 'Step ').replace('步：', ': ') for s in steps_zh],
                "expected": [e.replace('跨国', 'Cross-border').replace('联盟', 'Alliance').replace('危机', 'Crisis').replace('政府', 'Government').replace('军队', 'Military').replace('纪律', 'Discipline').replace('建设', 'Building').replace('管理', 'Management').replace('外交', 'Diplomacy').replace('谈判', 'Negotiation') for e in expected_zh],
                "case": f"{c['name_en']}'s core practice: {'; '.join(expected_zh)}",
                "era": era
            }
        
        # code_maps
        code_maps['CODE_MAP'][code] = c['name_zh']
        code_maps['CODE_MAP_EN'][code] = c['name_en']
        
        # scenario_tags
        scenario_tags['tags'][code] = {
            "code": code,
            "name_zh": c['name_zh'],
            "name_en": c['name_en'],
            "era": c['era'],
            "historical_domains": c['historical_domains'],
            "domains": c['domains'],
            "core_modes": c['core_modes'],
            "gender": c['gender'],
            "ethnicity": c['ethnicity']
        }
        
        print(f"  Added {code}: {c['name_zh']}")
    
    # Update metadata in scenario_tags
    scenario_tags['metadata']['total_scenarios'] = len(scenario_tags['tags'])
    
    # Save all files
    save_json(scenarios_zh, 'scenarios_zh.json')
    save_json(scenarios_en, 'scenarios_en.json')
    save_json(code_maps, 'code_maps.json')
    save_json(scenario_tags, 'scenario_tags.json')
    
    print(f"\nDone! Added {len(candidates)} Batch 3 figures.")
    print(f"Total scenarios: {len(scenarios_zh)}")
    
    # Verify
    h_count = sum(1 for k in scenarios_zh if k.startswith('H-') or k.startswith('M-'))
    print(f"H-* historical figures: {h_count}")

if __name__ == '__main__':
    main()