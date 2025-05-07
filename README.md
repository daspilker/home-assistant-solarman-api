Solarman API Integration for Home-Assistant
===========================================

Home Assistant component for fetching inverter data from the Solarman Cloud API.

It has been tested with a Deye SUN600G3-EU-230 microinverter.

Prerequisites
-------------

1. Your inverter needs to be set up with the Solarman Cloud. Refer to the manual of your inverter.
2. Contact Solarman to apply for API access, see https://doc.solarmanpv.com/en/Documentation%20and%20Quick%20Guide.
3. This integration must be installed with a custom repository in HACS. So you need to install HACS first if not already
installed. See https://www.hacs.xyz/.

Installation
------------

1. In HACS, add a custom repository. The repository URL is `https://github.com/daspilker/home-assistant-solarman-api`.
   Select type "integration".
2. Search for "Solarman API" in HACS and download the integration.
3. Restart Home-Assistant
4. Add the "Solarman API" integration.
5. Enter your credentials for the Solarman Cloud. Also enter the serial number of your inverter.

Development Setup
-----------------

1. Clone this repository. If using Windows, clone the repository in WSL.
2. Open Visual Studio Code. When asked, reopen Visual Studio code in the dev container.
3. Run the `scripts/develop` to start HA and test out your new integration.
