# 📄 REPORT.md – GITA GURU: Voice of Telugu, Powered by You

---

## 1.1. Team Information

| Name               | Role                         | Responsibilities                           |
|--------------------|------------------------------|--------------------------------------------|
| Yashwanth          | Project Lead/Product Manager | MVP scoping, user acquisition, team sync   |
| Amar               | Full-Stack Developer         | Streamlit app, backend integration         |
| Varshit            | AI Engineer                  | Speech-to-text models, AI scoring logic    |
| Shashank           | UX & Growth Strategist       | UI/UX flow, campaign design, partnerships  |
| Dipika             | QA & Testing Lead            | Beta testing, feedback loop, iterations    |

---

## 1.2. Application Overview – MVP Scope

**Project Name**: GITA GURU – A Community-Powered Telugu Corpus Builder

**Problem Statement**:  
Current AI models lack deep understanding of **regional dialects, intonations, and cultural semantics** in Indian languages, especially Telugu. We aim to bridge this gap through a **community-driven, devotional experience** that naturally generates high-quality, diverse speech and text datasets.

**MVP Objective (1 Week Sprint)**:
- A **Streamlit Web App** where users can:
  - View a Bhagavad Gita sloka (Unicode text + reference audio)
  - Upload **two audio recordings** per sloka:
    - Recitation in their **native dialect & tone**
    - Personal explanation in their **own words/slang**
  - Submit **age and region metadata**
- Offline-first considerations (local caching, compressed uploads)
- Minimal **Leaderboard or Contribution Tracker** for engagement

---

## 1.3. AI Integration Details

### AI Modules in MVP:
- **Open-Source ASR (Whisper/espnet)** for transcription validation (post-processing batch pipeline)
- **Pronunciation Scoring (Phase 2)** – Plan to use open-source phoneme alignment tools (like Gentle or MFA)
- **Paraphrase & Semantic Analysis (Phase 3)** – Leveraging BERT-based similarity scoring for user explanations
- **Future Scope**: Fine-tune Telugu LLMs and ASR models on the collected dataset to improve dialect recognition

All AI integrations strictly use **open-source models** and aim to contribute back cleaned datasets to the community.

---

## 1.4. Technical Architecture & Development

### Tech Stack:
- **Frontend**: Streamlit (Python)
- **Backend**: Supabase (Auth, Storage), Firebase (optional fallback)
- **AI Processing**: Whisper (batch), Coqui TTS (optional), MFA Alignment Tools
- **Database**: Supabase Postgres for metadata
- **Deployment**: Hugging Face Spaces (public deployment)

### Development Breakdown:
| Day | Focus                           | Deliverables                             |
|-----|----------------------------------|------------------------------------------|
| 1   | App scaffolding + UI Design      | Streamlit layout, sloka viewer           |
| 2   | File Upload Workflow             | Audio upload (2 files), metadata form    |
| 3   | Backend Integration              | Supabase connection, storage pipeline    |
| 4   | Offline-first Optimization       | Caching strategy, file size optimization |
| 5   | Contribution Tracker (Leaderboard)| Basic user progress display              |
| 6   | End-to-End Testing & Bug Fixes   | Functional MVP, deploy to HF Spaces      |
| 7   | Buffer / Stretch Features        | UI polish, fallback edge case handling   |

---

## 1.5. User Testing & Feedback (Week 2)

### Methodology:
- **Testers Recruited From**:
  - Local Telugu communities (WhatsApp, Telegram groups)
  - School/college students for dialect variation
  - Gita Chanting enthusiasts for quality recitations
- **Test Environment**:
  - Focus on **low-bandwidth testing scenarios**
  - Device diversity: Low-end smartphones to desktops
- **Testing Tasks**:
  - Complete sloka recording submission (recitation + explanation)
  - Measure upload success rates under weak internet
  - Provide feedback on UI clarity, upload speed, and audio quality

### Feedback Loop:
| Feedback Theme         | Insights Collected                                | Actions Taken                           |
|------------------------|---------------------------------------------------|-----------------------------------------|
| Upload Failures         | Large file issues in 2G connections               | Added local file compression, retries   |
| UI Confusion (Step Flow)| Users confused between Recitation & Explanation   | Introduced tooltips & visual cues       |
| Metadata Friction       | Too many fields discouraged quick contribution    | Kept only **Age & Region** as required  |
| Engagement Drop-off     | Users lacked immediate gratification              | Implemented “Your Contribution Count”   |

---

## 1.6. Project Lifecycle & Roadmap

### Week 1: Rapid Development Sprint
- **Objective**: Deploy a functional MVP on Hugging Face Spaces
- **Key Deliverables**:
  - Streamlit Web App with sloka viewer and upload workflow
  - Backend integration with Supabase
  - Offline-first optimization for weak internet regions

### Week 2: Beta Testing & Iteration Cycle
- **Objective**: Validate app performance in real-world low-bandwidth environments
- **Methodology**:
  - Recruit 50+ testers from Telugu-speaking regions
  - Execute structured feedback collection forms
  - Implement iteration cycles every 2 days based on feedback
- **Outcomes Expected**:
  - Optimized upload workflows
  - Enhanced UI clarity and engagement hooks

### Weeks 3-4: User Acquisition & Corpus Growth Campaign
- **Target Audience & Channels**:
  - Students, spiritual communities, and dialect clubs
  - WhatsApp broadcast groups, local influencers, community radio
- **Growth Strategy & Messaging**:
  - “Record Your Voice for Telugu” campaign with daily sloka challenges
  - Collaborations with local schools & Gita chanting forums
- **Execution & Results**:
  - Target: 500 unique contributors
  - Metrics: Total contributions, daily active users, dialect diversity stats

### Post-Internship Vision & Sustainability
- Scale the dataset to cover 500+ slokas across 1000+ contributors
- Integrate AI feedback tools for pronunciation and comprehension
- Build a community of language preservation ambassadors

---

## 2. Code Repository Submission
- Repository: [https://code.swecha.org/yash_1206/teamtejas]
- Contents:
  - README.md
  - CONTRIBUTING.md
  - CHANGELOG.md
  - requirements.txt
  - LICENSE
  - REPORT.md
  - Clean & well-structured codebase

---

# 🔒 End of Report
