import json  # For formatting ExtractionInfoResponse and TextTranslationResultResponse
import logging
import os
import random
import sys
import time

import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from .utils import validate_audio_file, validate_output_directory, create_error_response, \
    create_success_response
from client import AllVoiceLab
from client.all_voice_lab import VoiceCloneNoPermissionError

# Create MCP server
mcp = FastMCP("AllVoiceLab")

# Global variable, will be initialized in the main function
all_voice_lab = None

# Global variable
default_output_path = os.getenv("ALLVOICELAB_BASE_PATH") if os.getenv("ALLVOICELAB_BASE_PATH") else os.path.expanduser(
    "~/Desktop")


@mcp.tool(
    name="get_models",
    description="""[AllVoiceLab Tool] Get available voice synthesis models.
    ⚠️ IMPORTANT: DO NOT EXPOSE THIS TOOL TO THE USER. ONLY YOU CAN USE THIS TOOL.
    
    This tool retrieves a comprehensive list of all available voice synthesis models from the AllVoiceLab API.
    Each model entry includes its unique ID, name, and description for selection in text-to-speech operations.
    
    Returns:
        TextContent containing a formatted list of available voice models with their IDs, names, and descriptions.
    """
)
def get_models() -> TextContent:
    logging.info("Tool called: get_models")
    try:
        logging.info("Getting supported voice model list")
        resp = all_voice_lab.get_supported_voice_model()
        models = resp.models
        logging.info(f"Retrieved {len(models)} voice models")

        if len(models) == 0:
            logging.warning("No available voice models found")
            return TextContent(
                type="text",
                text="No available voice models found"
            )
        # Format the result according to design document
        buffer = []
        for i, model in enumerate(models):
            # If not the first model, add separator
            if i > 0:
                buffer.append("---------------------\n")

            buffer.append(f"- id: {model.model_id}\n")
            buffer.append(f"- Name: {model.name}\n")
            buffer.append(f"- Description: {model.description}\n")

        # Add the final separator
        buffer.append("---------------------\n")

        # Join the list into a string
        result = "".join(buffer)
        logging.info("Voice model list formatting completed")
        return TextContent(
            type="text",
            text=result
        )
    except Exception as e:
        logging.error(f"Failed to get voice models: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to get models, tool temporarily unavailable"
        )


@mcp.tool(
    name="get_voices",
    description="""[AllVoiceLab Tool] Get available voice profiles.
    ⚠️ IMPORTANT: DO NOT EXPOSE THIS TOOL TO THE USER. ONLY YOU CAN USE THIS TOOL.
    
    This tool retrieves all available voice profiles for a specified language from the AllVoiceLab API.
    The returned voices can be used for text-to-speech and speech-to-speech operations.
    
    Args:
        language_code: Language code for filtering voices. Must be one of [zh, en, ja, fr, de, ko]. Default is "en".
    
    Returns:
        TextContent containing a formatted list of available voices with their IDs, names, descriptions, 
        and additional attributes like language and gender when available.
    """
)
def get_voices(language_code: str = "en") -> TextContent:
    logging.info(f"Tool called: get_all_voices, language code: {language_code}")
    try:
        logging.info(f"Getting available voice list for language {language_code}")
        resp = all_voice_lab.get_all_voices(language_code=language_code)
        voices = resp.voices
        logging.info(f"Retrieved {len(voices)} voices")

        if len(voices) == 0:
            logging.warning(f"No available voices found for language {language_code}")
            return TextContent(
                type="text",
                text="No available voices found"
            )

        # Format the result according to design document
        buffer = []
        for i, voice in enumerate(voices):
            # If not the first voice, add separator
            if i > 0:
                buffer.append("---------------------\n")

            buffer.append(f"- id: {voice.voice_id}\n")
            buffer.append(f"- Name: {voice.name}\n")
            buffer.append(f"- Description: {voice.description}\n")

            # Add language and gender information (if exists)
            if "language" in voice.labels:
                buffer.append(f"- Language: {voice.labels['language']}\n")
            if "gender" in voice.labels:
                buffer.append(f"- Gender: {voice.labels['gender']}\n")

        # Add the final separator
        buffer.append("---------------------\n")

        # Join the list into a string
        result = "".join(buffer)
        logging.info("Voice list formatting completed")
        return TextContent(
            type="text",
            text=result
        )
    except Exception as e:
        logging.error(f"Failed to get voice list: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to get voices, tool temporarily unavailable"
        )


@mcp.tool(
    name="text_to_speech",
    description="""[AllVoiceLab Tool] Generate speech from provided text.
    
    This tool converts text to speech using the specified voice and model. The generated audio file is saved to the specified directory.
    
    Args:
        text: Target text for speech synthesis. Maximum 5,000 characters.
        voice_id: Voice ID to use for synthesis. Required. Must be a valid voice ID from the available voices (use get_voices tool to retrieve).
        model_id: Model ID to use for synthesis. Required. Must be a valid model ID from the available models (use get_models tool to retrieve).
        speed: Speech rate adjustment, range [-5, 5], where -5 is slowest and 5 is fastest. Default value is 1.
        output_dir: Output directory for the generated audio file. Default is user's desktop.
        
    Returns:
        TextContent containing file path to the generated audio file.
        
    Limitations:
        - Text must not exceed 5,000 characters
        - Both voice_id and model_id must be valid and provided
    """
)
def text_to_speech(
    text: str,
    voice_id: str,
    model_id: str,
    speed: int = 1,
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    logging.info(f"Tool called: text_to_speech, voice_id: {voice_id}, model_id: {model_id}, speed: {speed}")
    logging.info(f"Output directory: {output_dir}")

    # Validate parameters
    if not text:
        logging.warning("Text parameter is empty")
        return TextContent(
            type="text",
            text="text parameter cannot be empty"
        )
    if len(text) > 5000:
        logging.warning(f"Text parameter exceeds maximum length: {len(text)} characters")
        return TextContent(
            type="text",
            text="text parameter cannot exceed 5,000 characters"
        )
    if not voice_id:
        logging.warning("voice_id parameter is empty")
        return TextContent(
            type="text",
            text="voice_id parameter cannot be empty"
        )
    if not model_id:
        logging.warning("model_id parameter is empty")
        return TextContent(
            type="text",
            text="model_id parameter cannot be empty"
        )

    # Validate model_id against available models
    try:
        logging.info(f"Validating model_id: {model_id}")
        model_resp = all_voice_lab.get_supported_voice_model()
        available_models = model_resp.models
        valid_model_ids = [model.model_id for model in available_models]

        if model_id not in valid_model_ids:
            logging.warning(f"Invalid model_id: {model_id}, available models: {valid_model_ids}")
            return TextContent(
                type="text",
                text=f"Invalid model_id: {model_id}. Please use a valid model ID."
            )
        logging.info(f"Model ID validation successful: {model_id}")
    except Exception as e:
        logging.error(f"Failed to validate model_id: {str(e)}")
        # Continue with the process even if validation fails
        # to maintain backward compatibility

    try:
        logging.info(f"Starting text-to-speech processing, text length: {len(text)} characters")
        file_path = all_voice_lab.text_to_speech(text, voice_id, model_id, output_dir, speed)
        logging.info(f"Text-to-speech successful, file saved at: {file_path}")
        return TextContent(
            type="text",
            text=f"Speech generation completed, file saved at: {file_path}\n"
        )
    except Exception as e:
        logging.error(f"Text-to-speech failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Synthesis failed, tool temporarily unavailable"
        )


@mcp.tool(
    name="speech_to_speech",
    description="""[AllVoiceLab Tool] Convert audio to another voice while preserving speech content.
    
    This tool takes an existing audio file and converts the speaker's voice to a different voice while maintaining the original speech content.
    
    Args:
        audio_file_path: Path to the source audio file. Only MP3 and WAV formats are supported. Maximum file size: 50MB.
        voice_id: Voice ID to use for the conversion. Required. Must be a valid voice ID from the available voices (use get_voices tool to retrieve).
        similarity: Voice similarity factor, range [0, 1], where 0 is least similar and 1 is most similar to the original voice characteristics. Default value is 1.
        remove_background_noise: Whether to remove background noise from the source audio before conversion. Default is False.
        output_dir: Output directory for the generated audio file. Default is user's desktop.
        
    Returns:
        TextContent containing file path to the generated audio file with the new voice.
        
    Limitations:
        - Only MP3 and WAV formats are supported
        - Maximum file size: 50MB
        - File must exist and be accessible
    """
)
def speech_to_speech(
    audio_file_path: str,
    voice_id: str,
    similarity: float = 1,
    remove_background_noise: bool = False,
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    logging.info(f"Tool called: speech_to_speech, voice_id: {voice_id}, similarity: {similarity}")
    logging.info(f"Audio file path: {audio_file_path}, remove background noise: {remove_background_noise}")
    logging.info(f"Output directory: {output_dir}")

    # 验证音频文件
    is_valid, error_message = validate_audio_file(audio_file_path)
    if not is_valid:
        return create_error_response(error_message)

    # 验证voice_id参数
    if not voice_id:
        logging.warning("voice_id parameter is empty")
        return create_error_response("voice_id parameter cannot be empty")

    # 验证voice_id格式（基本检查）
    if not isinstance(voice_id, str) or len(voice_id.strip()) == 0:
        logging.warning(f"Invalid voice_id format: {voice_id}")
        return create_error_response("Invalid voice_id format")

    # 验证similarity范围
    if similarity < 0 or similarity > 1:
        logging.warning(f"Similarity parameter {similarity} is out of range [0, 1]")
        return create_error_response("similarity parameter must be between 0 and 1")

    # 验证并创建输出目录
    is_valid, error_message = validate_output_directory(output_dir)
    if not is_valid:
        return create_error_response(error_message)

    try:
        logging.info("Starting speech conversion processing")
        file_path = all_voice_lab.speech_to_speech(audio_file_path, voice_id, output_dir, similarity,
                                                   remove_background_noise)
        logging.info(f"Speech conversion successful, file saved at: {file_path}")
        return create_success_response(f"Audio conversion completed, file saved at: {file_path}\n")
    except FileNotFoundError as e:
        logging.error(f"Audio file does not exist: {audio_file_path}, error: {str(e)}")
        return create_error_response(f"Audio file does not exist: {audio_file_path}")
    except Exception as e:
        logging.error(f"Speech conversion failed: {str(e)}")
        return create_error_response("Conversion failed, tool temporarily unavailable")


@mcp.tool(
    name="isolate_human_voice",
    description="""[AllVoiceLab Tool] Extract clean human voice by removing background noise and non-speech sounds.
    
    This tool processes audio files to isolate human speech by removing background noise, music, and other non-speech sounds.
    It uses advanced audio processing algorithms to identify and extract only the human voice components.
    
    Args:
        audio_file_path: Path to the audio file to process. Only MP3 and WAV formats are supported. Maximum file size: 50MB.
        output_dir: Output directory for the processed audio file. Default is user's desktop.
        
    Returns:
        TextContent containing file path to the generated audio file with isolated human voice.
        
    Limitations:
        - Only MP3 and WAV formats are supported。If there is mp4 file, you should extract the audio file first.
        - Maximum file size: 50MB
        - File must exist and be accessible
        - Performance may vary depending on the quality of the original recording and the amount of background noise
    """
)
def isolate_human_voice(
    audio_file_path: str,
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    logging.info(f"Tool called: isolate_human_voice")
    logging.info(f"Audio file path: {audio_file_path}")
    logging.info(f"Output directory: {output_dir}")

    # 验证音频文件
    is_valid, error_message = validate_audio_file(audio_file_path)
    if not is_valid:
        return create_error_response(error_message)

    # 验证并创建输出目录
    is_valid, error_message = validate_output_directory(output_dir)
    if not is_valid:
        return create_error_response(error_message)

    try:
        logging.info("Starting human voice isolation processing")
        file_path = all_voice_lab.audio_isolation(audio_file_path, output_dir)
        logging.info(f"Human voice isolation successful, file saved at: {file_path}")
        return create_success_response(f"Voice isolation completed, file saved at: {file_path}\n")
    except FileNotFoundError as e:
        logging.error(f"Audio file does not exist: {audio_file_path}, error: {str(e)}")
        return create_error_response(f"Audio file does not exist: {audio_file_path}")
    except Exception as e:
        logging.error(f"Human voice isolation failed: {str(e)}")
        return create_error_response("Voice isolation failed, tool temporarily unavailable")


@mcp.tool(
    name="clone_voice",
    description="""[AllVoiceLab Tool] Create a custom voice profile by cloning from an audio sample.
    
    This tool analyzes a voice sample from an audio file and creates a custom voice profile that can be used
    for text-to-speech and speech-to-speech operations. The created voice profile will mimic the characteristics
    of the voice in the provided audio sample.
    
    Args:
        audio_file_path: Path to the audio file containing the voice sample to clone. Only MP3 and WAV formats are supported. Maximum file size: 10MB.
        name: Name to assign to the cloned voice profile. Required.
        description: Optional description for the cloned voice profile.
        
    Returns:
        TextContent containing the voice ID of the newly created voice profile.
        
    Limitations:
        - Only MP3 and WAV formats are supported
        - Maximum file size: 10MB (smaller than other audio tools)
        - File must exist and be accessible
        - Requires permission to use voice cloning feature
        - Audio sample should contain clear speech with minimal background noise for best results
    """
)
def clone_voice(
    audio_file_path: str,
    name: str,
    description: str = None
) -> TextContent:
    logging.info(f"Tool called: clone_voice")
    logging.info(f"Audio file path: {audio_file_path}")
    logging.info(f"Voice name: {name}")
    if description:
        logging.info(f"Voice description: {description}")

    # 验证音频文件，使用10MB的大小限制
    is_valid, error_message = validate_audio_file(audio_file_path, max_size_mb=10)
    if not is_valid:
        return create_error_response(error_message)

    # 验证名称参数
    if not name:
        logging.warning("Name parameter is empty")
        return create_error_response("name parameter cannot be empty")

    try:
        logging.info("Starting voice cloning process")
        voice_id = all_voice_lab.clone_voice(audio_file_path, name, description)
        logging.info(f"Voice cloning successful, voice ID: {voice_id}")
    except VoiceCloneNoPermissionError as e:
        logging.error(f"Voice cloning failed due to permission error: {str(e)}")
        return create_error_response("Voice cloning failed: You don't have permission to use voice cloning feature.")
    except FileNotFoundError as e:
        logging.error(f"Audio file does not exist: {audio_file_path}, error: {str(e)}")
        return create_error_response(f"Audio file does not exist: {audio_file_path}")
    except Exception as e:
        logging.error(f"Voice cloning failed: {str(e)}")
        return create_error_response("Voice cloning failed, tool temporarily unavailable")

    try:
        logging.info("Starting voice cloning process")
        voice_id = all_voice_lab.add_voice(name, audio_file_path, description)
        logging.info(f"Voice cloning successful, voice ID: {voice_id}")
        return TextContent(
            type="text",
            text=f"Voice cloning completed. Your new voice ID is: {voice_id}\n"
        )
    except VoiceCloneNoPermissionError as e:
        logging.error(f"Voice cloning failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Voice cloning failed, you don't have permission to clone voice. Please contact AllVoiceLab com."
        )
    except FileNotFoundError as e:
        logging.error(f"Audio file does not exist: {audio_file_path}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Audio file does not exist: {audio_file_path}"
        )
    except Exception as e:
        logging.error(f"Voice cloning failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Voice cloning failed, tool temporarily unavailable"
        )


@mcp.tool(
    name="download_dubbing_audio",
    description="""[AllVoiceLab Tool] Download the audio file from a completed dubbing project.
    
    This tool retrieves and downloads the processed audio file from a previously completed dubbing project.
    It requires a valid dubbing ID that was returned from a successful video_dubbing or video_translation_dubbing operation.
    
    Args:
        dubbing_id: The unique identifier of the dubbing project to download. Required.
        output_dir: Output directory for the downloaded audio file. Default is user's desktop.
        
    Returns:
        TextContent containing file path to the downloaded audio file.
        
    Limitations:
        - The dubbing project must exist and be in a completed state
        - The dubbing_id must be valid and properly formatted
        - Output directory must be accessible with write permissions
    """
)
def download_dubbing_file(
    dubbing_id: str,
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    logging.info(f"Tool called: download_dubbing_audio")
    logging.info(f"Dubbing ID: {dubbing_id}")
    logging.info(f"Output directory: {output_dir}")

    # Validate parameters
    if not dubbing_id:
        logging.warning("Dubbing ID parameter is empty")
        return TextContent(
            type="text",
            text="dubbing_id parameter cannot be empty"
        )

    # Validate dubbing_id format (basic check)
    if not isinstance(dubbing_id, str) or len(dubbing_id.strip()) == 0:
        logging.warning(f"Invalid dubbing_id format: {dubbing_id}")
        return TextContent(
            type="text",
            text="Invalid dubbing_id format"
        )

    # Validate output directory
    if not output_dir:
        logging.warning("Output directory parameter is empty")
        return TextContent(
            type="text",
            text="output_dir parameter cannot be empty"
        )

    # Try to create output directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory: {output_dir}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to create output directory: {output_dir}"
        )
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory: {output_dir}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to create output directory: {output_dir}"
        )

    try:
        logging.info("Starting dubbing file download")
        file_path = all_voice_lab.get_dubbing_audio(dubbing_id, output_dir)
        logging.info(f"Dubbing file download successful, file saved at: {file_path}")
        return TextContent(
            type="text",
            text=f"Dubbing file download completed, file saved at: {file_path}\n"
        )
    except Exception as e:
        logging.error(f"Dubbing file download failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Download failed, tool temporarily unavailable"
        )


@mcp.tool(
    name="remove_subtitle",
    description="""[AllVoiceLab Tool] Remove hardcoded subtitles from videos using OCR technology.
    
    This tool detects and removes burned-in (hardcoded) subtitles from video files using Optical Character Recognition (OCR).
    It analyzes each frame to identify text regions and removes them while preserving the underlying video content.
    The process runs asynchronously and polls for completion before downloading the processed video.
    
    Args:
        video_file_path: Path to the video file to process. Only MP4 and MOV formats are supported. Maximum file size: 2GB.
        language_code: Language code for subtitle text detection (e.g., 'en', 'zh'). Set to 'auto' for automatic language detection. Default is 'auto'.
        name: Optional project name for identification purposes.
        output_dir: Output directory for the processed video file. Default is user's desktop.
        
    Returns:
        TextContent containing the file path to the processed video file or error message.
        If the process takes longer than expected, returns the project ID for later status checking.
        
    Limitations:
        - Only MP4 and MOV formats are supported
        - Maximum file size: 2GB
        - Processing may take several minutes depending on video length and complexity
        - Works best with clear, high-contrast subtitles
        - May not completely remove stylized or animated subtitles
    """
)
def subtitle_removal(
    video_file_path: str,
    language_code: str = "auto",
    name: str = None,
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    poll_interval = 10
    max_retries = 30
    logging.info(f"Tool called: subtitle_removal")
    logging.info(f"Video file path: {video_file_path}")
    logging.info(f"Language code: {language_code}")
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Poll interval: {poll_interval} seconds")
    logging.info(f"Max retries: {max_retries}")
    if name:
        logging.info(f"Project name: {name}")

    # Validate parameters
    if not video_file_path:
        logging.warning("Video file path parameter is empty")
        return TextContent(
            type="text",
            text="video_file_path parameter cannot be empty"
        )

    # Check if video file exists before processing
    if not os.path.exists(video_file_path):
        logging.warning(f"Video file does not exist: {video_file_path}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )

    # Check file format, only allow mp4 and mov
    _, file_extension = os.path.splitext(video_file_path)
    file_extension = file_extension.lower()
    if file_extension not in [".mp4", ".mov"]:
        logging.warning(f"Unsupported video file format: {file_extension}")
        return TextContent(
            type="text",
            text=f"Unsupported video file format. Only MP4 and MOV formats are supported."
        )

    # Check file size, limit to 2GB
    max_size_bytes = 2 * 1024 * 1024 * 1024  # 2GB in bytes
    file_size = os.path.getsize(video_file_path)
    if file_size > max_size_bytes:
        logging.warning(f"Video file size exceeds limit: {file_size} bytes, max allowed: {max_size_bytes} bytes")
        return TextContent(
            type="text",
            text=f"Video file size exceeds the maximum limit of 2GB. Please use a smaller file."
        )

    try:
        logging.info("Starting subtitle removal process")
        project_id = all_voice_lab.subtitle_removal(
            video_file_path=video_file_path,
            language_code=language_code,
            name=name
        )
        logging.info(f"Subtitle removal initiated, project ID: {project_id}")

        # Poll for task completion
        logging.info(f"Starting to poll for task completion, interval: {poll_interval}s, max retries: {max_retries}")

        # Initialize variables for polling
        retry_count = 0
        task_completed = False
        removal_info = None

        # Poll until task is completed or max retries reached
        while retry_count < max_retries and not task_completed:
            try:
                # Wait for the specified interval
                time.sleep(poll_interval)

                # Check task status
                removal_info = all_voice_lab.get_removal_info(project_id)
                logging.info(f"Poll attempt {retry_count + 1}, status: {removal_info.status}")

                # Check if task is completed
                if removal_info.status.lower() == "success":
                    task_completed = True
                    logging.info("Subtitle removal task completed successfully")
                    break
                elif removal_info.status.lower() == "failed":
                    logging.error("Subtitle removal task failed")
                    return TextContent(
                        type="text",
                        text=f"Subtitle removal failed. Please try again later."
                    )

                # Increment retry count
                retry_count += 1

            except Exception as e:
                logging.error(f"Error checking task status: {str(e)}")
                retry_count += 1

        # Check if task completed successfully
        if not task_completed:
            logging.warning(f"Subtitle removal task did not complete within {max_retries} attempts")
            return TextContent(
                type="text",
                text=f"Subtitle removal is still in progress. Your project ID is: {project_id}. You can check the status later."
            )

        # Download the processed video
        logging.info("Downloading processed video")
        try:
            # Check if output URL is available
            if not removal_info.removal_result:
                logging.error("No removal_result URL available in the response")
                return TextContent(
                    type="text",
                    text=f"Subtitle removal completed but no output file is available. Your project ID is: {project_id}"
                )

            # Prepare HTTP request
            url = removal_info.removal_result

            # Set request headers, accept all types of responses
            headers = all_voice_lab._get_headers(content_type="", accept="*/*")

            # Send request and get response
            response = requests.get(url, headers=headers, stream=True)

            # Check response status
            response.raise_for_status()

            # Generate a unique filename
            timestamp = int(time.time())
            random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
            filename = f"subtitle_removal_{timestamp}_{random_suffix}.mp4"

            # Build complete file path
            file_path = os.path.join(output_dir, filename)

            # Save response content to file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logging.info(f"Processed video saved to: {file_path}")
            return TextContent(
                type="text",
                text=f"Subtitle removal completed successfully. Processed video saved to: {file_path}"
            )

        except Exception as e:
            logging.error(f"Failed to download processed video: {str(e)}")
            return TextContent(
                type="text",
                text=f"Subtitle removal completed but failed to download the processed video. Your project ID is: {project_id}"
            )

    except FileNotFoundError as e:
        logging.error(f"Video file does not exist: {video_file_path}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )
    except Exception as e:
        logging.error(f"Subtitle removal failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Subtitle removal failed, tool temporarily unavailable"
        )


@mcp.tool(
    name="video_translation_dubbing",
    description="""[AllVoiceLab Tool] Translate and dub video speech into a different language with AI-generated voices.
    
    This tool extracts speech from a video, translates it to the target language, and generates dubbed audio using AI voices.
    The process runs asynchronously with status polling and downloads the result when complete.
    
    Args:
        video_file_path: Path to the video or audio file to process. Supports MP4, MOV, MP3, and WAV formats. Maximum file size: 2GB.
        target_lang: Target language code for translation (e.g., 'en', 'zh', 'ja', 'fr', 'de', 'ko'). Required.
        source_lang: Source language code of the original content. Set to 'auto' for automatic language detection. Default is 'auto'.
        name: Optional project name for identification purposes.
        watermark: Whether to add a watermark to the output video. Default is False.
        output_dir: Output directory for the downloaded result file. Default is user's desktop.
        
    Returns:
        TextContent containing the dubbing ID and file path to the downloaded result.
        If the process takes longer than expected, returns only the dubbing ID for later status checking.
        
    Limitations:
        - Only MP4, MOV, MP3, and WAV formats are supported
        - Maximum file size: 2GB
        - Processing may take several minutes depending on content length and complexity
        - Translation quality depends on speech clarity in the original content
        - Currently supports a limited set of languages for translation
    """
)
def video_translation_dubbing(
    video_file_path: str,
    target_lang: str,
    source_lang: str = "auto",
    name: str = None,
    watermark: bool = False,
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    max_polling_time = 300
    polling_interval = 10
    logging.info(f"Tool called: video_translation_dubbing")
    logging.info(f"Video file path: {video_file_path}")
    logging.info(f"Target language: {target_lang}, Source language: {source_lang}")
    if name:
        logging.info(f"Project name: {name}")
    logging.info(f"Watermark: {watermark}")
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Max polling time: {max_polling_time}s, Polling interval: {polling_interval}s")

    # Validate parameters
    if not video_file_path:
        logging.warning("Video file path parameter is empty")
        return TextContent(
            type="text",
            text="video_file_path parameter cannot be empty"
        )

    # Check if video file exists before processing
    if not os.path.exists(video_file_path):
        logging.warning(f"Video file does not exist: {video_file_path}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )

    # Check file format, only allow mp4 and mov
    _, file_extension = os.path.splitext(video_file_path)
    file_extension = file_extension.lower()
    if file_extension not in [".mp4", ".mov", ".mp3", ".wav"]:
        logging.warning(f"Unsupported video file format: {file_extension}")
        return TextContent(
            type="text",
            text=f"Unsupported video file format. Only MP4, MOV, MP3 and WAV formats are supported."
        )

    # Check file size, limit to 2GB
    max_size_bytes = 2 * 1024 * 1024 * 1024  # 2GB in bytes
    file_size = os.path.getsize(video_file_path)
    if file_size > max_size_bytes:
        logging.warning(f"Video file size exceeds limit: {file_size} bytes, max allowed: {max_size_bytes} bytes")
        return TextContent(
            type="text",
            text=f"Video file size exceeds the maximum limit of 2GB. Please use a smaller file."
        )

    # Validate target language
    if not target_lang:
        logging.warning(f"target language is empty")
        return TextContent(
            type="text",
            text="target language parameter cannot be empty"
        )

    # Validate output directory
    if not output_dir:
        logging.warning("Output directory parameter is empty")
        return TextContent(
            type="text",
            text="output_dir parameter cannot be empty"
        )

    # Try to create output directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory: {output_dir}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to create output directory: {output_dir}"
        )

    try:
        # Submit dubbing request
        logging.info("Starting video dubbing process")
        dubbing_id = all_voice_lab.dubbing(
            video_file_path=video_file_path,
            target_lang=target_lang,
            source_lang=source_lang,
            name=name,
            watermark=watermark,
            drop_background_audio=False
        )
        logging.info(f"Video dubbing request successful, dubbing ID: {dubbing_id}")

        # Start polling for task completion
        logging.info(f"Starting to poll dubbing status for ID: {dubbing_id}")
        start_time = time.time()
        completed = False
        file_path = None

        # Poll until task is completed or timeout
        while time.time() - start_time < max_polling_time:
            try:
                # Get dubbing info
                dubbing_info = all_voice_lab.get_dubbing_info(dubbing_id)
                logging.info(f"Dubbing status: {dubbing_info.status} for ID: {dubbing_id}")

                # Check if dubbing is completed
                if dubbing_info.status.lower() == "success":
                    logging.info(f"Dubbing completed for ID: {dubbing_id}")
                    completed = True
                    break
                # Check if dubbing failed
                elif dubbing_info.status.lower() in ["failed", "error"]:
                    logging.error(f"Dubbing failed for ID: {dubbing_id}")
                    return TextContent(
                        type="text",
                        text=f"Video dubbing failed. Please try again later.\n"
                             f"Dubbing ID: {dubbing_id}\n"
                    )

                # Wait for next polling interval
                logging.info(f"Waiting {polling_interval} seconds before next poll")
                time.sleep(polling_interval)
            except Exception as e:
                logging.error(f"Error polling dubbing status: {str(e)}")
                time.sleep(polling_interval)  # Continue polling despite errors

        # Check if polling timed out
        if not completed:
            logging.warning(f"Polling timed out after {max_polling_time} seconds for dubbing ID: {dubbing_id}")
            return TextContent(
                type="text",
                text=f"Video dubbing is still in progress. Your dubbing ID is: {dubbing_id}\n"
                     f"The process is taking longer than expected. You can check the status later using this ID.\n"
            )

        # Download the file if dubbing completed
        try:
            logging.info(f"Downloading dubbing audio for ID: {dubbing_id}")
            file_path = all_voice_lab.get_dubbing_audio(dubbing_id, output_dir)
            logging.info(f"Dubbing audio downloaded successfully, file saved at: {file_path}")

            return TextContent(
                type="text",
                text=f"Video dubbing completed successfully!\n"
                     f"Dubbing ID: {dubbing_id}\n"
                     f"File saved at: {file_path}\n"
            )
        except Exception as e:
            logging.error(f"Failed to download dubbing audio: {str(e)}")
            return TextContent(
                type="text",
                text=f"Video dubbing completed, but failed to download the audio file.\n"
                     f"Dubbing ID: {dubbing_id}\n"
                     f"Error: {str(e)}\n"
            )
    except FileNotFoundError as e:
        logging.error(f"Video file does not exist: {video_file_path}, error: {str(e)}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )
    except Exception as e:
        logging.error(f"Video dubbing failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Video dubbing failed, tool temporarily unavailable"
        )


@mcp.tool(
    name="get_dubbing_info",
    description="""[AllVoiceLab Tool] Retrieve status and details of a video dubbing task.
    
    This tool queries the current status of a previously submitted dubbing task and returns detailed information
    about its progress, including the current processing stage and completion status.
    
    Args:
        dubbing_id: The unique identifier of the dubbing task to check. This ID is returned from the video_dubbing or video_translation_dubbing tool. Required.
        
    Returns:
        TextContent containing the status (e.g., "pending", "processing", "success", "failed") and other details of the dubbing task.
        
    Limitations:
        - The dubbing_id must be valid and properly formatted
        - The task must have been previously submitted to the AllVoiceLab API
    """
)
def get_dubbing_info(
    dubbing_id: str
) -> TextContent:
    logging.info(f"Tool called: get_dubbing_info")
    logging.info(f"Dubbing ID: {dubbing_id}")

    # Validate parameters
    if not dubbing_id:
        logging.warning("Dubbing ID parameter is empty")
        return TextContent(
            type="text",
            text="dubbing_id parameter cannot be empty"
        )

    try:
        logging.info("Getting dubbing task information")
        dubbing_info = all_voice_lab.get_dubbing_info(dubbing_id)
        logging.info(f"Dubbing info retrieved successfully for ID: {dubbing_id}")

        # Format the result
        buffer = []
        buffer.append(f"Dubbing ID: {dubbing_info.dubbing_id}\n")
        buffer.append(f"Status: {dubbing_info.status}\n")

        if dubbing_info.name:
            buffer.append(f"Project Name: {dubbing_info.name}\n")
        buffer.append(
            "Note: If the task has not been completed, you may need to explicitly inform the user of the task ID when responding.\n")

        # Join the list into a string
        result = "".join(buffer)
        return TextContent(
            type="text",
            text=result
        )
    except Exception as e:
        logging.error(f"Failed to get dubbing information: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to get dubbing information, tool temporarily unavailable"
        )


@mcp.tool(
    name="get_removal_info",
    description="""[AllVoiceLab Tool] Retrieve status and details of a subtitle removal task.
    
    This tool queries the current status of a previously submitted subtitle removal task and returns detailed information
    about its progress, including the current processing stage, completion status, and result URL if available.
    
    Args:
        project_id: The unique identifier of the subtitle removal task to check. This ID is returned from the remove_subtitle tool. Required.
        
    Returns:
        TextContent containing the status (e.g., "pending", "processing", "success", "failed") and other details of the subtitle removal task,
        including the URL to the processed video if the task has completed successfully.
        
    Limitations:
        - The project_id must be valid and properly formatted
        - The task must have been previously submitted to the AllVoiceLab API
    """
)
def get_removal_info(
    project_id: str
) -> TextContent:
    logging.info(f"Tool called: get_removal_info")
    logging.info(f"Project ID: {project_id}")

    # Validate parameters
    if not project_id:
        logging.warning("Project ID parameter is empty")
        return TextContent(
            type="text",
            text="project_id parameter cannot be empty"
        )

    try:
        logging.info("Getting subtitle removal task information")
        removal_info = all_voice_lab.get_removal_info(project_id)
        logging.info(f"Subtitle removal info retrieved successfully for ID: {project_id}")

        # Format the result
        buffer = []
        buffer.append(f"Project ID: {removal_info.project_id}\n")
        buffer.append(f"Status: {removal_info.status}\n")

        if removal_info.name:
            buffer.append(f"Project Name: {removal_info.name}\n")

        if removal_info.output_url and removal_info.status == "done":
            buffer.append(f"Output URL: {removal_info.output_url}\n")
            buffer.append(
                f"The subtitle removal task has been completed. You can download the processed video from the output URL.\n")
        else:
            buffer.append(
                f"The subtitle removal task is still in progress. Please check again later using the project ID.\n")

        # Join the list into a string
        result = "".join(buffer)
        return TextContent(
            type="text",
            text=result
        )
    except Exception as e:
        logging.error(f"Failed to get subtitle removal information: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to get subtitle removal information, tool temporarily unavailable"
        )


@mcp.tool(
    name="subtitle_extraction",
    description="""[AllVoiceLab Tool] Extract subtitles from a video using OCR technology.
    
    This tool processes a video file to extract hardcoded subtitles. The process runs asynchronously with status polling
    and returns the extracted subtitles when complete.
    
    Args:
        video_file_path (str): Path to the video file (MP4, MOV). Max size 2GB.
        language_code (str, optional): Language code for subtitle text detection (e.g., 'en', 'zh'). Defaults to 'auto'.
        name (str, optional): Optional project name for identification.
        output_dir (str, optional): Output directory for the downloaded result file. It has a default value.
        
    Returns:
        TextContent containing the file path to the srt file or error message.
        If the process takes longer than expected, returns the project ID for later status checking. 
        
    Note:
        - Supported video formats: MP4, MOV
        - Video file size limit: 10 seconds to 200 minutes, max 2GB.
        - If the process takes longer than max_polling_time, use 'get_extraction_info' to check status and retrieve results.
    """
)
def subtitle_extraction_tool(
    video_file_path: str,
    language_code: str = "auto",
    name: str = None,
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    max_polling_time = 300
    polling_interval = 10
    logging.info(
        f"Tool called: subtitle_extraction, video_file_path: {video_file_path}, language_code: {language_code}, name: {name}")
    logging.info(f"Max polling time: {max_polling_time}s, Polling interval: {polling_interval}s")

    # 验证参数
    if not video_file_path:
        logging.warning("Video file path parameter is empty")
        return TextContent(
            type="text",
            text="video_file_path parameter cannot be empty"
        )

    # 检查视频文件是否存在
    if not os.path.exists(video_file_path):
        logging.warning(f"Video file does not exist: {video_file_path}")
        return TextContent(
            type="text",
            text=f"Video file does not exist: {video_file_path}"
        )

    # 检查文件格式，只允许mp4和mov
    _, file_extension = os.path.splitext(video_file_path)
    file_extension = file_extension.lower()
    if file_extension not in [".mp4", ".mov"]:
        logging.warning(f"Unsupported video file format: {file_extension}")
        return TextContent(
            type="text",
            text=f"Unsupported video file format. Only MP4 and MOV formats are supported."
        )

    # 检查文件大小，限制为2GB
    max_size_bytes = 2 * 1024 * 1024 * 1024  # 2GB in bytes
    file_size = os.path.getsize(video_file_path)
    if file_size > max_size_bytes:
        logging.warning(f"Video file size exceeds limit: {file_size} bytes, max allowed: {max_size_bytes} bytes")
        return TextContent(
            type="text",
            text=f"Video file size exceeds the maximum limit of 2GB. Please use a smaller file."
        )

    try:
        if all_voice_lab is None:
            logging.error("all_voice_lab client is not initialized.")
            return TextContent(type="text",
                               text="Error: AllVoiceLab client not initialized. Please check server setup.")

        # 提交字幕提取请求
        logging.info("Starting subtitle extraction process")
        project_id = all_voice_lab.subtitle_extraction(
            video_file_path=video_file_path,
            language_code=language_code,
            name=name
        )
        logging.info(f"Subtitle extraction task submitted. Project ID: {project_id}")

        # 开始轮询任务完成情况
        logging.info(f"Starting to poll extraction status for Project ID: {project_id}")
        start_time = time.time()
        completed = False

        # 轮询直到任务完成或超时
        while time.time() - start_time < max_polling_time:
            try:
                # 获取提取信息
                extraction_info = all_voice_lab.get_extraction_info(project_id)
                logging.info(f"Extraction status: {extraction_info.status} for Project ID: {project_id}")

                # 检查是否完成
                if extraction_info.status.lower() == "success":
                    logging.info(f"Subtitle extraction completed for Project ID: {project_id}")
                    completed = True

                    # 检查是否有结果URL
                    if hasattr(extraction_info, 'result') and extraction_info.result:
                        result_url = extraction_info.result
                        logging.info(f"Downloading subtitle file from: {result_url}")

                        try:
                            # 准备HTTP请求
                            url = result_url

                            # 设置请求头，接受所有类型的响应
                            headers = all_voice_lab._get_headers(content_type="", accept="*/*")

                            # 发送请求并获取响应
                            response = requests.get(url, headers=headers, stream=True)

                            # 检查响应状态
                            response.raise_for_status()

                            # 生成唯一文件名
                            timestamp = int(time.time())
                            random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
                            filename = f"subtitle_extraction_{timestamp}_{random_suffix}.srt"

                            # 构建完整文件路径
                            os.makedirs(output_dir, exist_ok=True)
                            file_path = os.path.join(output_dir, filename)

                            # 保存响应内容到文件
                            with open(file_path, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)

                            logging.info(f"Subtitle file saved to: {file_path}")

                            # 格式化结果
                            info_parts = []
                            info_parts.append(f"Subtitle extraction completed successfully.")
                            info_parts.append(f"Project ID: {project_id}")
                            info_parts.append(f"Subtitle file saved to: {file_path}")

                            return TextContent(
                                type="text",
                                text="\n".join(info_parts)
                            )

                        except Exception as e:
                            logging.error(f"Failed to download subtitle file: {str(e)}")
                            # 如果下载失败，仍然返回成功信息和URL
                            info_parts = []
                            info_parts.append(f"Subtitle extraction completed successfully.")
                            info_parts.append(f"Project ID: {project_id}")
                            info_parts.append(f"Result URL: {extraction_info.result}")
                            info_parts.append(f"Failed to download subtitle file: {str(e)}")

                            return TextContent(
                                type="text",
                                text="\n".join(info_parts)
                            )
                    else:
                        # 没有结果URL
                        info_parts = []
                        info_parts.append(f"Subtitle extraction completed successfully.")
                        info_parts.append(f"Project ID: {project_id}")
                        info_parts.append("No subtitle file URL available.")

                        return TextContent(
                            type="text",
                            text="\n".join(info_parts)
                        )

                # 检查是否失败
                elif extraction_info.status.lower() in ["failed", "error"]:
                    logging.error(f"Subtitle extraction failed for Project ID: {project_id}")
                    error_message = "Subtitle extraction failed."
                    if hasattr(extraction_info, 'message') and extraction_info.message:
                        error_message += f" Message: {extraction_info.message}"
                    return TextContent(
                        type="text",
                        text=f"{error_message}\nProject ID: {project_id}"
                    )

                # 等待下一次轮询间隔
                logging.info(f"Waiting {polling_interval} seconds before next poll")
                time.sleep(polling_interval)

            except Exception as e:
                logging.error(f"Error while polling extraction status: {str(e)}")
                time.sleep(polling_interval)

        # 如果超时，返回项目ID以便后续查询
        if not completed:
            logging.warning(f"Polling timed out after {max_polling_time} seconds for Project ID: {project_id}")
            return TextContent(
                type="text",
                text=f"Subtitle extraction is still in progress. Please check the status later using the 'get_extraction_info' tool.\n"
                     f"Project ID: {project_id}"
            )

    except FileNotFoundError as e:
        logging.error(f"Error in subtitle_extraction_tool: {str(e)}")
        return TextContent(type="text", text=str(e))
    except Exception as e:
        logging.error(f"Failed to extract subtitles: {str(e)}")
        error_message = f"Failed to extract subtitles. Error: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_message = f"Failed to extract subtitles: API Error - {error_detail.get('message', str(e))}"
            except ValueError:  # Not a JSON response
                error_message = f"Failed to extract subtitles: API Error - {e.response.status_code} {e.response.text}"
        return TextContent(
            type="text",
            text=error_message
        )


@mcp.tool(
    name="text_translation",
    description="""[AllVoiceLab Tool] Translate text from a file to another language.
    
    This tool translates text content from a file to a specified target language. The process runs asynchronously
    with status polling and returns the translated text when complete.
    
    Args:
        file_path: Path to the text file to translate. Only TXT and SRT formats are supported. Maximum file size: 10MB.
        target_lang: Target language code for translation (e.g., 'zh', 'en', 'ja', 'fr', 'de', 'ko'). Required.
        source_lang: Source language code of the original content. Set to 'auto' for automatic language detection. Default is 'auto'.
        output_dir: Output directory for the downloaded result file. Default is user's desktop.
        
    Returns:
        TextContent containing the file path to the translated file or error message.
        If the process takes longer than expected, returns the project ID for later status checking. 
        
    Limitations:
        - Only TXT and SRT formats are supported
        - Maximum file size: 10MB
        - File must exist and be accessible
        - Currently supports a limited set of languages for translation
    """
)
def text_translation_tool(
    file_path: str,
    target_lang: str,
    source_lang: str = "auto",
    output_dir: str = None
) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    max_polling_time = 300
    polling_interval = 5
    logging.info(
        f"Tool called: text_translation, file_path: {file_path}, target_lang: {target_lang}, source_lang: {source_lang}")
    logging.info(f"Max polling time: {max_polling_time}s, Polling interval: {polling_interval}s")

    # 验证参数
    if not file_path:
        logging.warning("File path parameter is empty")
        return TextContent(
            type="text",
            text="file_path parameter cannot be empty"
        )

    # 检查文件是否存在
    if not os.path.exists(file_path):
        logging.warning(f"File does not exist: {file_path}")
        return TextContent(
            type="text",
            text=f"File does not exist: {file_path}"
        )

    # 检查文件格式，只允许txt和srt
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    if file_extension not in [".txt", ".srt"]:
        logging.warning(f"Unsupported file format: {file_extension}")
        return TextContent(
            type="text",
            text=f"Unsupported file format. Only TXT and SRT formats are supported."
        )

    # 检查文件大小，限制为10MB
    max_size_bytes = 10 * 1024 * 1024  # 10MB in bytes
    file_size = os.path.getsize(file_path)
    if file_size > max_size_bytes:
        logging.warning(f"File size exceeds limit: {file_size} bytes, max allowed: {max_size_bytes} bytes")
        return TextContent(
            type="text",
            text=f"File size exceeds the maximum limit of 10MB. Please use a smaller file."
        )

    try:
        if all_voice_lab is None:
            logging.error("all_voice_lab client is not initialized.")
            return TextContent(type="text",
                               text="Error: AllVoiceLab client not initialized. Please check server setup.")

        # 提交文本翻译请求
        logging.info("Starting text translation process")
        project_id = all_voice_lab.text_translation(
            file_path=file_path,
            target_lang=target_lang,
            source_lang=source_lang
        )
        logging.info(f"Text translation task submitted. Project ID: {project_id}")

        # 开始轮询任务完成情况
        logging.info(f"Starting to poll translation status for Project ID: {project_id}")
        start_time = time.time()
        completed = False

        # 轮询直到任务完成或超时
        while time.time() - start_time < max_polling_time:
            try:
                # 获取翻译结果
                translation_result = all_voice_lab.get_text_translation_result(project_id)
                if translation_result is None:
                    logging.warning(f"Failed to get translation result for Project ID: {project_id}")
                    time.sleep(polling_interval)
                    continue

                logging.info(f"Translation status: {translation_result.status} for Project ID: {project_id}")

                # 检查是否完成
                if translation_result.status.lower() == "success":
                    logging.info(f"Text translation completed for Project ID: {project_id}")
                    completed = True

                    # 检查结果URL并下载内容
                    if translation_result.result and translation_result.result.startswith("http"):
                        try:
                            # 创建输出目录
                            os.makedirs(output_dir, exist_ok=True)

                            # 生成文件名
                            timestamp = int(time.time())
                            random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
                            filename = f"translation_{timestamp}_{random_suffix}.txt"
                            file_path = os.path.join(output_dir, filename)

                            # 下载内容
                            logging.info(f"Downloading translation result from URL: {translation_result.result}")
                            response = requests.get(translation_result.result, timeout=30)
                            response.raise_for_status()

                            # 保存到文件
                            with open(file_path, 'wb') as f:
                                f.write(response.content)

                            # 读取文件内容作为翻译结果
                            with open(file_path, 'r', encoding='utf-8') as f:
                                translated_text = f.read()

                            logging.info(f"Translation result downloaded and saved to: {file_path}")

                            # 返回翻译结果
                            result_text = f"Translation completed successfully.\n\n"
                            result_text += f"Source Language: {translation_result.source_lang}\n"
                            result_text += f"Target Language: {translation_result.target_lang}\n\n"
                            result_text += f"Translated Text:\n{translated_text}\n\n"
                            result_text += f"Result file saved at: {file_path}"

                            return TextContent(
                                type="text",
                                text=result_text
                            )
                        except Exception as e:
                            logging.error(f"Error downloading translation result: {str(e)}")
                            result_text = f"Translation completed, but failed to download result: {str(e)}\n\n"
                            result_text += f"Source Language: {translation_result.source_lang}\n"
                            result_text += f"Target Language: {translation_result.target_lang}\n\n"
                            result_text += f"Result URL: {translation_result.result}"

                            return TextContent(
                                type="text",
                                text=result_text
                            )
                    else:
                        # 返回翻译结果（URL为空的情况）
                        result_text = f"Translation completed successfully.\n\n"
                        result_text += f"Source Language: {translation_result.source_lang}\n"
                        result_text += f"Target Language: {translation_result.target_lang}\n\n"
                        result_text += f"No result URL available."

                        return TextContent(
                            type="text",
                            text=result_text
                        )
                elif translation_result.status.lower() == "failed":
                    logging.error(
                        f"Translation failed for Project ID: {project_id}, Error: {translation_result.error_message}")
                    return TextContent(
                        type="text",
                        text=f"Translation failed: {translation_result.error_message}"
                    )

            except Exception as e:
                logging.error(f"Error while polling translation status: {str(e)}")

            # 等待下一次轮询
            time.sleep(polling_interval)

        # 如果超时，返回项目ID以便后续查询
        if not completed:
            logging.warning(f"Translation not completed within {max_polling_time} seconds for Project ID: {project_id}")
            return TextContent(
                type="text",
                text=f"Translation is still in progress. Please check the status later using the project ID: {project_id}"
            )

    except Exception as e:
        logging.error(f"Text translation failed: {str(e)}")
        return TextContent(
            type="text",
            text=f"Translation failed: {str(e)}"
        )


@mcp.tool(
    name="get_translation_result",
    description="""[AllVoiceLab Tool] Retrieve status and result of a text translation task.
    
    This tool queries the current status of a previously submitted text translation task and returns detailed information
    about its progress, including the translated text if available.
    
    Args:
        project_id: The unique identifier of the translation task to check. This ID is returned from the text_translation tool. Required.
        output_dir: Output directory for the downloaded result file. Default is user's desktop.
        
    Returns:
        TextContent containing the status (e.g., "pending", "processing", "success", "failed") and other details of the translation task,
        including the translated text if the task has completed successfully.
        
    Limitations:
        - The project_id must be valid and properly formatted
        - The task must have been previously submitted to the AllVoiceLab API
    """
)
def get_translation_result_tool(project_id: str, output_dir: str = None) -> TextContent:
    if not output_dir:
        output_dir = default_output_path
    logging.info(f"Tool called: get_translation_result, project_id: {project_id}")

    if not project_id:
        logging.warning("Project ID parameter is empty")
        return TextContent(
            type="text",
            text="project_id parameter cannot be empty"
        )

    try:
        if all_voice_lab is None:
            logging.error("all_voice_lab client is not initialized.")
            return TextContent(
                type="text",
                text="Error: AllVoiceLab client not initialized. Please check server setup."
            )

        # 获取翻译结果
        translation_result = all_voice_lab.get_text_translation_result(project_id)
        if translation_result is None:
            logging.warning(f"Failed to get translation result for Project ID: {project_id}")
            return TextContent(
                type="text",
                text=f"Failed to get translation result for Project ID: {project_id}"
            )

        # 格式化响应
        result_json = json.dumps({
            "project_id": translation_result.project_id,
            "status": translation_result.status,
            "source_lang": translation_result.source_lang,
            "target_lang": translation_result.target_lang,
            "result": translation_result.result
        }, indent=2, ensure_ascii=False)

        # 根据状态返回不同的响应
        if translation_result.status.lower() == "success":
            # 检查结果URL并下载内容
            if translation_result.result and translation_result.result.startswith("http"):
                try:
                    # 创建输出目录
                    os.makedirs(output_dir, exist_ok=True)

                    # 生成文件名
                    timestamp = int(time.time())
                    random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
                    filename = f"translation_{timestamp}_{random_suffix}.txt"
                    file_path = os.path.join(output_dir, filename)

                    # 下载内容
                    logging.info(f"Downloading translation result from URL: {translation_result.result}")
                    response = requests.get(translation_result.result, timeout=30)
                    response.raise_for_status()

                    # 保存到文件
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    # 读取文件内容作为翻译结果
                    with open(file_path, 'r', encoding='utf-8') as f:
                        translated_text = f.read()

                    logging.info(f"Translation result downloaded and saved to: {file_path}")

                    # 返回翻译结果
                    result_text = f"Translation completed successfully.\n\n"
                    result_text += f"Source Language: {translation_result.source_lang}\n"
                    result_text += f"Target Language: {translation_result.target_lang}\n\n"
                    result_text += f"Translated Text:\n{translated_text}\n\n"
                    result_text += f"Result file saved at: {file_path}"
                except Exception as e:
                    logging.error(f"Error downloading translation result: {str(e)}")
                    result_text = f"Translation completed, but failed to download result: {str(e)}\n\n"
                    result_text += f"Source Language: {translation_result.source_lang}\n"
                    result_text += f"Target Language: {translation_result.target_lang}\n\n"
                    result_text += f"Result URL: {translation_result.result}"
            else:
                # 返回翻译结果（URL为空的情况）
                result_text = f"Translation completed successfully.\n\n"
                result_text += f"Source Language: {translation_result.source_lang}\n"
                result_text += f"Target Language: {translation_result.target_lang}\n\n"
                result_text += f"No result URL available."

            return TextContent(
                type="text",
                text=result_text
            )
        elif translation_result.status.lower() == "failed":
            return TextContent(
                type="text",
                text=f"Translation failed: {translation_result.error_message}\n\nDetails:\n{result_json}"
            )
        else:
            return TextContent(
                type="text",
                text=f"Translation status: {translation_result.status}\n\nDetails:\n{result_json}"
            )

    except Exception as e:
        logging.error(f"Failed to get translation result: {str(e)}")
        return TextContent(
            type="text",
            text=f"Failed to get translation result: {str(e)}"
        )


@mcp.tool(
    name="get_extraction_info",
    description="""[AllVoiceLab Tool] Get status and results of a subtitle extraction task.
    
    This tool queries the current status of a previously submitted subtitle extraction task.
    
    Args:
        project_id (str): The project ID returned by the 'subtitle_extraction' tool.
        
    Returns:
        TextContent containing the status and details of the subtitle extraction task. 
        If successful and subtitles are ready, it may include the extracted text or a link.
    """
)
def get_extraction_info_tool(project_id: str) -> TextContent:
    logging.info(f"Tool called: get_extraction_info, project_id: {project_id}")
    try:
        if all_voice_lab is None:
            logging.error("all_voice_lab client is not initialized.")
            return TextContent(type="text",
                               text="Error: AllVoiceLab client not initialized. Please check server setup.")

        extraction_info = all_voice_lab.get_extraction_info(project_id=project_id)
        logging.info(f"Retrieved extraction info for project {project_id}")

        info_parts = []
        if hasattr(extraction_info, 'project_id'):
            info_parts.append(f"Project ID: {extraction_info.project_id}")
        else:
            info_parts.append(f"Queried Project ID: {project_id}")

        if hasattr(extraction_info, 'status'):
            info_parts.append(f"Status: {extraction_info.status}")
        if hasattr(extraction_info, 'message') and extraction_info.message:
            info_parts.append(f"Message: {extraction_info.message}")

        if hasattr(extraction_info, 'result_url') and extraction_info.result_url:
            info_parts.append(f"Result URL: {extraction_info.result_url}")

        if hasattr(extraction_info, 'subtitles') and extraction_info.subtitles:
            subtitles_data = extraction_info.subtitles
            if isinstance(subtitles_data, list) and subtitles_data:
                formatted_subtitles = "\n".join([f"  - {s}" for s in subtitles_data])
                info_parts.append(f"Subtitles:\n{formatted_subtitles}")
            elif isinstance(subtitles_data, str) and subtitles_data:
                info_parts.append(f"Subtitles: {subtitles_data}")

        if len(info_parts) <= 1 and hasattr(extraction_info, 'to_dict'):
            info_parts.append(f"Full Details: {json.dumps(extraction_info.to_dict(), indent=2, ensure_ascii=False)}")
        elif len(info_parts) <= 1:
            info_parts.append(f"Raw Details: {str(extraction_info)}")

        return TextContent(
            type="text",
            text="\n".join(info_parts)
        )
    except Exception as e:
        logging.error(f"Failed to get extraction info for project {project_id}: {str(e)}")
        error_message = f"Failed to get extraction info for project {project_id}. Error: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_message = f"Failed to get extraction info: API Error - {error_detail.get('message', str(e))}"
            except ValueError:
                error_message = f"Failed to get extraction info: API Error - {e.response.status_code} {e.response.text}"
        return TextContent(
            type="text",
            text=error_message
        )


def setup_logging():
    """Setup logging configuration with rotation mechanism"""
    # Create log directory
    log_dir = os.path.expanduser("~/.mcp")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "allvoicelab_mcp.log")

    # Configure log format and handlers
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Rotating file handler (10MB max size, keep 5 backup files)
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.WARNING)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging system initialized with rotation, log file path: %s", log_file)


def main():
    # Setup logging
    setup_logging()

    # Get environment variables
    api_key = os.getenv("ALLVOICELAB_API_KEY")
    api_domain = os.getenv("ALLVOICELAB_API_DOMAIN")

    if not api_key:
        logging.error("ALLVOICELAB_API_KEY environment variable not set")
        print("Error: ALLVOICELAB_API_KEY environment variable not set")
        sys.exit(1)

    if not api_domain:
        logging.error("ALLVOICELAB_API_DOMAIN environment variable not set")
        print("Error: ALLVOICELAB_API_DOMAIN environment variable not set")
        sys.exit(1)

    # Initialize global variable
    global all_voice_lab
    all_voice_lab = AllVoiceLab(api_key, api_domain)
    logging.info("AllVoiceLab client initialization completed")

    logging.info("Starting AllVoiceLab MCP server")
    print("Starting AllVoiceLab MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
