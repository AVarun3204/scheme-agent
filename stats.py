import json
import os

def get_scheme_stats(schemes_file="schemes.json"):
    """Get statistics about the schemes database"""
    with open(schemes_file, "r", encoding="utf-8") as f:
        schemes = json.load(f)
    
    total_schemes = len(schemes)
    
    # Count by category
    categories = {}
    for scheme in schemes:
        cat = scheme.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
    
    # Count Telangana specific
    telangana_schemes = sum(1 for s in schemes 
                           if s.get("eligibility", {}).get("state") == "telangana")
    
    # Count with real URLs
    online_schemes = sum(1 for s in schemes 
                        if s.get("apply_link", "").startswith("http"))
    
    # Count offline schemes
    offline_schemes = total_schemes - online_schemes
    
    return {
        "total_schemes": total_schemes,
        "categories": categories,
        "telangana_schemes": telangana_schemes,
        "central_schemes": total_schemes - telangana_schemes,
        "online_schemes": online_schemes,
        "offline_schemes": offline_schemes
    }

def get_application_stats(tracker_file="applications.json"):
    """Get statistics about applications"""
    if not os.path.exists(tracker_file):
        return {
            "total_applications": 0,
            "by_status": {},
            "unique_users": 0
        }
    
    with open(tracker_file, "r", encoding="utf-8") as f:
        try:
            applications = json.load(f)
        except:
            applications = []
    
    total = len(applications)
    
    by_status = {}
    users = set()
    for app in applications:
        status = app.get("status", "Unknown")
        by_status[status] = by_status.get(status, 0) + 1
        users.add(app.get("user_name", ""))
    
    return {
        "total_applications": total,
        "by_status": by_status,
        "unique_users": len(users)
    }

if __name__ == "__main__":
    stats = get_scheme_stats()
    print("\n📊 SCHEME AGENT STATISTICS")
    print("="*40)
    print(f"Total schemes: {stats['total_schemes']}")
    print(f"Central schemes: {stats['central_schemes']}")
    print(f"Telangana schemes: {stats['telangana_schemes']}")
    print(f"Online apply: {stats['online_schemes']}")
    print(f"Offline apply: {stats['offline_schemes']}")
    print("\nBy category:")
    for cat, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")