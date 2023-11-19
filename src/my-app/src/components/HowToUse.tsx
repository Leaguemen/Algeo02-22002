import React from "react";
import "./page.css";

function HowToUse() {
  return (
    <div className="cara">
      <h1>How to Use</h1>
      <hr></hr>
      <ol>
        <li>Masuk ke menu Home</li>
        <li>
          Klik choose file dan masukkan folder yang isinya dataset gambat-
          gambar yang ingin diuji
        </li>
        <li>
          Klik toggle bila anda ingin mengganti parameter pencarian, ada dua
          pilihan, dibandingkan terhadap warna atau dibandingkan terhadap
          tekstur
        </li>
        <li>Klik choose image untuk memilih gambar apa yang ingin di cari</li>
        <li>Klik search</li>
        <li>Tunggu beberapa saat</li>
        <li>
          Program akan menampilkan gambar - gambar dari dataset yang telah
          diurut dari kemiripannya
        </li>
      </ol>
    </div>
  );
}

export default HowToUse;
