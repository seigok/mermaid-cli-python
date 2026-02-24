# CI Checklist

Use this checklist when setting up or validating CI for this repository.

## Environment

- [ ] Python installed (recommended: same major/minor as local dev)
- [ ] `venv` created and activated
- [ ] `pip`/`setuptools` up to date

## Dependencies

- [ ] Install runtime deps: `python -m pip install -r requirements.txt`
- [ ] Install test deps: `python -m pip install pytest`
- [ ] Install the package in editable mode: `python -m pip install -e . --no-build-isolation`

## Playwright Browsers

- [ ] Install Chromium for Playwright: `python -m playwright install chromium`

## Regression Test Suite

- [ ] Run all tests: `python -m pytest`
- [ ] Verify coverage of features against `tests/REGRESSION_SCENARIOS.md`

## Artifacts (Optional)

- [ ] Preserve `tests/.pytest_cache` on failure for debugging
