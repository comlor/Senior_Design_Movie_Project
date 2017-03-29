import sys

def main():
    print("Argument: " + sys.argv[7])

if __name__ == "__main__":
    main()



'''
import subprocess

def start_job_py():
    blender = "PATH TO BLENDER APPLICATION" ( id: blender.exe )
    main_scene = "PATH TO BLENDER FILE ( ie: my_test.blend )
    script = "PATH TO SCRIPT YOU ARE PASSING TO BLENDER ( ie: job.py )

    sub = subprocess.Popen([blender + " " + main_scene + " -b -P " + script,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = sub.communicate()

def start_render_py():
    This is largely dependant on how the scene is setup.  If we are splitting the blend file into multiples the code
    will change.  Otherwise the code will work as is except adding the hadoop call.



def start_animation():
    script = PATH TO ANIMATE SCRIPT ( ie: animate_scene.py )
    blender = PATH TO BLENDER ( ie: blender.exe )

    sub = subprocess.Popen(blender + " -b -P " + script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = sub.communicate()
'''
