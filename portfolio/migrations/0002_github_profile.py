from django.db import migrations


def add_profile_content(apps, schema_editor):
    profile = apps.get_model("portfolio", "Profile")
    project = apps.get_model("portfolio", "Project")
    if not profile.objects.exists():
        profile.objects.create(
            headline="Building for the web.",
            intro="I’m Alan Shaju, a senior software engineer working across full-stack development and application architecture.",
            about=(
                "I’m based in Thrissur, Kerala, India. My work spans full-stack development, "
                "scalable application architecture, and enterprise software. On GitHub, "
                "I’m exploring modular PHP frameworks and tooling for understanding large codebases."
            ),
            focus="Full stack · Application architecture",
        )
    project.objects.get_or_create(
        url="https://github.com/Alan2k2/CnA-Framework",
        defaults={
            "title": "CnA Framework",
            "description": "A modular PHP framework designed for APIs, web applications, and long-running workers.",
            "stack": "PHP · Application framework",
            "position": 10,
            "published": True,
        },
    )
    project.objects.get_or_create(
        url="https://github.com/Alan2k2/crispy-spork",
        defaults={
            "title": "crispy-spork",
            "description": "A framework-independent tool for PHP 8.4+ codebases that combines static analysis, architecture mapping, and change-impact analysis.",
            "stack": "PHP 8.4+ · Static analysis",
            "position": 20,
            "published": True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]
    operations = [migrations.RunPython(add_profile_content, migrations.RunPython.noop)]
