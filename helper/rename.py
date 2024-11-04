import os
import shutil
from pathlib import Path

# RENAME FILE DALAM DATASET

def rename_pcr_files(source_folder, target_folder):
    # Buat folder target jika belum ada
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Folder '{target_folder}' telah dibuat.")
    
    # Dictionary untuk menyimpan counter terakhir untuk setiap kategori
    last_numbers = {
        'cocci': -1,
        'healthy': -1,
        'ncd': -1,
        'salmo': -1
    }
    
    # Salin semua file non-pcr ke folder baru dan temukan nomor terakhir
    for filename in os.listdir(source_folder):
        if not filename.startswith('pcr'):
            # Salin file non-pcr
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)
            shutil.copy2(source_path, target_path)
            print(f"Copied: {filename}")
            
            # Update nomor terakhir
            for category in last_numbers.keys():
                if filename.startswith(category + '.'):
                    try:
                        number = int(filename.split('.')[1].split('.')[0])
                        last_numbers[category] = max(last_numbers[category], number)
                    except ValueError:
                        continue

    # Proses file PCR
    for filename in sorted(os.listdir(source_folder)):
        if filename.startswith('pcr'):
            # Ekstrak kategori dari nama file pcr
            for category in last_numbers.keys():
                if filename.startswith('pcr' + category):
                    # Increment counter
                    last_numbers[category] += 1
                    
                    # Buat nama file baru
                    source_path = os.path.join(source_folder, filename)
                    new_filename = f"{category}.{last_numbers[category]}.jpg"
                    target_path = os.path.join(target_folder, new_filename)
                    
                    # Salin file dengan nama baru
                    try:
                        shutil.copy2(source_path, target_path)
                        print(f"Renamed and copied: {filename} -> {new_filename}")
                    except Exception as e:
                        print(f"Error processing {filename}: {str(e)}")
                    break

def main():
    source_folder = "all"      # Folder sumber
    target_folder = "all_new"  # Folder target
    
    if not os.path.exists(source_folder):
        print(f"Folder sumber '{source_folder}' tidak ditemukan!")
        return
    
    print("Memulai proses rename dan copy file...")
    rename_pcr_files(source_folder, target_folder)
    print("Proses selesai!")
    
    # Hitung jumlah file di folder target
    file_count = len([name for name in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, name))])
    print(f"Total file di folder {target_folder}: {file_count}")

if __name__ == "__main__":
    main()