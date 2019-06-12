This is a program that handles drone-related problems. The program contains mainly two functions: 
1) Display of the room plan and drone routes based on data from LIDARPoints.csv and Flightpath.csv;
2) Mapping of the room plan based on data from LIDARPoints.csv and Flightpath.csv.

To run the Display program, simply use "python SCVL.py Display TEST_MODE_BOOL SCAN_ID" command.

Detailed explanation: 
1) The first argument must be correctly spelled as Display (case sensitive);
2) The second argument is the test mode option. It can either be True or False.
3) The third argument is the scan ID that the user wants to display. It ranges from 0 to 33, according to the data in LIDARPoints.csv and Flightpath.csv. If the user wants all scans to be displayed at once, simply type in 'all'(no quotation marks) to run. 

When the program displays single scans, the current scan will be displayed in dark blue where othere scans' data will be shown in light blue. When the progtam displays all scans together, the route of the drone will be marked in red lines. 

To run the Mapping program, simply use "python SCVL.py Mapping TEST_MODE_BOOL" command. This command only takes two arguments. There will be a graph poping up showing all the walls created in different colors. And if there are no Mapping.csv file under your directory earlier, it should appear after the command is excecuted. 

In Mapping, the walls are created within 2 steps:
1) take look at each scan dot and merge the ones close to each other together as line segements. 
2) further merge the line segements until the maximum length is achieved. 
