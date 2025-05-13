from mcp.server.fastmcp import FastMCP

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from youtube_transcript_api._transcripts import Transcript

server = FastMCP("youtube-transcript-api")


def _format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"[{hours}:{minutes:02d}:{secs:02d}]"
    return f"[{minutes}:{secs:02d}]"


@server.tool()
def get_transcript(
    video_id: str,
    with_timestamps: bool = False,
    language: str = "en",
) -> str:
    """Get transcript for a video ID and format it as readable text."""
    transcript: Transcript = None
    available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    try:
        transcript = available_transcripts.find_transcript([language])
    except NoTranscriptFound:
        for t in available_transcripts:
            transcript = t
            break
        else:
            return f"No transcript found for video {video_id}"
    transcript = transcript.fetch()
    if with_timestamps:
        return "\n".join(
            f"{_format_timestamp(entry.start)} {entry.text}" for entry in transcript
        )
    else:
        return "\n".join(entry.text for entry in transcript)


def main():
    server.run()


if __name__ == "__main__":
    main()
