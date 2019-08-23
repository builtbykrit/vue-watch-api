from faker import Faker

from vue_plugins.models import VuePlugin


def create_vue_plugin(name, description=None):
    fake = Faker()
    if not description:
        description = fake.text()

    plugin = VuePlugin.objects.create(
        name=name,
        description=description,
        repo_url=fake.url(),
        repo_readme=fake.text(),
        repo_license_name=fake.word(),
        repo_num_open_issues=fake.pyint(max_value=200),
        has_demo=fake.boolean(),
        has_meaningful_tests=fake.boolean(),
        has_api_documented=fake.boolean(),
        has_ci=fake.boolean(),
        has_example_code=fake.boolean(),
        last_release_date=fake.date(),
        last_release_tag_name=fake.word(),
        num_commits_recently=fake.pyint(max_value=100),
        num_contributors=fake.pyint(max_value=100),
        num_downloads_recently=fake.pyint(max_value=10000),
        num_stars=fake.pyint(max_value=5000)
    )

    plugin.tags.add(fake.word(), fake.word())

    return plugin
