# Module 08 — Browser capabilities

## Goal

Handle the browser behaviors that make real applications more than simple pages and buttons.

## Lesson

### Forms

Use user-facing labels and roles:

```python
page.get_by_label("First name").fill("Christian")
page.get_by_label("Country").select_option("NG")
page.get_by_role("checkbox", name="Subscribe").check()
page.get_by_role("button", name="Continue").click()
```

Test both valid and invalid input. For validation, assert the message and the control state. Avoid testing browser-native validation only if the product requirement is about custom messaging; otherwise your test may be checking the browser rather than the application.

### Dialogs

Register the handler before triggering the dialog:

```python
page.once("dialog", lambda dialog: dialog.accept())
page.get_by_role("button", name="Confirm delete").click()
```

If the dialog itself is the product behavior, assert its message before accepting it.

### Popups and tabs

```python
with page.expect_popup() as popup_info:
    page.get_by_role("link", name="Open receipt").click()
receipt = popup_info.value
expect(receipt.get_by_role("heading", name="Receipt")).to_be_visible()
```

Keep references to the right page. A test that asserts the original tab after clicking a link that opened a new tab may pass for the wrong reason.

### Frames

```python
payment = page.frame_locator("iframe[title='Payment form']")
payment.get_by_label("Card number").fill("test-only-value")
```

Never enter real payment details in a learning exercise. Use a local fixture or sandbox.

### Downloads

```python
with page.expect_download() as download_info:
    page.get_by_role("button", name="Export CSV").click()
download = download_info.value
assert download.suggested_filename.endswith(".csv")
download.save_as("test-results/export.csv")
```

### Uploads

```python
page.get_by_label("Avatar").set_input_files("fixtures/avatar.png")
```

Use repository fixture files, not personal documents.

### Keyboard, mouse, and drag-and-drop

Keyboard actions should describe a user need: pressing Enter to submit a form or Escape to close a dialog. Coordinate clicks should be rare because they are sensitive to viewport and layout. Use `drag_to` when an application exposes draggable elements and the behavior matters.

## Exercise

Create a local HTML lab under `course/projects/browser-lab/` with a form, a dialog button, a download link, an upload input, and a second-tab link. Write one test per behavior. Synchronize every event with its triggering action.

## Solution pattern

```python
with page.expect_popup() as popup_info:
    page.get_by_role("link", name="Open details").click()
new_page = popup_info.value
expect(new_page).to_have_url(re.compile("details"))
```

## Common mistakes

Do not attach an event listener after the action. Do not assume a new tab is the same `Page` object. Do not use coordinates when a role locator exists. Do not upload secrets or personal files.

## Checkpoint

You pass when you can test a form, accept a dialog, inspect a popup, access a frame, save a download, and upload a fixture file.
