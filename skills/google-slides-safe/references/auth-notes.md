# Auth notes

## Supported auth modes

### service-account
Use when:
- automation runs in a controlled environment
- you can create decks in a shared Drive or shared folder
- you want to avoid browser OAuth login during automation

Requirements:
- service-account JSON file
- target Drive folder shared with the service account email if needed

### oauth
Use when:
- the deck must be created under a personal Google account
- the user is present to complete the browser consent flow

Requirements:
- OAuth client secret JSON
- writable token path

## Scope policy

Use only:
- Google Slides API
- Google Drive file scope (`drive.file`)

Avoid broad scopes unless explicitly justified.

## Safety checklist

Before first use:
1. Confirm the credential file path explicitly.
2. Run `auth-check`.
3. Confirm the resolved Google account email matches the intended account.
4. Create into a test folder first.
5. Export to PDF and sanity-check the output.
