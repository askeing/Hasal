# Prepare

## Install `Rust` and `Cargo`

You can follow the [Installation Guide](https://doc.rust-lang.org/cargo/getting-started/installation.html) to install `Rust` and `Cargo`.

## Build `crop` library

Build the library:
```bash
cd rust_crop
cargo build --release
```

Copy library into current folder, the file name might be `libcrop.so` or `crop.dll`:
```bash
$ cd ..
$ cp cp rust_crop/target/release/libcrop.dylib ./
```

# Run

Running script by following command:
```bash
$ python image_crop_tester.py
### Crop Image 10 times ###
###   Rust: 10.3863492012 seconds ###
### Python: 19.5685751438 seconds ###
```

# Clean output result

```bash
$ rm rust_output_*.jpg py_output_*.jpg
```

# Reference

- Image file: `Kings_College_London_Chapel_2.jpg` 
  - Photo by DAVID ILIFF.
  - License: [CC-BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en)
  - Source: [File:King's College London Chapel 2, London - Diliff.jpg](https://en.wikipedia.org/wiki/File:King%27s_College_London_Chapel_2,_London_-_Diliff.jpg).
