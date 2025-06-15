| Test Case Name                  | Simulates                                |
| ------------------------------- | ---------------------------------------- |
| `messages_dont_match_falcon.c`  | Message altered after verification       |
| `signed_message_length_wrong.c` | Wrong `smlen` passed to verifier         |
| `trivial_forgery_possible.c`    | All signatures accepted as valid         |
| `verification_failure.c`        | All signatures rejected, even valid ones |
