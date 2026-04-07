<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Jpresso Coffee | Beans, Green Beans & Equipment</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>☕</text></svg>">
<style>html{scroll-behavior:smooth}body{margin:0;padding:0;-webkit-font-smoothing:antialiased}</style>
</head><body><div id="root"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.9/babel.min.js"></script>
<script type="text/babel">
const { useState, useEffect, useRef, useMemo } = React;


const C = {
  purple:"#4E1F73",purpleDeep:"#2D1145",purpleLight:"#6B3A94",purplePale:"#F3EDF8",
  gold:"#DAB07B",goldLight:"#E8C99B",goldDark:"#C49A5E",goldPale:"#FBF5EC",
  bg:"#FDFCFA",card:"#FFFFFF",soft:"#F8F5F1",
  text:"#2D1145",body:"#4A3560",muted:"#8E7BA3",
  border:"#E8DFF0",borderLt:"#F0EBF5",green:"#16A34A",red:"#DC2626",
};

/* ═══ ROASTED BEANS ═══ */
const ROASTED=[
  {id:"r1",name:"Ethiopia Yirgacheffe Chelchele",process:"Washed",origin:"Ethiopia",cat:"Classic",price:69,varietal:"Heirloom",altitude:"1,800–2,100m",farm:"Chelchele Washing Station",notes:"Lavender, purple grapes, blueberry, creamy",brew:"V60 at 92°C, 1:16 ratio.",roast:"Filter"},
  {id:"r2",name:"Ethiopia Guji Siko",process:"Natural",origin:"Ethiopia",cat:"Classic",price:68,varietal:"Heirloom",altitude:"1,950–2,300m",farm:"Siko, Guji Zone",notes:"Mango, stone fruits, grapes, lychee",brew:"AeroPress at 94°C, 1:15.",roast:"Filter"},
  {id:"r3",name:"Ethiopia Beyou Gersay",process:"Natural",origin:"Ethiopia",cat:"Classic",price:68,varietal:"Heirloom",altitude:"1,650m",farm:"Beyou Gersay, Yirgacheffe",notes:"Jasmine, lavender, peach, fig, pawpaw, blackcurrant",brew:"AeroPress inverted at 90°C.",roast:"Filter"},
  {id:"r4",name:"Honduras La Falda",process:"Washed",origin:"Honduras",cat:"Classic",price:75,varietal:"Bourbon",altitude:"1,800m",farm:"La Falda by Juan Montoya",notes:"Purple grapes, stone fruits, lychee, mango",brew:"V60 at 92°C or espresso at 93°C.",roast:"Filter / Espresso"},
  {id:"r5",name:"Honduras Flor De Cafe",process:"Washed",origin:"Honduras",cat:"Classic",price:72,varietal:"Typica",altitude:"1,750m",farm:"Flor De Café by Maria Eva Lopez",notes:"Orange, apricot jam, lime, black tea, jasmine",brew:"Pour-over at 92°C.",roast:"Filter"},
  {id:"r6",name:"Honduras El Roble",process:"Honey",origin:"Honduras",cat:"Classic",price:73,varietal:"Pacas",altitude:"1,600m",farm:"El Roble by Rosa Dimas Funez",notes:"Blood orange, rose, brown sugar, grapefruit",brew:"Kalita Wave at 93°C, 1:15.",roast:"Filter"},
  {id:"r7",name:"Honduras El Carrizal",process:"Natural",origin:"Honduras",cat:"Classic",price:65,varietal:"Pacas",altitude:"1,400m",farm:"El Carrizal",notes:"Strawberry, milk chocolate, cherry, banana",brew:"Espresso — 18g:38g at 93°C.",roast:"Espresso / Filter"},
  {id:"r8",name:"Nicaragua El Lino",process:"Washed",origin:"Nicaragua",cat:"Classic",price:68,varietal:"Caturra",altitude:"1,250–1,450m",farm:"El Lino by Luis Emilio Valladárez",notes:"Mandarin, peach, floral, jasmine tea, sweet",brew:"V60 at 93°C or espresso.",roast:"Filter / Espresso"},
  {id:"r9",name:"Nicaragua Los Jilgueros",process:"Washed",origin:"Nicaragua",cat:"Classic",price:80,varietal:"Java",altitude:"1,350m",farm:"Los Jilgueros by Manuel Peralta",notes:"Jasmine, rose water, very clean and transparent",brew:"V60 at 93°C, 1:16.",roast:"Filter"},
  {id:"r10",name:"Nicaragua El Torito",process:"Anaerobic Natural",origin:"Nicaragua",cat:"Experimental",price:84,varietal:"Yellow Catuai",altitude:"1,350m",farm:"El Torito by Isacio Albir",notes:"Strawberry yoghurt, vanilla, cherry",brew:"AeroPress at 88°C, quick 1:30.",roast:"Filter"},
  {id:"r11",name:"Nicaragua La Estrella",process:"Anaerobic Natural",origin:"Nicaragua",cat:"Experimental",price:76,varietal:"Catuai",altitude:"1,500m",farm:"La Estrella",notes:"Cranberry, blackcurrant, lavender, berries, peach",brew:"French press at 90°C.",roast:"Filter"},
  {id:"r12",name:"El Salvador Finca Himalaya",process:"Supernatural",origin:"El Salvador",cat:"Experimental",price:88,varietal:"Bourbon/Pacas",altitude:"1,500m",farm:"Finca Himalaya by Mauricio Salaverria",notes:"Raspberry, cherry, marmalade, strawberry, winey",brew:"AeroPress at 89°C or V60 at 91°C.",roast:"Filter"},
  {id:"r13",name:"Honduras Finca Gosen",process:"Anaerobic Natural",origin:"Honduras",cat:"Experimental",price:70,varietal:"H-27",altitude:"1,500m",farm:"Finca Gosen by Mariano Nolasco",notes:"Tropical fruits, cherry, ripe banana",brew:"AeroPress or clever dripper at 91°C.",roast:"Filter"},
  {id:"r14",name:"Brazil Fazenda Lagoinha",process:"Anaerobic Natural",origin:"Brazil",cat:"Classic",price:72,varietal:"Yellow Catuai",altitude:"1,100–1,300m",farm:"Fazenda Lagoinha, Minas Gerais",notes:"Peanut butter, dark chocolate, cherry cola",brew:"Espresso — 18g:36g at 94°C.",roast:"Espresso"},
  {id:"r15",name:"Colombia Yacuanquer",process:"Washed",origin:"Colombia",cat:"Classic",price:70,varietal:"Caturra/Castillo",altitude:"1,900–2,000m",farm:"Various Small Producers",notes:"Blueberry, purple grapes, blackcurrant, peach",brew:"V60 at 93°C, 1:16.",roast:"Filter"},
  {id:"r16",name:"Kenya Maguta Waridi",process:"Supernatural",origin:"Kenya",cat:"Experimental",price:89,varietal:"SL28/SL34",altitude:"1,650–1,800m",farm:"Maguta Estate by David Ngibuini",notes:"Cherry, caramel, milk chocolate, plum, cranberry",brew:"V60 at 93°C, 1:15.",roast:"Filter"},
  {id:"r17",name:"Malaysia My Liberica N26",process:"Anaerobic Natural",origin:"Malaysia",cat:"Experimental",price:103,varietal:"Liberica",altitude:"0–20m",farm:"My Liberica, Johor",notes:"Berries, peach, red date, caramelized sugar",brew:"French press at 95°C, 4 min.",roast:"Filter"},
  {id:"r18",name:"Dawn",process:"Blend",origin:"House Blend",cat:"Blend",price:62,varietal:"Seasonal Espresso",altitude:"Various",farm:"Jpresso House Blend",notes:"Milk chocolate, caramel, toasted nuts",brew:"Espresso: 18g:36g at 93°C. Great in lattes.",roast:"Espresso"},
  {id:"r19",name:"Rubix",process:"Blend",origin:"House Blend",cat:"Blend",price:50,varietal:"House Blend",altitude:"Various",farm:"Jpresso House Blend",notes:"Dried fruit, cocoa, brown sugar, smooth",brew:"Works as espresso, drip, French press.",roast:"Omni"},
];

/* ═══ GREEN BEANS (abbreviated for space — same data) ═══ */
const GREEN=[
  {id:"g1",name:"Brazil Classico",process:"Natural",origin:"Brazil",cat:"Classic",varietal:"Yellow Bourbon",altitude:"900–1,300m",farm:"Various Small Producers",notes:"Raisin, caramel, nougat, milk chocolate",score:"83pts",tiers:[{qty:"1kg",p:83},{qty:"5kg",p:73},{qty:"10kg",p:66},{qty:"30kg",p:58}]},
  {id:"g2",name:"Ethiopia Guji Shakiso Tero G1",process:"Washed",origin:"Ethiopia",cat:"Classic",varietal:"Heirloom",altitude:"1,950–2,300m",farm:"Various Small Producers",notes:"White grapes, creamy, white peach, sweet berries",score:"86.5pts",tiers:[{qty:"1kg",p:106},{qty:"5kg",p:91},{qty:"10kg",p:83},{qty:"60kg",p:78}]},
  {id:"g3",name:"Ethiopia Chelchele G1 Lot #3",process:"Washed",origin:"Ethiopia",cat:"Classic",varietal:"Heirloom",altitude:"1,200–3,200m",farm:"Various Small Producers",notes:"Lavender, purple grapes, blueberry, creamy",score:"86pts",tiers:[{qty:"1kg",p:113},{qty:"5kg",p:98},{qty:"10kg",p:90},{qty:"60kg",p:85}]},
  {id:"g4",name:"Ethiopia Guji Siko G1",process:"Natural",origin:"Ethiopia",cat:"Classic",varietal:"Heirloom",altitude:"1,950–2,300m",farm:"Various Small Producers",notes:"Mango, stone fruits, grapes, lychee",score:"87pts",tiers:[{qty:"1kg",p:110},{qty:"5kg",p:95},{qty:"10kg",p:87},{qty:"60kg",p:82}]},
  {id:"g5",name:"Nicaragua El Avión",process:"Washed",origin:"Nicaragua",cat:"Classic",varietal:"Catuai/Catimor",altitude:"1,500–1,750m",farm:"Mario Gonzalez",notes:"Mandarin, caramel, florals, strawberry, fig",score:"—",tiers:[{qty:"1kg",p:116},{qty:"5kg",p:101},{qty:"10kg",p:93},{qty:"30kg",p:87}]},
  {id:"g6",name:"Nicaragua Santa Trinidad",process:"Washed",origin:"Nicaragua",cat:"Classic",varietal:"Maracaturra/Pacamara",altitude:"1,400m",farm:"Favio Rodriguez",notes:"Purple grapes, peach, jasmine, creamy, great body",score:"—",tiers:[{qty:"1kg",p:133},{qty:"5kg",p:118},{qty:"10kg",p:110},{qty:"30kg",p:105}]},
  {id:"g7",name:"Honduras El Gravileo",process:"Washed",origin:"Honduras",cat:"Classic",varietal:"Typica",altitude:"1,900m",farm:"Lester Francisco Marquez",notes:"Pink bubblegum, orange, lime, lemongrass, white pear",score:"89pts",tiers:[{qty:"1kg",p:178},{qty:"5kg",p:163},{qty:"10kg",p:155},{qty:"30kg",p:150}]},
  {id:"g8",name:"Honduras El Laurel",process:"Washed",origin:"Honduras",cat:"Classic",varietal:"Parainema",altitude:"1,400m",farm:"Oscar Ramirez Chavez",notes:"Jasmine, peach, lemongrass, white grapes, lavender",score:"89pts",tiers:[{qty:"1kg",p:188},{qty:"5kg",p:173},{qty:"10kg",p:165},{qty:"30kg",p:160}]},
  {id:"g9",name:"Honduras El Roble",process:"Honey",origin:"Honduras",cat:"Classic",varietal:"Pacas",altitude:"1,600m",farm:"Rosa Dimas Funez",notes:"Blood orange, rose, brown sugar, grapefruit",score:"88pts",tiers:[{qty:"1kg",p:120},{qty:"5kg",p:105},{qty:"10kg",p:97},{qty:"30kg",p:92}]},
  {id:"g10",name:"Kenya Maguta Diamond HP4",process:"CM Washed",origin:"Kenya",cat:"Signature",varietal:"SL28/SL34",altitude:"1,650–1,800m",farm:"Maguta Estate",notes:"Pink champagne, jasmine, citrus",score:"—",tiers:[{qty:"1kg",p:320},{qty:"5kg",p:315},{qty:"10kg",p:310},{qty:"15kg",p:300}]},
  {id:"g11",name:"Kenya Thageini CM Indigo",process:"CM Natural",origin:"Kenya",cat:"Signature",varietal:"SL28/SL34",altitude:"1,650–1,800m",farm:"Thageini, Nyeri County",notes:"Dark berries, black forest, mango, dark chocolate",score:"—",tiers:[{qty:"1kg",p:240},{qty:"5kg",p:235},{qty:"10kg",p:230},{qty:"15kg",p:220}]},
  {id:"g12",name:"Ethiopia Koke Indigo 1124",process:"CM Natural",origin:"Ethiopia",cat:"Signature",varietal:"Heirloom",altitude:"1,900–2,000m",farm:"Koke Washing Station",notes:"Tropical fruits, purple grapes, blueberry, passionfruit",score:"87pts",tiers:[{qty:"1kg",p:220},{qty:"4kg",p:210},{qty:"16kg",p:200}]},
  {id:"g13",name:"Honduras La Salvaje — COE #1",process:"Washed",origin:"Honduras",cat:"Limited Release",varietal:"Geisha",altitude:"1,750m",farm:"Fabio Caballero Jr.",notes:"Peach, jasmine, stone fruits, mango, vanilla, creamy",score:"92pts",tiers:[{qty:"1kg",p:850},{qty:"5kg",p:800},{qty:"10kg",p:750}]},
  {id:"g14",name:"Honduras Kukurucho — COE #5",process:"Washed",origin:"Honduras",cat:"Limited Release",varietal:"Geisha",altitude:"1,650m",farm:"Rony Gamez",notes:"Lavender, perfumey, purple berries, pristine",score:"91pts",tiers:[{qty:"1kg",p:805},{qty:"5kg",p:700},{qty:"10kg",p:650}]},
  {id:"g15",name:"Brazil Ama Geisha Lilac",process:"CM Natural",origin:"Brazil",cat:"Limited Release",varietal:"Geisha",altitude:"1,300m",farm:"Sasa Sestic & Luiz Paulo",notes:"Purple grape, mulberry, blueberry",score:"—",tiers:[{qty:"1kg",p:263},{qty:"5kg",p:248},{qty:"10kg",p:240}]},
  {id:"g16",name:"Colombia La Negrita",process:"N₂ Flushed Natural",origin:"Colombia",cat:"Limited Release",varietal:"Pluma Hidalgo",altitude:"2,100m",farm:"Mauricio Shattah, Tolima",notes:"Raspberry jam, ribena, blackcurrant, purple grapes",score:"—",tiers:[{qty:"1kg",p:750}]},
  {id:"g17",name:"Panama Iris Estate Terroir",process:"Washed",origin:"Panama",cat:"Iris Estate",varietal:"Geisha",altitude:"1,850–2,300m",farm:"Savage, Sestic, Siew",notes:"Jasmine, white grape, peach, citrus",score:"—",tiers:[{qty:"1kg",p:805},{qty:"5kg",p:750},{qty:"10kg",p:700},{qty:"20kg",p:650}]},
  {id:"g18",name:"Panama Iris Estate Nirvana",process:"N₂-Flushed Natural",origin:"Panama",cat:"Iris Estate",varietal:"Geisha",altitude:"1,850–2,300m",farm:"Savage, Sestic, Siew",notes:"White florals, strawberry, apricot, orange, bergamot",score:"—",tiers:[{qty:"1kg",p:1155},{qty:"5kg",p:1100},{qty:"10kg",p:1050},{qty:"20kg",p:1000}]},
  {id:"g19",name:"Panama Iris Estate Enigma",process:"Extended Natural",origin:"Panama",cat:"Iris Estate",varietal:"Geisha",altitude:"1,850–2,300m",farm:"Savage, Sestic, Siew",notes:"Black cherry, purple grape, winey, blackcurrant, mango",score:"—",tiers:[{qty:"1kg",p:1005},{qty:"5kg",p:950},{qty:"10kg",p:900}]},
  {id:"g20",name:"Yemen Atarah Village",process:"Anaerobic Natural",origin:"Yemen",cat:"Classic",varietal:"Typica/Bourbon",altitude:"1,800–2,350m",farm:"Mohammed al Mashraqi",notes:"Orange, cloves, cinnamon, orange peels",score:"—",tiers:[{qty:"1kg",p:300},{qty:"5kg",p:350}]},
];

/* ═══ EQUIPMENT — Timemore ═══ */
const EQUIP=[
  {id:"e1",name:"Sculptor 078 Electric Grinder",cat:"Electric Grinder",price:2899,colors:["Black","White"],specs:"Turbo Burrs 078 · SUS 440 · 78mm\nMax 400W · 800–1400 rpm\nOptimized for pour-over",brand:"Timemore"},
  {id:"e2",name:"Sculptor 078S Electric Grinder",cat:"Electric Grinder",price:2899,colors:["Black","White"],specs:"Flat Burrs 078S · SUS420 · 78mm\nMax 400W · 800–1400 rpm\nMulti-purpose",brand:"Timemore"},
  {id:"e3",name:"Sculptor 064S Electric Grinder",cat:"Electric Grinder",price:1799,colors:["Black","White"],specs:"Flat Burrs 064S · SUS420 · 64mm\nMax 150W · 800–1200 rpm\nMulti-purpose",brand:"Timemore"},
  {id:"e4",name:"BRICKS 01S Electric Grinder",cat:"Electric Grinder",price:815,colors:["Black","White"],specs:"S2C-040-EI Burrs · SUS420 · 40mm · 5-blade\n450 rpm · Max 150W\nMulti-purpose",brand:"Timemore"},
  {id:"e5",name:"Whirly 01S Portable Grinder",cat:"Electric Grinder",price:415,colors:["Black"],specs:"S2C-042-EI Burrs · SUS420 · 42mm · 8-blade\n1000mAh battery · 45g capacity\nEspresso & pour-over",brand:"Timemore"},
  {id:"e6",name:"C5 Hand Grinder",cat:"Hand Grinder",price:230,colors:["Black","White"],specs:"S2C-042-III Burrs · SUS420 · 42mm · 7-blade\nMax 25g capacity\nPour-over, compatible with espresso",brand:"Timemore"},
  {id:"e7",name:"C5 Pro Hand Grinder",cat:"Hand Grinder",price:260,colors:["Black","White"],specs:"S2C-042-III Burrs · SUS420 · 42mm · 7-blade\nMax 25g capacity · External adjustment\nPour-over, compatible with espresso",brand:"Timemore"},
  {id:"e8",name:"C5 ESP Hand Grinder",cat:"Hand Grinder",price:250,colors:["Black"],specs:"S2C-042-III Burrs · SUS420 · 42mm · 7-blade\nMax 25g capacity\nMulti-purpose — espresso optimized",brand:"Timemore"},
  {id:"e9",name:"C5 ESP Pro Hand Grinder",cat:"Hand Grinder",price:270,colors:["Black"],specs:"S2C-042-III Burrs · SUS420 · 42mm · 7-blade\nMax 25g capacity · External adjustment\nMulti-purpose — espresso optimized",brand:"Timemore"},
  {id:"e10",name:"FISH SMART Pour Over Kettle",cat:"Kettle",price:299,colors:["Black"],specs:"600ml capacity\n1000W power\nTemp range: 40°C – 100°C\nPrecision gooseneck spout",brand:"Timemore",priceWhite:325},
  {id:"e11",name:"Mini Espresso Scale",cat:"Scale",price:145,colors:["Black","White"],specs:"Max 2kg\n760mAh battery\nModes: Espresso, auto-brewing & regular\nCompact for portafilter",brand:"Timemore",priceWhite:155},
  {id:"e12",name:"Basic 2 Scale",cat:"Scale",price:119,colors:["Black","White"],specs:"Max 2kg\n1600mAh battery\nModes: Auto-brewing & regular\nUSB-C charging",brand:"Timemore",priceWhite:129},
  {id:"e13",name:"Crystal Eye B75 Dripper",cat:"Dripper",price:50,colors:["Amber Black","Transparent"],specs:"Material: PCTG\n1–2 cups capacity\nB75 flat-bottom design\nEven extraction flow",brand:"Timemore"},
  {id:"e14",name:"Coffee Server 360ml",cat:"Server",price:44.90,colors:["Transparent"],specs:"Borosilicate glass\n360ml capacity\nIncludes lid + server\nHeat resistant",brand:"Timemore"},
  {id:"e15",name:"Coffee Server 600ml",cat:"Server",price:50.90,colors:["Transparent"],specs:"Borosilicate glass\n600ml capacity\nIncludes lid + server\nHeat resistant",brand:"Timemore"},
  {id:"e16",name:"Electric Thermometer",cat:"Accessory",price:44.90,colors:["Black","White"],specs:"Range: -20°C to 120°C\n°C / °F switchable\nCR2032 battery\nInstant reading",brand:"Timemore"},
  {id:"e17",name:"Thermometer Stick",cat:"Accessory",price:22.90,colors:["Black","White"],specs:"Stainless steel\n13.4 × 3.5cm\nAnalog display\nClip-on design",brand:"Timemore"},
  {id:"e18",name:"C5 Advanced All-in-One Gift Box",cat:"Gift Set",price:785,colors:["Black"],specs:"Includes: C5 Grinder + Glass Dripper 01\n+ Server 360ml + E-Kettle 600ml\n+ Basic 2 Scale + 50 Paper Filters\n+ Cleaning Brush",brand:"Timemore"},
  {id:"e19",name:"C3S Advanced All-in-One Gift Box",cat:"Gift Set",price:755,colors:["White"],specs:"Includes: C3S Grinder + Glass Dripper 01\n+ Server 360ml + E-Kettle 600ml\n+ Basic 2 Scale + 50 Paper Filters\n+ Cleaning Brush",brand:"Timemore"},
];

const EQUIP_CATS=["All","Electric Grinder","Hand Grinder","Kettle","Scale","Dripper","Server","Accessory","Gift Set"];

const fl=o=>({Ethiopia:"🇪🇹",Honduras:"🇭🇳",Nicaragua:"🇳🇮",Panama:"🇵🇦",Peru:"🇵🇪",Brazil:"🇧🇷",Colombia:"🇨🇴","El Salvador":"🇸🇻",Kenya:"🇰🇪",Malaysia:"🇲🇾",Yemen:"🇾🇪","House Blend":"✦"}[o]||"☕");
const catC=c=>({Classic:C.purpleLight,Experimental:"#9333EA","Limited Release":"#B8860B",Blend:C.goldDark,Signature:"#2D8B6F","Iris Estate":"#1B4D3E","Electric Grinder":"#6B3A94","Hand Grinder":"#8B5A2B",Kettle:"#C49A5E",Scale:"#2D8B6F",Dripper:"#9333EA",Server:"#6B3A94",Accessory:"#8E7BA3","Gift Set":"#B8860B"}[c]||C.muted);
const eqIcon=c=>({"Electric Grinder":"⚡","Hand Grinder":"🔧",Kettle:"🫖",Scale:"⚖️",Dripper:"☕",Server:"🫗",Accessory:"🌡️","Gift Set":"🎁"}[c]||"📦");

function useInView(t=0.08){const r=useRef(null);const[v,setV]=useState(false);useEffect(()=>{const el=r.current;if(!el)return;const o=new IntersectionObserver(([e])=>{if(e.isIntersecting){setV(true);o.disconnect()}},{threshold:t});o.observe(el);return()=>o.disconnect()},[t]);return[r,v]}
function FadeIn({children,delay=0,style={}}){const[r,v]=useInView();return<div ref={r} style={{...style,opacity:v?1:0,transform:v?"translateY(0)":"translateY(16px)",transition:`opacity .4s ease ${delay}s, transform .4s ease ${delay}s`}}>{children}</div>}

/* ═══ DETAIL MODALS ═══ */
function BeanModal({bean,onClose,onAdd,type}){
  const[selTier,setSelTier]=useState(0);
  if(!bean)return null;
  const isG=type==="green",isE=type==="equip";
  return(
    <div onClick={onClose} style={{position:"fixed",inset:0,background:"rgba(45,17,69,0.5)",backdropFilter:"blur(5px)",zIndex:1000,display:"flex",alignItems:"center",justifyContent:"center",padding:14,overflow:"auto"}}>
      <div onClick={e=>e.stopPropagation()} style={{background:C.card,borderRadius:16,maxWidth:520,width:"100%",maxHeight:"90vh",overflow:"auto",boxShadow:"0 20px 56px rgba(45,17,69,0.2)",position:"relative"}}>
        <button onClick={onClose} style={{position:"absolute",top:12,right:12,width:32,height:32,borderRadius:"50%",border:`1px solid ${C.border}`,background:C.card,cursor:"pointer",fontSize:16,color:C.muted,zIndex:2,display:"flex",alignItems:"center",justifyContent:"center"}}>×</button>
        <div style={{background:`linear-gradient(135deg,${C.purplePale},${C.goldPale})`,padding:"24px 22px 18px",borderRadius:"16px 16px 0 0"}}>
          <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
            {isE?<span style={{fontSize:20}}>{eqIcon(bean.cat)}</span>:<span style={{fontSize:18}}>{fl(bean.origin)}</span>}
            <span className="s" style={{fontSize:9,color:C.muted,letterSpacing:1,textTransform:"uppercase"}}>{isE?bean.brand:bean.origin}</span>
            {bean.score&&<span className="s" style={{fontSize:8,padding:"2px 6px",borderRadius:100,background:`${C.green}12`,color:C.green,fontWeight:600,marginLeft:"auto"}}>{bean.score}</span>}
            <span className="s" style={{fontSize:8,padding:"2px 6px",borderRadius:100,background:`${catC(bean.cat)}10`,color:catC(bean.cat),fontWeight:600,marginLeft:bean.score?"0":"auto"}}>{bean.cat}</span>
          </div>
          <h2 style={{fontSize:22,fontWeight:500,fontStyle:"italic",color:C.purpleDeep,lineHeight:1.2,marginBottom:6,fontFamily:"'Cormorant Garamond',Georgia,serif"}}>{bean.name}</h2>
          {isG&&bean.tiers.length>1&&(
            <div style={{display:"flex",gap:3,marginTop:8,flexWrap:"wrap"}}>
              {bean.tiers.map((t,i)=><button key={i} onClick={()=>setSelTier(i)} className="s" style={{padding:"5px 10px",borderRadius:5,border:selTier===i?`1px solid ${C.purple}44`:`1px solid ${C.border}`,background:selTier===i?C.purplePale:C.card,cursor:"pointer",fontSize:10,fontWeight:selTier===i?600:400,color:selTier===i?C.purple:C.body}}>{t.qty} — <strong>RM{t.p}</strong>/kg</button>)}
            </div>
          )}
          {isE&&bean.colors&&<div className="s" style={{fontSize:10,color:C.body,marginTop:6}}>Colors: {bean.colors.join(", ")}</div>}
          {!isG&&<div style={{display:"flex",alignItems:"baseline",gap:4,marginTop:8}}><span style={{fontSize:26,fontWeight:700,color:C.purple,fontFamily:"'Cormorant Garamond',Georgia,serif"}}>RM{bean.price}</span>{!isE&&<span className="s" style={{fontSize:11,color:C.muted}}>/ 200g</span>}</div>}
        </div>
        <div style={{padding:"18px 22px 22px"}}>
          {isE?(
            <>
            <div style={{marginBottom:16}}>
              <h4 className="s" style={{fontSize:10,color:C.purple,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6,fontWeight:600}}>📋 Specifications</h4>
              <div className="s" style={{fontSize:12,color:C.body,lineHeight:1.7,padding:"10px 14px",borderRadius:8,background:C.soft,borderLeft:`3px solid ${C.purple}`,whiteSpace:"pre-line"}}>{bean.specs}</div>
            </div>
            </>
          ):(
            <>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8,marginBottom:14}}>
              {[["Process",bean.process],["Varietal",bean.varietal],["Altitude",bean.altitude],["Type",isG?"Green Bean":bean.roast]].map(([l,v])=>(
                <div key={l} style={{padding:"7px 10px",borderRadius:7,background:C.soft,border:`1px solid ${C.borderLt}`}}>
                  <div className="s" style={{fontSize:8,color:C.muted,letterSpacing:1,textTransform:"uppercase",marginBottom:1}}>{l}</div>
                  <div className="s" style={{fontSize:11,color:C.text,fontWeight:500}}>{v}</div>
                </div>
              ))}
            </div>
            <div style={{padding:"7px 10px",borderRadius:7,background:C.soft,border:`1px solid ${C.borderLt}`,marginBottom:14}}>
              <div className="s" style={{fontSize:8,color:C.muted,letterSpacing:1,textTransform:"uppercase",marginBottom:1}}>Farm</div>
              <div className="s" style={{fontSize:11,color:C.text,fontWeight:500}}>{bean.farm}</div>
            </div>
            <div style={{marginBottom:14}}>
              <h4 className="s" style={{fontSize:10,color:C.purple,letterSpacing:1.5,textTransform:"uppercase",marginBottom:5,fontWeight:600}}>☕ Tasting Notes</h4>
              <p className="s" style={{fontSize:12,color:C.body,lineHeight:1.6,padding:"8px 12px",borderRadius:7,background:C.purplePale,borderLeft:`3px solid ${C.purple}`}}>{bean.notes}</p>
            </div>
            {!isG&&bean.brew&&<div style={{marginBottom:16}}>
              <h4 className="s" style={{fontSize:10,color:C.goldDark,letterSpacing:1.5,textTransform:"uppercase",marginBottom:5,fontWeight:600}}>🔥 Brew Guide</h4>
              <p className="s" style={{fontSize:12,color:C.body,lineHeight:1.6,padding:"8px 12px",borderRadius:7,background:C.goldPale,borderLeft:`3px solid ${C.gold}`}}>{bean.brew}</p>
            </div>}
            </>
          )}
          <button onClick={()=>{onAdd(bean,isG?bean.tiers[selTier]:null);onClose()}} style={{width:"100%",padding:"13px",borderRadius:7,border:"none",background:C.purple,color:"#fff",fontSize:11,fontWeight:600,fontFamily:"'DM Sans',sans-serif",letterSpacing:1.2,textTransform:"uppercase",cursor:"pointer"}}>
            Add to Cart — RM{isG?bean.tiers[selTier]?.p:bean.price}{isG?"/kg":""}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ═══ CART DRAWER ═══ */
function CartDrawer({cart,onClose,onRemove,onQty}){
  const total=cart.reduce((s,i)=>s+i.unitPrice*(i.isGreen?i.kgQty:i.qty),0);
  return(
    <div onClick={onClose} style={{position:"fixed",inset:0,background:"rgba(45,17,69,0.4)",backdropFilter:"blur(4px)",zIndex:1000,display:"flex",justifyContent:"flex-end"}}>
      <div onClick={e=>e.stopPropagation()} style={{width:"100%",maxWidth:360,background:C.card,height:"100%",overflow:"auto",boxShadow:"-8px 0 32px rgba(45,17,69,0.15)",display:"flex",flexDirection:"column"}}>
        <div style={{padding:"16px 18px",borderBottom:`1px solid ${C.border}`,display:"flex",justifyContent:"space-between",alignItems:"center"}}>
          <h3 className="s" style={{fontSize:14,fontWeight:600,color:C.purpleDeep}}>Cart ({cart.length})</h3>
          <button onClick={onClose} style={{background:"none",border:"none",fontSize:18,color:C.muted,cursor:"pointer"}}>×</button>
        </div>
        <div style={{flex:1,overflow:"auto",padding:"10px 18px"}}>
          {cart.length===0?<div style={{textAlign:"center",padding:"36px 0"}}><div style={{fontSize:32,marginBottom:8}}>☕</div><p className="s" style={{color:C.muted,fontSize:12}}>Cart is empty</p></div>
          :cart.map(item=>(
            <div key={item.cartId} style={{display:"flex",gap:10,padding:"12px 0",borderBottom:`1px solid ${C.borderLt}`}}>
              <div style={{width:36,height:36,borderRadius:7,background:item.isGreen?"#E8F5E9":item.isEquip?"#FFF3E0":C.purplePale,display:"flex",alignItems:"center",justifyContent:"center",fontSize:16,flexShrink:0}}>{item.isEquip?eqIcon(item.cat):item.isGreen?"🌿":fl(item.origin)}</div>
              <div style={{flex:1,minWidth:0}}>
                <h4 className="s" style={{fontSize:11,fontWeight:500,color:C.text,marginBottom:2,whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{item.name}</h4>
                <div className="s" style={{fontSize:9,color:C.muted}}>{item.isGreen?`${item.tierLabel} · Green`:item.isEquip?item.cat:`${item.process} · 200g`}</div>
                <div style={{display:"flex",alignItems:"center",gap:6,marginTop:5}}>
                  <div style={{display:"flex",alignItems:"center",border:`1px solid ${C.border}`,borderRadius:4,overflow:"hidden"}}>
                    <button onClick={()=>onQty(item.cartId,-1)} style={{width:24,height:24,border:"none",background:C.soft,cursor:"pointer",fontSize:12,color:C.body}}>−</button>
                    <span className="s" style={{width:26,textAlign:"center",fontSize:10,fontWeight:600,color:C.text}}>{item.isGreen?item.kgQty:item.qty}</span>
                    <button onClick={()=>onQty(item.cartId,1)} style={{width:24,height:24,border:"none",background:C.soft,cursor:"pointer",fontSize:12,color:C.body}}>+</button>
                  </div>
                  <span className="s" style={{fontSize:12,fontWeight:600,color:C.purple}}>RM{(item.unitPrice*(item.isGreen?item.kgQty:item.qty)).toLocaleString()}</span>
                  <button onClick={()=>onRemove(item.cartId)} className="s" style={{marginLeft:"auto",background:"none",border:"none",color:C.red,fontSize:9,cursor:"pointer",fontWeight:500}}>Remove</button>
                </div>
              </div>
            </div>
          ))}
        </div>
        {cart.length>0&&<div style={{padding:"14px 18px",borderTop:`1px solid ${C.border}`,background:C.soft}}>
          <div style={{display:"flex",justifyContent:"space-between",marginBottom:10}}>
            <span className="s" style={{fontSize:13,fontWeight:600}}>Total</span>
            <span style={{fontSize:18,fontWeight:700,color:C.purple,fontFamily:"'Cormorant Garamond',Georgia,serif"}}>RM{total.toLocaleString()}</span>
          </div>
          <button onClick={async()=>{const items=cart.map(i=>({name:i.name,price:i.unitPrice,quantity:i.isGreen?i.kgQty:i.qty,description:i.isGreen?`${i.process} · ${i.tierLabel} · Green Bean`:i.isEquip?i.cat:`${i.process} · 200g`,type:i.isGreen?"green":i.isEquip?"equip":"roasted"}));try{const res=await fetch("https://jpresso-checkout.onrender.com/create-checkout-session",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({items})});const data=await res.json();if(data.url){window.location.href=data.url}else{alert("Error: "+(data.error||"Unknown"))}}catch(err){alert("Network error. Please try again.")}}} style={{width:"100%",padding:"12px",borderRadius:7,border:"none",background:C.gold,color:C.purpleDeep,fontSize:11,fontWeight:700,fontFamily:"'DM Sans',sans-serif",letterSpacing:1.2,textTransform:"uppercase",cursor:"pointer"}}>Checkout with Stripe</button>
        </div>}
      </div>
    </div>
  );
}

/* ═══ MAIN APP ═══ */
function App(){
  const[tab,setTab]=useState("roasted");
  const[freq,setFreq]=useState("biweekly");
  const[cf,setCf]=useState("All");
  const[q,setQ]=useState("");
  const[sel,setSel]=useState(null);
  const[selType,setSelType]=useState("roasted");
  const[cart,setCart]=useState([]);
  const[showCart,setShowCart]=useState(false);
  const[faq,setFaq]=useState(null);

  const cats=tab==="roasted"?["All","Classic","Experimental","Blend"]:tab==="green"?["All","Classic","Signature","Limited Release","Iris Estate"]:EQUIP_CATS;

  const items=useMemo(()=>{
    const src=tab==="roasted"?ROASTED:tab==="green"?GREEN:EQUIP;
    return src.filter(b=>{
      if(cf!=="All"&&b.cat!==cf)return false;
      if(q){const l=q.toLowerCase();return b.name.toLowerCase().includes(l)||(b.process||"").toLowerCase().includes(l)||(b.varietal||"").toLowerCase().includes(l)||(b.origin||"").toLowerCase().includes(l)||(b.cat||"").toLowerCase().includes(l)}
      return true;
    });
  },[cf,q,tab]);

  useEffect(()=>{setCf("All");setQ("")},[tab]);

  const addToCart=(bean,tier)=>{
    const isG=tab==="green",isE=tab==="equip";
    const cartId=isG?`${bean.id}-${tier?.qty}`:bean.id;
    setCart(prev=>{
      const ex=prev.find(i=>i.cartId===cartId);
      if(ex)return prev.map(i=>i.cartId===cartId?{...i,...(isG?{kgQty:i.kgQty+1}:{qty:i.qty+1})}:i);
      return[...prev,{...bean,cartId,isGreen:isG,isEquip:isE,unitPrice:isG?tier.p:bean.price,tierLabel:tier?.qty||"",qty:1,kgQty:1}];
    });
    setShowCart(true);
  };

  const FREQS=[{id:"weekly",l:"Weekly",s:"Save 0%"},{id:"biweekly",l:"Biweekly",s:"Save 5%"},{id:"monthly",l:"Monthly",s:"Save 10%"}];
  const TIERS=[{id:"so",name:"Single Origin",prices:{weekly:55,biweekly:50,monthly:45},icon:"🌍"},{id:"bl",name:"Signature Blend",prices:{weekly:48,biweekly:44,monthly:40},icon:"✦"},{id:"es",name:"Espresso Club",prices:{weekly:58,biweekly:52,monthly:48},icon:"◉"}];

  return(
    <div style={{fontFamily:"'Cormorant Garamond',Georgia,serif",background:C.bg,color:C.text,minHeight:"100vh"}}>
      <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet"/>
      <style>{`*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}.s{font-family:'DM Sans',sans-serif}.bc{transition:transform .2s,box-shadow .2s;cursor:pointer}.bc:hover{transform:translateY(-3px);box-shadow:0 8px 18px rgba(78,31,115,.08)}.ch{display:inline-block;padding:3px 8px;border-radius:100px;font-size:9px;font-weight:500;cursor:pointer;border:none;transition:all .2s}input[type="text"]{background:${C.card};border:1px solid ${C.border};border-radius:6px;padding:7px 11px;color:${C.text};font-family:'DM Sans',sans-serif;font-size:11px;outline:none;width:100%}input::placeholder{color:${C.muted}}input:focus{border-color:${C.purpleLight}}.cb{position:absolute;top:-5px;right:-5px;width:15px;height:15px;border-radius:50%;background:${C.gold};color:${C.purpleDeep};font-size:8px;font-weight:700;display:flex;align-items:center;justify-content:center;font-family:'DM Sans',sans-serif}@media(max-width:768px){.bg{grid-template-columns:1fr!important}.tg{flex-direction:column!important}.fr{flex-direction:column!important}}`}</style>

      {sel&&<BeanModal bean={sel} onClose={()=>setSel(null)} onAdd={(b,t)=>addToCart(b,t)} type={selType}/>}
      {showCart&&<CartDrawer cart={cart} onClose={()=>setShowCart(false)} onRemove={id=>setCart(p=>p.filter(i=>i.cartId!==id))} onQty={(id,d)=>setCart(p=>p.map(i=>i.cartId===id?{...i,qty:Math.max(1,i.qty+d),kgQty:Math.max(1,i.kgQty+d)}:i))}/>}

      {/* NAV */}
      <nav style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"12px 28px",borderBottom:`1px solid ${C.borderLt}`,position:"sticky",top:0,background:`${C.bg}ee`,backdropFilter:"blur(12px)",zIndex:100}}>
        <div style={{display:"flex",alignItems:"center",gap:7}}>
          <div style={{width:28,height:28,borderRadius:"50%",background:C.purple,display:"flex",alignItems:"center",justifyContent:"center",fontSize:12,fontWeight:700,color:"#fff"}}>J</div>
          <span className="s" style={{fontSize:13,fontWeight:600,letterSpacing:2,textTransform:"uppercase",color:C.purple}}>Jpresso</span>
        </div>
        <div style={{display:"flex",gap:2,background:C.soft,borderRadius:7,padding:2,border:`1px solid ${C.border}`}}>
          {[["roasted","☕ Roasted"],["green","🌿 Green Beans"],["equip","🔧 Equipment"]].map(([id,label])=>(
            <button key={id} onClick={()=>setTab(id)} className="s" style={{padding:"7px 14px",borderRadius:5,border:"none",cursor:"pointer",fontSize:10,fontWeight:tab===id?600:400,background:tab===id?C.card:"transparent",color:tab===id?C.purple:C.muted,boxShadow:tab===id?"0 1px 3px rgba(78,31,115,.06)":"none",transition:"all .2s"}}>{label}</button>
          ))}
        </div>
        <button onClick={()=>setShowCart(true)} style={{position:"relative",background:"none",border:`1px solid ${C.border}`,borderRadius:6,width:36,height:36,cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",fontSize:15}}>🛒{cart.length>0&&<span className="cb">{cart.length}</span>}</button>
      </nav>

      {/* HERO */}
      <section style={{padding:"48px 28px 52px",textAlign:"center",background:`linear-gradient(180deg,${C.purplePale},${C.bg} 85%)`}}>
        <FadeIn>
          <div className="s" style={{display:"inline-block",padding:"4px 14px",borderRadius:100,background:C.card,border:`1px solid ${C.border}`,color:C.purple,fontSize:9,letterSpacing:2,textTransform:"uppercase",marginBottom:18}}>
            {tab==="roasted"?"✦ Specialty Roasted Beans":tab==="green"?"🌿 Wholesale Green Beans":"🔧 Timemore Brewing Equipment"}
          </div>
        </FadeIn>
        <FadeIn delay={0.04}><h1 style={{fontSize:44,fontWeight:400,lineHeight:1.1,maxWidth:600,margin:"0 auto 14px",fontStyle:"italic",color:C.purpleDeep}}>
          {tab==="roasted"?<>Freshly Roasted. <span style={{color:C.gold,fontStyle:"normal",fontWeight:600}}>Delivered.</span></>:tab==="green"?<>Green Beans. <span style={{color:C.gold,fontStyle:"normal",fontWeight:600}}>Direct from Origin.</span></>:<>Brewing Equipment. <span style={{color:C.gold,fontStyle:"normal",fontWeight:600}}>Precision Tools.</span></>}
        </h1></FadeIn>
        <FadeIn delay={0.08}><p className="s" style={{fontSize:14,color:C.body,maxWidth:440,margin:"0 auto",lineHeight:1.7}}>
          {tab==="roasted"?"Roasted to order at our KL roastery. Free shipping within Peninsular Malaysia.":tab==="green"?"Wholesale green beans sourced direct from producers. Volume pricing available.":"Professional-grade Timemore grinders, kettles, scales & accessories."}
        </p></FadeIn>
      </section>

      <div style={{height:1,background:`linear-gradient(90deg,transparent,${C.border},transparent)`,margin:"0 28px"}}/>

      {/* SUBSCRIPTION PLANS — roasted tab only */}
      {tab==="roasted"&&<>
        <section style={{padding:"40px 28px",background:C.soft}}>
          <FadeIn><div style={{textAlign:"center",marginBottom:10}}><p className="s" style={{fontSize:9,letterSpacing:3,textTransform:"uppercase",color:C.gold,marginBottom:6}}>Subscribe & save</p><h2 style={{fontSize:28,fontWeight:400,fontStyle:"italic",color:C.purpleDeep}}>Subscription Plans</h2></div></FadeIn>
          <FadeIn delay={0.05}>
            <div className="fr" style={{display:"flex",justifyContent:"center",gap:2,margin:"18px auto 24px",maxWidth:380,background:C.card,borderRadius:7,padding:3,border:`1px solid ${C.border}`}}>
              {FREQS.map(f=><button key={f.id} onClick={()=>setFreq(f.id)} className="s" style={{flex:1,padding:"7px 10px",borderRadius:5,border:"none",cursor:"pointer",textAlign:"center",background:freq===f.id?C.purplePale:"transparent",color:freq===f.id?C.purple:C.muted,fontWeight:freq===f.id?600:400,fontSize:10}}>{f.l}<span style={{display:"block",fontSize:8,color:C.goldDark}}>{f.s}</span></button>)}
            </div>
          </FadeIn>
          <div className="tg" style={{display:"flex",gap:12,maxWidth:860,margin:"0 auto"}}>
            {TIERS.map((t,i)=><FadeIn key={t.id} delay={0.03+i*0.05} style={{flex:1,minWidth:220}}><div style={{borderRadius:12,background:C.card,border:`1px solid ${C.border}`,padding:"20px 18px",textAlign:"center",boxShadow:"0 2px 10px rgba(78,31,115,.04)"}}>
              <div style={{fontSize:20,marginBottom:3}}>{t.icon}</div>
              <h3 style={{fontSize:18,fontWeight:500,fontStyle:"italic",color:C.purpleDeep,marginBottom:10}}>{t.name}</h3>
              <div style={{display:"flex",alignItems:"baseline",justifyContent:"center",gap:3,marginBottom:12}}><span className="s" style={{fontSize:10,color:C.muted}}>RM</span><span style={{fontSize:30,fontWeight:600,color:C.purple,lineHeight:1}}>{t.prices[freq]}</span><span className="s" style={{fontSize:9,color:C.muted}}>/ 200g</span></div>
              <button onClick={async()=>{try{const res=await fetch("https://jpresso-checkout.onrender.com/create-subscription-session",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({plan_id:`${t.id}-${freq}`})});const data=await res.json();if(data.url){window.location.href=data.url}else{alert(data.error||"Subscription not configured yet")}}catch(err){alert("Network error.")}}} className="s" style={{width:"100%",padding:"10px",borderRadius:6,border:"none",background:C.purple,color:"#fff",fontSize:10,fontWeight:600,letterSpacing:1.2,textTransform:"uppercase",cursor:"pointer"}}>Subscribe Now</button>
            </div></FadeIn>)}
          </div>
        </section>
        <div style={{height:1,background:`linear-gradient(90deg,transparent,${C.border},transparent)`}}/>
      </>}

      {/* CATALOG */}
      <section style={{padding:"40px 28px"}}>
        <FadeIn><div style={{textAlign:"center",marginBottom:6}}>
          <p className="s" style={{fontSize:9,letterSpacing:3,textTransform:"uppercase",color:C.gold,marginBottom:6}}>{tab==="roasted"?"Shop individual beans":tab==="green"?"Browse our catalog":"Browse our collection"}</p>
          <h2 style={{fontSize:28,fontWeight:400,fontStyle:"italic",color:C.purpleDeep}}>{tab==="roasted"?"Bean Collection":tab==="green"?"Green Bean Catalog":"Equipment & Accessories"}</h2>
          <p className="s" style={{fontSize:11,color:C.muted,marginTop:3}}>Click any item for full details</p>
        </div></FadeIn>

        <FadeIn delay={0.04}>
          <div style={{maxWidth:940,margin:"18px auto 6px"}}><input type="text" placeholder={`Search ${tab==="equip"?"equipment":"beans"}...`} value={q} onChange={e=>setQ(e.target.value)} style={{maxWidth:300,marginBottom:8}}/></div>
          <div style={{maxWidth:940,margin:"0 auto 14px",display:"flex",gap:4,flexWrap:"wrap",alignItems:"center"}}>
            {cats.map(c=><button key={c} onClick={()=>setCf(c)} className="ch s" style={{background:cf===c?C.purplePale:C.soft,color:cf===c?C.purple:C.muted,border:cf===c?`1px solid ${C.purple}33`:`1px solid ${C.borderLt}`}}>{c}</button>)}
          </div>
        </FadeIn>

        <div style={{maxWidth:940,margin:"0 auto 10px"}}><span className="s" style={{fontSize:10,color:C.muted}}>{items.length} item{items.length!==1?"s":""}</span></div>

        <div className="bg" style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:11,maxWidth:940,margin:"0 auto"}}>
          {items.map(item=>(
            <div key={item.id} className="bc" onClick={()=>{setSel(item);setSelType(tab)}} style={{borderRadius:10,background:C.card,border:`1px solid ${C.border}`,overflow:"hidden",boxShadow:"0 1px 5px rgba(78,31,115,.03)"}}>
              <div style={{padding:"13px 13px 11px"}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:5}}>
                  <div>
                    {tab==="equip"?<span style={{fontSize:16,marginRight:4}}>{eqIcon(item.cat)}</span>:<span style={{fontSize:13,marginRight:3}}>{fl(item.origin)}</span>}
                    <span className="s" style={{fontSize:8,color:C.muted}}>{tab==="equip"?item.brand:item.origin}</span>
                  </div>
                  <span className="s" style={{fontSize:7,padding:"2px 5px",borderRadius:100,background:`${catC(item.cat)}10`,color:catC(item.cat),fontWeight:600}}>{item.cat}</span>
                </div>
                <h4 style={{fontSize:13,fontWeight:500,lineHeight:1.25,marginBottom:4,fontStyle:"italic",color:C.purpleDeep,minHeight:34}}>{item.name}</h4>
                {tab!=="equip"&&<p className="s" style={{fontSize:9,color:C.muted,lineHeight:1.4,marginBottom:6,display:"-webkit-box",WebkitLineClamp:2,WebkitBoxOrient:"vertical",overflow:"hidden"}}>{item.notes}</p>}
                {tab==="equip"&&<p className="s" style={{fontSize:9,color:C.muted,lineHeight:1.4,marginBottom:6,display:"-webkit-box",WebkitLineClamp:2,WebkitBoxOrient:"vertical",overflow:"hidden"}}>{item.specs.split("\n")[0]}{item.colors&&` · ${item.colors.join("/")}`}</p>}
                <div className="s" style={{display:"flex",gap:3,flexWrap:"wrap",marginBottom:8}}>
                  {tab!=="equip"&&<><span style={{fontSize:7,padding:"2px 5px",borderRadius:3,background:C.soft,color:C.body,border:`1px solid ${C.borderLt}`}}>{item.process}</span><span style={{fontSize:7,padding:"2px 5px",borderRadius:3,background:C.soft,color:C.body,border:`1px solid ${C.borderLt}`}}>{item.varietal}</span></>}
                  {item.score&&<span style={{fontSize:7,padding:"2px 5px",borderRadius:3,background:`${C.green}10`,color:C.green,fontWeight:600}}>{item.score}</span>}
                </div>
                <div style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
                  <div style={{display:"flex",alignItems:"baseline",gap:2}}>
                    {tab==="green"?<><span className="s" style={{fontSize:8,color:C.muted}}>from</span><span style={{fontSize:16,fontWeight:600,color:C.purple}}>RM{Math.min(...item.tiers.map(t=>t.p))}</span><span className="s" style={{fontSize:8,color:C.muted}}>/kg</span></>
                    :<span style={{fontSize:16,fontWeight:600,color:C.purple}}>RM{item.price}</span>}
                  </div>
                  <button onClick={e=>{e.stopPropagation();addToCart(item,tab==="green"?item.tiers[0]:null)}} className="s" style={{padding:"4px 10px",borderRadius:4,border:"none",background:C.purple,color:"#fff",fontSize:8,fontWeight:600,cursor:"pointer"}}>+ Add</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <div style={{height:1,background:`linear-gradient(90deg,transparent,${C.border},transparent)`}}/>

      {/* SUBSCRIPTION vs ONE-TIME */}
      <section style={{padding:"48px 28px",background:C.soft}}>
        <FadeIn><div style={{textAlign:"center",marginBottom:24}}>
          <p className="s" style={{fontSize:9,letterSpacing:3,textTransform:"uppercase",color:C.gold,marginBottom:6}}>Which is right for you?</p>
          <h2 style={{fontSize:28,fontWeight:400,fontStyle:"italic",color:C.purpleDeep}}>Subscription vs One-Time Purchase</h2>
        </div></FadeIn>
        <FadeIn delay={0.06}>
          <div style={{display:"flex",gap:16,maxWidth:860,margin:"0 auto",flexWrap:"wrap"}}>
            {/* Subscription */}
            <div style={{flex:1,minWidth:280,borderRadius:14,background:C.card,border:`2px solid ${C.purple}33`,padding:"24px 22px",boxShadow:"0 2px 12px rgba(78,31,115,.06)",position:"relative"}}>
              <div className="s" style={{position:"absolute",top:-10,left:20,padding:"3px 12px",borderRadius:100,background:C.purple,color:"#fff",fontSize:9,fontWeight:600,letterSpacing:1,textTransform:"uppercase"}}>Recommended</div>
              <div style={{fontSize:22,marginBottom:6}}>🔄</div>
              <h3 className="s" style={{fontSize:16,fontWeight:600,color:C.purpleDeep,marginBottom:12}}>Monthly Subscription</h3>
              {[
                ["Save up to 10%","Lower price vs one-time purchases"],
                ["Free shipping always","Every delivery ships free within Peninsular MY"],
                ["Freshness guaranteed","Roasted to order on your schedule — never stale"],
                ["Auto-discovery","We curate new origins & blends for you each cycle"],
                ["Total flexibility","Switch plans, skip, pause, or cancel anytime — no lock-in"],
                ["Priority access","Subscribers get first pick on limited release lots"],
                ["Brew guides included","Tasting notes & brew tips with every shipment"],
              ].map(([t,d],i)=>(
                <div key={i} style={{display:"flex",gap:8,marginBottom:10}}>
                  <span style={{color:C.green,fontSize:14,lineHeight:1,marginTop:1}}>✓</span>
                  <div><div className="s" style={{fontSize:12,fontWeight:600,color:C.text}}>{t}</div><div className="s" style={{fontSize:10,color:C.muted,lineHeight:1.4}}>{d}</div></div>
                </div>
              ))}
              <a href="#plans" className="s" style={{display:"block",textAlign:"center",marginTop:16,padding:"10px",borderRadius:6,background:C.purple,color:"#fff",fontSize:10,fontWeight:600,letterSpacing:1.2,textTransform:"uppercase",textDecoration:"none",cursor:"pointer"}}>View Subscription Plans</a>
            </div>

            {/* One-Time */}
            <div style={{flex:1,minWidth:280,borderRadius:14,background:C.card,border:`1px solid ${C.border}`,padding:"24px 22px",boxShadow:"0 2px 12px rgba(78,31,115,.04)"}}>
              <div style={{fontSize:22,marginBottom:6}}>🛒</div>
              <h3 className="s" style={{fontSize:16,fontWeight:600,color:C.purpleDeep,marginBottom:12}}>One-Time Purchase</h3>
              {[
                ["Full control","Pick exactly the beans you want, when you want"],
                ["Try before you commit","Sample individual beans before subscribing"],
                ["Bulk green beans","Wholesale pricing with volume discounts up to 500kg+"],
                ["Equipment & accessories","Timemore grinders, kettles, scales — buy anytime"],
                ["Gift-friendly","Perfect for one-off gifts without recurring charges"],
              ].map(([t,d],i)=>(
                <div key={i} style={{display:"flex",gap:8,marginBottom:10}}>
                  <span style={{color:C.purple,fontSize:14,lineHeight:1,marginTop:1}}>•</span>
                  <div><div className="s" style={{fontSize:12,fontWeight:600,color:C.text}}>{t}</div><div className="s" style={{fontSize:10,color:C.muted,lineHeight:1.4}}>{d}</div></div>
                </div>
              ))}
              <div className="s" style={{marginTop:16,padding:"10px 14px",borderRadius:8,background:C.goldPale,border:`1px solid ${C.gold}33`,fontSize:11,color:C.body,textAlign:"center"}}>
                💡 Tip: Try a one-time order first, then subscribe to your favorites and save!
              </div>
            </div>
          </div>
        </FadeIn>
      </section>

      <div style={{height:1,background:`linear-gradient(90deg,transparent,${C.border},transparent)`}}/>

      {/* FAQ */}
      <section style={{padding:"48px 28px"}}>
        <FadeIn><div style={{textAlign:"center",marginBottom:24}}>
          <p className="s" style={{fontSize:9,letterSpacing:3,textTransform:"uppercase",color:C.gold,marginBottom:6}}>Got questions?</p>
          <h2 style={{fontSize:28,fontWeight:400,fontStyle:"italic",color:C.purpleDeep}}>Frequently Asked Questions</h2>
        </div></FadeIn>
        <div style={{maxWidth:680,margin:"0 auto"}}>
          {[
            {c:"Subscription",q:"How does the subscription work?",a:"Choose your plan (Single Origin, Signature Blend, or Espresso Club) and delivery frequency (weekly, biweekly, or monthly). We roast your beans fresh every Tuesday and ship on Wednesday. Your card is charged automatically each cycle."},
            {c:"Subscription",q:"Can I switch, pause, or cancel my subscription?",a:"Absolutely — you have full control. After your first shipment, you can switch between plans, change frequency, pause for a holiday, or cancel entirely. No lock-in contracts, no cancellation fees, no questions asked."},
            {c:"Subscription",q:"Do I get to choose which beans I receive?",a:"Subscription beans are curated by our roasters — that's part of the experience! Single Origin subscribers get a rotating selection from different farms each cycle. If you want a specific bean, you can always buy it separately as a one-time purchase."},
            {c:"Subscription",q:"How much do I save with a subscription vs one-time?",a:"Subscribers save 5% on biweekly plans and 10% on monthly plans compared to one-time purchases. Plus, every subscription order ships free within Peninsular Malaysia."},
            {c:"Orders",q:"When are beans roasted and shipped?",a:"Every order — both subscription and one-time — is roasted to order at our Bandar Sri Damansara roastery. We roast on Tuesdays and ship on Wednesdays to ensure maximum freshness."},
            {c:"Orders",q:"What grind options are available?",a:"We ship whole bean by default for the freshest experience. You can also request ground for espresso, filter drip, French press, or AeroPress — just leave a note at checkout."},
            {c:"Shipping",q:"Is shipping really free?",a:"For roasted beans and equipment: free shipping within Peninsular Malaysia, RM15 flat rate for East Malaysia. For green beans, shipping is weight-based — Peninsular MY ranges from RM15 (1–5kg) to free (60kg+). East Malaysia green bean shipping ranges from RM50 (1–5kg) to RM150 (10–30kg). Orders above 30kg to East Malaysia require a custom quote."},
            {c:"Shipping",q:"How long does delivery take?",a:"Peninsular Malaysia: 3–5 business days after roasting. East Malaysia: 5–10 business days. All orders are dispatched on Wednesdays."},
            {c:"Green Beans",q:"What are the minimum order quantities for green beans?",a:"Green beans are available from 1kg for sampling. Volume pricing kicks in at 5kg, 10kg, 30kg, and 60kg+ tiers. For orders above 500kg, contact us for the best wholesale rates."},
            {c:"Green Beans",q:"Do green beans ship the same way?",a:"Green bean orders within KL can be self-picked up at our PJ roastery. For delivery: Peninsular Malaysia has tiered shipping (free at 800kg). East Malaysia is RM10.50–RM13/kg."},
            {c:"Equipment",q:"Do Timemore products come with warranty?",a:"Yes — all Timemore equipment comes with the manufacturer's standard warranty. We provide after-sales support for grinders and electric equipment from our KL base."},
            {c:"Payment",q:"What payment methods do you accept?",a:"We accept all major credit and debit cards (Visa, Mastercard, Amex) through Stripe. All transactions are in Malaysian Ringgit (MYR) and processed securely."},
          ].map((f,i)=>(
            <FadeIn key={i} delay={i*0.03}>
              <div style={{borderBottom:`1px solid ${C.borderLt}`}}>
                <button onClick={()=>setFaq(faq===i?null:i)} className="s" style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"14px 4px",color:C.text,cursor:"pointer",border:"none",outline:"none",background:"none",width:"100%",textAlign:"left"}}>
                  <div style={{display:"flex",alignItems:"center",gap:8,flex:1}}>
                    <span style={{fontSize:8,padding:"2px 6px",borderRadius:100,background:f.c==="Subscription"?C.purplePale:f.c==="Shipping"?`${C.green}12`:f.c==="Green Beans"?`${C.green}12`:f.c==="Equipment"?C.goldPale:f.c==="Payment"?`${C.gold}22`:f.c==="Gifts"?`${C.gold}22`:C.soft,color:f.c==="Subscription"?C.purple:f.c==="Shipping"?C.green:f.c==="Green Beans"?C.green:f.c==="Equipment"?C.goldDark:f.c==="Payment"?C.goldDark:f.c==="Gifts"?C.goldDark:C.muted,fontWeight:600,flexShrink:0}}>{f.c}</span>
                    <span style={{fontSize:12,fontWeight:500,paddingRight:12}}>{f.q}</span>
                  </div>
                  <span style={{fontSize:16,color:C.purple,transform:faq===i?"rotate(45deg)":"rotate(0)",transition:"transform .25s",flexShrink:0}}>+</span>
                </button>
                <div style={{maxHeight:faq===i?200:0,overflow:"hidden",transition:"max-height .35s ease"}}>
                  <p className="s" style={{padding:"0 4px 14px 4px",fontSize:11,lineHeight:1.7,color:C.body,paddingLeft:60}}>{f.a}</p>
                </div>
              </div>
            </FadeIn>
          ))}
        </div>
      </section>

      <div style={{height:1,background:`linear-gradient(90deg,transparent,${C.border},transparent)`}}/>

      {/* CTA */}
      <section style={{padding:"48px 28px",textAlign:"center",background:`linear-gradient(180deg,${C.bg},${C.purplePale})`}}>
        <FadeIn>
          <h2 style={{fontSize:32,fontWeight:400,fontStyle:"italic",marginBottom:10,color:C.purpleDeep}}>Your next great cup <span style={{color:C.gold,fontWeight:600,fontStyle:"normal"}}>starts here.</span></h2>
          <p className="s" style={{fontSize:13,color:C.body,maxWidth:360,margin:"0 auto 22px"}}>Join coffee lovers across Malaysia who wake up to Jpresso every morning.</p>
          <div style={{display:"flex",gap:10,justifyContent:"center",flexWrap:"wrap"}}>
            <a href="#plans" className="s" style={{display:"inline-block",padding:"11px 28px",borderRadius:7,background:C.purple,color:"#fff",fontSize:10,fontWeight:600,letterSpacing:1.2,textTransform:"uppercase",textDecoration:"none"}}>Subscribe & Save</a>
            <a href="#beans" className="s" style={{display:"inline-block",padding:"11px 28px",borderRadius:7,background:"transparent",color:C.purple,fontSize:10,fontWeight:600,letterSpacing:1.2,textTransform:"uppercase",textDecoration:"none",border:`1.5px solid ${C.border}`}}>Shop Beans</a>
          </div>
        </FadeIn>
      </section>

      <div style={{height:1,background:`linear-gradient(90deg,transparent,${C.border},transparent)`}}/>
      <footer style={{padding:"20px 28px",display:"flex",justifyContent:"space-between",alignItems:"center",flexWrap:"wrap",gap:8,background:C.soft}}>
        <div className="s" style={{fontSize:9,color:C.muted}}>© 2026 Big Jpresso Sdn Bhd · Bandar Sri Damansara, KL</div>
        <div className="s" style={{display:"flex",gap:12,fontSize:9,color:C.muted}}><span>jpressocoffee.com</span><span>·</span><span>hello@jpressocoffee.com</span></div>
      </footer>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script></body></html>
