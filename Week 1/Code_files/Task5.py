total_seconds=int(input("Enter time in seconds:"))

hours=total_seconds//3600
remaining=total_seconds%3600
min=remaining//60
sec=remaining%60

print(f"{total_seconds} Time in Seconds=> {hours} Hours, {min} Minutes, {sec} Seconds")