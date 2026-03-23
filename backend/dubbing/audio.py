import os
from moviepy import VideoFileClip, AudioFileClip

def extract_audio(video_path: str, audio_path: str):
    """ Extract audio from the video (Requirement 1: Audio Extraction) """
    clip = VideoFileClip(video_path)
    # Using ffmpeg underneath via moviepy
    if clip.audio is not None:
        clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()

def merge_audio_video(video_path: str, audio_path: str, output_path: str):
    """ Merge translated audio back into the video matching original time (Requirement 5: Merging) """
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(audio_path)
    
    # Ensure audio duration matches original exactly
    if new_audio.duration > video.duration:
        new_audio = new_audio.subclipped(0, video.duration)
        
    final_video = video.with_audio(new_audio)
    
    # Export fully processed dubbed video
    final_video.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac", 
        threads=4, 
        preset="ultrafast", 
        logger=None
    )
    
    video.close()
    new_audio.close()
    final_video.close()
