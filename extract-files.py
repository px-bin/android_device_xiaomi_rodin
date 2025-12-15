#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3

# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0

from extract_utils.fixups_blob import (
    BlobFixupCtx,
    File,
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

from extract_utils.fixups_lib import (
    lib_fixup_remove_arch_suffix,
    lib_fixups_user_type,
    libs_clang_rt_ubsan,
)

from extract_utils.tools import (
    llvm_objdump_path,
)

from extract_utils.utils import (
    run_cmd,
)

namespace_imports = [
    'device/xiaomi/rodin',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
]

def blob_fixup_graphic_buffer_size(
    ctx: BlobFixupCtx,
    file: File,
    file_path: str,
    *args,
    **kwargs,
):
    for line in run_cmd(
        [
            llvm_objdump_path,
            '--disassemble-all',
            file_path,
        ]
    ).splitlines():
        line = line.split(maxsplit=5)
        if len(line) != 6:
            continue
        offset, _, instruction, register, value, _ = line
        if instruction == 'mov' and register[:-1] == 'w0' and value == '#0x100':
            with open(file_path, 'rb+') as f:
                f.seek(int(offset[:-1], 16))
                f.write(b'\x00\xa6\x81\x52')

lib_fixups: lib_fixups_user_type = {
    libs_clang_rt_ubsan: lib_fixup_remove_arch_suffix,
}

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None

def lib_fixup_odm_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'odm' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libneuron_graph_delegate.mtk',
        'libtflite_mtk',
        'vendor.mediatek.hardware.apuware.utils@2.0',
        'vendor.mediatek.hardware.apuware.utils-V1-ndk',
        'vendor.mediatek.hardware.apuware.apusys-V5-ndk',
        'vendor.mediatek.hardware.videotelephony-V1-ndk',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    # IMS
    'system_ext/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('blob-patches/ImsService/'),

    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),

    # KeyMint
    (
        'odm/lib64/libmt_mitee.so',
        'vendor/bin/hw/android.hardware.security.keymint@3.0-service.mitee',
    ): blob_fixup()
        .replace_needed('android.hardware.security.keymint-V3-ndk.so', 'android.hardware.security.keymint-V3-ndk-v34.so'),

    # Sensors
    'odm/bin/hw/vendor.xiaomi.sensor.citsensorservice.aidl': blob_fixup()
        .add_needed('libui_shim.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so')
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),

    'odm/bin/hw/vendor.xiaomi.hw.touchfeature-service': blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so')
        .replace_needed('vendor.xiaomi.hw.touchfeature-V1-ndk.so', 'vendor.xiaomi.hw.touchfeature-V1-ndk-prebuilt.so'),

    # Display
    'odm/lib64/hw/displayfeature.default.so': blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),

    (
        'vendor/bin/mnld',
        'vendor/lib64/mt6899/libpqconfig.so',
        'vendor/lib64/mt6899/libaalservice.so',
        'odm/lib64/libpaperMode.so',
        'odm/lib64/libmiBrightness.so',
        'odm/lib64/libmiSensorCtrl.so',
        'odm/lib64/libcolortempmode.so',
        'odm/lib64/libtruetone.so',
        'odm/lib64/libsre.so',
        'odm/lib64/libsdr2hdr.so',
        'odm/lib64/libdither.so',
        'odm/lib64/libhistprocess.so',
        'odm/lib64/libadaptivehdr.so',
        'odm/lib64/librhytheyecare.so',
        'odm/lib64/libflatmode.so',
        'odm/lib64/libvideomode.so',
    ): blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),

    (
        'vendor/lib64/hw/mt6899/vendor.mediatek.hardware.pq_aidl-impl.so',
        'vendor/lib64/mt6899/libmmlpqImpl.so',
        'vendor/lib64/libsilkybrightnesscore.so',
        'vendor/lib64/libaudiocloudctrl.so',
        'vendor/lib64/librt_extamp_intf.so',
        'vendor/lib64/libpqxmlparser.so',
        'vendor/lib64/libmicamera_aidl_provider.so',
        'vendor/lib64/libpqxmlflagparser.so',
        'odm/lib64/libmiXmlParser.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),

    # Graphics
    (
        'vendor/bin/hw/mt6899/android.hardware.graphics.allocator-V2-service-mediatek.mt6899',
        'vendor/lib64/libaimemc.so',
        'vendor/lib64/libgpud.so',
        'vendor/lib64/mt6899/libmtkcam_grallocutils.so',
        'vendor/lib64/libmtkcam_grallocutils_aidlv2helper.so',
        'vendor/lib64/egl/mt6899/libGLES_mali.so',
        'vendor/lib64/hw/mt6899/android.hardware.graphics.allocator-V2-mediatek.so',
        'vendor/lib64/hw/mt6899/mapper.mediatek.so',
        'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so',
    ): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),

    'vendor/lib64/libcodec2_fsr.so': blob_fixup()
        .call(blob_fixup_graphic_buffer_size)
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),

    'vendor/lib64/hw/hwcomposer.mtk_common.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),

    (
        'vendor/lib64/libmialgoengine.so',
        'vendor/lib64/libcom.xiaomi.grallocutils.so',
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so')
        .call(blob_fixup_graphic_buffer_size),

    # Camera
    'vendor/lib64/libmicamera_hal_core.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so')
        .call(blob_fixup_graphic_buffer_size)
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),

    (
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-client.so',
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-V1-ndk.so',
        'vendor/lib64/vendor.xiaomi.hardware.camera.injection-service.so',
    ): blob_fixup()
        .replace_needed('android.hardware.camera.device-V1-ndk.so', 'android.hardware.camera.device-V2-ndk.so'),

    'vendor/lib64/libcamera2ndk_vendor.so': blob_fixup()
        .replace_needed('android.frameworks.cameraservice.service-V2-ndk.so', 'android.frameworks.cameraservice.service-V3-ndk.so')
        .replace_needed('android.frameworks.cameraservice.device-V2-ndk', 'android.frameworks.cameraservice.device-V3-ndk'),

    (
        'vendor/lib64/libcameraopt.so',
        'vendor/lib64/mt6899/libcam.hal3a.so',
        'vendor/lib64/mt6899/libcam.hal3a.ctrl.so',
        'vendor/lib64/mt6899/libmtkcam_taskmgr.so',
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),

    # APU / ML
    (
        'vendor/lib64/mt6899/libneuralnetworks_sl_driver_mtk_prebuilt.so',
        'odm/lib64/libwa_widelens_undistort.so',
        'odm/lib64/libarcsoft_beautyshot.so',
        'odm/lib64/libMiPhotoFilter.so',
        'odm/lib64/libMiEmojiEffect.so',
        'vendor/lib64/mt6899/libneuron_adapter_mgvi.so',
        'system_ext/lib64/libMiVideoFilter.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle')
        .clear_symbol_version('AHardwareBuffer_isSupported')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),

    # UltraHDR
    'vendor/lib64/libultrahdr_rodin.so': blob_fixup()
        .replace_needed('libjpegencoder.so', 'libjpegencoder_rodin.so')
        .replace_needed('libjpegdecoder.so', 'libjpegdecoder_rodin.so'),

    (
        'odm/lib64/camera/plugins/capture/com.xiaomi.plugin.gainmap.so',
        'odm/lib64/camera/plugins/capture/com.xiaomi.plugin.jpegrAggr.so',
    ): blob_fixup()
        .replace_needed('libultrahdr.so', 'libultrahdr_rodin.so'),

    # Audio
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .replace_needed('android.hardware.audio.effect-V2-ndk.so', 'android.hardware.audio.effect-V3-ndk.so')
        .replace_needed('libalsautils.so', 'libalsautils-v34.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so')
        .replace_needed('libxlog.so', 'libxlog_stub.so'),

    'vendor/lib64/hw/android.hardware.soundtrigger3-impl.so': blob_fixup()
        .replace_needed('android.hardware.soundtrigger3-V2-ndk.so', 'android.hardware.soundtrigger3-V3-ndk.so'),

    # Bluetooth
    (
        'vendor/lib64/hw/audio.primary.mediatek.so',
        'vendor/lib64/hw/audio.bluetooth.default.so',
        'vendor/lib64/libbluetooth_audio_session_aidl_mtk.so',
        'vendor/lib64/android.hardware.bluetooth.audio-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('android.hardware.bluetooth.audio-V4-ndk.so', 'android.hardware.bluetooth.audio-V5-ndk-mtk.so'),

    (
        'vendor/lib64/hw/audio.bluetooth.default.so',
        'vendor/lib64/android.hardware.bluetooth.audio-V5-ndk-mtk.so',
        'vendor/lib64/vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so',
    ): blob_fixup()
        .replace_needed('android.hardware.audio.common-V3-ndk.so', 'android.hardware.audio.common-V4-ndk.so'),


    # Codec2
    (
        'vendor/lib64/libcodec2_hidl_plugin.so',
        'vendor/lib64/libcodec2_mtk_c2store.so',
        'vendor/lib64/libcodec2_vpp_mi_plugin.so',
        'vendor/lib64/libcodec2_vpp_qt_plugin.so',
        'vendor/lib64/libcodec2_vpp_fa_plugin.so',
        'vendor/lib64/libcodec2_vpp_frc_plugin.so',
        'vendor/lib64/libcodec2_vpp_rs_plugin.so',
        'vendor/lib64/libcodec2_vpp_ve_plugin.so',
    ): blob_fixup()
        .replace_needed('libcodec2.so', 'libcodec2-mtk.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-mtk.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-mtk.so'),

    # Codec2
    (
        'vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so',
        'vendor/lib64/libcodec2_vpp_AISR_plugin.so',
    ): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so')
        .replace_needed('libcodec2.so', 'libcodec2-mtk.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-mtk.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-mtk.so'),

    # Codec2 — full HIDL/AIDL/HAL dependents (vdec, venc, c2 service binaries)
    (
        'vendor/lib64/libcodec2_mtk_vdec.so',
        'vendor/lib64/libcodec2_mtk_venc.so',
        'vendor/bin/hw/android.hardware.media.c2-mediatek-64b',
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b',
    ): blob_fixup()
        .replace_needed('libcodec2.so', 'libcodec2-mtk.so')
        .replace_needed('libcodec2_aidl.so', 'libcodec2_aidl-mtk.so')
        .replace_needed('libcodec2_hal_common.so', 'libcodec2_hal_common-mtk.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-mtk.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-mtk.so')
        .replace_needed('libcodec2_hidl@1.2.so', 'libcodec2_hidl@1.2-mtk.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-mtk.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-mtk.so'),

    # Codec2
    (
        'vendor/lib64/libcodec2_aidl-mtk.so',
        'vendor/lib64/libcodec2_hal_common-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.0-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.1-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.2-mtk.so',
        'vendor/lib64/libcodec2_soft_common-mtk.so',
    ): blob_fixup()
        .replace_needed('libcodec2.so', 'libcodec2-mtk.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-mtk.so'),

    # Codec2
    (
        'vendor/lib64/libcodec2_aidl-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.0-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.1-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.2-mtk.so',
        'vendor/lib64/libcodec2_soft_common-mtk.so',
    ): blob_fixup()
        .replace_needed('libcodec2_hal_common.so', 'libcodec2_hal_common-mtk.so'),

    # Codec2
    (
        'vendor/lib64/libcodec2_aidl-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.0-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.1-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.2-mtk.so',
    ): blob_fixup()
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-mtk.so'),

    # Codec2
    (
        'vendor/lib64/libcodec2_hidl@1.0-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.1-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.2-mtk.so',
    ): blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-mtk.so'),

    # Codec2
    (
        'vendor/lib64/libcodec2_hidl@1.1-mtk.so',
        'vendor/lib64/libcodec2_hidl@1.2-mtk.so',
    ): blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-mtk.so'),

    # Codec2
    'vendor/lib64/libcodec2_hidl@1.2-mtk.so': blob_fixup()
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-mtk.so'),

} # fmt: skip
        .replace_needed('libxlog.so', 'libxlog_stub.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/lib64/libdlbdsservice.so': blob_fixup()
        .replace_needed("libstagefright_foundation.so", "libstagefright_foundation-v33.so"),
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),
    "odm/bin/hw/vendor.xiaomi.hw.touchfeature-service": blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so')
        .replace_needed('vendor.xiaomi.hw.touchfeature-V1-ndk.so', 'vendor.xiaomi.hw.touchfeature-V1-ndk-prebuilt.so'),
    (
        'vendor/lib64/hw/mt6899/vendor.mediatek.hardware.pq_aidl-impl.so',
        'vendor/lib64/mt6899/libmmlpqImpl.so',
        'vendor/lib64/libpqxmlparser.so'
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'rodin',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
