let token=null;
const API="http://localhost:8000";

async function signup(){
  const f=new FormData(); f.append("username",username.value); f.append("password",password.value);
  let r=await fetch(API+"/signup",{method:"POST",body:f}); let d=await r.json();
  token=d.token; showMain();
}

async function login(){
  const f=new FormData(); f.append("username",username.value); f.append("password",password.value);
  let r=await fetch(API+"/login",{method:"POST",body:f}); let d=await r.json();
  token=d.token; showMain();
}

function showMain(){
  document.getElementById("auth").style.display="none";
  document.getElementById("main").style.display="block";
  initMap();
}

async function upload(){
  const f=new FormData();
  f.append("latitude",lat.value); f.append("longitude",lon.value);
  f.append("file",photo.files[0]);
  let r=await fetch(API+"/upload/",{method:"POST",headers:{Authorization:"Bearer "+token},body:f});
  alert(await r.text());
}

let map;
function initMap(){
  map=L.map("map").setView([12.9716,77.5946],12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
}

async function loadRoute(){
  let r=await fetch(API+"/route/");
  let d=await r.json();
  const pts=d.route;
  let all=await (await fetch(API+"/points/")).json();
  all.features.forEach(f=>{
    const [lon,lat]=f.geometry.coordinates;
    L.marker([lat,lon]).addTo(map);
  });
}
