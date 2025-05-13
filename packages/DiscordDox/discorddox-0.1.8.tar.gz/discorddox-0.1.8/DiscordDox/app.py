import subprocess
import os

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(current_dir, "DiscordDox.exe")

    if os.path.exists(exe_path):
        subprocess.Popen(exe_path, shell=True)

if __name__ == "__main__":
    main()