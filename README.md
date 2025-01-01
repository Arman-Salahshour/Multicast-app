# Multicast App

## Overview

The **Multicast App** is a distributed multimedia streaming system that facilitates real-time video and image streaming across multiple clients and channels. It is built using Python and integrates with the FastAPI framework for efficient backend processing and communication.

The app allows for the setup of a multicast server to manage multiple channels and clients, enabling seamless streaming of multimedia content. The project showcases robust networking, multithreading, and media handling capabilities.

---

## Features

- **Multicast Streaming**: Real-time distribution of video frames across multiple channels using UDP multicast.
- **Dynamic Channel Management**: Supports dynamic creation and management of channels for efficient streaming.
- **Client-Server Architecture**: Modular separation of server and client logic for scalable design.
- **Image and Frame Processing**: Frame extraction and image-to-JSON conversion for efficient data transfer.
- **Configurable Components**: Flexible configurations for server, client, and channel settings.

---

## Architecture

The app is built using a modular architecture with the following components:

- **Server**: Handles channel initialization, media scheduling, and multicast streaming.
- **Client**: Receives streaming data and processes it for local storage or playback.
- **Channel**: Manages media schedules and serves as a node for multicast distribution.
- **Utilities**: Includes frame extraction and image-to-JSON conversion tools for preparing multimedia content.

---

## Algorithms Used

### 1. **Frame Extraction Algorithm**

- **Purpose**: Extracts frames from video files for streaming.
- **Implementation**:
  - The `frameConvertor.py` script reads a video file frame by frame using OpenCV.
  - Frames are resized to a fixed resolution for uniformity and saved at regular intervals.
  - Key steps:
    1. Open the video file.
    2. Resize each frame to a width of 720 pixels.
    3. Save every `n`-th frame to optimize data transfer and reduce storage.

### 2. **Image-to-JSON Conversion Algorithm**

- **Purpose**: Converts image data into JSON format for efficient network transmission.
- **Implementation**:
  - Images are encoded in Base64 to transform binary data into a string format.
  - Packets are created to divide the encoded image into manageable chunks.
  - Key steps:
    1. Read the image file as binary data.
    2. Encode the data into Base64.
    3. Split the encoded string into packets of size `win` bytes.
    4. Append packet metadata (e.g., frame number).

### 3. **Dynamic Scheduling for Media Programs**

- **Purpose**: Allocates time slots to media programs dynamically for each channel.
- **Implementation**:
  - Randomization ensures even distribution of media programs across the day.
  - Scheduling adjusts based on the number of programs and their durations.
  - Key steps:
    1. Shuffle the list of program keys.
    2. Assign time intervals by dividing 24 hours by the number of programs.
    3. Store the schedule in JSON format for client retrieval.

### 4. **Multicast Communication Protocol**

- **Purpose**: Enables real-time data transmission to multiple clients simultaneously.
- **Implementation**:
  - UDP sockets are used to multicast packets to subscribed clients.
  - Channels act as intermediaries, sending data to specific multicast groups.
  - Key steps:
    1. Create a socket and join a multicast group.
    2. Configure the Time-To-Live (TTL) parameter to control packet propagation.
    3. Continuously send data packets to the multicast group.

### 5. **Thread-Safe Networking**

- **Purpose**: Ensures reliable server-client communication under multithreading.
- **Implementation**:
  - Python’s threading and multiprocessing libraries are used to handle concurrent connections.
  - Locks are implemented to manage shared resources safely.
  - Key steps:
    1. Use thread locks to synchronize access to shared data structures.
    2. Spawn threads for handling client connections and data transmission.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multicast-app.git
   cd multicast-app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have a Python version compatible with the project (>=3.7).

---

## Usage

### Server Setup

1. Navigate to the server directory.
2. Run the `server.py` script:
   ```bash
   python server.py
   ```

### Channel Setup

1. Initialize channels using the `channel.py` script:
   ```bash
   python channel.py
   ```

### Client Interaction

1. Start a client instance by running the `client.py` script:
   ```bash
   python client.py
   ```
2. Specify the client ID and channel number to start receiving data.

---

## Configuration

The following constants are configurable in the `*_constants.py` files:

- **Host and Port**:
  - Default host: `127.0.0.1`
  - Default port: `65432`
- **Message Size**:
  - Text message size: `1024`
  - Image message size: `4096`
- **Multicast Group**:
  - Group IP: `224.0.0.0`
  - Starting port: `10000`

---

## Future Enhancements

- Implement a web-based frontend for monitoring and managing channels.
- Add support for multiple video formats and live stream input.
- Introduce advanced error handling for network interruptions.
- Expand to support cloud deployment.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

