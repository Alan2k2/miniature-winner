from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=100, default="Alan Shaju")
    headline = models.CharField(max_length=120, default="Building for the web.")
    intro = models.TextField(default="I’m Alan Shaju. This is my corner of the web for projects, experiments, and conversations about software.")
    about = models.TextField(default="I’m interested in building web applications that feel considered from the interface through to the backend.")
    github = models.URLField(default="https://github.com/Alan2k2")
    linkedin = models.URLField(default="https://www.linkedin.com/in/alanshaju2k2/")
    focus = models.CharField(max_length=150, default="React · Python · Django")

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    stack = models.CharField(max_length=180, blank=True)
    url = models.URLField(blank=True)
    position = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["position", "pk"]

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    emailed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Visit(models.Model):
    ip = models.GenericIPAddressField()
    city = models.CharField(max_length=120, blank=True)
    region = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    device = models.CharField(max_length=300, blank=True)
    referrer_host = models.CharField(max_length=253, blank=True)
    language = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Experience(models.Model):
    title = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    period = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["position", "pk"]

    def __str__(self):
        return f"{self.title} at {self.organization}"
