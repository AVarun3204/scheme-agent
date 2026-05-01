import json
import os
from datetime import datetime

TRACKER_FILE = "applications.json"

def load_applications():
    """Load all saved applications"""
    if not os.path.exists(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_application(user_name, scheme_name, scheme_benefit, apply_link):
    """Save a new application"""
    applications = load_applications()
    
    # Check if already saved
    for app in applications:
        if app["user_name"] == user_name and app["scheme_name"] == scheme_name:
            return False  # Already exists
    
    application = {
        "id": len(applications) + 1,
        "user_name": user_name,
        "scheme_name": scheme_name,
        "scheme_benefit": scheme_benefit,
        "apply_link": apply_link,
        "status": "Not Applied",
        "date_saved": datetime.now().strftime("%d-%m-%Y"),
        "date_applied": "",
        "notes": ""
    }
    
    applications.append(application)
    
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)
    
    return True

def update_status(application_id, new_status, notes=""):
    """Update the status of an application"""
    applications = load_applications()
    
    for app in applications:
        if app["id"] == application_id:
            app["status"] = new_status
            app["notes"] = notes
            if new_status == "Applied":
                app["date_applied"] = datetime.now().strftime("%d-%m-%Y")
            break
    
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)

def get_user_applications(user_name):
    """Get all applications for a specific user"""
    applications = load_applications()
    return [app for app in applications if app["user_name"].lower() == user_name.lower()]

def delete_application(application_id):
    """Delete an application"""
    applications = load_applications()
    applications = [app for app in applications if app["id"] != application_id]
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)

STATUS_OPTIONS = [
    "Not Applied",
    "Applied",
    "Documents Submitted",
    "Under Review",
    "Approved",
    "Rejected",
    "Received Benefit"
]

STATUS_COLORS = {
    "Not Applied": "#gray",
    "Applied": "#1565c0",
    "Documents Submitted": "#6a1b9a",
    "Under Review": "#e65100",
    "Approved": "#2e7d32",
    "Rejected": "#c62828",
    "Received Benefit": "#1b5e20"
}

STATUS_EMOJI = {
    "Not Applied": "⬜",
    "Applied": "📤",
    "Documents Submitted": "📋",
    "Under Review": "🔍",
    "Approved": "✅",
    "Rejected": "❌",
    "Received Benefit": "🎉"
}

if __name__ == "__main__":
    # Test the tracker
    print("Testing application tracker...\n")
    
    # Save test applications
    save_application("Varun", "PM Kisan Samman Nidhi", "6,000 per year", "https://pmkisan.gov.in")
    save_application("Varun", "Telangana Rythu Bandhu", "10,000 per acre", "Visit agriculture office")
    save_application("Varun", "Ayushman Bharat PM-JAY", "5 lakh health cover", "https://pmjay.gov.in")
    
    # Update status
    update_status(1, "Applied", "Applied online at pmkisan.gov.in")
    update_status(2, "Documents Submitted", "Submitted at local office")
    
    # Get applications
    apps = get_user_applications("Varun")
    print(f"Found {len(apps)} applications for Varun:\n")
    for app in apps:
        emoji = STATUS_EMOJI.get(app["status"], "⬜")
        print(f"{emoji} {app['scheme_name']}")
        print(f"   Status: {app['status']}")
        print(f"   Saved on: {app['date_saved']}")
        if app['date_applied']:
            print(f"   Applied on: {app['date_applied']}")
        print()
    
    print("✅ Tracker working!")