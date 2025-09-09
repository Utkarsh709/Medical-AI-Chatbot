# AI Doctor - Medical Conversational Assistant

An intelligent medical chatbot that combines voice interaction, image analysis, and conversational AI to provide basic medical guidance and information.

## ⚠️ Important Medical Disclaimer

**This application is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers for any medical concerns.**

## Features

- **Voice Input**: Record patient voice queries using microphone
- **Speech-to-Text**: Convert audio to text using Groq's Whisper model
- **Image Analysis**: Analyze medical images/photos using Vision Language Models
- **Text-to-Speech**: Respond with natural voice using gTTS or ElevenLabs
- **Conversational AI**: Powered by Meta's Llama model via Groq API

## Project Structure

```
AI_DOCTOR/
├── voice_input.py          # Patient voice recording and transcription
├── voice_output.py         # Doctor voice synthesis and audio playback  
├── medical_brain.py        # Core AI processing and image analysis
├── patient_voice.mp3       # Recorded patient audio (generated)
├── doctor_response.mp3     # Generated doctor response (generated)
└── README.md              # This file
```

## Components

### 1. Voice Input (`voice_input.py`)
- Records audio from microphone using `speech_recognition`
- Converts audio to MP3 format using `pydub`
- Transcribes speech to text using Groq's Whisper model
- Handles ambient noise adjustment and timeout settings

### 2. Voice Output (`voice_output.py`) 
- **gTTS Integration**: Free text-to-speech using Google TTS
- **ElevenLabs Integration**: Premium voice synthesis with natural voices
- **Audio Playback**: Uses ffplay for cross-platform audio playback
- Supports multiple output formats and voice customization

### 3. Medical Brain (`medical_brain.py`)
- **Vision Analysis**: Processes medical images using Llama Vision model
- **Query Processing**: Handles text-based medical questions
- **Image Encoding**: Converts images to base64 for API processing
- **Response Generation**: Creates contextual medical responses

## Installation

### Prerequisites
- Python 3.8+
- ffmpeg (for audio processing)
- Microphone access
- Internet connection

### Install Dependencies
```bash
pip install speech-recognition pydub python-dotenv groq gtts elevenlabs
```

### System Requirements
- **Windows**: Install ffmpeg and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### API Keys Required:
1. **Groq API Key**: Sign up at [groq.com](https://groq.com) for Whisper and Llama access
2. **ElevenLabs API Key** (Optional): For premium voice synthesis at [elevenlabs.io](https://elevenlabs.io)

## Usage

### Basic Voice Interaction
```python
from voice_input import record_audio, transcribe_with_groq
from voice_output import text_to_speech_with_gtts

# Record patient voice
record_audio("patient_voice.mp3")

# Transcribe to text
patient_query = transcribe_with_groq("whisper-large-v3", "patient_voice.mp3", GROQ_API_KEY)

# Generate doctor response
text_to_speech_with_gtts("Based on your symptoms...", "doctor_response.mp3")
```

### Image Analysis
```python
from medical_brain import encode_image, analyze_image_with_query

# Encode image
encoded_image = encode_image("medical_photo.jpg")

# Analyze with query
result = analyze_image_with_query(
    "What do you see in this medical image?", 
    "meta-llama/llama-4-scout-17b-16e-instruct",
    encoded_image
)
```

## Models Used

- **Speech-to-Text**: Whisper Large V3 (via Groq)
- **Vision Analysis**: Meta Llama 4 Scout 17B (via Groq)  
- **Text-to-Speech**: 
  - gTTS (Google Text-to-Speech)
  - ElevenLabs TTS (Premium option)

## Limitations

- **Not for Emergency Use**: Cannot handle medical emergencies
- **General Information Only**: Provides educational content, not diagnosis
- **Internet Required**: All AI processing happens via cloud APIs
- **Audio Quality**: Dependent on microphone and environment
- **Language Support**: Currently optimized for English

## Technical Specifications

- **Audio Format**: MP3 (128kbps)
- **Image Support**: JPEG, PNG (base64 encoded)
- **Timeout Settings**: 20 seconds for voice recording
- **Voice Models**: Multiple ElevenLabs voices available
- **API Rate Limits**: Subject to Groq and ElevenLabs limits

## Error Handling

The application includes comprehensive error handling for:
- Microphone access issues
- Network connectivity problems
- API rate limiting
- Audio processing errors
- File I/O operations

## Future Enhancements

- [ ] Multi-language support
- [ ] Medical history tracking
- [ ] Integration with medical databases
- [ ] Real-time conversation flow
- [ ] Mobile app development
- [ ] HIPAA compliance features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with local healthcare regulations and API terms of service.

## Support

For technical issues or questions:
- Check API documentation: [Groq Docs](https://docs.groq.com)
- Review error logs in console output
- Verify API key configuration
- Test microphone permissions

---

**Remember**: This is an educational AI project and should never replace professional medical consultation.
