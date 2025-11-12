// app/static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  const uploadForm = document.getElementById("uploadForm");
  const uploadResult = document.getElementById("uploadResult");
  const predictForm = document.getElementById("predictForm");
  const inputsDiv = document.getElementById("inputs");
  const predictResult = document.getElementById("predictResult");

  // Setup inputs for prediction based on numericCols from server
  if (hasModel && Array.isArray(numericCols) && numericCols.length > 0) {
    // We assume last numeric column is target; we will use others as features.
    // For simplicity, we present all numeric columns except last one as input features.
    const features = numericCols.slice(0, Math.max(0, numericCols.length - 1));
    if (features.length === 0) {
      inputsDiv.innerHTML = "<p>Tidak ada fitur numerik yang tersedia untuk prediksi.</p>";
    } else {
      features.forEach(f => {
        const wrapper = document.createElement("div");
        wrapper.className = "input-row";
        wrapper.innerHTML = `
          <label style="display:block;margin-bottom:6px;">${f}</label>
          <input name="${f}" type="number" step="any" placeholder="Masukkan nilai ${f}" style="padding:8px;margin-bottom:10px;width:100%;box-sizing:border-box;" />
        `;
        inputsDiv.appendChild(wrapper);
      });
    }

    // handle predict submit
    predictForm && predictForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(predictForm);
      const obj = {};
      for (let [k, v] of formData.entries()) {
        if (v === "") {
          predictResult.innerHTML = `<p style="color:#b45309;">Isi semua kolom fitur terlebih dahulu.</p>`;
          return;
        }
        obj[k] = parseFloat(v);
      }
      // POST to /predict
      fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(obj)
      })
      .then(r => r.json())
      .then(data => {
        if (data.error) {
          predictResult.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        } else {
          predictResult.innerHTML = `<p style="color:green;font-weight:bold;">Prediksi Beban Roda: ${data.predicted_wheel_load.toFixed(3)}</p>`;
        }
      })
      .catch(err => {
        predictResult.innerHTML = `<p style="color:red;">Request error: ${err}</p>`;
      });
    });
  }

  // handle upload
  uploadForm && uploadForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
      uploadResult.innerText = "Pilih file CSV terlebih dahulu.";
      return;
    }
    const fd = new FormData();
    fd.append("file", fileInput.files[0]);
    uploadResult.innerText = "Mengunggah...";
    fetch("/upload-dataset", { method: "POST", body: fd })
      .then(r => r.json())
      .then(data => {
        if (data.error) {
          uploadResult.innerHTML = `<span style="color:red;">Error: ${data.error}</span>`;
        } else {
          uploadResult.innerHTML = `<span style="color:green;">${data.message}</span>`;
        }
      })
      .catch(err => {
        uploadResult.innerHTML = `<span style="color:red;">Upload gagal: ${err}</span>`;
      });
  });
});
