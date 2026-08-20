"""Exercises for course Module 08.

Start a local server from course/labs/browser-lab before running:

    python -m http.server 8000 --directory course/labs/browser-lab

Then run:

    pytest course/labs/test_browser_lab.py -q
"""

from pathlib import Path

from playwright.sync_api import expect


LAB_URL = "http://127.0.0.1:8000/index.html"


def test_form_submission(page):
    page.goto(LAB_URL)
    page.get_by_label("Name").fill("Christian")
    page.get_by_role("button", name="Save profile").click()
    expect(page.get_by_role("status")).to_have_text("Profile saved")


def test_confirm_dialog(page):
    page.goto(LAB_URL)
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete draft").click()
    expect(page.get_by_role("status")).to_have_text("Draft deleted")


def test_download(page, tmp_path: Path):
    page.goto(LAB_URL)
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Download file").click()
    download_info.value.save_as(tmp_path / download_info.value.suggested_filename)
    assert (tmp_path / "course-lab.txt").read_text() == "Playwright course download"


def test_upload(page, tmp_path: Path):
    fixture = tmp_path / "fixture.txt"
    fixture.write_text("course fixture")
    page.goto(LAB_URL)
    page.get_by_label("Upload fixture").set_input_files(fixture)
    expect(page.locator("#upload")).to_have_value("C:\\fakepath\\fixture.txt")


def test_popup(page):
    page.goto(LAB_URL)
    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="Open details").click()
    popup = popup_info.value
    expect(popup.get_by_role("heading", name="Details")).to_be_visible()
