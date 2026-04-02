#!/usr/bin/env python3
"""
templates.json validator - Geliştirilmiş Versiyon
"""

import json
import sys


def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print("FAIL: %s gecerli JSON degil: %s" % (path, e))
        sys.exit(1)
    except FileNotFoundError:
        print("FAIL: %s bulunamadi" % path)
        sys.exit(1)


def validate_format(data):
    errors = []
    warnings = []

    if not isinstance(data, list):
        return ["templates.json bir array olmali"], []

    if len(data) == 0:
        return [], ["templates.json bos, ama gecerli"]

    template_names = []
    # FieldType 11 ve 12 listeye eklendi
    valid_types = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    for i, tmpl in enumerate(data):
        prefix = "Template[%d]" % i

        if not isinstance(tmpl, dict):
            errors.append("%s: obje olmali" % prefix)
            continue

        for key in ["name", "desc", "json"]:
            if key not in tmpl:
                errors.append("%s: '%s' alani zorunlu" % (prefix, key))

        if "name" not in tmpl:
            continue

        name = tmpl["name"]
        prefix = 'Template[%d] "%s"' % (i, name)

        if name in template_names:
            errors.append("%s: ayni isimde baska template var" % prefix)
        template_names.append(name)

        form = tmpl.get("json")
        if not isinstance(form, dict):
            errors.append("%s: json bir obje olmali" % prefix)
            continue

        # --- Sections ---
        sections = form.get("Sections", [])
        section_ids = set()
        if not isinstance(sections, list):
            errors.append("%s: json.Sections bir liste olmali" % prefix)
        else:
            for j, sec in enumerate(sections):
                sp = "%s Section[%d]" % (prefix, j)
                if "Id" not in sec:
                    errors.append("%s: Id zorunlu" % sp)
                else:
                    if sec["Id"] in section_ids:
                        errors.append("%s: duplicate Id" % sp)
                    section_ids.add(sec["Id"])
                if "Title" not in sec:
                    warnings.append("%s: Title eksik" % sp)

        # --- FormFields ---
        fields = form.get("FormFields", [])
        if not isinstance(fields, list) or len(fields) == 0:
            errors.append("%s: json.FormFields bos veya eksik" % prefix)
        else:
            field_ids = set()
            for j, field in enumerate(fields):
                fp = "%s Field[%d]" % (prefix, j)
                if not isinstance(field, dict):
                    errors.append("%s: obje olmali" % fp)
                    continue

                # ID Kontrolü
                if "Id" not in field:
                    errors.append("%s: Id zorunlu" % fp)
                else:
                    if field["Id"] in field_ids:
                        errors.append("%s: duplicate Id" % fp)
                    field_ids.add(field["Id"])

                # FieldType Kontrolü (1-12)
                if "FieldType" not in field:
                    errors.append("%s: FieldType zorunlu" % fp)
                elif field["FieldType"] not in valid_types:
                    errors.append("%s: FieldType %s gecersiz (1-12)" % (fp, field["FieldType"]))

                # SectionId Kontrolü (Opsiyonel hale getirildi)
                if "SectionId" in field:
                    # Eğer SectionId varsa, gerçekten mevcut bir section olmalı
                    if sections and field["SectionId"] not in section_ids:
                        errors.append("%s: Tanimlanan SectionId (%s) mevcut sectionlar arasinda bulunamadi" % (fp, field["SectionId"]))
                else:
                    # Eskiden hataydı, artık sadece bilgi amaçlı belki ileride lazım olur diye boş bıraktık
                    pass

                config = field.get("Config", {})
                if not isinstance(config, dict):
                    errors.append("%s: Config bir obje olmali" % fp)

                dep = field.get("DependsOn")
                if dep is not None:
                    if not isinstance(dep, dict):
                        errors.append("%s: DependsOn bir obje olmali" % fp)
                    elif "FieldId" not in dep:
                        errors.append("%s: DependsOn.FieldId zorunlu" % fp)

    return errors, warnings


def check_protection(old_data, new_data):
    errors = []
    old_map = {t["name"]: t for t in old_data if isinstance(t, dict) and "name" in t}
    new_map = {t["name"]: t for t in new_data if isinstance(t, dict) and "name" in t}

    for name in old_map:
        if name not in new_map:
            errors.append('"%s" silindi! Mevcut templateler silinemez.' % name)
        else:
            old_json = json.dumps(old_map[name].get("json", {}), sort_keys=True)
            new_json = json.dumps(new_map[name].get("json", {}), sort_keys=True)
            if old_json != new_json:
                errors.append('"%s" degistirildi! Mevcut templatelerin jsonu degistirilemez.' % name)

    return errors


def main():
    protect_mode = False
    old_path = None

    if "--protect" in sys.argv:
        idx = sys.argv.index("--protect")
        if idx + 1 < len(sys.argv):
            old_path = sys.argv[idx + 1]
            protect_mode = True
        else:
            print("FAIL: --protect icin eski dosya yolu gerekli")
            sys.exit(1)

    new_data = load_json("templates.json")
    errors, warnings = validate_format(new_data)

    if protect_mode and old_path:
        old_data = load_json(old_path)
        errors.extend(check_protection(old_data, new_data))

    if warnings:
        print("\nUYARILAR:")
        for w in warnings: print("  WARN: %s" % w)

    if errors:
        print("\nHATALAR:")
        for e in errors: print("  FAIL: %s" % e)
        print("\n%d hata bulundu." % len(errors))
        sys.exit(1)

    count = len(new_data) if isinstance(new_data, list) else 0
    print("OK: %d template, hepsi gecerli (FieldType 1-12 destekleniyor, SectionId opsiyonel)." % count)
    sys.exit(0)


if __name__ == "__main__":
    main()
