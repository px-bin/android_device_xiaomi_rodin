#
# Copyright (C) 2025 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit from rodin device
$(call inherit-product, device/xiaomi/rodin/device.mk)

# AOSP Flags
TARGET_SHIPS_DOLBY := true
TARGET_BOOT_ANIMATION_RES := 1080
TARGET_FACE_UNLOCK_SUPPORTED := true
EXTRA_UDFPS_ANIMATIONS := true
TORCH_STR_SUPPORTED := true
TARGET_ENABLE_BLUR := true
TARGET_INCLUDE_LIVE_WALLPAPERS := true
TARGET_INCLUDE_WEATHER := true
TARGET_SUPPORTS_GOOGLE_FILES := true
TARGET_SUPPORTS_64_BIT_APPS := true
TARGET_SHIPS_VIPERFX := false
TARGET_SHIPS_PIXELPLAY := true
TARGET_SHIPS_BCR := true
TARGET_SHIPS_GCAM := true
TARGET_SHIPS_MIUICAMERA := false
TARGET_SUPPORTS_GOOGLE_TELEPHONY := false
TARGET_OPTIMIZED_DEXOPT := true
WITH_GMS := true
WITH_BCR := true
PERF_ANIM_OVERRIDE := true
TARGET_CUSTOM_UDFPS := true
WITH_GMS_COMMS_SUITE := true

PRODUCT_DEVICE := rodin
PRODUCT_NAME := lineage_rodin
PRODUCT_BRAND := POCO
PRODUCT_MODEL := 2412DPC0AG
PRODUCT_MANUFACTURER := xiaomi
PRODUCT_MARKETNAME=POCO X7 Pro

PRODUCT_SYSTEM_NAME := rodin_global
PRODUCT_SYSTEM_DEVICE := rodin

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="missi-user 16 BP2A.250605.031.A3 OS3.0.10.0.WOJMIXM release-keys" \
    BuildFingerprint=POCO/rodin_global/rodin:15/AP3A.240905.015.A2/OS3.0.10.0.WOJMIXM:user/release-keys \
    DeviceName=$(PRODUCT_SYSTEM_DEVICE) \
    DeviceProduct=$(PRODUCT_SYSTEM_NAME)

