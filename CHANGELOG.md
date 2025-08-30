# 📋 Changelog

All notable changes to the Gita Guru project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Professional UI improvements with glassmorphism design
- Enhanced microphone recording interface
- Recent uploads tracking in sidebar
- Improved profile section with user contributions
- Hidden category selection for simplified UX
- Clean upload success messages

### Changed
- Refactored audio upload logic into reusable function
- Standardized API parameters for audio uploads
- Improved error handling and user feedback
- Enhanced CSS styling for better visual appeal

### Fixed
- Critical API call bug in explanation upload
- Indentation errors in upload button section
- String formatting issues in recording UI
- Category warning message display

## [0.1.0] - 2024-01-15

### Added
- Initial release of Gita Guru platform
- Complete Bhagavad Gita learning interface
- Audio recording and upload functionality
- User authentication system (password and OTP)
- Admin dashboard for content management
- Supabase integration for backend services
- Database schema for chapters and slokas
- Audio file management system
- Reference audio playback
- Telugu and English translations
- Progress tracking for users
- File upload support (MP3, WAV, OGG)
- Session state management
- Professional UI with custom CSS
- Responsive design for mobile devices

### Features
- **User Portal**: Complete learning interface with chapter/sloka selection
- **Audio Recording**: In-app recording with multiple library support
- **File Upload**: Support for external audio files
- **Authentication**: Secure login with phone number and OTP
- **Admin Dashboard**: Content management and submission review
- **Database Integration**: PostgreSQL with Supabase
- **Storage**: Audio file storage with Supabase Storage
- **API Client**: Comprehensive API integration for Swecha backend

### Technical Stack
- **Frontend**: Streamlit 1.47.0
- **Backend**: Python 3.9+
- **Database**: PostgreSQL (Supabase)
- **Storage**: Supabase Storage
- **Authentication**: Custom OTP system
- **Audio Libraries**: audio-recorder-streamlit, streamlit-mic-recorder, audiorecorder

### Dependencies
- supabase>=2.8.0,<3.0.0
- gotrue>=2.8.0,<3.0.0
- httpx>=0.27.0,<0.28.0
- streamlit==1.47.0
- python-dotenv==1.0.1
- pandas==2.2.1
- numpy==1.26.4
- audio-recorder-streamlit==0.0.10

## [0.0.1] - 2024-01-01

### Added
- Project initialization
- Basic project structure
- Development environment setup
- Initial documentation
- License (AGPLv3)

---

## 🔄 Migration Guide

### From 0.0.1 to 0.1.0
- Complete rewrite of the application
- New database schema required
- Environment variables need to be updated
- Supabase project setup required

### From 0.1.0 to Unreleased
- No breaking changes
- UI improvements are backward compatible
- Enhanced user experience with same functionality

---

## 📝 Release Notes

### Version 0.1.0
This is the first stable release of Gita Guru, providing a complete learning platform for the Bhagavad Gita. The platform includes all core features for audio learning, user management, and content administration.

### Version 0.0.1
Initial project setup with basic structure and documentation.

---

## 🐛 Known Issues

### Version 0.1.0
- Audio recording may not work on all browsers
- Large file uploads may timeout on slow connections
- Some mobile devices may have limited audio recording support

### Unreleased
- None currently known

---

## 🔮 Roadmap

### Upcoming Features
- [ ] Multi-language support (Hindi, Sanskrit)
- [ ] Advanced audio processing and analysis
- [ ] Social features (comments, ratings)
- [ ] Mobile app development
- [ ] Offline mode support
- [ ] Advanced analytics and reporting
- [ ] Integration with external learning platforms
- [ ] AI-powered pronunciation feedback

### Planned Improvements
- [ ] Performance optimization for large datasets
- [ ] Enhanced security features
- [ ] Better error handling and recovery
- [ ] Improved accessibility features
- [ ] Advanced search and filtering
- [ ] Export functionality for learning progress

---

## 🙏 Acknowledgments

### Version 0.1.0
- Bhagavad Gita text and translations
- Supabase team for backend services
- Streamlit team for the web framework
- All contributors and beta testers

### Version 0.0.1
- Initial project contributors
- Open source community

---

**🕉️ May the wisdom of the Bhagavad Gita continue to inspire our development journey!**
