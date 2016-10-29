# Senior_Design_Movie_Project
CSULA Senior Design Project for JPL Movie Project

PROJECT FILES: Short Description with noted known issues.

OBJ_import.py -- Imports OBJ file into blender and saves the .blend file

create_camera.py -- Creates camera path and camera objects and add follow_path to camera.
          -- Using blender UI can verify the camera path and camera exist and camera follows the path
          
render.py -- Gets the number of frames from the .blend header and renders each frame as a still image(currently png)
        -- PROBLEM** All rendered images are black.
        -- If rendered in blender UI 
              1. Press 0 on numpad - switches view to camera view
              2. Alt-A will start animation - and works ok, shows correct view, although textures are not working
              3. F12 in blender UI -- Renders black image
              
animate.py -- animate still images into a movie

movie_merge.py -- merges multiple movie files into single movie.
