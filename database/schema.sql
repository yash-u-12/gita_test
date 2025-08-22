
-- =====================================
-- Enable UUID Extension
-- =====================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================
-- Drop existing policies and tables if needed
-- =====================================
DROP POLICY IF EXISTS "Users can manage own data" ON users;
DROP POLICY IF EXISTS "Users can manage own submissions" ON user_submissions;
DROP POLICY IF EXISTS "Anyone can read chapters" ON chapters;
DROP POLICY IF EXISTS "Anyone can read slokas" ON slokas;

-- =====================================
-- TABLE: CHAPTERS
-- =====================================
CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_number INTEGER UNIQUE NOT NULL,
    chapter_name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =====================================
-- TABLE: SLOKAS
-- =====================================
CREATE TABLE IF NOT EXISTS slokas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    sloka_number INTEGER NOT NULL,
    sloka_text_telugu TEXT NOT NULL,
    meaning_telugu TEXT NOT NULL,
    meaning_english TEXT NOT NULL,
    reference_audio_url TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(chapter_id, sloka_number)
);

-- =====================================
-- TABLE: USERS
-- =====================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =====================================
-- TABLE: USER SUBMISSIONS
-- =====================================
CREATE TABLE IF NOT EXISTS user_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    sloka_id UUID REFERENCES slokas(id) ON DELETE CASCADE,
    recitation_audio_url TEXT,
    explanation_audio_url TEXT,
    status TEXT CHECK (status IN ('Submitted', 'Approved', 'Rejected')) DEFAULT 'Submitted',
    admin_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- =====================================
-- DISABLE RLS for simplicity (enable later if needed)
-- =====================================
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_submissions DISABLE ROW LEVEL SECURITY;
ALTER TABLE chapters DISABLE ROW LEVEL SECURITY;
ALTER TABLE slokas DISABLE ROW LEVEL SECURITY;

-- =====================================
-- STORAGE SETUP
-- =====================================
-- Ensure audio bucket exists
INSERT INTO storage.buckets (id, name, public)
VALUES ('audio', 'audio', true)
ON CONFLICT (id) DO NOTHING;

-- Clear existing storage policies
DELETE FROM storage.policies WHERE bucket_id = 'audio';

-- Simple open storage policies for audio files
CREATE POLICY "Public can upload audio files"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'audio');

CREATE POLICY "Public can read audio files"
ON storage.objects FOR SELECT
USING (bucket_id = 'audio');

CREATE POLICY "Public can delete audio files"
ON storage.objects FOR DELETE
USING (bucket_id = 'audio');

CREATE POLICY "Public can update audio files"
ON storage.objects FOR UPDATE
USING (bucket_id = 'audio');

-- =====================================
-- CREATE INDEXES FOR PERFORMANCE
-- =====================================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_chapters_number ON chapters(chapter_number);
CREATE INDEX IF NOT EXISTS idx_slokas_chapter ON slokas(chapter_id, sloka_number);
CREATE INDEX IF NOT EXISTS idx_submissions_user ON user_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_sloka ON user_submissions(sloka_id);
