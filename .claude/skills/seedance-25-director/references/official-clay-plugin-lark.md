# 【Dreamina】Seedance 2.5 Clay Renderer Plugin User Guide

> **Աղբյուր՝** https://bytedance.larkoffice.com/wiki/TrbCwqIZFiblb0kqshZccJ4mndd  
> **Պատճենված է՝** 2026-10-29, ամբողջական տեքստով։ Հիմնական ուղեցույցում հղված ենթաուղեցույցն է։  
> Նկարները (33) նշված են ֆայլի անունով, իրենք ներբեռնված չեն։


> 💬 This is the official user guide for the Dreamina Seedance 2.5 Clay Renderer plugin for Blender and Maya. Follow the steps below to install the plugin, export clay render videos with one click, and go straight to Dreamina's web platform’s Generate flow or Canvas where your renders serve as reference video input. This creates a seamless pipeline from 3D clay render production to AI-powered video generation.

### Set up the plugin in Blender

#### Download the plugin zip package from the official website

Log in to the Dreamina website at https://jimeng.jianying.com/ai-tool/home and download the plugin from the downloads section. 

[🖼 Image: 截屏2026-09-29 11.32.24.png] <!-- lark-image:WU56bsGPKoM2f4xyoYicuNtsnEe -->

[🖼 Image: 截屏2026-09-29 11.34.28.png] <!-- lark-image:CDp7buEreoQZRyxJxpBcb1sZn0f -->

#### Install in Blender

- Once Blender is downloaded and installed, click**Edit**in the top menu bar, then select **Preferences**.

[🖼 Image: image.png] <!-- lark-image:VamfbJUUToTmhpxvEnccID2QnQe -->

[🖼 Image: image.png] <!-- lark-image:WozpbTCuRo54WKxcXvEclpt6nya -->

- In the**Preferences**panel, select **Add-ons**from the left sidebar, click the dropdown arrow on the far right, and select **Install from Disk**.

[🖼 Image: image.png] <!-- lark-image:Zjn1bJyEVor1TEx96Oyc5RmKnBb -->

- Navigate to the saved zip package, select the appropriate plugin version, and click**Install from Disk**in the bottom-right corner to install.

[🖼 Image: image.png] <!-- lark-image:QP7jbWmnToLLrVxzxcFcS69gnSf -->

- Once installed, the page will display "Seedance 2.5 Clay Render & Upload". Keep the plugin **checked** and return to the main page.

[🖼 Image: image.png] <!-- lark-image:EBVtbYrVXoJ7UXxDveXcuLhvnkb -->

- In the main 3D View, click the **arrow on the right edge** or press **N** to open the Sidebar, then select the Dreaminatab to open the panel. 

[🖼 Image: image.png] <!-- lark-image:J2olb4dUwog3YuxtQf4chpybnZd -->

[🖼 Image: 新07-panel.png] <!-- lark-image:LAAKbd1JBoChIYx5IeLcdw05nLe -->

#### Export and upload to Dreamina web

##### Method 1: Render and export from Blender

- Under Source in the plugin panel, select **Camera**.

- Set camera parameters, resolution, save location, etc. as needed, then click **Render**.

- Once the render is complete, the upload option will appear. Click **Generate** to upload the video to Dreamina Generate flow, or click **Canvas** to upload the video to Dreamina Canvas.

[🖼 Image: en01-camera-idle.png] <!-- lark-image:UpmObrC1io3f6gxF5aFcyrbcnob -->

[🖼 Image: en02-camera-ready.png] <!-- lark-image:LwQgbCDKJoOav2xhukDcSEBmnId -->

##### Method 2: Upload a local video

- Under Source in the plugin panel, select **Local File**.

- Navigate to the local clay render video file. Click **Generate** to upload the video to Dreamina Generate flow, or click **Canvas** to upload the video to Dreamina Canvas.

[🖼 Image: 1104-local-ready.png] <!-- lark-image:FMwUbAppvoin9rxAIqwc1dUonjb -->

[🖼 Image: image.png] <!-- lark-image:THq4bKrmwoa9pRxaBKkcPsBondh -->

- Both methods take you to the Dreamina web page, with your clay render video loaded as reference video input.

[🖼 Image: 截屏2026-09-29 11.42.37.png] <!-- lark-image:M9zAbXEf6on02XxdqKwcuXIUnre -->

[🖼 Image: 截屏2026-09-29 11.43.06.png] <!-- lark-image:NYe0beC9DoHFkaxdNuPccBU4nCf -->

### Set up the plugin in Maya

#### Download the plugin zip package from the official website

Log in to the Dreamina website at https://jimeng.jianying.com/ai-tool/home and download the plugin from the downloads section. 

[🖼 Image: 截屏2026-09-29 11.32.24.png] <!-- lark-image:JQDvb2BqnoyF6Lxqb0PcVI0bnL2 -->

[🖼 Image: 截屏2026-09-29 11.44.59.png] <!-- lark-image:OFYIbdpW1oJAyqxyrOXchZ4gnnd -->

#### Unzip and run the installation script

On Mac, run install_maya_plugin.command

On Windows, run install_maya_plugin.bat

[🖼 Image: image.png] <!-- lark-image:XjiZbdyzYo163zxuNi0c3uW4nde -->

- On Mac, you may need to click the question mark in the top-right corner of the security popup, then go to Privacy & Security and select **Open Anyway**.

[🖼 Image: image.png] <!-- lark-image:EWBzbFzXboUXlqxaTZKc2hHEnDd -->

[🖼 Image: image.png] <!-- lark-image:SUC8b7fh1opj8Wx4rQzcSw93nnf -->

- The script will run in Terminal. Once it shows "Done", press Enter to close, then restart Maya and allow access to the plugin location.

[🖼 Image: image.png] <!-- lark-image:WSp2bFdlCoZWwQx9zgicQf9lnxf -->

#### Select the plugin in Maya

- Open Maya and create a new project or open an existing one.

- In the top menu bar, click **Windows** → **Settings/Preferences → Plug-in Manager**

[🖼 Image: image.png] <!-- lark-image:Ja2DbDJWPoaPqDxg3NycqjNfnNA -->

- In the **Plug-in Manager**, click Browse  →  navigate to the Dreamina plugin folder and open the plug-ins directory.

- Select jimeng_maya_uploader_plugin.py and click Open.

[🖼 Image: image.png] <!-- lark-image:UFzhbqeYroVaYLxL20vcnO3Tn8c -->

[🖼 Image: image.png] <!-- lark-image:MMc2bUrMwoTTASxyoDzcl85lnfh -->

[🖼 Image: image.png] <!-- lark-image:IKrDbCMkloI5MbxlSz0cyE1PnFg -->

- In the Plug-in Manager, find jimeng_maya_uploader_plugin.py and check **Loaded** and **Auto load**.

[🖼 Image: image.png] <!-- lark-image:RNrpbLi9CoonjuxlJ8Fc6XOLnad -->

- Once the plugin is installed, **Seedance 2.5 Clay Render & Upload** will appear at the top of the page.

[🖼 Image: 截屏2026-09-29 15.13.25.png] <!-- lark-image:PQuqb57SDoEMg5xJGt2cV0Vknda -->

#### Export and upload to Dreamina web

##### Method 1: Render and export from Maya

- Under Source, select **Camera**

- Set camera parameters, resolution, frame range, and save location as needed, then click **Render**.

- Navigate to the local clay render video file. Click **Generate** to upload the video to Dreamina Generate flow, or click **Canvas** to upload the video to Dreamina Canvas.

[🖼 Image: 截屏2026-09-29 15.15.16.png] <!-- lark-image:IDsfbBDsyoJr9xxR22bcZ8fon2c -->

[🖼 Image: 截屏2026-09-29 15.15.31.png] <!-- lark-image:Hf7cb0DDBoagqUx6Symckdd6nUd -->

##### Method 2: Upload a local video

- Under Source, select **Local File**.

- Navigate to the local file, click **Render**, then click **Generate** to upload the video to Dreamina Generate flow, or click **Canvas** to upload the video to Dreamina Canvas.

[🖼 Image: 3maya-en-local-idle.png] <!-- lark-image:QvjOb4v4zowUxgxqr53cY0ManJh -->

[🖼 Image: 3maya-en-local.png] <!-- lark-image:YGKAbgilloA0kXxcvx4cvVlknwh -->

Both methods take you to the Dreamina web page, with your clay render video loaded as reference video input.

[🖼 Image: 截屏2026-09-29 11.42.37.png] <!-- lark-image:NBVVbvqhHo8svmxNlJIc67Hvnld -->

[🖼 Image: 截屏2026-09-29 11.43.06.png] <!-- lark-image:JwzJbZ0vyofJfkxBgm5coq3knsd -->
