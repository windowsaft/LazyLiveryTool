import PySimpleGUI as sg
import subprocess
import os
import json
import datetime
from psgtray import SystemTray


"""
Simple GUI for DEV LIVERY BUILDS.
Added the ability to auto-generate the models.json file.
Buttons just do what they say.
"""

def LazyLiveryTool():
    sg.ChangeLookAndFeel('Dark')
    layout =  [
                [sg.Text('LazyLiveryTool', size=(40, 1), font=('Any 15'))],
                [sg.Output(size=(90,20), font='Courier 12')],
                [sg.Button('generate models.js'), sg.Button('update gltf-files'), sg.Button('merge files'), sg.Button("Hide window", button_color=("orange")), sg.Button('Exit', button_color=('white', 'firebrick3'))],
                ]

    icon = "./icon.ico"
    menu = ['', ['Show Window', 'Hide Window', 'Exit']]
    window = sg.Window('LazyLiveryTool', layout, finalize=True, icon=icon)
    tray = SystemTray(menu, single_click_events=False, window=window, tooltip="LazyLiveryTool", icon=icon)
    

    # --------------- main loop --------------- 
    while True:
        event, values = window.read()

        if event == tray.key:
            event = values[event]

        # ----- exit app -----
        if event in ('Exit', None):
            break

        # ----- show window -----
        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        
        # ----- hide window in app tray -----
        elif event in ('Hide Window'):
            window.hide()
            tray.show_icon()

        # ----- hide window in app tray -----
        if event == "Hide window":
            window.hide()
            tray.show_icon()     

        # ----- generate models.js -----
        if event == 'generate models.js':
            print(f'{LogTime()} Building model.js....')
            modeljs()
            window.Refresh()
            print(f'{LogTime()} Done')

        # ----- merge files -----
        if event == 'merge files':
            print(f'{LogTime()} Merging files...')
            cmd = 'node build.js'
            sp = subprocess.Popen(cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

            rc=sp.wait()
            out,err=sp.communicate()

            if rc == 0:
                print(f'{LogTime()} Done')

            else:
                print("Error!")
                print(err.decode("UTF-8"))

        # ----- update gltfs -----
        if event == 'update gltf-files':
            print(f'{LogTime()} Updating gltf-files....')

            files = os.listdir(".\\ext")
            for item in files:
                if ".gltf" in item:
                    gltf("./ext/"+ item)
                    print( f"    ./ext/{item} updated!")

            window.Refresh()
            print(f'{LogTime()} Done')
    
    tray.close()
    window.close()

# --------------- models.js function ---------------
def modeljs():
    # --------------- models.js ---------------
    data = [
                {
                    "gltf": [
                        ""
                    ],
                    "bin": [
                        ""
                    ],
                    "output": {
                        "gltf": [
                            ""
                        ],
                        "bin": [
                            ""
                        ]
                    },
                    "additions": [
                        {
                            "gltf": "",
                            "bin": ""
                        }
                    ]
                }
            ]

    # --------------- ./ext & ./out ---------------
    ext = os.listdir(".\\ext")
    binExtItems = []
    binOutItems = []
    gltfExtItems = []
    gltfOutItems = []

    for item in ext:
        if ".bin" in item:
            binExtItems.append("./ext/" + item)
            binOutItems.append("./.out/" + item)
        
        elif ".gltf" in item:
            gltfExtItems.append("./ext/" + item)
            gltfOutItems.append("./.out/" + item)

    data[0]["bin"] = binExtItems
    data[0]["gltf"] = gltfExtItems
    data[0]["output"]["bin"] = binOutItems
    data[0]["output"]["gltf"] = gltfOutItems



    # --------------- ./add---------------
    add = os.listdir(".\\add")
    for item in add:
        if ".bin" in item:
            data[0]["additions"][0]["bin"] = "./add/" + item
        
        elif ".gltf" in item:
            data[0]["additions"][0]["gltf"] = "./add/" + item


    # --------------- write to file & print ---------------
    print(json.dumps(data, indent=4))

    with open(file="models.json", mode='w') as jf:
        json.dump(data, jf, indent=4)
    

    # --------------- debug ---------------
    return data

# --------------- gltf update function ---------------
def gltf(gltfFile):
    # --------------- load models.js ---------------
    materials = {
        "materials": [
        {
            "name": "",
            "alphaMode": "BLEND",
            "pbrMetallicRoughness": {
                "metallicFactor": 0,
                "roughnessFactor": 0.2,
                "baseColorTexture": { "index": 0 }
            },
            "extensions": {
                "ASOBO_material_blend_gbuffer": {
                    "emissiveBlendFactor": 0,
                    "normalBlendFactor": 0,
                    "occlusionBlendFactor": 0
                },
                "ASOBO_material_draw_order": { "drawOrderOffset": 1 }
            }
        }
    ],
    }

    textures = {
        "textures": [
        {
            "extensions": {
                "MSFT_texture_dds": {
                    "source": 0
                }
            }
        }
    ],
    }

    images = {
        "images": [
        {
            "uri": "",
            "extras": "ASOBO_image_converted_meta"
        }
    ],
    }

    # --------------- load file ---------------
    with open(gltfFile, "r") as gltf:
        data = json.loads(gltf.read())
        gltf.close()


    materials["materials"][0]["name"] = data["materials"][0]["name"] # Materials
    images["images"][0]["uri"] = data["images"][0]["uri"]   # Images

    # --------------- write to file ---------------
    data["materials"] = materials["materials"]
    data["textures"] = textures["textures"]
    data["images"][0] = images["images"][0]
    
    with open(file=gltfFile, mode='w') as gltf:
        json.dump(data, gltf, indent=4)
    
    return(data)

# --------------- timestamps ---------------
def LogTime():
    x = datetime.datetime.now()
    time = x.strftime("[%H:%M:%S]")
    return time

if __name__ == '__main__':
    LazyLiveryTool()
