extern crate libc;
extern crate image;

use libc::{c_char, uint32_t};
use std::ffi::CStr;
use std::path::Path;

use image::imageops;

#[no_mangle]
pub extern fn crop_image(input_path_p: *const c_char, output_path_p: *const c_char, x: uint32_t, y: uint32_t, w: uint32_t, h: uint32_t) {
    // read string and convert to rust string slice
    let input_path_cstr = unsafe {
        // ensure that C pointer is not NULL.
        assert!(!input_path_p.is_null());
        // use CStr to wrap the pointer, finding the string length base on the NUL.
        CStr::from_ptr(input_path_p)
    };
    // convert it to Rust string slice.
    let input_path = input_path_cstr.to_str().unwrap();

    // read string and convert to rust string slice
    let output_path_cstr = unsafe {
        // ensure that C pointer is not NULL.
        assert!(!output_path_p.is_null());
        // use CStr to wrap the pointer, finding the string length base on the NUL.
        CStr::from_ptr(output_path_p)
    };
    // convert it to Rust string slice.
    let output_path = output_path_cstr.to_str().unwrap();

    // open image file
    let ref mut img = image::open(&Path::new(input_path)).unwrap();

    // crop image
    let subimg = imageops::crop(img, x, y, w, h);

    // save file
    let subimg_buff = subimg.to_image();
    subimg_buff.save(&Path::new(output_path)).unwrap();
}
