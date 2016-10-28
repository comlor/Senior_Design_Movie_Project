import json
#any of the variable names can be changed these are just what i came up for now.
#we would put the name of the file, this one is just a specific to my computer
with open('C:\\Users\\Angel Jimenez\\Downloads\\sample_format.czml') as czml_file:
    
#once we open the file we need to load into a variable, almost like a database
	czml_data = json.load(czml_file)

	#The movies_properties will hold format,quality, resolution, and email
	#movies _properties is a dictionary we can access the value using 
	#        movieproperties[''nameOfKey]
movie_properties = {'format': czml_data["movieProperties"]["format"],
                   'quality': czml_data["movieProperties"]["quality"],
                   'resolution': czml_data["movieProperties"]["resolution"],
                   'email': czml_data["movieProperties"]["email"]}

#gtlf_path will hold the file name
gltf_path = czml_data["czml"][0]["model"]["gltf"]

#Nested tuple conatining all the info scene.
#can be changed into a different data structure if needed.
#color and color  hold rgba
color = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["color"]["rgba"]
outlineColor = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["outlineColor"]["rgba"]
#outline width of the polyline
outlineWidth = czml_data["czml"][0]["path"]["material"]["polylineOutline"]["outlineWidth"]

#polylineOutline holds color, outlineColor, width 
polylineOutline = color, outlineColor, outlineWidth

#material holds polylineOutline
material = polylineOutline, ''

#path holds material, width, leadTime, trailTime, resolution
path = polylineOutline, czml_data["czml"][0]["path"]["width"],czml_data["czml"][0]["path"]["leadTime"],czml_data["czml"][0]["path"]["trailTime"],czml_data["czml"][0]["path"]["resolution"]

#cesium_version will hold hte version of cesium 
cesium_version =  czml_data["czml"][1]["version"]

#cameraPosition and sunPosition are dictionaries that hold three strings interpolationAlgorithm, interpolationDegree, 
#epoc, and cartographicRadian which is a list for values
cameraPosition = {'interpolationAlgorithm': czml_data["czml"][1]["position"]["interpolationAlgorithm"],
          'interpolationDegree': czml_data["czml"][1]["position"]["interpolationDegree"],
          'epoc': czml_data["czml"][1]["position"]["epoc"],
		  #each four elements in the list are for one point
          'cartographicRadian': czml_data["czml"][1]["position"]["cartographicRadian"]}  
sunPosition = {'interpolationAlgorithm': czml_data["czml"][2]["position"]["interpolationAlgorithm"],
          'interpolationDegree': czml_data["czml"][2]["position"]["interpolationDegree"],
          'epoc': czml_data["czml"][2]["position"]["epoc"],
		  #each four elements in the list are for one point         
		 'cartographicRadian': czml_data["czml"][2]["position"]["cartographicRadian"]}
		  
#cameraOrientation and sunOrientation hold three strings interpolationAlgorithm, interpolationDegree, 
#epoc, and unitQuaternion which is a list fo values	  		  
cameraOrientation = {'interpolationAlgorithm': czml_data["czml"][1]["orientation"]["interpolationAlgorithm"],
          'interpolationDegree': czml_data["czml"][1]["orientation"]["interpolationDegree"],
          'epoc': czml_data["czml"][1]["orientation"]["epoc"],
          		  #each five elements in the list are for one point
		  'cartographicRadian': czml_data["czml"][1]["orientation"]["unitQuaternion"]}
sunOrientation = {'interpolationAlgorithm': czml_data["czml"][2]["orientation"]["interpolationAlgorithm"],
          'interpolationDegree': czml_data["czml"][2]["orientation"]["interpolationDegree"],
          'epoc': czml_data["czml"][2]["orientation"]["epoc"],
          		  #each five elements in the list are for one point         
		 'cartographicRadian': czml_data["czml"][2]["orientation"]["unitQuaternion"]}






