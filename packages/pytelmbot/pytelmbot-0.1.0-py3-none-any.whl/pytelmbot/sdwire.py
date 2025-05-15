#!python
import os
import time
import shutil
import ftd2xx
import psutil

class SDWire:
    BITMODE_CBUS = 0x20
    MASK_DUT = 0xF0
    MASK_TS = 0xF1
    
    def __init__(self, name=None):
        self.sdw = None
        try:
            self.sdw = ftd2xx.openEx(name.encode())
            
            self.select_dut()    
            time.sleep(3)
            self.select_ts()
        except Exception as e:
            print(f"Unable to connect to {name}: {e}")
            self.__class__.list_devices()            

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Handled exception: {exc_value}")
            
        return False # Propagate exception if any
        
    def __del__(self):
        self.close()
        
    def select_dut(self):
        self.sdw.setBitMode(self.MASK_DUT, self.BITMODE_CBUS)
        self.drive = None
    
    def select_ts(self):
        known_drives = self.get_usb_drives()
        self.sdw.setBitMode(self.MASK_TS, self.BITMODE_CBUS)
        time.sleep(3)
        current_drives = self.get_usb_drives()
       
        for drive in current_drives:
            if drive not in known_drives:
                self.drive = drive
                break
                
        print(f"Drive is: {self.drive}")
        
    
    def get_usb_drives(self):
        drives = [disk.device for disk in psutil.disk_partitions() if 'removable' in disk.opts and disk.fstype]
        if drives:
            print("Detected drives:")
            for drive in drives:
                print(f"{  drive}")
                
        return drives
    
    def write_file(self, file, path=""):
        shutil.copy(file, os.path.join(self.drive, path))
                
    def copy_file(self, file, dst):
        file_path = os.path.join(self.drive, file)
        dst_path  = os.path.join(self.drive, dst)
        if os.path.exists(file_path):
            shutil.copy(file_path, dst_path)
            print("File copied successfully.")
        else:
            print("File not found.")      
              
    def rename_file(self, file, new_name):
        file_path = os.path.join(self.drive, file)
        new_path  = os.path.join(os.path.dirname(file_path), new_name)
        if os.path.exists(file_path):
            os.rename(file_path, new_path)
            print("File renamed successfully.")
        else:
            print("File not found.")

    def delete_file(self, file):
        file_path = os.path.join(self.drive, file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File deleted successfully.")
        else:
            print("File not found.")
            
    def get_file(self, file, dst):
        file_path = os.path.join(self.drive, file)
        dst_path  = os.path.join(dst, os.path.basename(file))
        
        shutil.copy(file_path, dst_path)
                
    def close(self):
        if self.sdw:
            print("Closing SDWire...")
            self.sdw.close()
            self.sdw = None
            
    @staticmethod
    def list_devices():
        devices = ftd2xx.listDevices()
        if devices is None:
            print("No devices")
        else:
            print("Available devices:")
            for device in devices:
                print(f"  {device.decode('utf-8')}")
                
