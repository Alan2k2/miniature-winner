from django.db import migrations


# Public repositories listed on Alan2k2's GitHub profile.
REPOSITORIES = [('miniature-winner', 'This portfolio, built with React and Django.', 'Python'),
 ('djangoproject', '', 'JavaScript'),
 ('Snakegame.org',
  'Snake Arcade is a browser version of the Java Swing project. It supports keyboard and touch '
  'controls, adjustable speed, pause and restart, and a best score saved in the browser.',
  'Java'),
 ('Quiz-game.py', '', 'JavaScript'),
 ('crispy-spork',
  'PHP Codebase Intelligence Engine A framework-independent static analysis, architecture mapping, risk '
  'intelligence, and change-impact platform for PHP 8.4+ repositories.',
  'PHP'),
 ('CnA-Framework',
  'CnA is designed as a complete modular PHP framework for APIs, web applications and long-running '
  'workers. It should offer a coherent developer experience without forcing every application to depend '
  '…',
  'PHP'),
 ('dreamdesignsinteriors.in', '', 'TypeScript'),
 ('mentor_machine_test',
  'An inventory and purchase-order management module built with Laravel 11.',
  'Blade'),
 ('partzoo', 'Partzoo mobile app connects clients to the workshops and the dealers....', 'C++ · Fork'),
 ('ai_watermark_remover', '', 'Python'),
 ('homeireland_website', '', 'Blade'),
 ('d-django-mywebsite', '', 'JavaScript'),
 ('my-website', '', 'JavaScript'),
 ('RidingBookingApp',
  'Uber-like ride-hailing app built with Flutter, Node.js (Express), MongoDB, and Google Maps API. '
  'Developed for Nubicus Consultancy by Alan Shaju.',
  'Dart'),
 ('noriton-ERP', '', 'PHP'),
 ('CMS-Laravel-9.0', 'A content management system built with Laravel 9.', 'Blade'),
 ('minutedesign', '', 'HTML'),
 ('minuteassignment', '', 'JavaScript'),
 ('minersafetydevice', 'An IoT project for coal miner safety using MQTT.', 'HTML'),
 ('erp-software', '', 'CSS'),
 ('minersafety-device', '', 'HTML'),
 ('infinitygroup', '', 'Hack'),
 ('tailweb', '', 'PHP'),
 ('Alan-shaju.com', '', 'HTML'),
 ('IPCSGlobal.com-Landingpage',
  'A landing page built for an IPCS Global technical assessment.',
  'JavaScript')]


def add_repositories(apps, schema_editor):
    project = apps.get_model("portfolio", "Project")
    projects = project.objects.using(schema_editor.connection.alias)
    for index, (name, description, stack) in enumerate(REPOSITORIES, start=1):
        url = f"https://github.com/Alan2k2/{name}"
        if not projects.filter(url__iexact=url).exists():
            projects.create(
                title=name,
                description=description,
                stack=stack,
                url=url,
                position=20 + index * 10,
                published=True,
            )


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0003_experience")]
    operations = [migrations.RunPython(add_repositories, migrations.RunPython.noop)]
