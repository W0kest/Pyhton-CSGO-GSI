let f0 = document.getElementById('f0');
let f1 = document.getElementById('f1');
let boxLeft = document.getElementById('PlaceHolder');

console.log(f0.innerText.length);
LCount = f0.innerText.length;
console.log(LCount);

if(LCount <=30)
{
  boxLeft.id = "SingleLine";
}

else if(LCount >= 31 && LCount <= 59)
{
  boxLeft.id = "DoubleLine";
}

else if(LCount >= 60)
{
  boxLeft.id = "TripleLine"; 
}
