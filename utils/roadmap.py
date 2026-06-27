# utils/roadmap.py

def recommend_learning(missing_skills):
    """
    Groups missing technical skills into operational dynamic priority streams
    to establish structured learning pathways.
    """
    priority1 = [] # High Criticality Infrastructure & Core Systems
    priority2 = [] # Mid Tier Business Intelligence & Analytics Tools
    priority3 = [] # Essential Platform Utilities & Foundations

    # Priority Blueprint Classification Rule Targets
    P1_TARGETS = {"aws", "gcp", "azure", "docker", "kubernetes", "tensorflow", "pytorch", "python", "machine learning"}
    P2_TARGETS = {"power bi", "tableau", "excel", "matplotlib", "seaborn", "pandas", "sql"}
    
    for skill in missing_skills:
        skill_lower = skill.strip().lower()
        
        if any(p1 in skill_lower for p1 in P1_TARGETS):
            priority1.append(skill)
        elif any(p2 in skill_lower for p2 in P2_TARGETS):
            priority2.append(skill)
        else:
            priority3.append(skill)

    return priority1, priority2, priority3