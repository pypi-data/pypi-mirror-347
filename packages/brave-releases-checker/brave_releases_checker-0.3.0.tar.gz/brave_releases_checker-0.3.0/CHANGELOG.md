# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-05-11
### Fixed
- **README.md file:** Corrected an issue in the README.md file that affected the display or interpretation of bash commands. This ensures that bash commands are now viewed as intended.
### Updated
- **Development status:** The project's development status has been updated to Beta. This indicates that the software is now in a beta testing phase, meaning it has most features implemented but may still contain bugs and undergo further refinement before a stable release.

## [0.2.1] - 2025-05-11
### Fixed
- **Subprocess execution error:** Resolved an issue that caused an error during the execution of the zypper output command check on openSUSE systems. This problem occurred when interacting with the zypper package management system and has now been fixed.

## [0.2.0] - 2025-05-11
### Fixed
- **Double load config:** Prevented the configuration from being loaded twice during startup.

## [0.1.9] - 2025-05-10
### Added
- **Dedicated Distribution Module:** Introduced a separate `distributions.py` module to handle the logic for detecting the installed Brave Browser version on different operating systems. This improves code organization and maintainability.
### Fixed
- **Fixed default arch:** Correct default architecture value if the config.ini file not set.

## [0.1.8] - 2025-05-10
### Fixed
- **Fixed for config path:** Corrected to check config.ini file if exists instead the path of the config.ini.
### Added
- **Default Configurations from `config.ini`:** Implemented support for automatically loading default values for command-line arguments from the `config.ini` configuration file.
- **List Available Releases Option (`--list`):** Added a new command-line parameter `--list` that allows users to display a detailed list of available releases, filtered according to other specified parameters (channel, architecture, file suffix).
- **Page Range Support (`--pages`):** Integrated the ability to specify a range of pages on the GitHub API to search for releases, using the `--pages` parameter (e.g., `--pages 1-5`).

## [0.1.7] - 2025-05-09
### Fixed
- **Fixed rpm return exit code:** Corrected the method for extracting the installed Brave Browser version from rpm and packages on openSUSE with zypper command.
- **Fixed find brave-browser:**  Corrected the method for extracting the installed Brave Browser version and package on archlinux and pacman package manager. 

## [0.1.6] - 2025-05-09
### Fixed
- **Fixed rpm return exit code:** Corrected the method for extracting the installed Brave Browser version from rpm packages on Fedora.
### Added
- **Added support:** Arch x86_64 for .rpm packages.
### Updated
- **Updated command:** Replaced command rpm with dnf to find the package installed and grab version.

## [0.1.5] - 2025-05-08
### Fixed
- Fixed Snap package version detection:** Corrected the method for extracting the installed Brave Browser version from Snap packages on Ubuntu, ensuring accurate version retrieval when Brave is installed via Snap.

## [0.1.4] - 2025-05-08
### Added
- **Added Snap support for Ubuntu:** Implemented functionality to detect the installed Brave Browser version on Ubuntu systems where it is installed as a Snap package. The tool will now attempt to retrieve the version using `snap info brave` if the standard Debian package check (`dpkg`) fails.

## [0.1.3] - 2025-05-08
### Changed
- **Refactored Configuration Handling:** Configuration settings are now managed through a dedicated `config.py` file, utilizing `dataclasses` for structured configuration. The `load_config` function handles reading from `config.ini` files in `/etc/brave-releases-checker/` or `~/.config/brave-releases-checker/`. This change improves code organization, readability, and maintainability by centralizing configuration logic.

### Added
- Introduced a `Colors` `dataclass` within `config.py` to manage ANSI escape codes for terminal colors and styles, enhancing the visual output of the application.
- **Added `--version` option:** Implemented a command-line option to display the current version of the Brave Releases Checker.

## [0.1.2] - 2025-05-08
### Fixed
- Fixed an issue where the 'brc' console script was not being correctly registered during installation.

## [0.1.1] - 2025-05-07
### Fixed
- Fixed an issue where the 'brc' console script was not being correctly registered during installation.

## [0.1.0] - 2025-05-07
### Added
- Initial release of Brave Releases Checker on PyPI.
- Support for checking stable, beta, and nightly releases.
- Ability to filter by architecture (e.g., x64).
- Reading configuration from `config.ini` (in `/etc/brave-releases-checker/` or `~/.config/brave-releases-checker/`).
- Provision of `brc` console script for command-line usage.
