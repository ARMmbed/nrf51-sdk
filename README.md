# nrf51-sdk
Module to contain files provided by the nordic nRF51 SDK. The latest version of this module uses files from Nordic SDK 8.1.0. The files are extracted from [here]. (https://developer.nordicsemi.com/nRF51_SDK/nRF51_SDK_v8.x.x/nRF51_SDK_8.1.0_b6ed55f.zip)

## Changes made to Nordic files
The files are kept the same as much as possible to the Nordic SDK. These minor modifications are made in order to integrate with mbed:

1. Add `#define asm __ASM` to the top of [nrf_delay.h](https://github.com/ARMmbed/nrf51-sdk/blob/master/source/nordic_sdk/components/drivers_nrf/hal/nrf_delay.h). Because all yotta mobules compile with -std=c99 which does not include "asm" keyword.
1. Add `#define BLE_STACK_SUPPORT_REQD` to the top of [ble_stack_handler_types.h](https://github.com/ARMmbed/nrf51-sdk/blob/master/source/nordic_sdk/components/softdevice/common/softdevice_handler/ble_stack_handler_types.h).
1. Add this patch to [nrf_svc.h](https://github.com/ARMmbed/nrf51-sdk/blob/master/source/nordic_sdk/components/softdevice/s130/headers/nrf_svc.h)

  ```diff
  index 3e907ea..fcb05a1 100644
  --- a/source/nordic_sdk/components/softdevice/s130/headers/nrf_svc.h
  +++ b/source/nordic_sdk/components/softdevice/s130/headers/nrf_svc.h
  @@ -53,7 +53,7 @@
     { \
       __asm( \
           "svc %0\n" \
  -        "bx r14" : : "I" (number) : "r0" \
  +        "bx r14" : : "I" ((uint32_t) number) : "r0" \
       ); \
     }    \
     _Pragma("GCC diagnostic pop")
  ```

## Porting new versions of Nordic SDK
A list of files currently requierd by mbed is maintained in [script/required_files.txt](https://github.com/ARMmbed/nrf51-sdk/blob/master/script/required_files.txt). [A python script](https://github.com/ARMmbed/nrf51-sdk/blob/master/script/pick_nrf51_files.py) is written to help porting from nordic sdk releases. **required_files.txt** is parsed to find a list of filenames. The script searches for these filenames in the sdk folder, and copy then into the yotta module mirroring the folder structure in the sdk. **extraIncludes** is automatically added to module.json to allow direct inclusion of noridc headers with just he filename.

### Script usage
```
python pick_nrf51_files.py <full-noridc-sdk-path> <nrf51-sdk-yotta-module-path>
```

There are files in the sdk with the same filename but in different folder. This is dealt with by excluding certain directories. The excluded directories are listed in [pick_nrf51_files.py](https://github.com/ARMmbed/nrf51-sdk/blob/master/script/pick_nrf51_files.py).

After running the script, the changes in [the previous section](#changes-made-to-nordic-files) will have to be applied manually again.

Folder structure or even file name can change between releases of the nordic sdk, hence a degree of manual adjustment is needed when porting.

## Using Noridc Headers
The nordic sdk is written in C and yotta modules support C++. If you are trying to include Nordic files in a cpp program, you need to use the `extern "C"` keyword around the includes.
```c
extern "C" {
#include "softdevice_handler.h"
}
```
