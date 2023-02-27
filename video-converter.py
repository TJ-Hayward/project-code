import cv2
import numpy as np
import csv 
# Here k is one more that how many videos you need to convert into coordinates
# It will run the code until all the videos are converted
participant_id = 1
all_data = []
while participant_id <= 48 :
    trick = 1
    while trick <= 6:
        status = 1
        while status <= 3:
            # Set up video capture
            cap = cv2.VideoCapture(f'Videos/p{participant_id}-t{trick}-s{status}.mp4')

            #record the frame height and width
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Define the color range for the dot
            lower = np.array([116,110,144])
            upper = np.array([121,255,249])

            # Initialize the location of the dot and time elapsed
            x, y = 0, 0
            time_elapsed = 0

            #log dots 
            dot_location = []

            while cap.isOpened():
                # Read a frame from the video
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert the frame to the HSV color space
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                # Threshold the frame to find the dot
                mask = cv2.inRange(hsv, lower, upper)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # If the dot is found, update its location
                if contours:
                    contour = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(contour)
                    t = str(cap.get(cv2.CAP_PROP_POS_MSEC))
                
                # Draw a circle at the location of the dot
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                #add the coords to the list
                dot_location.append((x,y))

                # Write the coordinates to the log file with unique corresponding name
                # with open(f'Results/dot_coordinates{k}.json', 'a') as f:
                #     f.write(f"({x},{y},{time_elapsed}),") 
                'frame_dimensions'
                frame_dimensions= ({frame_width}, {frame_height})
                all_data.append({'participant_id': participant_id, 'trick': trick, 'status': status, "x":x, "y":y, "time_stamp":time_elapsed, 'frame_dimensions': frame_dimensions})
                
                # Display the frame
                # cv2.imshow('frame', frame)
                # if cv2.waitKey(1) == ord('q'):
                #     break
                
                # Update the time elapsed
                time_elapsed = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            # Release the video capture and close all windows
            # cap.release()
            # cv2.destroyAllWindows()
            status = status + 1
        trick = trick + 1
    participant_id = participant_id + 1

fields = ['participant_id', 'trick', 'status', "x", "y", "time_stamp",'frame_dimensions']

with open('data.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields)

    writer.writeheader() 

    writer.writerows(all_data)
