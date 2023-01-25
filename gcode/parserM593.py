#!/usr/bin/env python
import re, sys

# Purpose: Add M593 codes to ringer tower or other M593 prints for calibration
#
# Assumes Cura used and no M593 already added
#
# command line: parserM593.py input_file.gcode new_or_overwrite_M593_file.gcode

def main():
  # Make sure we have enough arguments
  if (len(sys.argv) < 3): # 0, 1, 2
    print("Missing paramters, run like this: parserM593.py input.gocde output.gcode required")
    return(-1)

  # Save so we can put it back
  stdout_def = sys.stdout
  
  input=sys.argv[1]; 
  output=sys.argv[2];

  fdin = open(input, "r")
  sys.stdout = open(output, "w") # This is now stdout so we can use print()

  # Initialize out variables
  layer=0

  # Loop through the input file
  for line in fdin:
    # Print the line, note we are adding M593 lines at layer changes
    # but keeping all else the same.
    print(line, end='')
    # Looking for ;LAYER:
    if 'LAYER:' in line:
      # Now get the layer number
      layer = int(line.split(':')[1])

      # Found layer so insert new m593 command here
      # M593 F{(layer < 2 ? 0 : 15 + 45.0 * (layer - 2) / 297)} ; Hz Input Shaping Test
      if layer < 2:
        value = 0
      else:
        value = 15 + 45.0 * (layer - 2) / 297

      print("M593 F", value, sep='')

  sys.stdout.close() # Close the physical file
  sys.stdout = stdout_def # Put it back
  return();  

# Kick off the code
if __name__ == "__main__":
  main()
