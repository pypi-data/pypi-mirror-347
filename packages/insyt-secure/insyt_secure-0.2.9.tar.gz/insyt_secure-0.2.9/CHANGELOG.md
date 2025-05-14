# Changelog

All notable changes to the `insyt-secure` package will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and follows the format from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.9] - 2025-05-13

### Added
- DNS caching mechanism to improve resilience against DNS server outages
- Cached DNS resolutions are stored for up to 24 hours and used as fallback
- Initial release of version 0.2.6 