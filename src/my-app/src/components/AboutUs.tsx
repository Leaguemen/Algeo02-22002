import React from "react";
import "./page.css";

function AboutUs() {
  return (
    <div className="about">
      <h1>About Us</h1>
      <hr></hr>
      <p className="about-us-text">
        Halo kakak - kakak asisten yang baik dan pengunjung sekalian , moga -
        moga kalian menikmati website kami :D. Perkenalkan kami kelompok "Linier
        bukan Linear" yang beranggotakan:
        <ul className="team-members">
          <li>Ariel Herfrison (13522002)</li>
          <li>Bastian H.S. (13522034)</li>
          <li>Venantius Sean Ardi Nugroho (13522078)</li>
          kami adalah sekelompok orang yang sebenarnya jarang berinteraksi
          sebelum tugas ini tapi karena niat kita dalam menyelamatkan nilai
          Algeo, kita bersatu untuk melaksanakan tubes ini. Well anyway, selamat
          menikmati websitenya ya!!!
        </ul>
      </p>
    </div>
  );
}

export default AboutUs;
