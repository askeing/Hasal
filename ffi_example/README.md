# Prepare

## Install `Rust` and `Cargo`

You can follow the [Installation Guide](https://doc.rust-lang.org/cargo/getting-started/installation.html) to install `Rust` and `Cargo`.

### Windows

On Windows, you may have to install [Visual C++ 2015 Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) for `link.exe`.

## Build `crop` library

Build the library:
```bash
cd rust_crop
cargo build --release
```

Copy library into `ffi_example` folder, the file name might be `libcrop.so` or `crop.dll`:
```bash
$ cd ..
$ cp cp rust_crop/target/release/libcrop.dylib ./
```

### Windows

If the `python` on Windows is 32-bit, it can only load the 32-bit dll file.
You may have to cross compile the library by adding `i686-pc-windows-msvc` target on 64-bit Windows.
```bash
C:\Hasal\ffi_example\rust_crop> rustup target add i686-pc-windows-msvc
C:\Hasal\ffi_example\rust_crop> cargo build --release --target=i686-pc-windows-msvc
```

The `crop.dll` file should locate under `rust_crop\target\i686-pc-windows-msvc\release` folder.
You have to copy output dll file into `ffi_example` folder.

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
