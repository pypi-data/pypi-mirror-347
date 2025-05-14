# Change log

[TOC]

## 1.7.0
- Added API to add/remove HTML symbol conversions (see #158)
- Added HTML symbol conversion API to Python bindings
- Fixed attribute parsing with whitespace around equals sign (see #159)
- Added full support for uppercase tags/attributes
- Supported whitespace around tag names
- Fixed issues with self-closing tags
- Improved performance
- Improved blockquote handling (see #157)

## 1.6.6
- Python: Fix wheels not uploaded

## 1.6.5
- Fix handling of `<br>` tags

## 1.6.4
- Fix handling of `<br>` tags outside of paragraphs (`<p>`)

## 1.6.3
- Update python dependencies, hopefully fixes (#133)

## 1.6.2
- Fix HTML entities not converted (see #131)

## 1.6.0

- Add option for soft line break
- Add option for hard line break
- Fix handling of self-closing tags
- Updated python package building (see #100)

## 1.5.4

- Fix crash (see #67)
- Add support for newer Python versions

## 1.5.3

- Make `blockquote` work correctly!
- Additional note for 1.5.2: Add Python 12 packages

## 1.5.2

- FIXED: Add `titile` support for images
- FIXED: Code got formatted (Spaces removed)
- Fixed some formatting issues (like a space infront of `!`)
- FIXED: Escaping of `*`, \`, and `\`
- Reduced memory usage
- Improved performance

## v1.5.1

- **~40% Performance Improvement**

## v1.5.0

- **Added a option to Format Markdown Tables**
- More tests
- Reworked cli program for better usability

## v1.4.4

- New release with Python 3.11 support/packages
- Updated internal dependencies

## v1.4.3

- Improved performance
- Updated 3rdparty tools (for creating python packages and creating releases)
- Fix code example

## v1.4.2

- Fixed windows release build are linked against debug libraries

## v1.4.1

- **Fixed <u>ALL</u> memory leaks**
- Fixed bugs(`html2md::Options::includeTitle` not working)
- Added more tests
- Documentation: Updated Doxygen to v1.9.6
- Include Windows to releases

## v1.4.0

- Improved CMake support massively!
- Fixed tests
- Added support for CMake 3.8
- Fix Python source package

## v1.3.0

**BREAKING CHANGES!**

- Renamed `Converter::Convert2Md` -> `Converter::convert()`
- Renamed `options` -> `Options`

## v1.2.2

- Fixed bug when calling `Convert2Md()` multiple times
- Corrected serval typos. Ignore the rest of the change log.

## v1.2.1

- Added missing python dependency

## v1.2.0

- **Added python bindings**
- Added new option: `includeTable`.

## v1.1.5

- Added more command line options to the executable

## v1.1.4

- Releases now include deb files

## v1.1.3

The user can now test his own Markdown files. Simply specify to the test program as argument.

## v1.1.2

- Add changes for v1.1.1
- Create releases when a new tag is added(automatically)

## v.1.1.1

- Fix windows build(by replacing get)

## v1.1.0

- Reworked command line program
- Renamed `AppendToMd` to `appendToMd`
- Renamed `AppendBlank` to `appendBlank`
- **Require *c++11* instead of *c++17*.** Only the tests require *c++17* now.
- Added more tests
- Fix typos in comments
- Improved documentation

## v1.0.1

- Fixed several bugs
- Added more tests: make test
- Updated documentation: make doc
- Added packaging: make package

## v1.0.0

Initial release. All basics work but `blockquote` needs a rework.

