
# Video Streamer

A Python class for streaming video from a camera or a video file. It supports frame resizing, FPS control, and automatic restart of the video stream in case of errors.

## Features

- Stream video from a given source (camera or video file).
- Control the FPS of the video stream.
- Option to resize the video frames.
- Automatic restart of the video stream if the source becomes unavailable.
- Multi-threaded streaming for asynchronous video frame retrieval.

## Installation

To install the required dependencies, you need to install OpenCV:

```bash
pip install opencv-python
```

## Usage

Here is an example of how to use the `VideoStreamer` class:

```python
from video_streamer import VideoStreamer
import cv2

# Set your video source (camera index 0 or a video file path)
video_source = "1.avi"  # Change this to your video source (0 for webcam, or a video file path)

# Create a VideoStreamer instance
streamer = VideoStreamer(video_source)

# Start the video stream in a separate thread
streamer.start()

# Continuously display the video stream
while True:
    frame = streamer.get_frame()
    if frame is None:
        continue
    cv2.imshow("Video Stream", frame)
    
    # Press 'q' to quit the video stream
    if cv2.waitKey(300) & 0xFF == ord('q'):
        break

# Stop the video stream
streamer.stop_thread()
cv2.destroyAllWindows()
```

### Arguments:

- `video_source`: The source of the video, which could be a file path or a camera index (`0` for webcam).
- `fps` (optional): Frames per second for the video stream. If not provided, the default FPS of the video source is used (or `30` if unavailable).
- `resolution` (optional): A tuple specifying the width and height for resizing the video frames. If not provided, the original resolution of the video source is used.
- `auto_restart` (optional): If set to `True`, the video stream will automatically restart if the video source becomes unavailable. Default is `False`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
