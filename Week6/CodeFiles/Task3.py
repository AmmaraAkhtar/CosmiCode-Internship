import json 


data={
    "Name":"Ammara Akhtar",
    "Age":19,
    "Languages":["C++","JAVA","C#"],

}

with open("data.json","w") as file:
    json.dump(data,file,indent=4)
    print("Data is write to data.json Sucessfully..")


with open("data.json", "r") as file:
    loaded=json.load(file)
    print("Data is read successfully from json.data")


print(loaded)
print("Name",loaded["Name"])