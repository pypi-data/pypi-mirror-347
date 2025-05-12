Traccar offers a free, open-source solution for researchers to gather GPS data from many participants. It achieves this through a robust client-server architecture, ensuring the security and reliability of your data collection process.

The system consists of two main components:

`Traccar Server`
: This server-side application (runs on a computer) acts as a central hub, receiving data from participant devices. It also provides a web interface for researchers to configure the system and access collected information.

`Traccar Client`
: This mobile application, available for Android and iOS, runs on participants' phones. It collects GPS data and sensor readings and then transmits them securely to the Traccar Server.

Traccar also offers API, which researchers can use with the LABDA package to download, parse, and integrate the collected data seamlessly into their analysis for in-depth exploration. Traccar simplifies the entire data collection and processing workflow for researchers.

For detailed information on Traccar server and client functionalities, visit their [official website](https://www.traccar.org/).

!!! warning "Limitations"

    **Offline Buffering:** If a phone loses connection, any GPS data collected during that time won't be saved. However, Traccar can temporarily store data on the device, but it might take over 24 hours to reach the server after reconnection.

    **Battery Drain:** The client app can be pretty demanding on phone batteries. Participants might need to charge their phones more often to ensure uninterrupted tracking.


## How to use it?

Below, we've outlined the steps to get started with Traccar.

### Server

!!! info

    This guide is for advanced users only. For most people, a cloud-based Traccar solution is easier to use. If you want to host your server at your institution, contact your IT department for assistance.

This docker-compose setup offers a simplified approach to launching the Traccar Server locally. It utilizes the built-in H2 database, allows customization through your configuration file, and directs logs to a designated folder.

``` yaml title="docker-compose.yml"
version: "3.9"

services:
  traccar:
    image: traccar/traccar:ubuntu
    container_name: traccar
    restart: unless-stopped
    ports:
      - 8082:8082
      - 5000-5150:5000-5150
      - 5000-5150:5000-5150/udp
    volumes:
      - ./logs:/opt/traccar/logs:rw
      - ./conf/traccar.xml:/opt/traccar/conf/traccar.xml:ro
```

To create a [custom configuration file](https://github.com/traccar/traccar/blob/master/setup/traccar.xml), refer to the provided template and [list of customizable parameters](https://www.traccar.org/configuration-file/]).

### Client

Download the mobile client apps for [Android](https://play.google.com/store/apps/details?id=org.traccar.client) and [iOS](https://itunes.apple.com/us/app/traccar-client/id843156974). To configure the app for your research project, you'll need to adjust these settings:

`Service status`
: Enable/disable the data collection.

`Device Identifier`
: This unique ID is crucial. The administrator must manually add your device to the Traccar server.

`Server URL`
: Enter the web address of your Traccar server.

`Location Accuracy`
: Set this to "High" for continuous GPS tracking. Other options rely on cell towers for location, which can be less precise.

`Frequency (seconds)`
: Choose how often location data is logged (ideally 15, 30, or 60 seconds).

`Distance (meters)`
: Leave this blank. It only sends data when the location changes by a set distance.

`Angle (meters)`
: Like distance, leave it blank for continuous updates.

`Offline Buffering`
: Enable this to store data on the phone if there's no connection. It will be sent later (up to 24 hours).

`Wake Lock`
: This prevents the phone from sleeping and ensures uninterrupted tracking.

!!! warning "Important Reminders"

    Allow the app to collect data in the background and make sure the app doesn't get automatically closed when idle.

::: labda.parsers.traccar.TraccarConnector
    options:
        heading_level: 2
        show_root_heading: true
        show_root_full_path: true
        show_bases: false
        members:
        - from_auth
        - get_server_info
        - get_subjects
        - get_data

::: labda.parsers.traccar.Subject
    options:
        heading_level: 3
        show_root_heading: true
        show_root_full_path: true
        show_bases: false
