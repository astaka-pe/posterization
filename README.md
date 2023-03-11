# Posterization

<img src="anim.gif" width=500>

## Environment

<img src="https://img.shields.io/badge/OS-macOS-blue" alt="macOS">
<img src="https://img.shields.io/badge/python-3.7-blue" alt="python3.7">

```
pyside6
opencv-python
pillow
```

## Demo

1. Run
```
python main_gui.py
```

2. Open a source file from `Sidebar -> File -> Open`

<img src="docs/openfile.png" width=500>

3. Get a posterized image

   - Obtain various posterized images by changing the hyperparameters
   - Switch images by `original image` and `posterized image` buttons

4. Save the posterized image from `Sidebar -> File -> Save`

## Note

- https://docs.opencv.org/4.x/d3/d50/group__imgproc__colormap.html