# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.0+  | :white_check_mark: |
| < 2.0.0 | :x:                |

## Security Features

Starting from version 2.0.0, normattiva2md implements the following security measures:

### URL Validation

- **Domain Whitelist**: Only URLs from `normattiva.it` and `www.normattiva.it` are accepted
- **HTTPS Only**: HTTP connections are rejected to prevent man-in-the-middle attacks
- **Scheme Validation**: URL parsing validates proper format and rejects malformed URLs

### Path Traversal Protection

- **Output Path Sanitization**: All file output paths are validated to prevent directory traversal attacks
- **Temp File Security**: Temporary files are created using Python's `tempfile` module with secure defaults
- **Forbidden Paths**: Attempts to write to system directories (`/etc`, `/sys`) are blocked

### File Size Limits

- **Maximum File Size**: XML files larger than 50MB are rejected
- **Download Size Check**: HTTP responses are checked for size before downloading
- **Local File Validation**: Local XML files are validated before parsing

### Network Security

- **SSL Certificate Verification**: All HTTPS connections verify SSL certificates (`verify=True`)
- **Proper User-Agent**: Tool identifies itself as `normattiva2md/version` instead of impersonating browsers
- **Timeout Protection**: All network requests have a 30-second timeout
- **Session Cleanup**: HTTP sessions are properly managed and cleared

### XML Bomb Protection

- **File Size Pre-Check**: Files are size-checked before XML parsing
- **Entity Expansion**: Limited by file size constraints
- **Memory Protection**: Size limits prevent memory exhaustion attacks

## Validated Domains

The tool only accepts URLs from:

- `https://www.normattiva.it`
- `https://normattiva.it`

Any other domain will be rejected with an error message.

## Reporting a Vulnerability

If you discover a security vulnerability in normattiva2md, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Send an email to the maintainers with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

3. Wait for acknowledgment (we aim to respond within 48 hours)
4. Allow time for a patch to be developed and released
5. Coordinate disclosure timeline with maintainers

## Security Best Practices for Users

When using normattiva2md:

1. **Always use HTTPS URLs**: Never use HTTP links to normattiva.it
2. **Verify Sources**: Only process XML files from trusted sources
3. **Check File Sizes**: Be cautious with unusually large XML files
4. **Use Latest Version**: Always update to the latest version for security fixes
5. **Validate Output**: Review generated Markdown files, especially from untrusted sources
6. **Sandbox Processing**: Consider running in isolated environments for untrusted inputs

## Changelog

### Version 2.0.0 (2025-12-03)

**Security Fixes:**
- Added URL domain validation and HTTPS enforcement
- Implemented path traversal protection
- Added file size limits (50MB max)
- Enabled SSL certificate verification
- Changed User-Agent to proper tool identification
- Replaced manual temp file naming with `tempfile` module
- Removed dead code that could cause maintenance issues

## Dependencies

normattiva2md has minimal dependencies to reduce attack surface:

- `requests>=2.25.0` - HTTP library with security features
- Python 3.7+ standard library

No external XML parsing libraries are used (uses standard library `xml.etree.ElementTree`).

## Acknowledgments

We thank security researchers and users who responsibly disclose vulnerabilities to help keep Akoma2MD secure.
