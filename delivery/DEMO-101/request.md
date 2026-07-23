# DEMO-101: Add personalized greetings

Status: Approved for future live-demo implementation

## Work request

Add personalized greetings. The UI should accept a name, the API should accept
the name safely, and the resulting greeting should be recorded in the database
without breaking the default Hello World behavior.

## Acceptance criteria

- The presentation tier accepts an optional name and communicates loading,
  success, validation, and service-error states accessibly.
- The application tier safely validates the name and returns a personalized
  greeting when one is supplied.
- The data tier records the resulting personalized greeting.
- An unnamed request retains the baseline `Hello, world!` behavior.
- Tests cover normal, default, invalid, and failure paths across affected
  tiers.
- No credentials, personal data, or production secrets are added.
- The governed workflow produces the plan, ADR, verification report, and
  machine-readable release evidence described in `outputs.md`.

## Scope boundary

This request is approved as the subject of the live demo. It is not implemented
in the repository baseline. Starting implementation still requires the
`governed-sdlc` workflow and every explicit approval checkpoint it defines.

