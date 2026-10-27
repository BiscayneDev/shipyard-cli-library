# OpenTable reservation response: sanitized research note

The original live response capture was removed because it contained a per-reservation security token and reservation identifiers. Do not commit live reservation responses, guest details, confirmation numbers, cookies, or access tokens.

This fictional example preserves the shape only. It is not a working reservation and must not be sent to a service.

```json
{
  "reservationId": "fictional-reservation",
  "restaurantId": "fictional-restaurant",
  "reservationDateTime": "2000-01-01T12:00:00Z",
  "partySize": 2,
  "confirmationNumber": "FICTIONAL_CONFIRMATION",
  "securityToken": "FICTIONAL_NOT_A_CREDENTIAL",
  "reservationHash": "FICTIONAL_HASH"
}
```

The captured token belonged to a reservation response, not evidence of an account-level master API key. Current validity was not tested. Any future live research must sanitize output before storing it and must not create, modify, or cancel a real booking merely to test access.
