#!/usr/bin/env python3
"""
Adds the "Support the Project" settings strings to every bundled localization.

The tweak ships an English string table plus 26 translations. `String.localized`
falls back to the English bundle when a key is missing from the active language,
so a missing key is never a crash - but a brand new user-facing row is exactly the
kind of thing that should be translated on day one rather than left to drift.

This script is idempotent: it only writes keys that are not already present, so it
is safe to re-run after adding another language to the table below.

Usage:
    python3 Scripts/add-support-strings.py [--check]
"""

import os
import subprocess
import sys

BUNDLE_DIR = os.path.join(
    "layout", "Library", "Application Support", "EeveeSpotify.bundle"
)

TITLE = "Support the Project"

SUBTITLE = (
    "Your contributions keep this tweak updated and help buy Hysan "
    "a courage potion for Elsa."
)

# Language code (the .lproj directory name, minus the extension) -> translations.
TRANSLATIONS = {
    "ar-EG": (
        "ادعم المشروع",
        "مساهماتك تُبقي هذا التعديل محدَّثًا وتساعد في شراء جرعة شجاعة لـ Hysan من أجل Elsa.",
    ),
    "az": (
        "Layihəni dəstəkləyin",
        "Kontribusiyalarınız bu tweak-in yenilənməsini saxlayır və Hysan-ə Elsa üçün cürət dərmanı almağa kömək edir.",
    ),
    "bg": (
        "Подкрепете проекта",
        "Вашите дарения поддържат тази модификация актуализирана и помагат да се купи бутилка смелост за Hysan заради Elsa.",
    ),
    "ca": (
        "Dona suport al projecte",
        "Les teves contribucions mantenen actualitzada aquesta modificació i ajuden a comprar a Hysan una poció de valor per a Elsa.",
    ),
    "da": (
        "Støt projektet",
        "Dine bidrag holder denne tweak opdateret og hjælper med at købe en livsgnist til Hysan til Elsa.",
    ),
    "de": (
        "Projekt unterstützen",
        "Deine Beiträge halten dieses Tweaks aktuell und helfen dabei, Hysan einen Mut-Trank für Elsa zu kaufen.",
    ),
    # Swiss German shares the German table.
    "de-CH": (
        "Projekt unterstützen",
        "Deine Beiträge halten dieses Tweaks aktuell und helfen dabei, Hysan einen Mut-Trank für Elsa zu kaufen.",
    ),
    "es": (
        "Apoya el proyecto",
        "Tus aportaciones mantienen actualizada esta modificación y ayudan a comprarle a Hysan una poción de valor para Elsa.",
    ),
    "fa": (
        "از پروژه حمایت کنید",
        "مشارکت شما این تغییرات را به‌روز نگه می‌دارد و کمک می‌کند Hysan برای Elsa یک معجون شجاعت بخرد.",
    ),
    "fr": (
        "Soutenir le projet",
        "Vos contributions permettent de mettre à jour ce tweak et aident Hysan à acheter une potion de courage pour Elsa.",
    ),
    "hr": (
        "Podrži projekt",
        "Vaši doprinosi održavaju ovaj tweak ažurnim i pomažu Hysanu kupiti napitak hrabrosti za Elsu.",
    ),
    "hu": (
        "Támogasd a projektet",
        "A hozzájárulásaid frissen tartják ezt a tweaket, és segítenek Hysannak bátorságitalt vásárolni Elzáért.",
    ),
    "it": (
        "Sostieni il progetto",
        "I tuoi contributi mantengono aggiornato questo tweak e aiutano Hysan a comprare una pozione di coraggio per Elsa.",
    ),
    "ja": (
        "プロジェクトを支援",
        "ご支援によってこの tweak の更新が続き、Hysan が Elsa 用の勇気のポーションを買う助けになります。",
    ),
    "ko": (
        "프로젝트 후원하기",
        "후원으로 이 tweak가 계속 업데이트되고 Hysan이 Elsa를 위한 용기 물약을 살 수 있도록 돕습니다.",
    ),
    "np": (
        "परियोजनालाई सहयोग गर्नुहोस्",
        "तपाईंको योगदानले यो tweak अद्यावधिक राख्छ र Hysan ले Elsa को लागि साहसको पोसन किन्न मद्दत गर्छ।",
    ),
    "pl": (
        "Wesprzyj projekt",
        "Twoje wkłady utrzymują ten mod aktualnym i pomagają Hysanowi kupić miksturę odwagi dla Elsy.",
    ),
    "pt": (
        "Apoia o projeto",
        "As tuas contribuições mantêm esta modificação atualizada e ajudam o Hysan a comprar uma poção de coragem para a Elsa.",
    ),
    "pt-BR": (
        "Apoie o projeto",
        "Suas contribuições mantêm este mod atualizado e ajudam o Hysan a comprar uma poção de coragem para a Elsa.",
    ),
    "ro": (
        "Sprijină proiectul",
        "Contribuțiile tale păstrează acest tweak la zi și îl ajută pe Hysan să cumpere un elixir de curaj pentru Elsa.",
    ),
    "ru": (
        "Поддержать проект",
        "Ваш вклад помогает обновлять этот твик и покупать Хисану зелье смелости для Эльзы.",
    ),
    "tr": (
        "Projeyi destekle",
        "Katkıların bu tweak'i güncel tutmaya ve Hysan'ın Elsa için bir cesaret iksiri almasına yardımcı olur.",
    ),
    "uk": (
        "Підтримати проєкт",
        "Ваш внесок допомагає оновлювати цей твік і купити Гисану зілля хоробрості для Ельзи.",
    ),
    "vi": (
        "Hỗ trợ dự án",
        "Đóng góp của bạn giúp tweak này được cập nhật và giúp Hysan mua một lọ thuốc dũng cảm cho Elsa.",
    ),
    "zh-CN": (
        "支持本项目",
        "你的支持让这个 tweak 持续更新，也帮 Hysan 给 Elsa 买一份勇气的药剂。",
    ),
    "zh-TW": (
        "支持本專案",
        "你的支持讓這個 tweak 持續更新，也幫 Hysan 幫 Elsa 買一份勇氣的藥水。",
    ),
}

# English is the source of truth and is written by hand; only used as a self-check.
REFERENCE = {
    "en": (
        TITLE,
        SUBTITLE,
    )
}

CHECK_ONLY = "--check" in sys.argv


def quoted(value):
    return '"%s"' % value.replace('"', '\\"')


def main():
    if not os.path.isdir(BUNDLE_DIR):
        sys.exit("error: %s not found - run this from the repository root" % BUNDLE_DIR)

    tables = dict(REFERENCE)
    tables.update(TRANSLATIONS)

    touched, missing, failed = [], [], []

    for lang in sorted(tables):
        title, subtitle = tables[lang]
        path = os.path.join(BUNDLE_DIR, "%s.lproj" % lang, "Localizable.strings")

        if not os.path.isfile(path):
            missing.append(lang)
            continue

        with open(path, encoding="utf-8") as handle:
            body = handle.read()

        if "support_the_project =" in body:
            continue

        block = (
            "\n// Support the Project, links to Ko-fi in EeveeSettingsView\n"
            "support_the_project = %s;\n"
            "support_the_project_description = %s;\n" % (quoted(title), quoted(subtitle))
        )

        if CHECK_ONLY:
            print("would add: %s" % lang)
            continue

        with open(path, "w", encoding="utf-8") as handle:
            handle.write(body.rstrip("\n") + "\n" + block)

        touched.append(lang)

    # Lint every table we may have written, including English.
    if not CHECK_ONLY:
        for lang in sorted(tables):
            path = os.path.join(BUNDLE_DIR, "%s.lproj" % lang, "Localizable.strings")
            if not os.path.isfile(path):
                continue
            result = subprocess.run(
                ["plutil", "-lint", path], capture_output=True, text=True
            )
            if result.returncode != 0:
                failed.append(lang)
                print(result.stdout.strip() or result.stderr.strip())

    print("updated: %d" % len(touched))
    if touched:
        print("  " + ", ".join(touched))
    if missing:
        print("no table for: " + ", ".join(missing))
    if failed:
        sys.exit("plutil rejected: " + ", ".join(failed))


if __name__ == "__main__":
    main()
