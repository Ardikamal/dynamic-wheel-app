# Dynamic Wheel Load - Flask App

Instalasi & jalankan:

1. Pastikan Python 3.x terpasang.
2. Buat virtualenv (opsional):
   - `python -m venv venv`
   - Activate: `venv\Scripts\activate` (Windows) atau `source venv/bin/activate` (Linux/Mac)
3. Install dependency:
   - `pip install -r requirements.txt`
4. Letakkan dataset `dynamic_wheel_load.csv` di folder `data/`.
5. Latih model:
   - `python train_and_save_model.py`
   - Jika sukses, model akan tersimpan di `app/models/model_rf.pkl`
6. Jalankan server:
   - `python run.py`
   - Buka `http://127.0.0.1:5000` di browser.
7. Gunakan halaman untuk upload dataset (opsional) dan prediksi.

Catatan:
- Jika struktur dataset berbeda, sesuaikan pemilihan fitur di `train_and_save_model.py`.
- Matikan `debug=True` di `run.py` saat deploy ke production.
