// Animate buttons on hover
document.querySelectorAll(".btn-animated").forEach(btn => {
    btn.addEventListener("mouseover", () => {
        btn.style.transform = "scale(1.08)";
        btn.style.boxShadow = "0 12px 25px rgba(0,0,0,0.3)";
    });

    btn.addEventListener("mouseout", () => {
        btn.style.transform = "scale(1)";
        btn.style.boxShadow = "0 6px 15px rgba(0,0,0,0.2)";
    });
});

// Show live image preview on upload page
const fileInput = document.getElementById("image-upload");
const preview = document.getElementById("preview");

if (fileInput && preview) {
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = e => {
                preview.src = e.target.result;
                preview.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });
}
