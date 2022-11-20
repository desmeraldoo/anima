# Changelog

## 0.2.0

- Remove auto-cap of Armor Value to accommodate Armor Values above 10
- `atk` and its dependencies now only report `"MISSED"` if the attack missed due to Absorption
  - Previously, it would report `"MISSED"` if the damage was perfectly nullfied by Armor without being reduced into the negative range

## 0.1.4

- Correct method of adding `tabulate` to dependencies in `pyproject.toml`

## 0.1.3

- Update project name to `anima-utils` to avoid conflict on PyPI

## 0.1.2

- Add `tabulate` to dependencies in `pyproject.toml`

## 0.1.1

- Update [documentation](README.md)

## 0.1.0

- Refurbish combo command to help with complicated multiattack scenarios

## 0.0.0

- Restructure repo into package form
- Add pre-commit hooks
- Introduce changelog
