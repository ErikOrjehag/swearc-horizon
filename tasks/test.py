from time import time

unix = 1463827662
mins = int((unix - time()) / 60)
hours = int(mins // 60)
mins -= int(hours * 60)

print("Your train leaves in " + str(hours) + " hours and " + str(mins) + " minutes.")