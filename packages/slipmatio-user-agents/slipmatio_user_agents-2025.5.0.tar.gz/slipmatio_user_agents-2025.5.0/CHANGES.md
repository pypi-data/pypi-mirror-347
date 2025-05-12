# Changelog

### Version 2025.5.0 ()

- Refactored project to use `uv`, moved CI to GitHub Actions.
- Upgraded `ua-parser` to version 1.0.0. Thanks @AndreyKlychnikov!
- Removed Python 2 compatibility code. Thanks @AndreyKlychnikov!

### Version 2.2.0 (2020-08-23)

- `ua-parser` >= 0.10.0 is required. Thanks @jnozsc!
- Added `get_device()`, `get_os()` and `get_browser()` instance methods
  to `UserAgent`. Thanks @rodrigondec!

### Version 2.1 (2020-02-08)

- `python-user-agents` now require `ua-parser>=0.9.0`. Thanks @jnozsc!
- Properly detect Chrome Mobile browser families. Thanks @jnozsc!

### Version 2.0 (2019-04-07)

- `python-user-agents` now require `ua-parser>=0.8.0`. Thanks @IMDagger!

### Version 1.1

- Fixes packaging issue

### Version 1.0

- Adds compatibility with `ua-parser` 0.4.0
- Access to more device information in `user_agent.device.brand` and `user_agent.device.model`

### Version 0.3.2

- Better mobile detection
- Better PC detection

### Version 0.3.1

- user_agent.is_mobile returns True when mobile spider is detected

### Version 0.3.0

- Added **str**/**unicode** methods for convenience of pretty string

### Version 0.2.0

- Fixed errors when running against newer versions if ua-parser
- Support for Python 3

### Version 0.1.1

- Added `is_bot` property
- Symbian OS devices are now detected as a mobile device

### Version 0.1

- Initial release

Developed by the cool guys at [Stamps](http://stamps.co.id).
