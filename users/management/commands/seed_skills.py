from django.core.management.base import BaseCommand

from users.models import Skill


class Command(BaseCommand):
    help = "Seed skills (with categories) into the database"

    def handle(self, *args, **kwargs):
        # (name, category) — categories match Skill.CATEGORY_CHOICES keys
        skills = [
            ("Flutter", "programming"),
            ("Django", "programming"),
            ("React", "programming"),
            ("Node.js", "programming"),
            ("MongoDB", "programming"),
            ("PostgreSQL", "programming"),
            ("Python", "programming"),
            ("TypeScript", "programming"),
            ("Vue.js", "programming"),
            ("Rust", "programming"),
            ("Go", "programming"),
            ("Docker", "programming"),
            ("Kubernetes", "programming"),
            ("AWS", "programming"),
            ("GraphQL", "programming"),
            ("SQL", "programming"),
            ("Git", "programming"),
            ("Ruby on Rails", "programming"),
            ("Tennis", "sports"),
            ("Yoga", "sports"),
            ("Guitar", "music"),
            ("Piano", "music"),
            ("Digital photography", "art"),
            ("Figure drawing", "art"),
            ("Spanish", "language"),
            ("French", "language"),
        ]

        created_count = 0
        updated_count = 0

        for name, category in skills:
            obj, created = Skill.objects.update_or_create(
                name=name,
                defaults={"category": category, "is_active": True},
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Skills synced: {created_count} created, {updated_count} updated "
                f"({len(skills)} total)."
            )
        )
