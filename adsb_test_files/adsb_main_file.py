import subprocess
import webbrowser
import time
def run(runfile):
    try:
        subprocess.run(["python",runfile], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata olustu (subprocess): {e}")
def run_background(runfile):
    try:
        subprocess.Popen(["python", runfile],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Arkaplanda çalıştırma hatası: {e}")
x = 0
while True:
    run("adsb_test_files/adsb-test4.py")
    
    # Open adsb_planes_map.html in the default web browser
    if x == 0:
        run_background("adsb_test_files/raw_data_analiz.py")
        print("adsb_planes_map.html dosyası oluşturuldu.")
        time.sleep(5)
        webbrowser.open("adsb_planes_map.html")
        x = 1
    
    time.sleep(10)
    # Close the browser tab after 10 seconds
    try:
        webbrowser.get().close()
    except:
        print("Browser tab could not be closed.")
