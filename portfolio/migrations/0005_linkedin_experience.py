from django.db import migrations


ROLES = [
    {
        "title": "Senior Software Development Engineer",
        "organization": "Nubicus Consultancy Services PVT. Ltd",
        "period": "Jun 2025 – Present",
        "location": "Kochi, Kerala, India · On-site",
        "description": "Full-time\nJava development and software construction.",
    },
    {
        "title": "Lead FullStack Engineer",
        "organization": "Nubicus Consultancy Services PVT. Ltd",
        "period": "Jan 2025 – Jun 2025",
        "location": "Kochi, Kerala, India · On-site",
        "description": (
            "Full-time\nDeveloped a ride-hailing app for Nubicus Consultancy using Flutter, "
            "Node.js (Express), MongoDB, and the Google Maps API. Skills include Flutter and project planning."
        ),
    },
    {
        "title": "Full Stack Engineer",
        "organization": "Nubicus Consultancy Services PVT. Ltd",
        "period": "Dec 2024 – Jan 2025",
        "location": "Kochi, Kerala, India · On-site",
        "description": "Developed a content management system using PHP and Laravel 9.",
    },
    {
        "title": "Full Stack Engineer",
        "organization": "Bold Legal",
        "period": "Oct 2024 – Dec 2024",
        "location": "Texas, United States · On-site",
        "description": "Full-time\nJava development and software construction.",
    },
    {
        "title": "Cyber Security Specialist",
        "organization": "Clazzo Innovations",
        "period": "May 2024 – Oct 2024",
        "location": "On-site",
        "description": "Full-time",
    },
]


def add_experience(apps, schema_editor):
    experience = apps.get_model("portfolio", "Experience")
    roles = experience.objects.using(schema_editor.connection.alias)
    for index, role in enumerate(ROLES, start=1):
        title = role["title"]
        organization = role["organization"]
        if not roles.filter(title__iexact=title, organization__iexact=organization).exists():
            roles.create(**role, position=index * 10, published=True)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0004_public_github_repositories")]
    operations = [migrations.RunPython(add_experience, migrations.RunPython.noop)]
