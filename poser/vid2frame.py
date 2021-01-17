import cv2

vidcap = cv2.VideoCapture('C:\\Users\\micha\Videos\\HtN Workout Vide\\workout.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("frames\\frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1