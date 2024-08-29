import datetime
import typing

from jinja2 import Template


class Rule(typing.NamedTuple):
    host: list[str] | None
    comment: str


def read_rules() -> list[Rule]:
    rules: list[Rule] = []

    with open("rules.txt", "r+", encoding="utf-8") as fs:

        for line in fs:
            line = line.rstrip()

            if len(line) == 0:
                continue

            if line.startswith("#"):
                rules.append(Rule(None, line.lstrip("#").strip()))
            else:
                if "#" in line:
                    line = line.split("#")[0].strip()
                if len(line) == 0:
                    continue

                rules.append(Rule(line.split("|"), ""))

    return rules


def render(path: str, path_template: str, kargv: dict):
    with open(path_template, "r", encoding="utf-8") as fs:
        tmpl = Template(fs.read())

    with open(path, "w", encoding="utf-8") as fs:
        fs.truncate(0)
        fs.seek(0, 0)
        fs.write(tmpl.render(**kargv))


if __name__ == "__main__":
    now = (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y.%m.%d.%H.%M")
        + " (UTC)"
    )

    rules = read_rules()

    kargv = {
        "NOW": now,
        "RULES": rules,
    }

    render("filter.txt", "build/template/filter.txt", kargv)
