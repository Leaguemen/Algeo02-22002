import React from "react";

function Concepts() {
  return (
    <div className="konsep">
      <h1>Concepts</h1>
      <hr></hr>
      <p>Content-Based Image Retrieval (CBIR) adalah sebuah proses yang digunakan untuk mencari dan mengambil gambar berdasarkan kontennya. Proses ini dimulai dengan ekstraksi fitur-fitur penting dari gambar, seperti warna, tekstur, dan bentuk. Setelah fitur-fitur tersebut diekstraksi, mereka diwakili dalam bentuk vektor atau deskripsi numerik yang dapat dibandingkan dengan gambar lain.</p>
      <p>Kemudian, CBIR menggunakan algoritma pencocokan untuk membandingkan vektor-fitur dari gambar yang dicari dengan vektor-fitur gambar dalam dataset. Hasil dari pencocokan ini digunakan untuk mengurutkan gambar-gambar dalam dataset dan menampilkan gambar yang paling mirip dengan gambar yang dicari.</p>
      <p>Proses CBIR membantu pengguna dalam mengakses dan mengeksplorasi koleksi gambar dengan cara yang lebih efisien, karena tidak memerlukan pencarian berdasarkan teks atau kata kunci, melainkan berdasarkan kesamaan nilai citra visual antara gambar-gambar tersebut.</p>
      <p>CBIR yang diimplementasikan pada aplikasi ini adalah CBIR dengan parameter warna dan CBIR dengan parameter tekstur.</p>
      <p>CBIR dengan parameter warna dilakukan dengan cara mengekstrak nilai-nilai RGB dari setiap pixel pada gambar. Kemudian, gambar tersebut dibagi menjadi blok 4x4. Dari masing-masing blok, dicari suatu nilai yang merepresentasikan blok tersebut. Nilai representatif dihitung dengan mencari rata-rata nilai HSV dari blok tersebut. Setelah itu, perbandingan gambar dilakukan dengan menghitung cosine similarity dari gamber tersebut.</p>
      <p>CBIR dengan parameter tekstur dimulai dengan mengekstrak nilai RGB dari setiap pixel pada gambar, lalu mengubahnya ke nilai greyscale. Setelah itu, dibuat co-occurence matrix berdasarkan nilai greyscale tersebut. Pada website kami, pada pembuatan co-occurence matrix, nilai offset yang digunakan 1 dan angle yang digunakan adalah 0. Dari co-occurence matrix, dicari nilai contrast, homogeneity, dan entropy dari gambar. Terakhir, perbandingan gambar dilakukan dengan perhitungan cosine similarity.</p>
    </div>
  );
}

export default Concepts;
