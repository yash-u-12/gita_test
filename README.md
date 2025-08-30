# 🕉️ Gita Guru - Bhagavad Gita Learning Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47.0-red.svg)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green.svg)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-AGPLv3-orange.svg)](LICENSE)
[![Contributors](https://img.shields.io/badge/Contributors-Welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive full-stack learning platform for studying the Bhagavad Gita with interactive audio features, designed to make ancient wisdom accessible through modern technology.

## 🌟 Features

### 🎯 Core Features
- **📖 Complete Sloka Text** in Telugu with proper formatting
- **🎵 Reference Audio** for proper pronunciation and learning
- **📝 Dual Meanings** in Telugu and English for comprehensive understanding
- **📤 Interactive Learning** through audio submissions and practice
- **📊 Progress Tracking** with submission history and analytics
- **🔐 Secure Authentication** with OTP and password-based login
- **📱 Responsive Design** optimized for desktop and mobile devices

### 🎙️ Audio Features
- **In-App Recording** with multiple library support
- **File Upload** support for MP3, WAV, and OGG formats
- **Audio Preview** with duration and quality indicators
- **Chunked Upload** for large audio files
- **Real-time Processing** with progress indicators

### 👥 User Experience
- **Professional UI** with glassmorphism design
- **Intuitive Navigation** with chapter and sloka selection
- **Recent Uploads** tracking in sidebar
- **User Profile** with contribution statistics
- **Clean Interface** with minimal distractions

### 🔧 Technical Features
- **Modern Tech Stack** with Python 3.9+ and Streamlit
- **Database Integration** with PostgreSQL via Supabase
- **API Integration** with Swecha backend services
- **Session Management** for persistent user state
- **Error Handling** with user-friendly messages

### 🧪 Testing & Development
- **Comprehensive Testing** with pytest
- **Code Quality** with Black, Ruff, and MyPy
- **Type Safety** with full type annotations
- **Documentation** with detailed docstrings
- **CI/CD Ready** with proper project structure


### 🎯 For Users
- **📖 Complete Sloka Text** in Telugu with proper formatting
- **🎵 Reference Audio** for proper pronunciation and learning
- **📝 Dual Meanings** in Telugu and English for comprehensive understanding
- **📤 Interactive Learning** through audio submissions and practice
- **📊 Progress Tracking** with submission history and analytics
- **🔐 Secure Authentication** with OTP and password-based login
- **📱 Responsive Design** optimized for desktop and mobile devices

### 👨‍💼 For Admins
- **📋 Review Submissions** with audio playback and quality assessment
- **✅ Approve/Reject** user submissions with feedback
- **📝 Add Admin Notes** for detailed feedback and guidance
- **📊 View Statistics** and analytics for platform insights
- **🔧 Content Management** tools for chapters and slokas
- **👥 User Management** with contribution tracking
- **📈 Performance Monitoring** with detailed metrics

## 🛠️ Tech Stack

- **Backend**: Python, Supabase (PostgreSQL + Storage)
- **Frontend**: Streamlit
- **Database**: PostgreSQL (via Supabase)
- **Storage**: Supabase Storage
- **Authentication**: Email-based user system

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** installed on your system
- **Git** for version control
- **Supabase account** for backend services
- **Audio files** in MP3 format (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/gita-guru.git
   cd gita-guru
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit with your Supabase credentials
   nano .env
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app/login.py
   ```

### Test Login
For testing purposes, you can use:
- **Phone**: `+910000000000`
- **OTP**: `123456`

## 📁 Project Structure

```
gita-guru/
├── 📄 Project Files
│   ├── pyproject.toml                # Project configuration
│   ├── uv.lock                      # Dependency lock file
│   ├── requirements.txt             # Python dependencies
│   ├── .gitignore                   # Git ignore rules
│   └── config.py                    # Configuration settings
│
├── 📚 Documentation
│   ├── README.md                    # Project overview
│   ├── CONTRIBUTING.md              # Contribution guidelines
│   ├── CHANGELOG.md                 # Version history
│   ├── CODE_OF_CONDUCT.md           # Community guidelines
│   └── LICENSE                      # AGPLv3 license
│
├── 🖥️ IDE Configuration
│   └── .vscode/
│       ├── settings.json            # VS Code settings
│       ├── extensions.json          # Recommended extensions
│       ├── launch.json              # Debug configurations
│       └── tasks.json               # Build tasks
│
├── 🔧 GitLab Templates
│   └── .gitlab/
│       ├── issue_templates/         # Issue templates
│       └── merge_request_templates/ # MR templates
│
├── 🗄️ Database
│   ├── schema.sql                   # Database schema
│   └── db_utils.py                  # Database utilities
│
├── 🌐 Streamlit Applications
│   └── streamlit_app/
│       ├── main.py                  # Main application
│       ├── login.py                 # Authentication app
│       └── __init__.py              # Package init
│
├── 🔌 API Integration
│   ├── api_client.py                # Swecha API client
│   └── test_api_endpoints.py        # API tests
│
├── 🧪 Testing
│   ├── test_login.py                # Login tests
│   └── tests/                       # Test directory
│
├── 📁 Data & Assets
│   ├── data/                        # JSON data files
│   ├── attached_assets/             # Project assets
│   └── slokas/                      # Audio files
│
└── 🔧 Development Tools
    ├── .venv/                       # Virtual environment
    ├── __pycache__/                 # Python cache
    └── .github/                     # GitHub templates
```

## 🛠️ Development Setup

### Prerequisites
1. **Supabase Project**: Create a project at [supabase.com](https://supabase.com)
2. **Python 3.9+**: Ensure Python is installed
3. **Audio Files**: Place MP3 files in `slokas/` folder structure
4. **JSON Data**: Ensure chapter JSON files are available

### Development Tools

#### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .

# Run tests
pytest
```

#### VS Code Integration
- Install recommended extensions from `.vscode/extensions.json`
- Use provided launch configurations for debugging
- Access build tasks via `Ctrl+Shift+P` → "Tasks: Run Task"

#### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files
```

### Step 1: Clone and Install
```bash
# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup
1. Go to your Supabase project SQL editor
2. Copy and run the contents of `database/schema.sql`
3. This creates all necessary tables and indexes

### Step 3: Run Complete Setup
```bash
python setup.py
```

This script will:
- ✅ Install all dependencies
- ✅ Populate database with JSON data
- ✅ Upload all audio files to Supabase Storage
- ✅ Link audio URLs to database records

### Step 4: Launch Applications

**User Portal:**
```bash
streamlit run streamlit_app/user_portal.py
```

**Admin Dashboard:**
```bash
streamlit run streamlit_app/admin_dashboard.py
```

## 📖 Usage Guide

### For Users

1. **Browse Chapters**: Select any chapter from the dropdown
2. **Choose Slokas**: Pick specific slokas to study
3. **Listen & Learn**: Play reference audio and read meanings
4. **Practice**: Upload your own recitation and explanation
5. **Track Progress**: Monitor your submissions and feedback

### For Admins

1. **Access Dashboard**: Use password `admin123`
2. **Review Submissions**: Listen to user audio files
3. **Take Action**: Approve, reject, or add notes
4. **View Statistics**: Monitor platform usage

## 🔧 Manual Setup (Alternative)

If you prefer to run scripts individually:

### 1. Database Population
```bash
python scripts/db_populator.py
```

### 2. Audio Upload
```bash
python scripts/bulk_audio_uploader.py
```

### 3. Audio URL Updates
```bash
python scripts/db_audio_url_updater.py
```

## 📊 Database Schema

### Tables
- **chapters**: Chapter information (id, chapter_number, chapter_name)
- **slokas**: Sloka details (id, chapter_id, sloka_number, text, meanings, audio_url)
- **users**: User accounts (id, name, email)
- **user_submissions**: User audio submissions (id, user_id, sloka_id, audio_urls, status)

### Relationships
- Chapters → Slokas (one-to-many)
- Users → Submissions (one-to-many)
- Slokas → Submissions (one-to-many)

## 🎵 Audio File Structure

```
slokas/
├── 12/                    # Chapter 12
│   ├── 1.mp3             # Sloka 1
│   ├── 2.mp3             # Sloka 2
│   └── ...
├── 15/                    # Chapter 15
│   ├── 1.mp3
│   └── ...
└── 16/                    # Chapter 16
    ├── 1.mp3
    └── ...
```

## 📝 JSON Data Format

Each chapter JSON file should contain:
```json
[
  {
    "chapter": 12,
    "chapter_name": "భక్తియోగము",
    "sloka_number": "1",
    "sloka_text": "ఏవం సతతయుక్తా యే...",
    "telugu_meaning": "అర్జునుడు పలికెను...",
    "english_meaning": "Arjuna said...",
    "audio_link": ""  // Ignored - will be updated automatically
  }
]
```

## 🔒 Security Notes

- **Admin Password**: Change `admin123` in production
- **API Keys**: Store Supabase credentials securely
- **File Uploads**: Validate audio files before processing
- **User Data**: Implement proper authentication for production

## 🚀 Deployment

### Local Development
```bash
# Run user portal
streamlit run streamlit_app/user_portal.py --server.port 8501

# Run admin dashboard
streamlit run streamlit_app/admin_dashboard.py --server.port 8502
```

### Production Deployment
1. **Streamlit Cloud**: Deploy directly to Streamlit Cloud
2. **Heroku**: Use Procfile and requirements.txt
3. **AWS/GCP**: Containerize with Docker

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify Supabase URL and key in `config.py`
   - Check if database schema is created

2. **Audio Upload Failures**
   - Ensure audio files are valid MP3 format
   - Check Supabase Storage permissions
   - Verify file paths are correct

3. **Streamlit App Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)
   - Verify file paths and imports

### Debug Mode
```bash
# Run with debug output
python -u scripts/bulk_audio_uploader.py
```

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for detailed information on how to:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit code changes
- 🧪 Add tests

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

### 🙏 Spiritual Guidance
- **Bhagavad Gita** text and translations for spiritual wisdom
- Ancient scholars and commentators for their insights

### 🛠️ Technical Stack
- **Supabase** for backend services and database
- **Streamlit** for the web framework
- **Python** community for excellent libraries
- **Open Source** community for inspiration

### 👥 Community
- All contributors and users who make this project better
- Beta testers and feedback providers
- Documentation writers and reviewers

## 📞 Support & Community

### Getting Help
- 📖 **Documentation**: Check this README and [CONTRIBUTING.md](CONTRIBUTING.md)
- 🐛 **Bug Reports**: Use our [issue templates](.gitlab/issue_templates/)
- 💬 **Discussions**: Join our community discussions
- 📧 **Email**: For sensitive or private matters

### Community Guidelines
Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to understand our community standards and expectations.

## 🔮 Roadmap

### Upcoming Features
- [ ] Multi-language support (Hindi, Sanskrit)
- [ ] Advanced audio processing and analysis
- [ ] Social features (comments, ratings)
- [ ] Mobile app development
- [ ] Offline mode support
- [ ] AI-powered pronunciation feedback

### Planned Improvements
- [ ] Performance optimization for large datasets
- [ ] Enhanced security features
- [ ] Better error handling and recovery
- [ ] Improved accessibility features
- [ ] Advanced search and filtering

---

## 🕉️ Project Philosophy

Gita Guru is more than just a learning platform - it's a bridge between ancient wisdom and modern technology. Our mission is to make the profound teachings of the Bhagavad Gita accessible to everyone, everywhere, through innovative digital solutions.

**May the wisdom of the Bhagavad Gita guide your learning journey! 🕉️**

---

<div align="center">

**Made with ❤️ for the global spiritual community**

[![GitHub stars](https://img.shields.io/github/stars/your-username/gita-guru?style=social)](https://github.com/your-username/gita-guru)
[![GitHub forks](https://img.shields.io/github/forks/your-username/gita-guru?style=social)](https://github.com/your-username/gita-guru)
[![GitHub issues](https://img.shields.io/github/issues/your-username/gita-guru)](https://github.com/your-username/gita-guru/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/your-username/gita-guru)](https://github.com/your-username/gita-guru/pulls)

</div> 