# Audio Fingerprinting

## Setup Instructions

### 1. System Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) (for `pydub` to handle various file formats)

#### Install ffmpeg:

- **Ubuntu/Debian:**
  ```sh
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Mac (Homebrew):**
  ```sh
  brew install ffmpeg
  ```

- **Windows:**
  Download and install from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add ffmpeg to your PATH.

---

### 2. Project Setup

Clone or copy the files into a directory.
Create the following folder structure:

```
your_project/
│
├── app.py
├── db.py
├── fingerprint.py
├── peak_hash.py
├── requirements.txt
├── README.md
├── fingerprints.db  # (auto-created)
├── uploads/         # (create this)
└── templates/
      └── index.html
```

Create the folders:
```sh
mkdir uploads
mkdir templates
```

Place `index.html` in the `templates/` folder.

---

### 3. Install Python Dependencies

```sh
pip install -r requirements.txt
```

---

### 4. Run the Application

```sh
python app.py
```

Access the app at [http://localhost:5000](http://localhost:5000).

---

## Usage

- **Store Fingerprint:**
  Upload an audio file using the "Store Fingerprint" form. This will extract and store its unique audio hashes.

- **Query Audio:**
  Upload an audio file using the "Query Audio" form. The system will try to identify the file by matching audio fingerprints.

- Results (matches and scores) will be displayed on the web page.

---

## How It Works

- **Audio Preprocessing:**
  Converts audio to mono, resamples, normalizes, and computes a spectrogram.

- **Peak Finding:**
  Identifies local maxima (landmarks) in the spectrogram.

- **Hash Generation:**
  Each hash is generated from a pair of peaks (frequency, time difference), resulting in robust audio fingerprints.

- **Database:**
  Hashes are stored in SQLite for fast lookup.

- **Querying:**
  Incoming audio is processed the same way, and hashes are matched in the database to find the best candidate.

---