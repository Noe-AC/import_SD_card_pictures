# Import SD card pictures and videos

**Description:**
Here is a Python script to import pictures and videos from a SD card to a computer.

**How to use:**

1. Put the script in the directory that you wish to find a folder of your pictures.
2. Run the script `copy_sony_pictures.py`.
3. Wait until the script ends.

**What it does:**

1. A folder named `/transferred_pictures` will be created in the same directory of the script.
2. When importing a picture, the script looks at the date that this picture was taken and copies it in the subfolder `/transferred_pictures/YYYY-MM-DD/file_type` where "`YYYY-MM-DD`" is the date of the picture and "`file_type`" is the type of file (`JPG` or `RAW` or `MTS` or `MP4`). A Sony `.AWR` raw file goes in the `RAW` folder. Only the `MTS` files are copied, not the whole `AVCHD` container.
4. Once all pictures are imported, a compressed and resized (3000x2000 pixels) copy of the jpegs are generated in the folder `/transferred_pictures/previews`. This compression/resize is done by [`sips`](https://ss64.com/mac/sips.html).

**Why is this script relevant:**

- Everyone has a different workflow. This script make my workflow faster, so maybe it could make yours faster too. I like to organize photos by date then file type.
- The compressed/resized pictures are nice to have because over time a big number of original high resolution JPGs and RAWs can be too heavy to carry on a mundane laptop. Having a compressed local version is nice to have (e.g. in the Photos app or else) while the original bigger files are backed somewhere in external hard drives and/or cloud providers.

**Dependencies:**

- `exifread` to read JPG and RAW metadata. Install with [`pip install ExifRead`](https://pypi.org/project/ExifRead/).
- `exiftool` to read MTS and MP4 metadata. Install with [`pip install PyExifTool`](https://pypi.org/project/PyExifTool/).

**Limitations:**

- It only imports `JPG`, `AWR`, `MTS` and `MP4` files for now.
- For now, it only imports the content of a SD card from Sony camera and the script was only tested on macOS. In particular, the `sips` command to make the compressed/resized images is only available on macOS, so this extra step must be turned off on other OS (just set the boolean variable `do_create_pictures_previews` to `False` in the script).

**See also:**

- A medium post about the first version of the script on [Medium](https://medium.com/@noe.aubin.cadot/importer-les-photos-et-les-vidéos-dune-carte-sd-grâce-à-python-6da6dfc46c9d) (in french).

**Changelog:**

- 2024-06-01: First release of the script `copy_sony_pictures.py`. It only imports the 'old' file structure.
- 2024-04-19: Added the option to import from the 'new' file structure.
- 2024-04-25: Expanded and reorganized the readme.
- 2024-05-10: Added the import of MP4 video files.

**To do:**

- Import SD cards from Canon, Nikon, Pentax, etc., with folders structures other than Sony. Technically this shouldn't be complicated using a recursive search in the SD card as this is independent on the specific file structure of the card. Nevertheless it should be tested that the script works with the specific RAW files of each brand. 
- Create also a compressed/resized version of the `MTS` and `MP4` videos for local storage, possibly via `ffmpeg`.

**Credit:** Noé Aubin-Cadot