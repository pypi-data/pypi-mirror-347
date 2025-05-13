=========
Changelog
=========

0.4.0 - 2021-Feb-02
---------------------
- ``platoons`` module for analysis using multiple driving routes
- Currently supporting finding similar routes using ``spatial_finder`` functions

0.3.6 - 2020-Nov-11
--------------------
- Interactive plot in ``strymread``
- Default map for ``strymmap`` set to Mapbox with an option for Googlemap
- Now ``strymread`` function ``plt_ts`` can take a non-default column other than 'Message' for plotting as an argument
- Bug fixes


0.3 - 2020-Oct-15
--------------------
- Bug fixes in ``strymread``
- Strym tools
    - ``graham_scan`` function to find convex hull and its perimeter for a cluster
    - ``ellipse_fit`` function to fit an ellipse/circle to a cluster of points on phase-space

0.2.4 - 2020-Sep-26
--------------------
- Documentation bug fixes
- Plotting bug fixes and improvement
- Strym tools
    - ACD Tool added to measure stop-and-go distance. Animation generation for phasespace evolution supported
    - Acceleration messages added to :code:`strymread` to be dbc independent
    - DBC now supports headlight message for highbeam, lowbeam etc. 

0.2.2 - 2020-Sep-09
--------------------
- Documentation format fix
- Minor fixes in code

0.2.1 - 2020-Aug-17
--------------------
- Documentation bug fixes
- Minor improvment over state-space calculation

0.2.0 - 2020-Aug-15
-----------------------
- Standalone functions from all classes moved to respective class definition as static method to reflect their usability
- Sphinx version updated
- Strym now packages DBC file. Currently suppported DBC file. Currently supported DBC file: Honda Pilot 2017, Toyota RAV4 2019 and 2020
- Support for creating serverless sqlite3 database in local system for easy querying of driving information

- class: :code:`strymread`
    - Bug fix: removes duplicate timestamped data from signals
    - `get_ts` now has additional column *BUS* that provides number of each timestamped message
    - Option to save RAW, UNDECODED Dataframe as sqlite3 via `createdb` parameter while object instantiation
    - A helper message `lead_distance` to retrive lead distance from csv file
    - Function name `extract` changed to `export2mat` that creates matlab .mat file of known, import signals
    - `state_space` function to extract consolidated dataframe with a number of signals that represents state space of the vehicle, resampled to desire frequency. Optional argument todb, when `True` saves state space dataframe to a sqlite3 table `STATE_SPACE`
    - `differentiate` method automatically falls back to AutoEncoder method when number of datapoints is less than 6.

0.1.13 - 2020-July-29
----------------------
- class: :code:`strymread`
    - Fixed Issue #16

0.1.12 - 2020-July-25
----------------------
- class: :code:`strymread`
    - Fixed a scaling bug in prediction made in AE-based differentiation

0.1.11 - 2020-July-23
----------------------
- Changes to permit strymread to work with Honda
 
- class :code:`strymread`
    - Added rel_velocity to retrieve relative velocity of targets from radar traces
    - Added create_chunks function to split discontinuous timeseries into continuous-chunked timeseries
    - Autoencoder based denoising method and application for estimation of lead vehicle's velocity
    - DBC support for Honda Pilot
    - Some inconsistency fixes

2020-July-02
---------------------
- modified for robust calling of meta and dashboard from snakemake files

- class :code:`meta`
    - Takes an array of dbc files, and calls methods from the vin_parser package to confirm that the VIN of a CSV file shoudl correspond to a particular dbc

- class :code:`strymread`
    - Added new functionality to do dictionary lookup of message/signal pairs when extracting a timeseries, rather than assuming all message/signal pairs correspond to Toyota naming conventions. New methods to touch when adding new message/signal pairs are prefixed with `_dbc_`

0.1.10 - 2020-July-01
---------------------
- setup modified to package examples and README folder in install path

- class :code:`dashboard`
    - works within the strym package to collect metadata files from within a folder and print interesting aspects of the collection
    
- class :code:`meta`
    - Works within the strym package to extract metadata from drives that are recorded using libpanda, with optional corresponding dashcam video

- class :code:`strymread`
    - Checks for monotonicity of the time in the recorded data
    - Two new Flag Attributes added: burst and success. Burst flag tells if data was recorded in burst, success tells if reading of csv file was successful

- class :code:`strymmap`
    - Conditionally import of bokeh and other widget-based libraries in Jupyter only to making strym work from terminal
    
    
0.1.9 - 2020-May-20
-------------------
- class :code:`strymread`
    - A new function :code:`extract` for extracting data in .MAT format to work with matlab
    - Changes to :code:`msg_subset` function, now returns an object of type :code:`strymread` with modified dataframe
    - Changes to plotting functions

0.1.8 - 2020-May-16
-------------------

- A few bug fixes and cosmetic changes.
- Freezing the master branch and creating a devel branch for active development.

0.1.7 - 2020-May-06
---------------------

- A new class :code:`phasespace` for phasespace analysis


0.1.6 - 2020-Apr-22
-----------------------
- class :code:`strymread`
    - Modified function to read radar traces. 
    - Bug fix for Function :code: `frequency`
    - New functions:
        - :code:`msg_subset`: For deriving a subset of original messages satisfying given criteria. See commit #819f2d6
        - :code:`time_subset`: For getting time-slices of original messages satisfying given criteria
        - :code:`acc_state`: Get the ACC (Adaptive Cruise Control) state of driving
        - :code:`accel_x`: Get the longitudinal acceleration. See commit #819f2d6
- Address issue #4, and issue #5.

- Function :code:`ts_sync` modified to inherit sample from one of the two input dataframes.
- New function :code: `time_index` and :code: `timeslices` for improved analysis of timeseries data


0.1.5 - 2020-Apr-01
----------------------
- class :code:`strymmap`
    - Replaced gmplot mapping with bokeh plot for map
    - Now saves map with drive route as png file using selenium and chormium webdriver

0.1.4 - 2020-Apr-01
---------------------
- Added a new class :code: `strymmap`
    - Added basic funcionality to read and parse CSV file containing GPS data obtained from Grey Panda.
    - Save Map HTML file from GPS Data to show drive route

0.1.3 - 2020-Apr-01
---------------------
- Bux fix. Refer to commit 9ef1a95

0.1.2 - 2020-Apr-01
--------------------
- A function to resample non-uniformly sampled timeseries to uniformly sampled timeseries data
- A function to differentiate timeseries data based on spline derivative method
- A function to denoise timeseries data based on moving average
- A function to perform temporal-splitting of timeseries dataframe
- A function to return centroid of a phase-space cluster
- A function to calculate average distance of a phase-space cluster from its centroid
- Plotting utility for temporal violin plot
- Can retrieve a timeseries message by given message ID/signal ID or message name/signal name

0.1.1 - 2020-Mar-30
--------------------
- class :code:`strymread`
   - Get the message count
   - Functions to retrieve yaw, acceleration, steer torque, steer rate, steering angle, steering fraction, wheel speeds, longitudinal and laternal measurements from Radar traces
   - Get datarate statistics from CAN data
   - Plot trajectory of driving based on Kinematic model
- timeseries-sync of two timeseries data of different and non-uniform sampling period
- Off-the-shelf integration function for timeseries data
- Function to analyze data rate throughput of a particular message.
- Visualize data distributionb through violin plot

0.1
-----
- Added a new class :code:`strymread`
   - Added basic functionality to Parse CSV-formatted CAN data captured usin comma.ai Panda and Giraffe connector.
   - Plot timeseries data by message name

unreleased
-----------
* Real-time capturing and visualization of CAN data using comma.ai Panda and Giraffe connector.
